# Metis FCA Handbook AI Harness — MCP Server

<!-- mcp-name: io.github.99blakeD99/the-metis-fca-handbook-ai-harness-mcp -->

An MCP (Model Context Protocol) server that integrates the Metis FCA Handbook AI Harness into your AI workflow. MCP is supported by Claude, OpenAI, Gemini, and most desktop/IDE MCP clients (Cursor, Windsurf, Cline, and others) — this README uses Claude Desktop as a fully worked example; adjust the configuration steps to fit your own client.

**Source & full documentation:** [github.com/99blakeD99/the-metis-fca-handbook-ai-harness-mcp-files](https://github.com/99blakeD99/the-metis-fca-handbook-ai-harness-mcp-files)

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

### 3. Configure your MCP client

This section walks through Claude Desktop as a fully worked example. The `mcpServers` JSON shape below is shared by most desktop/IDE MCP clients (Claude Code, Cursor, Windsurf, Cline, and others) — but the config file location and restart step are Claude Desktop's specifically. If you are using a different client, including one with a GUI-based connector flow (some OpenAI and Gemini integrations work this way) rather than a JSON config file, consult that client's own documentation for where to add a server.

**Claude Desktop file location:**
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

### 4. Restart your MCP client

For Claude Desktop: quit and restart the app. Other clients reload MCP connections differently — check your client's documentation if unsure. Once connected, the `evaluate_fca_handbook_applicability` tool will be available in agent workflows.

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

**Tool not appearing (Claude Desktop; the same class of issue applies to most desktop MCP clients):**
- Verify the config file path (platform-specific, see above)
- Confirm `fca-handbook-harness-mcp` resolves on the command line (`which fca-handbook-harness-mcp` / `where fca-handbook-harness-mcp`). Desktop MCP clients typically launch with a minimal environment and may not see the same PATH as your shell — if the command does not resolve, replace `"command": "fca-handbook-harness-mcp"` with the absolute path from that lookup
- Restart your MCP client (not just reload)

**401 Unauthorized:**
- Verify `METIS_API_KEY` is set in the config `env`
- Check the key is correct (copy from dashboard again)
- Ensure no extra spaces or newlines in the key

**Connection timeout:**
- The analysis can take 60-120 seconds (quick mode) or longer (full mode)
- Ensure you have internet access to fcahandbookharnessimplementation.onrender.com

## Files

- **mcp_server.py** — MCP server implementation (main entry point)
- **pyproject.toml** — pypi package manifest
- **tool.json** — Tool schema definition for LLMs and registries
- **server.json** — MCP registry manifest (registry.modelcontextprotocol.io format)
- **manifest.json** — MCPB/Smithery bundle manifest
- **requirements.txt** — Python dependencies (`mcp`, `requests`)
- **uv.lock** — Pinned dependency resolution for reproducible `uv run`
- **`__init__.py`** — Python package marker
- **README.md** — This file
- **LICENSE** — MIT License
- **.gitignore** — Git ignore rules
- **.mcpbignore** — Files excluded from the MCPB bundle

## Support

For questions or issues, contact: `the-metis-fca-handbook-ai-harness@jbmd.co.uk`

---

**Product:** Metis FCA Handbook AI Harness  
**License:** MIT
