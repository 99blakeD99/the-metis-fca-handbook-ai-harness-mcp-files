"""MCP server exposing the FCA Handbook Harness's /v1/analyze endpoint as a tool.

Wraps the deployed HTTP API for use by any MCP-aware client (Claude Code,
Claude Desktop, etc.). Calls a live, already-billed account via METIS_API_KEY
— every call costs money.

Config (env vars):
    METIS_API_KEY   Required. Bearer token from an account's API Keys dashboard.
    METIS_BASE_URL  Optional. Defaults to the live Render deployment.
"""

import json
import os

import requests
from mcp.server.fastmcp import Context, FastMCP

BASE_URL = os.environ.get("METIS_BASE_URL", "https://fcahandbookharnessimplementation.onrender.com")
API_KEY = os.environ.get("METIS_API_KEY")

# "message" events on a full run: one per reasoning node (7-8 total, including
# final "Analysis complete"). Just a hint for the progress indicator, not a hard
# guarantee — a triage rejection ends after step 1, with an error, not 8.
_EXPECTED_PROGRESS_STEPS = 8

mcp = FastMCP("Metis FCA Handbook AI Harness")


@mcp.tool()
async def evaluate_fca_handbook_applicability(
    user_input: str, analysis_mode: str = "quick", ctx: Context = None
) -> dict:
    """Evaluate which FCA Handbook entries apply to a situation as input by the user, using the Metis FCA Handbook AI Harness.

    Calls a live compliance reasoning run, billed to the configured account.
    Use for questions involving the FCA Handbook, including authorisation, permissions, or obligations for a specific firm/product/service.

    This call takes 60-120+ seconds (longer in 'full' mode). Tell the user
    up front that you are starting a long-running call, before you call the
    tool — do not go silent. The Harness attempts to stream progress messages
    as each reasoning node completes - if you receive them, relay each one
    to the user as it arrives — they contain genuine detail, not filler.

    First call: use analysis_mode='quick'. Before calling, check whether you
    already have (from this conversation, documents you were given, or other
    tools) grounded answers to these six things — the specific compliance
    question, the product/service, who is providing it (platform/adviser/
    bank/etc.), its key features, the target market (retail/institutional/
    professional/customer segment), and what data it handles. If you are missing more than
    one or two, ask the user for them first rather than calling with thin
    input. Every call is billed at a flat rate regardless of input quality,
    so a vague call incurs unnecessary cost.

    The result
    includes refinement_suggestions — gaps the Harness could not resolve
    from user_input alone, typically subtler than the six basics above (e.g.
    a regulatory edge case, not a missing fact you could have just asked
    for). For each suggestion worth pursuing, get the grounded information —
    retrieve it from this conversation, documents you were given, or other
    tools if you already have it; otherwise ask the user directly. Do not
    speculate or infer plausible-sounding detail you do not actually have —
    that reintroduces the hallucination risk this Harness exists to avoid,
    one level up.

    Refining (second call onward): use analysis_mode='full'. Either way, before calling again, confirm with the user
    that you are about to run a further 'full' pass with the refined input —
    do not call again unilaterally, and do not just list the gaps and stop.
    Repeat this pattern for further rounds if the new result still leaves
    suggestions worth resolving.

    The result's citations field contains verbatim quotes from the FCA
    Handbook — this is a core part of what the Harness offers, not
    generative invention, and distinct from the summary/obligations text. They can best be viewed as an Appendix.
    Citations can be long, so ask the user whether they want the relevant
    verbatim citations included, rather than omitting them by default as
    mere detail.

    Args:
        user_input: Everything together as one piece of text (up to 5000
            characters) — the specific compliance question, the
            product/service, who is providing it, its key features, the
            target market, and what data it handles. On later rounds, refine
            all six using existing chat context and whatever additional
            detail later rounds have gathered. See "First call" and
            "Refining" above.
        analysis_mode: 'quick' for the first call (default, ~60-120
            seconds); 'full' (longer) for refined calls after the first —
            detailed conditional reasoning: conditions, interactions
            between rules, and second-order implications. See "Refining"
            above for when to switch and why to confirm with the user first.
    """
    if not API_KEY:
        raise RuntimeError("METIS_API_KEY is not set in the MCP server's environment")

    response = requests.post(
        f"{BASE_URL}/v1/analyze",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={"user_input": user_input, "analysis_mode": analysis_mode},
        stream=True,
        timeout=300,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Harness request failed ({response.status_code}): {response.text}")

    result = None
    error = None
    step = 0
    for line in response.iter_lines():
        if not line or not line.startswith(b"data:"):
            continue
        event = json.loads(line[len(b"data:"):].decode("utf-8"))
        event_type = event.get("type")
        if event_type == "analysis":
            result = event["content"]
        elif event_type == "error":
            error = event["content"]
        elif event_type == "message" and ctx is not None:
            step += 1
            # report_progress is a silent no-op unless the client opted into
            # progress tracking (sent a progressToken on the tool call) — most
            # hosts do not. ctx.info() sends an unconditional logging
            # notification instead, so the message actually reaches the
            # client regardless of host support for progress tracking.
            await ctx.info(event["content"])
            await ctx.report_progress(
                progress=step, total=_EXPECTED_PROGRESS_STEPS, message=event["content"]
            )

    if error:
        raise RuntimeError(f"Harness returned an error: {error}")
    if result is None:
        raise RuntimeError("Harness stream ended without an analysis result")
    return result


def main():
    mcp.run()


if __name__ == "__main__":
    main()
