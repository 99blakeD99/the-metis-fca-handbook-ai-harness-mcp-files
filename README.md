# Metis FCA Handbook AI Harness — MCP Server

<!-- mcp-name: io.github.99blakeD99/the-metis-fca-handbook-ai-harness-mcp -->

An MCP (Model Context Protocol) server that integrates the Metis FCA Handbook AI Harness into Claude Desktop and other MCP-compatible agents.

## Tools

### `evaluate_fca_handbook_applicability`

Evaluate which FCA Handbook entries apply to an entity, via the Metis FCA Handbook AI Harness. One-shot: no session, no conversation state. Supports quick mode (60-120 seconds, default) and full mode (longer, more detailed). Returns a compliance report with verbatim citations, gaps, and refinement suggestions.

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

Email `the-metis-fca-handbook-ai-harness@jbmd.co.uk` and request a free temporary Access Code.

Ask compliance questions in natural language and watch each reasoning step unfold in real-time.

## Design Principles

The Harness is built on proven principles:

- **Stateless** — Each request is independent; no session coupling
- **One-shot** — Complete analysis in a single call; no multi-turn state
- **Clear contract** — Explicit input/output schemas for easy integration
- **Hosted** — Single canonical source; no version drift or stale data

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

## Quick Start

### 1. Get an API Key

Visit the Metis account dashboard:
```
https://fcahandbookharnessimplementation.onrender.com
```

- Click **"Create Account"** (modal on the homepage)
- Complete Stripe payment flow (accounts are paid)
- Navigate to **API Keys** and generate a new key
- Save it securely

### 2. Install the MCP Server

```bash
pip install fca-handbook-harness-mcp
```

### 3. Configure Claude Desktop

Edit your Claude Desktop config file:

**File location:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

Add this server entry (create the file if it doesn't exist):

```json
{
  "mcpServers": {
    "fca-handbook-harness": {
      "command": "fca-handbook-harness-mcp",
      "env": {
        "METIS_API_KEY": "sk_live_..."
      }
    }
  }
}
```

Replace `sk_live_...` with your actual API key from your Metis account.

### 4. Restart Claude Desktop

Quit and restart Claude Desktop. The `evaluate_fca_handbook_applicability` tool will now be available in agent workflows.

## Using the Tool

The tool accepts two parameters:

- **user_input** (required, max 5000 characters): Everything together as one piece of text — firm type, products/services, target market, regulatory question, etc.
- **analysis_mode** (optional): `"quick"` (default, ~60-120 seconds) or `"full"` (longer, detailed conditional reasoning)

The tool returns:
- **summary**: 2-3 sentence overview of applicability
- **entry_analysis**: Retrieved FCA Handbook entries with reasoning
- **obligations**: High-confidence, conditional, and low-confidence obligations
- **gaps**: What the analysis couldn't determine from your input
- **refinement_suggestions**: Follow-up information that would improve accuracy
- **citations**: Verbatim quotes from FCA Handbook with binding levels (R=Rule, G=Guidance)
- **tokens**: Token count for cost/complexity tracking

## Troubleshooting

**Tool not appearing in Claude Desktop:**
- Verify the config file path (platform-specific, see above)
- Confirm `fca-handbook-harness-mcp` resolves on the command line (`which fca-handbook-harness-mcp` / `where fca-handbook-harness-mcp`). Claude Desktop launches with a minimal environment and may not see the same PATH as your shell — if the command does not resolve, replace `"command": "fca-handbook-harness-mcp"` with the absolute path from that lookup
- Restart Claude Desktop (not just reload)

**401 Unauthorized:**
- Verify `METIS_API_KEY` is set in the config `env`
- Check the key is correct (copy from dashboard again)
- Ensure no extra spaces or newlines in the key

**Connection timeout:**
- The analysis can take 60-120 seconds (quick mode) or longer (full mode)
- Ensure you have internet access to fcahandbookharnessimplementation.onrender.com

## Files

- **mcp_server.py** — MCP server implementation (main entry point)
- **tool.json** — Tool schema definition for LLMs and registries
- **server.json** — MCP registry manifest (registry.modelcontextprotocol.io format)
- **requirements.txt** — Python dependencies (`mcp`, `requests`)
- **__init__.py** — Python package marker
- **README.md** — This file
- **LICENSE** — MIT License
- **.gitignore** — Git ignore rules

## Support

For questions or issues, contact: `the-metis-fca-handbook-ai-harness@jbmd.co.uk`

---

**Product:** Metis FCA Handbook AI Harness  
**Version:** 3.0.0  
**License:** MIT
