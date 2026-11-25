"""MCP server exposing the FCA Handbook Harness's /v1/analyze endpoint as a tool.

Wraps the deployed HTTP API for use by any MCP-aware client (Claude Code,
Claude Desktop, etc.). Calls a live, already-billed account via METIS_API_KEY
— every call costs money.

Config (env vars):
    METIS_API_KEY   Required. Bearer token from an account's API Keys dashboard.
    METIS_BASE_URL  Optional. Defaults to the live Render deployment.

Both can also be set via a .env file (loaded automatically, if present, from
the current directory or any parent) rather than placed literally in the MCP
client's own config file — see the README's Quick Start. A value already
present in the environment (e.g. set directly in the client config) takes
precedence over .env; .env only fills in what is not already set.
"""

import json
import os
import re
from pathlib import Path
from typing import Annotated, Any, Dict

import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import Context, FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

load_dotenv()

BASE_URL = os.environ.get("METIS_BASE_URL", "https://fcahandbookharnessimplementation.onrender.com")
API_KEY = os.environ.get("METIS_API_KEY")

# "message" events on a run: one per node (Nodes 2 to 8, seven in all, since this route
# runs no Node 1 gate) plus the final "Analysis complete". Just a hint for the progress
# indicator, not a hard guarantee.
_EXPECTED_PROGRESS_STEPS = 8

TOOL_DESCRIPTION_PATH = Path(__file__).with_name("tool-description.md")


def load_tool_spec(path: Path = TOOL_DESCRIPTION_PATH) -> Dict[str, Any]:
    """Read tool-description.md, the single source of the tool's description.

    Returns {"title", "annotations" (a ToolAnnotations), "description", "args"
    (argument name -> description; optional, and empty when the file has no
    "##" sections, in which case the arguments carry no description in the
    input schema)}. Plain text parsing, with no YAML
    dependency, because the published package depends only on mcp, requests
    and python-dotenv. Raises a clear error at startup if the file is missing
    or incomplete, rather than serving an empty description.
    """
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(
            f"The tool description file {path} is missing or unreadable ({exc}). "
            "It is part of the package; reinstall it."
        ) from exc

    match = re.match(r"^---\n(.*?)\n---\n(.*)\Z", text, re.DOTALL)
    if not match:
        raise RuntimeError(f"{path} must start with a front matter block between --- lines")
    front = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            front[key.strip()] = value.strip()
    body = re.sub(r"<!--.*?-->", "", match.group(2), flags=re.DOTALL)
    body = re.sub(r"^# .*\n", "", body, flags=re.MULTILINE)

    sections = re.split(r"^## ", body, flags=re.MULTILINE)
    description = sections[0].strip()
    args = {}
    for section in sections[1:]:
        name, _, arg_text = section.partition("\n")
        args[name.strip()] = arg_text.strip()

    if not description or not front.get("title"):
        raise RuntimeError(f"{path} needs a title in the front matter and a description")

    def flag(key: str) -> bool:
        return front.get(key, "false").lower() == "true"

    annotations = ToolAnnotations(
        readOnlyHint=flag("read_only"),
        destructiveHint=flag("destructive"),
        idempotentHint=flag("idempotent"),
        openWorldHint=flag("open_world"),
    )
    return {"title": front["title"], "annotations": annotations, "description": description, "args": args}


TOOL_SPEC = load_tool_spec()

mcp = FastMCP("Metis FCA Handbook AI Harness")


@mcp.tool(
    title=TOOL_SPEC["title"],
    description=TOOL_SPEC["description"],
    annotations=TOOL_SPEC["annotations"],
)
async def evaluate_fca_handbook_applicability(
    user_input: Annotated[str, Field(description=TOOL_SPEC["args"].get("user_input"))],
    analysis_mode: Annotated[str, Field(description=TOOL_SPEC["args"].get("analysis_mode"))] = "quick",
    ctx: Context = None,
) -> dict:
    # The description (and the argument descriptions above) live in
    # tool-description.md, not in a docstring.
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
