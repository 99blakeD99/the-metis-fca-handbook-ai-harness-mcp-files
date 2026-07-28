# HTTP API Schema for FCA Handbook Harness

**MCP Tool Name:** `evaluate_fca_handbook_applicability`

Defines the contract for the HTTP API at `POST /v1/analyze`. Integrates with
Supabase accounts, API keys, and Stripe billing. Available over HTTP and via
MCP (Model Context Protocol).

## Endpoint

`POST /v1/analyze`

Live at: `https://fcahandbookharnessimplementation.onrender.com/v1/analyze`

## Description

Analyze an entity against the FCA Handbook. Returns a compliance report with
verbatim citations. One-shot: each call is an independent analysis; there is
no session or conversation state.

Supports both analysis modes: "quick" (fast pass, default) and "full"
(detailed conditional reasoning — conditions, interactions between rules,
second-order implications; takes longer).

**Before calling:** gather enough input first — provide the specific compliance question, the product/service, who's providing it, key features, target market, and data handled all in one user_input blob. Each call is billed at a flat rate regardless of input quality, so calling with thin input and relying on `refinement_suggestions` to backfill costs more than collecting details upfront.

## Authentication

**Required:**
```
Authorization: Bearer <api_key>
```

Where `<api_key>` is an account-level API key generated from the admin
dashboard (format: `sk_live_...`, stored in `METIS_API_KEY` environment variable).

**Pre-flight checks (performed by `analyze_api`):**
1. API key exists in the `api_keys` table and `revoked_at` is null (else `401`)
2. Account exists for that key (else `404`)
3. If the account is a paid (Stripe) account: current-month spend vs.
   `monthly_limit` — if the limit is reached, the run is refused (see
   "Error handling" below)

⚠️ **Security note:** Always use the `Bearer` header. Never put the API key in
a URL or query parameter.

## Request Body

```json
{
  "user_input": "string (required)",
  "analysis_mode": "quick | full (optional, default: quick)"
}
```

The request takes `user_input` and an optional `analysis_mode` — nothing else.
There's no separate `entity_description` field, no `question` field, no `context`
field. Put everything in one piece of text: firm/product/entity details, the
specific compliance question, and any other context, in whatever structure reads
naturally.

Node 2 of the Harness (`extract_features`) is responsible for semantically
parsing this one blob into structured fields (entity type, signifiers,
target market, the question, etc.) for the rest of the pipeline. If your
text does not make the question clearly identifiable, extraction quality
suffers — be explicit, e.g. lead with "Question: ..." or make it the last
sentence.

### user_input
- **Type:** string, required
- **Max length:** 5000 characters
- **Description:** Everything together — firm type, regulatory status,
  products/services, key activities, target market, data handled, and the
  compliance question you want answered.
- **Example:** `"Asset manager operating a UCITS fund focused on European equities, managing €100M AUM, targeting institutional investors. Question: Do we need FCA approval to run this fund?"`

