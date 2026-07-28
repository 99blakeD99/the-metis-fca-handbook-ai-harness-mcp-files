# Metis FCA Handbook AI Harness — Integration Guide

## What This Is

The Metis FCA Handbook AI Harness is a **hosted compliance reasoning service** that provides semantic analysis of FCA Handbook applicability. It is not a self-hosted product. Instead, FS firms and compliance AI platforms integrate with it via a simple HTTP API (`POST /v1/analyze`) or MCP (Model Context Protocol) tool (`evaluate_fca_handbook_applicability`).

## Why choose The Metis FCA Handbook AI Harness?

- **Efficiency** Multiplies effectiveness of compliance advice. Saves £80+ in token fees per Harness run.

- **Deals with "Hard Problem"**, in which LLMs' token incentives prioritise training data so results are unreliable.

- **Verbatim citations** Quotes verbatim entries from the FCA Handbook. Other AI systems struggle to do this.

- **Matches real-world need** You do not have to start off knowing which sections you are looking for. Carries out structured searches across all 10,000+ FCA Handbook entries.

- **Secure Design** Harness compartmentalisation, one-shot structure, and statelessness fits natively with emerging AI agent security standards such as OWASP Top 10 for Agentic Applications 2026.

- **AI Accessible** Integrates easily with AI workflows and agents. Your LLM can use it as a tool.

## Try the Harness Live

Experience the Harness interactively before integrating:

```
https://fcahandbookharnessimplementation.onrender.com
```

Ask compliance questions in natural language and watch each reasoning step unfold in real-time.


## Architecture: Hosted Service, Not Self-Hosted

The Harness follows a modular, composable design:

- **Single canonical server** — No version drift, no distributed maintenance burden
- **Stateless reasoning** — Each request is independent; no internal state coupling
- **Clear contracts** — Well-defined API schema; easy to audit and screen
- **Operational resilience** — Vulnerabilities and failures are isolated and detectable by elimination

### Why Hosted Over Self-Hosting

**Self-hosting risks:**
- Version fragmentation across deployments
- Data staleness (handbook updates not propagated)
- Audit trail fragmentation
- Compliance liability spillback to users

**Hosted model benefits:**
- Single point of audit (one server, one audit trail)
- Transparent updates (users always see the latest)
- Data governance (we control FCA data residency)
- Clear responsibility (Metis owns the compliance)

This aligns with fundamental software architecture principles: **composition of stateless services**, not distributed monoliths.

## Integration Methods

### HTTP API

**Endpoint:** `POST /v1/analyze`

Send a JSON request with your compliance question and context. Returns structured analysis with FCA Handbook citations.

See [`schema.md`](./schema.md) for complete request/response schema, error codes, and examples.

### MCP (Model Context Protocol)

**Tool name:** `evaluate_fca_handbook_applicability`

Integrate the Harness as a composable tool in Claude or other MCP-compatible agents. See [`schema.md`](./schema.md) for MCP configuration and usage examples.

## Use Cases

### Compliance AI Platforms
Embed FCA reasoning as a service within your compliance platform. Users ask natural-language questions; your platform calls the Harness and presents structured reasoning.

### AI Agent Workflows
Agents building compliance workflows can include FCA Handbook reasoning as a composed tool—no external API calls, just MCP configuration.

### Compliance Review Automation
Integrate into document review or due-diligence pipelines. Automatically screen new rules against FCA applicability.

## For Regulatory Screening

FS firms screening MCP servers will find:
- **Simple model:** Stateless, no hidden state, no background jobs
- **Clear contract:** Explicit input schema, output schema, error modes
- **Transparent updates:** Version pinning; no automatic upgrades
- **Single point of failure:** If the Harness is down, it is obvious; no cascading config issues
- **Audit-friendly:** All calls logged centrally, not distributed

## Getting Started

### 1. Create an Account & Get an API Key

Visit the Metis account dashboard:
```
https://fcahandbookharnessimplementation.onrender.com
```

