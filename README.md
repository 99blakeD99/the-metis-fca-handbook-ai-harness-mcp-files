# Metis FCA Handbook AI Harness — MCP Server

<!-- mcp-name: io.github.99blakeD99/the-metis-fca-handbook-ai-harness-mcp -->

An MCP (Model Context Protocol) server that integrates the Metis FCA Handbook AI Harness into your AI workflow. MCP is supported by Claude, OpenAI, Gemini, and most desktop/IDE MCP clients (Cursor, Windsurf, Cline, and others) — this README uses Claude Code and Claude Desktop as fully worked examples; adjust the configuration steps to fit your own client.

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

**Important:** The Harness API key should be supplied at runtime from an environment variable or secrets manager, never hardcoded as a literal value in a configuration file that may be committed to a shared repository. Two methods are supported — pick one, since they require different MCP config:

- **Method A — Shell Profile.** Add `export METIS_API_KEY="sk_live_..."` to your shell startup file (`~/.bashrc`, `~/.zshrc`, etc.), before launching your MCP client (VS Code, Claude Desktop, etc.), so the variable is present in the client's own process environment. With this method, your MCP config should reference the variable via substitution:
  ```json
  "env": { "METIS_API_KEY": "${METIS_API_KEY}" }
  ```
- **Method B — .env File.** Create a `.env` file in your project directory containing `METIS_API_KEY=sk_live_...`. The server loads this itself at startup (via `load_dotenv()`) — your MCP client never needs to see the value. With this method, **omit the `env` block from your MCP config entirely.** Do not copy the `"${METIS_API_KEY}"` snippet from Method A — your client's own environment will not have that variable set, so the substitution will silently fail and pass the literal string `${METIS_API_KEY}` through as your API key. This produces a 401 error that is easy to mistake for a bad/revoked key.

⚠️ If your MCP config lives in your home directory (e.g. `~/.claude/settings.json`) rather than a project-local location (e.g. `.claude/settings.json` in a project root), it applies to every project on the machine — a stray `${METIS_API_KEY}` placeholder there will break the harness for every project, not just the one you are setting up. Prefer a project-local config unless you specifically want a shared, machine-wide key.

#### 3a. Claude Code

Claude Code (the Claude IDE extension) supports both global (user-level) and project-level MCP configuration.

##### Global Configuration (Recommended for FS Firms)

If you work across multiple projects, configure the MCP globally in your user's `.claude/settings.json` so it is available everywhere. Because this file is shared machine-wide, use **Method A** — a stray `.env` lookup path is per-project and does not fit a global setup as cleanly.

**File location:** `~/.claude/settings.json` (your home directory)

Edit or create `~/.claude/settings.json` and add:

```json
{
  "mcpServers": {
    "fca-handbook-harness-mcp": {
      "command": "fca-handbook-harness-mcp",
      "env": {
        "METIS_API_KEY": "${METIS_API_KEY}"
      }
    }
  }
}
```

Then add to your shell profile (e.g. `~/.bashrc`, `~/.zshrc`, `~/.fish/config.fish`), **before** starting Claude Code:

```bash
export METIS_API_KEY="sk_live_..."
```

Replace `sk_live_...` with your actual API key from your Metis account. Claude Code substitutes `${METIS_API_KEY}` from this environment variable when it starts the server — if the variable is not set at that point, Claude Code loads the server with the literal string `${METIS_API_KEY}` instead (and warns about it), which is what causes the misleading 401 described in Troubleshooting below.

**Restart:** Restart Claude Code. Once connected, the `evaluate_fca_handbook_applicability` tool will be available in all projects.

##### Project-Level Configuration (Single-Project Setup)

If you only need the MCP in one specific project, configure it project-locally instead. This is the natural fit for **Method B**.

**File location:** `.claude/settings.json` (in your project root, under `.claude/` directory)

Edit or create `.claude/settings.json` and add — no `env` block, per Method B above:

```json
{
  "mcpServers": {
    "fca-handbook-harness-mcp": {
      "command": "fca-handbook-harness-mcp"
    }
  }
}
```

Then create a `.env` file in your project root containing:

```
METIS_API_KEY=sk_live_...
```

Replace `sk_live_...` with your actual API key from your Metis account.

**Important:** Project-level `.env` files are often checked into version control — ensure `METIS_API_KEY` is in `.gitignore` before committing, or use the global configuration approach instead (recommended for FS firms).

**Restart:** Claude Code will detect the change and reload MCP connections automatically (or you can restart the IDE).

#### 3b. Claude Desktop

**File location:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

Claude Desktop's config is inherently machine-wide (there is no project-local variant), so **Method A** is the more consistent fit — see the ⚠️ note above before using Method B here.

**Method A — Shell Profile:**

```json
{
  "mcpServers": {
    "fca-handbook-harness-mcp": {
      "command": "fca-handbook-harness-mcp",
      "env": {
        "METIS_API_KEY": "${METIS_API_KEY}"
      }
    }
  }
}
```

Set `METIS_API_KEY` in your system environment (e.g. in `~/.bashrc`, system preferences, or via GUI) **before** launching Claude Desktop:

```bash
export METIS_API_KEY="sk_live_..."
```

**Method B — .env File:** create a `.env` file in the directory Claude Desktop runs from, containing `METIS_API_KEY=sk_live_...`, and use the config above with the `env` block omitted entirely (not left in with the `${METIS_API_KEY}` placeholder — see Method B warning above).

**Restart:** Quit and restart the Claude Desktop app. Once connected, the `evaluate_fca_handbook_applicability` tool will be available.

#### 3c. Other Clients (Cursor, Windsurf, Cline, etc.)

These clients typically use the same `mcpServers` JSON shape as Claude Desktop above. Consult your client's documentation for the config file location, restart procedure, and whether it performs `${VAR}` substitution in `env` blocks the way Claude Code and Claude Desktop do (some use GUI connectors rather than JSON files, or may not substitute at all — check before relying on Method A).

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

**401 Unauthorized with a key you've confirmed is valid on the dashboard:**
- Check whether your MCP config still contains a literal `${METIS_API_KEY}` (or similar) placeholder that never got substituted — this happens when Method B (`.env`) is used but the config still has an `env` block written for Method A. Inspect the actual spawned server process's environment (e.g. `/proc/<pid>/environ` on Linux) to confirm what value it is really receiving
- Verify `METIS_API_KEY` is set — either in the config `env` (Method A) or in a `.env` file the server can find (Method B), not both and not neither
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