### analysis_mode
- **Type:** string, optional, `"quick"` or `"full"` — defaults to `"quick"` if omitted or unrecognized
- **Description:** `"quick"` gives a fast pass identifying the most critical
  binding obligations. `"full"` performs detailed conditional reasoning —
  each entry's applicability, mandatory vs. conditional obligations,
  tensions between provisions, second-order gaps — and returns more
  refinement suggestions (2-4, vs. quick's 1). Full mode takes longer than
  the 60-120 seconds typical of quick mode; size client timeouts
  accordingly (300 seconds is a safe default).

There is no server-side length or emptiness validation on this endpoint
beyond Pydantic requiring `user_input` to be present — an empty string will
reach the Harness and most likely produce a low-quality or triage-rejected
analysis rather than a clean `400`.

## Response

Always a **Server-Sent Events (SSE) stream** (`text/event-stream`), even on
success — there is no non-streaming JSON mode. Each line is `data: <json>\n\n`
where the JSON has a `type` and a `content`.

### SSE message types (this endpoint only emits these three)

| type | content | meaning |
|------|---------|---------|
| `message` | string | A progress notification — see "Progress Notifications" below. Fires multiple times over the run, plus once more (`"Analysis complete\n"`) right before the final `analysis` event. |
| `error` | string | Something stopped the run — see "Error handling" below. The stream ends after this. |
| `analysis` | object (see below) | The final result. The stream ends after this. |

Note: this is a **narrower type vocabulary** than the web UI's `/api/chat`
endpoint, which additionally distinguishes `status`, `harness_working`,
`node6_stream`, `node_progress`, and `complete` as separate SSE types.
`/v1/analyze` folds all of that into one `message` type instead — do not
build an integration expecting the richer type set.

### Progress Notifications

The Harness has 7 internal nodes (triage → extract features → check
terminology → embed → retrieve entries → reason → report). Each one emits
a `message` event as it starts with its own fixed, human-written
description of what it is doing — the same text a human user sees in the
web UI. A typical quick-mode run produces 7–8 `message` events total (one
per node, plus a final "Analysis complete" message). For example:

```
{"type": "message", "content": "Doing a quick check to ensure that your information is appropriate for this tool..."}
{"type": "message", "content": "Condensing your information into a form which optimises AI effectiveness and efficiency..."}
{"type": "message", "content": "Checking key terms in your information against your terminology in the FCA Handbook Glossary..."}
{"type": "message", "content": "Embedding your question. This involves converting it into 1024-dimensional space using the Voyage 3-large embedding model."}
{"type": "message", "content": "Searching FCA Handbook for relevant entries..."}
{"type": "message", "content": "Scanning for key risks and obligations, using the \"Quick\" setting..."}
{"type": "message", "content": "Neatening up Claude's reasoning into a formal report..."}
{"type": "message", "content": "Analysis complete\n"}
{"type": "analysis", "content": { ... }}
```

If the input is rejected as out of scope (Node 1 triage gate), only one `message`
arrives, followed by an `error` event instead of the rest.

**If you are relaying this to an end user** (directly, or via an MCP/agent
tool wrapping this endpoint): show these messages as they arrive rather
than waiting silently for `analysis`. They're genuinely informative — which
stage is running and what it is doing — not filler, and a run can take
60-120 seconds (quick) or longer (full) with nothing else to show for it.
`http_api/mcp_server.py` does exactly this, via MCP progress notifications
(`ctx.report_progress()`), and its tool description tells the calling LLM
the same thing.

### `analysis` content shape

```json
{
  "summary": "string",
  "entry_analysis": [ { "entry_id": "...", "entry_text": "...", "applies": true, "conditional": false, "reasoning": "..." } ],
  "obligations": { "high_confidence": [], "conditional_obligations": [], "low_confidence_or_tangential": [] },
  "gaps": [ { "gap": "...", "why_it_matters": "..." } ],
  "refinement_suggestions": [ { "suggestion": "...", "priority": "..." } ],
  "citations": [ { "entry_id": "...", "cited_text": "...", "binding_level": "R|G|E" } ],
  "tokens": { "input": 15988, "output": 1770, "total": 17758 }
}
```

`entry_analysis`, `obligations`, `gaps`, `refinement_suggestions`, and
`citations` all come from the Harness's reasoning phase. Their shape is
defined in the "analysis_content_schema" section below and in `tool.json`.

### Acting on `refinement_suggestions`

Each suggestion is something the Harness couldn't determine from the input given.
If you are an LLM/agent calling this on a user's behalf and you already have
grounded information that addresses a suggestion — from the conversation,
documents you were given, or other tools you called — fold it directly into the
next `user_input` and call again, rather than just relaying the suggestion back
to the user as a question. Don't speculate or infer plausible-sounding detail you
don't actually have — that reintroduces hallucination risk. Only ask the user
directly for whatever is left that you genuinely do not know.

There is **no separate `metadata` object and no `billing` object** in the
response. Billing happens server-side (a Stripe invoice charged immediately
on completion, if the account is a paid account) but nothing about that
invoice is returned to the caller.

## Error handling

Two different failure modes, at two different levels:

### HTTP-level errors (raised before streaming starts)

| Status | When |
|--------|------|
| `401` | Missing/malformed `Authorization` header, or the API key does not exist / is revoked |
| `404` | The key's account no longer exists |
| `422` | `user_input` missing from the request body (standard FastAPI/Pydantic validation) |
| `500` | Supabase is not configured (deployment issue, not a caller issue) |

These come back as a plain FastAPI error body (`{"detail": "..."}`), not SSE.

### In-stream errors (HTTP 200, but `type: "error"` in the stream)

Once streaming starts, everything is reported as an SSE `error` event,
including:
- **Budget exceeded** — the account's Stripe spend this month has reached
  `monthly_limit`. Content is exactly: `"This account has been used up to
  your budget. The monthly limit needs to be reset."`
- **Out-of-scope question** — Node 1 (the triage gate) rejected the question
  as not being about financial services. Content currently includes an
  internal-looking prefix, e.g. `"Workflow halted at node 'triage_gate':
  Please ask a question relating to the provision of financial services."`
- **Any other Harness failure** — content is `str(exception)`.

There is no `code` field, no structured error object, and no `429` rate
limiting implemented anywhere in this path today. Treat any `error` event as
terminal — the stream ends after it.

## Billing

If the account is a paid (Stripe) account (`status == 'active'` and it has a
`stripe_customer_id`), a flat £7.95 invoice is created and charged immediately
after the analysis completes. Quick and Full are billed at the same flat rate.
Billing failures are logged but never block the response — the user always
receives a result or an explicit error.

## Examples

### cURL

```bash
curl -N -X POST https://fcahandbookharnessimplementation.onrender.com/v1/analyze \
  -H "Authorization: Bearer $METIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Robo-advisor platform offering automated portfolio management to retail investors, managing £500k-£1M portfolios. Question: What FCA authorisation and permissions do we need to launch this service?"
  }'
```

(`-N` disables curl's output buffering so you see the stream as it arrives. Make sure `METIS_API_KEY` is exported in your shell first.)

### Python

```python
import json
import requests
import os

api_key = os.getenv("METIS_API_KEY")  # From the admin dashboard

response = requests.post(
    "https://fcahandbookharnessimplementation.onrender.com/v1/analyze",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "user_input": "Asset manager, UCITS fund, European equities, €100M AUM. Question: Do we need FCA approval to launch?",
    },
    stream=True,
    timeout=180,
)

result = None
for line in response.iter_lines():
    if not line or not line.startswith(b"data:"):
        continue
    event = json.loads(line[len(b"data:"):].decode("utf-8"))
    if event["type"] == "analysis":
        result = event["content"]
    elif event["type"] == "error":
        raise RuntimeError(event["content"])

print(result["summary"])
print(result["tokens"])
```

To request Full mode, add `"analysis_mode": "full"` to the JSON body in
either example above, and raise the client timeout to ~300 seconds.

### Complete Example: Fund Compliance Analysis

**Request:**

```json
POST /v1/analyze
Authorization: Bearer sk_live_...
Content-Type: application/json

{
  "user_input": "We are establishing an open-ended investment fund structured as a Unit Trust investing in emerging market equities with an annual management charge of 1.2%. The fund is purchased directly through our platform. Customers receive annual fact sheets, quarterly performance reports, and can redeem units monthly. Our fund maintains diversification across multiple emerging market countries and sectors. What are the FCA Handbook requirements for fund prospectuses, unit pricing, dealing procedures, fund governance, best execution, and customer reporting?"
}
```

**Response (parsed from SSE stream):**

```json
{
  "summary": "An open-ended Unit Trust investing in emerging market equities must comply with comprehensive prospectus disclosure requirements (COLL 4.2), unit pricing and valuation rules (COLL 6.3), dealing procedures including redemption arrangements (COLL 6.2), and conduct of business rules including best execution (COBS 11.2) and periodic customer reporting (COBS 16.3).",
  "entry_analysis": [
    {
      "entry_id": "2409",
      "entry_text": "COLL 4.2.2 R (1) A prospectus must be drawn up in English and published as a document by the authorised fund manager containing investment objectives, policy, risk profile, unit pricing, dealing procedures, and redemption arrangements.",
      "applies": true,
      "conditional": false,
      "reasoning": "As an open-ended fund accepting direct customer purchases, you must publish a prospectus meeting these disclosure requirements."
    },
    {
      "entry_id": "2456",
      "entry_text": "COLL 6.3.3 R A fund manager must conduct fair and accurate valuation of scheme property at least twice monthly and calculate unit prices to four significant figures.",
      "applies": true,
      "conditional": false,
      "reasoning": "Monthly unit pricing with redemption options requires valuation at this frequency and precision."
    }
  ],
  "obligations": {
    "high_confidence": [
      "Draw up and publish prospectus with investment objectives, policy, risk disclosures, dealing procedures, unit pricing methodology, and charges (COLL 4.2.2R)",
      "Conduct fair valuation of scheme property at least twice monthly and calculate unit prices to four significant figures (COLL 6.3.3R)",
      "Effect redemption of units on request within four business days of redemption price determination (COLL 6.2.16R)",
      "Comply with best execution requirements for fund orders (COBS 11.2.1R)",
      "Provide semi-annual statements showing fund value, composition, and charges (COBS 16.3.1R)"
    ],
    "conditional_obligations": [
      "If operating dilution levy or adjustment, apply it fairly and disclose policy in prospectus (COLL 6.3.8R) — applies if dilution adjustment is used"
    ],
    "low_confidence_or_tangential": []
  },
  "gaps": [
    {
      "gap": "UCITS vs AIFM classification",
      "why_it_matters": "Affects governance, remuneration policy disclosure, and periodic reporting format. Clarify whether your fund qualifies as UCITS-managed."
    },
    {
      "gap": "Depositary delegation",
      "why_it_matters": "If you delegate depositary functions, additional conflict-of-interest disclosures are required. Confirm your depositary arrangement."
    }
  ],
  "refinement_suggestions": [
    {
      "suggestion": "Clarify whether your fund qualifies as UCITS or AIFM-managed — this affects disclosure and governance requirements.",
      "priority": "high"
    },
    {
      "suggestion": "Confirm your approach to unit pricing and whether you will use dilution adjustment or a dilution levy.",
      "priority": "medium"
    }
  ],
  "citations": [
    {
      "entry_id": "2409",
      "cited_text": "COLL 4.2.2 R (1) A prospectus must be drawn up in English and published as a document by the authorised fund manager...",
      "binding_level": "R"
    },
    {
      "entry_id": "2456",
      "cited_text": "COLL 6.3.3 R A fund manager must conduct fair and accurate valuation of scheme property at least twice monthly...",
      "binding_level": "R"
    }
  ],
  "tokens": {
    "input": 12500,
    "output": 5200,
    "total": 17700
  }
}
```

**Key fields in the response:**

- `summary` — Plain-English overview of applicability and key obligations
- `entry_analysis` — Array of retrieved FCA Handbook entries with applicability assessment
- `obligations` — Three categories: high_confidence (binding rules), conditional_obligations (rules with conditions), low_confidence_or_tangential (weaker matches)
- `gaps` — What the analysis couldn't resolve from your input; consider answering these to refine
- `refinement_suggestions` — Structured suggestions with priority level for what to ask next
- `citations` — Verbatim quotes from FCA Handbook entries with binding level (R = Rule, G = Guidance)
- `tokens` — Input, output, and total tokens (for cost/complexity transparency; not the billed amount, which is a flat £7.95)

## Notes

- **Two fields.** `user_input` (required) and `analysis_mode` (optional,
  `"quick"`/`"full"`) — no `entity_description`/`question`/`context` split.
  Say it all in one piece of text; the Harness figures out the structure.
- **One-shot, stateless.** No session ID, no history. The client manages any
  multi-turn conversation.
- **Always streams.** There is no non-streaming response mode. You will receive
  7-8 `message` events (one per reasoning node, plus final "Analysis complete"),
  interspersed with processing time, then the final `analysis` or `error` event.
  Expect ~60-120 seconds total for quick mode, longer for full.