- Click **"Create Account"** (there is no separate signup page; it is a modal)
- Complete the Stripe payment flow (accounts are paid; current rate is £7.95 per analysis call)
- Once created, navigate to **API Keys** in the dashboard
- Generate a new key and copy it (shown once, then hidden)
- Save it securely

### 2. Set Environment Variables

```bash
export METIS_API_KEY="sk_live_..."
# Optional: set to override the default deployment URL
export METIS_BASE_URL="https://fcahandbookharnessimplementation.onrender.com"
```

### 3. Integration Methods

#### HTTP API

See [`setup-guide.md`](./setup-guide.md) for CLI and code examples (Python, JavaScript, Go, cURL).

#### MCP (Model Context Protocol) — Claude Desktop

Add the Harness as a tool in your Claude Desktop config:

**File location:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

Create the file if it doesn't exist.

```json
{
  "mcpServers": {
    "fca-handbook-harness": {
      "command": "python",
      "args": ["/path/to/mcp_server.py"],
      "env": {
        "METIS_API_KEY": "sk_live_..."
      }
    }
  }
}
```

Replace `/path/to/mcp_server.py` with the actual path to the file (or use a virtual environment wrapper). Optionally add `"METIS_BASE_URL"` to the `env` object if you need to override the default deployment URL.

Then restart Claude Desktop. The `evaluate_fca_handbook_applicability` tool will be available to use in agent workflows.

### 4. Try It Live

Visit the web UI interactively at:
```
https://fcahandbookharnessimplementation.onrender.com
```

## Files in This Folder

### `schema.md`
**Authoritative API contract.** Specifies:
- Request/response JSON schemas
- Input validation (field types, constraints, examples)
- Error codes and messages
- Authentication requirements

This is the source of truth for integration. Keep it in sync with the actual HTTP implementation.

### `mcp_server.py`
**MCP (Model Context Protocol) server implementation.** Wraps the HTTP API as a composable tool for Claude and other MCP-compatible agents. Handles:
- MCP server lifecycle (startup, shutdown)
- Tool schema definition
- Request/response translation
- Progress notifications

To use: install dependencies from `requirements.txt`, set `METIS_API_KEY` in your environment, and configure Claude Desktop as shown in "Getting Started" → "Integration Methods" above.

### `setup-guide.md`
**Getting started guide.** Covers:
- Environment setup (API keys, endpoints)
- CLI examples (curl, Python requests)
- Authentication flows
- Error troubleshooting
- Best practices

Start here if you are new to the Harness or integrating via HTTP.

### `tool.json`
**Tool schema definition.** Describes the tool schema for compatibility with tool-calling LLMs and registries. Maps to the same inputs/outputs as `schema.md`.

### `requirements.txt`
**Python dependencies for the MCP server.** Install with `pip install -r requirements.txt`.

### `__init__.py`
**Python module marker** for the MCP package.

### `LICENSE`
**MIT License.** The code is open-source and freely usable under these terms.

---

## Try It Live

The Metis FCA Handbook AI Harness is hosted and ready to use. To see the reasoning in action:

1. **Via web UI:** [https://fcahandbookharnessimplementation.onrender.com](https://fcahandbookharnessimplementation.onrender.com)
   - Ask questions in natural language
   - Watch each reasoning node unfold in real-time
   - See structured outputs and relevant handbook entries

2. **Via API:** Use the examples in `setup-guide.md` to call the HTTP endpoint directly

3. **Via MCP:** Configure the tool in Claude Desktop (see "Integration Methods" → "MCP" above) and use it in agent workflows

---

## Development & Contributing

This folder documents the public interface. The actual reasoning logic, data, and prompts are proprietary and hosted by Metis.

For integration questions or bugs, contact: `the-metis-fca-handbook-ai-harness@jbmd.co.uk`

---

**Product:** Metis FCA Handbook AI Harness  
**License:** See LICENSE  
**Version:** 3.0.0
