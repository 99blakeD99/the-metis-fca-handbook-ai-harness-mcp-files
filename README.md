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

The `mcpServers` JSON shape below is shared by most desktop/IDE MCP clients, but the config file location and restart step vary by client. Pick the one that matches what you are using.

**Important:** The Harness API key should be supplied at runtime from an environment variable or secrets manager, never hardcoded as a literal value in a configuration file that may be committed to a shared repository. The server supports this directly: it loads a `.env` file automatically, so `METIS_API_KEY` never needs to appear in the client config at all.

#### 3a. Claude Code

Claude Code (the Claude IDE extension) stores MCP configuration in your project's `.claude/settings.json`. This is project-local, not global — you configure it once per project.

**File location:** `.claude/settings.json` (in your project root)

Edit or create `.claude/settings.json` and add:

```json
{
  "mcpServers": {
    "fca-handbook-harness-mcp": {
      "command": "fca-handbook-harness-mcp"
    }
  }
}
```

Then create a `.env` file (in your project root) containing:

```
METIS_API_KEY=sk_live_...
```

Replace `sk_live_...` with your actual API key from your Metis account.

**Restart:** Claude Code will detect the change and reload MCP connections automatically (or you can restart the IDE). Once connected, the `evaluate_fca_handbook_applicability` tool will be available.

#### 3b. Claude Desktop

**File location:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

Add this server entry (create the file if it doesn't exist):

```json
{
  "mcpServers": {
    "fca-handbook-harness-mcp": {
      "command": "fca-handbook-harness-mcp"
    }
  }
}
```

Then create a `.env` file (in the directory this server runs from) containing:

```
METIS_API_KEY=sk_live_...
```

Replace `sk_live_...` with your actual API key from your Metis account. (If your client does not run the server from a directory you control — some GUI-based connector flows do not — fall back to an `env` block in the config above instead.)

**Restart:** Quit and restart the Claude Desktop app. Once connected, the `evaluate_fca_handbook_applicability` tool will be available.

#### 3c. Other Clients (Cursor, Windsurf, Cline, etc.)

These clients typically use the same `mcpServers` JSON shape as Claude Desktop above. Consult your client's documentation for the config file location and restart procedure (some use GUI connectors rather than JSON files).

### 4. Verify the connection

Once restarted, you should see `evaluate_fca_handbook_applicability` available as a tool in your agent workflows. If it does not appear, check the Troubleshooting section below.

## Using the Tool

The tool accepts two parameters:

- **user_input** (required, max 5000 characters): Everything together as one piece of text — firm type, products/services, target market, regulatory question, etc.
- **analysis_mode** (optional): `"quick"` (default, ~60-120 seconds) or `"full"` (longer, detailed conditional reasoning)

The tool returns:
- **summary**: 2-3 sentence overview of applicability
- **entry_analysis**: Retrieved FCA Handbook entries with reasoning
- **obligations**: High-confidence and low-confidence/tangential obligations, each optionally flagged with the specific condition under which it applies
- **refinement_suggestions**: What the analysis couldn't determine from your input and why it matters, paired with the specific edit to make to improve accuracy
- **citations**: Verbatim quotes from FCA Handbook with binding levels (R=Rule, G=Guidance)
- **tokens**: Object with `input`, `output`, and `total` token counts, for cost/complexity tracking

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

- **mcp_server.py** — MCP server implementation (main entry point; its docstring is the source of truth for the tool schema)
- **pyproject.toml** — pypi package manifest
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
