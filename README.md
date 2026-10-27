# Metis FCA Handbook AI Harness — MCP Server

<!-- mcp-name: io.github.99blakeD99/the-metis-fca-handbook-ai-harness-mcp -->

An MCP (Model Context Protocol) server that integrates the Metis FCA Handbook AI Harness into your AI workflow. MCP is supported by Claude, OpenAI, Gemini, and most desktop/IDE MCP clients (Cursor, Windsurf, Cline, and others) — this README uses Claude Code as the tested, worked example for the recommended remote server, and Claude Code and Claude Desktop for the local fallback; adjust the configuration steps to fit your own client.

**Source & full documentation:** [github.com/99blakeD99/the-metis-fca-handbook-ai-harness-mcp-files](https://github.com/99blakeD99/the-metis-fca-handbook-ai-harness-mcp-files)

## Tools

### `evaluate_fca_handbook_applicability`

Evaluate which FCA Handbook entries apply to an entity, via the Metis FCA Handbook AI Harness. One-shot: no session, no conversation state. Supports quick mode (60-120 seconds, default) and full mode (longer, more detailed). Returns a compliance report with verbatim citations and refinement suggestions, which identify gaps in the information you provided and how to fill them.

## Why choose The Metis FCA Handbook AI Harness?

- **Efficiency** Multiplies effectiveness of compliance advice. Saves £80+ in token fees per Harness run.

- **Deals with "Hard Problem"**, in which LLMs' token incentives prioritise training data so results are unreliable.

- **Verbatim citations** Quotes verbatim entries from the FCA Handbook. Other AI systems struggle to do this.

- **Matches real-world need** You do not have to start off knowing which sections you are looking for. Carries out structured searches across all 33,000+ FCA Handbook entries.

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

Setup is a one-off task for whoever manages your AI tools. Once it is connected, your compliance staff simply ask their AI assistant.

**Which setup to use:**

1. Use the **remote server** (step 2 below) if your client can connect to a remote MCP server and send a custom `Authorization` header. Nothing is installed; you need only a URL and your API key. This is the recommended setup.
2. Otherwise use the [local server](#alternative-run-the-server-locally-stdio), which runs on your machine and passes each call on to the hosted Harness.

Both give the same tool and the same results, billed at the same rate. For Claude Desktop, use the local server.

### If you are an AI assistant setting this up for a user

Follow these rules in addition to the steps below:

- Use the setup chosen by the rule above. For Claude Code, that is the remote setup in step 2a, with `--scope user` unless the user asks for a project-only setup. For Claude Desktop, use the local setup. For other clients, use the settings in step 2b.
- The API key must come from the user's environment variable `METIS_API_KEY`. Never ask the user to paste the key into this conversation, never write it to a file in a project or repository, and never put it as a literal value in a configuration file. Configuration files use the `${METIS_API_KEY}` reference shown below. To check that it is set without printing it, run `[ -n "$METIS_API_KEY" ] && echo set || echo unset`. If it is not set, tell the user how to set it (step 2), wait until they confirm it is set, and change no configuration and use no placeholder in the meantime. If the user pastes their key into the conversation anyway, do not use it, repeat it or write it anywhere, and suggest they regenerate it on the dashboard.
- MCP servers are configured with `claude mcp add`, or in `.mcp.json` or `~/.mcp.json`. Never put an `mcpServers` entry in `.claude/settings.json`.
- Verify the setup by checking that the tool `evaluate_fca_handbook_applicability` is listed. In Claude Code, run `claude mcp list` to see whether the server is connected. `/mcp` lists its tools, but it is a slash command that only the user can run, so ask them to run it. In other clients, check the client's MCP settings screen. **Do not call the tool to test it.** Every call is a real analysis run, billed to the user's account, and takes one to two minutes or more. Call it only when the user asks a real FCA Handbook question.
- Success means the server shows as connected and the tool is listed. Two known failure signs are `⏸ Pending approval` (the user must approve the server; see "Verify the connection" below) and a 401 error on first use (see Troubleshooting).

### 1. Get an API Key

If you already have an API key, skip to step 2.

Visit the Metis account dashboard:
```
https://fcahandbookharnessimplementation.onrender.com
```

- Click **"Create Account"** (modal on the homepage)
- Complete Stripe payment flow (accounts are paid)
- Navigate to **API Keys** and generate a new key
- Save it securely

### 2. Connect your client to the remote server

The remote server is at:

```
https://fcahandbookharnessimplementation.onrender.com/mcp
```

It uses the Streamable HTTP transport and expects your API key as a bearer token in the `Authorization` header of each request.

**Important:** Supply the key from an environment variable or secrets manager, never as a literal value in a configuration file that may be committed to a shared repository. Add this line to your shell startup file (`~/.bashrc`, `~/.zshrc`, etc.), before launching your client, so the variable is present in the client's own process environment:

```bash
export METIS_API_KEY="sk_live_..."
```

Replace `sk_live_...` with your actual API key from your Metis account.

On Windows, run `setx METIS_API_KEY "sk_live_..."` in Command Prompt instead, then restart your client. In every case, start your client after the variable is set, from a terminal if you can: an app launched from the Dock, Spotlight or the Start menu may not see a variable set in a shell startup file.

#### 2a. Claude Code

The easiest route is the CLI, which writes the correct file for you. Quote the header exactly as shown (single quotes) so your shell does not expand `${METIS_API_KEY}` before `claude mcp add` sees it. Otherwise your actual key is written into the config file as a literal, which is the hardcoding the note above warns against.

```bash
claude mcp add --transport http --scope user fca-handbook-harness-mcp https://fcahandbookharnessimplementation.onrender.com/mcp --header 'Authorization: Bearer ${METIS_API_KEY}'
```

Use `--scope project` instead of `--scope user` for a project-only setup. If you would rather edit the file directly, put this in `~/.mcp.json` (all projects) or in `.mcp.json` in your project root (that project only). These are standalone files, not inside `.claude/`; Claude Code rejects an `mcpServers` key in `.claude/settings.json`.

```json
{
  "mcpServers": {
    "fca-handbook-harness-mcp": {
      "type": "http",
      "url": "https://fcahandbookharnessimplementation.onrender.com/mcp",
      "headers": {
        "Authorization": "Bearer ${METIS_API_KEY}"
      }
    }
  }
}
```

Claude Code substitutes `${METIS_API_KEY}` from your environment when it starts. If the variable is not set at that point, Claude Code sends the literal text `${METIS_API_KEY}` as your key (and warns about it), which produces a 401 error that is easy to mistake for a bad key. Start Claude Code from a shell where `[ -n "$METIS_API_KEY" ] && echo set` prints `set`. If the tool does not appear after you add the server, restart Claude Code.

#### 2b. Other clients

Cursor, VS Code (Copilot), Gemini CLI, Cline, and other developer tools and agent frameworks can connect to a remote MCP server when given a URL and a custom header. They should work with the settings below, but they have not been tested by us. Field names and file locations differ between clients and are still changing, so follow your client's own documentation for adding a remote MCP server.

- **URL:** `https://fcahandbookharnessimplementation.onrender.com/mcp`
- **Transport:** Streamable HTTP
- **Header:** `Authorization: Bearer <your API key>`. Read the key from an environment variable if your client supports that.
- **Timeout:** a quick call takes 60-120 seconds and a full call longer. If your client has a short default timeout, raise it.

The syntax for referring to an environment variable differs between clients. For example, Cursor documents `${env:METIS_API_KEY}` where Claude Code uses `${METIS_API_KEY}`. Use your client's own syntax, and never a literal key.

A client that accepts only no authentication or OAuth for remote servers cannot send a static API key. Use the [local server](#alternative-run-the-server-locally-stdio) with that client.

### 3. Verify the connection

**Claude Code, first run only:** the first time you launch `claude` (interactively, not with `-p`) in a project with a new or changed project-scoped `.mcp.json`, it shows a one-time trust/approval prompt for that server before connecting. Until you accept it, the server sits in a "pending approval" state and its tool is not actually available (running `claude mcp list` shows `⏸ Pending approval`). Accept the prompt, or run `/mcp` in an existing session to approve it there. This gate does not apply to `~/.mcp.json` (global scope).

Once connected, you should see `evaluate_fca_handbook_applicability` available as a tool in your agent workflows. If it does not appear, check the Troubleshooting section below.

Verify by checking that the tool is listed. Do not call the tool just to test the connection: every call is a real analysis run, billed to your account.

## Alternative: run the server locally (stdio)

Use this if your client cannot connect to the remote server above. A small local server runs on your machine and passes each call on to the hosted Harness, using the same API key. You need Python 3.10 or later.

### Install the local server

```bash
pip install fca-handbook-harness-mcp
```

### Configure your MCP client (local)

The `mcpServers` JSON shape below is shared by most desktop/IDE MCP clients, but the config file location and restart step vary by client. Pick the one that matches what you are using.

**Important:** The Harness API key should be supplied at runtime from an environment variable or secrets manager, never hardcoded as a literal value in a configuration file that may be committed to a shared repository. Two methods are supported — pick one, since they require different MCP config:

- **Method A — Shell Profile.** Add `export METIS_API_KEY="sk_live_..."` to your shell startup file (`~/.bashrc`, `~/.zshrc`, etc.), before launching your MCP client (VS Code, Claude Desktop, etc.), so the variable is present in the client's own process environment. With this method, your MCP config should reference the variable via substitution:
  ```json
  "env": { "METIS_API_KEY": "${METIS_API_KEY}" }
  ```
- **Method B — .env File.** Create a `.env` file in your project directory containing `METIS_API_KEY=sk_live_...`. The server loads this itself at startup (via `load_dotenv()`) — your MCP client never needs to see the value. With this method, **omit the `env` block from your MCP config entirely.** Do not copy the `"${METIS_API_KEY}"` snippet from Method A — your client's own environment will not have that variable set, so the substitution will silently fail and pass the literal string `${METIS_API_KEY}` through as your API key. This produces a 401 error that is easy to mistake for a bad/revoked key.

⚠️ If your MCP config lives in your home directory (`~/.mcp.json`) rather than a project-local location (`.mcp.json` in a project root), it applies to every project on the machine — a stray `${METIS_API_KEY}` placeholder there will break the harness for every project, not just the one you are setting up. Prefer a project-local config unless you specifically want a shared, machine-wide key.

#### Claude Code (local)

Claude Code (the Claude IDE extension) supports both global (user-level) and project-level MCP configuration. **Note:** MCP servers are configured in `.mcp.json` files, never in `.claude/settings.json` — that file is for permissions/preferences only and does not recognize an `mcpServers` key (Claude Code will reject it with `Unrecognized field: mcpServers`).

The easiest way to add either scope is the CLI itself, which writes the correct file for you. Quote the `${METIS_API_KEY}` reference exactly as shown (single quotes) so your shell does not expand it before `claude mcp add` sees it — otherwise your actual key gets written as a literal into the config file, which is the hardcoding this whole section is trying to avoid:

```bash
claude mcp add --scope user fca-handbook-harness-mcp -e 'METIS_API_KEY=${METIS_API_KEY}' -- fca-handbook-harness-mcp
```

This is Method A — export the real key in your shell profile as shown below. Use `--scope project` instead of `--scope user` for a project-local setup. If you would rather edit the file directly, or want Method B (`.env`), see below.

##### Global Configuration (Recommended for FS Firms)

If you work across multiple projects, configure the MCP globally so it is available everywhere. Because this file is shared machine-wide, use **Method A** — a stray `.env` lookup path is per-project and does not fit a global setup as cleanly.

**File location:** `~/.mcp.json` (your home directory — note this is a standalone file, not inside `.claude/`)

Edit or create `~/.mcp.json` and add:

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

**File location:** `.mcp.json` in your project root (a standalone file, not inside `.claude/`)

Edit or create `.mcp.json` and add — no `env` block, per Method B above:

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

**Important:** Project-level `.mcp.json` and `.env` files are often checked into version control — ensure `METIS_API_KEY` is in `.gitignore` before committing (the `.mcp.json` itself contains no secret, since Method B omits the `env` block), or use the global configuration approach instead (recommended for FS firms).

**Restart:** Claude Code will detect the change and reload MCP connections automatically (or you can restart the IDE).

#### Claude Desktop (local)

**File location:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

Claude Desktop's config is inherently machine-wide (there is no project-local variant), so **Method A** is the more consistent fit — see the ⚠️ note above before using Method B here. If the file already exists, add the `mcpServers` entry to it rather than overwriting the file. On Windows, set the variable with `setx` (see step 2 above) and restart Claude Desktop.

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

#### Other clients (local)

These clients typically use the same `mcpServers` JSON shape as Claude Desktop above. Consult your client's documentation for the config file location, restart procedure, and whether it performs `${VAR}` substitution in `env` blocks the way Claude Code and Claude Desktop do (some use GUI connectors rather than JSON files, or may not substitute at all — check before relying on Method A).

### Verify the local connection

See [Verify the connection](#3-verify-the-connection) above. The same first-run approval gate applies to a project-scoped `.mcp.json`.

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

**Remote server: the tool returns "Missing API key" or "Invalid or revoked API key":**
- "Missing API key" means the client is not sending an `Authorization: Bearer <key>` header. Check the `headers` entry in your config.
- "Invalid or revoked API key" with a key you have confirmed on the dashboard usually means the `${METIS_API_KEY}` placeholder was not substituted, because the variable was not set when your client started. Start the client from a shell where `[ -n "$METIS_API_KEY" ] && echo set` prints `set`. Otherwise copy the key again from the dashboard, with no extra spaces or newlines.

**Remote server: the tool is not listed:**
- In Claude Code, run `claude mcp list`. `⏸ Pending approval` means the server needs approving (see "Verify the connection" above). Restart your client after adding the server.
- Check that your client supports the Streamable HTTP transport and can send a custom `Authorization` header. If it cannot, use the local server.

**Remote server: the connection drops or times out during a call:**
- A quick call takes 60-120 seconds and a full call longer. Raise your client's timeout if it has a short default. If your client or network cannot hold a connection open that long, use the local server instead.

**Claude Code: "Settings validation failed: Unrecognized field: mcpServers":**
- This means `mcpServers` was added to `.claude/settings.json` (or `~/.claude/settings.json`) — that file does not support it. Move the `mcpServers` block to `.mcp.json` (project-local) or `~/.mcp.json` (global) instead, per the local Claude Code section above, or run `claude mcp add --scope project|user ...` to have Claude Code write it for you.

**Claude Code: the model seems vaguely aware "an MCP" exists but does not know its name or what it does, and never calls it:**
- This is the first-run approval gate (see "Verify the connection" above), not a tool-description problem — an unapproved project-scoped `.mcp.json` server never actually connects, so the model never receives its real name/description/schema, only generic MCP-resource tools. Run `claude mcp list` to confirm (`⏸ Pending approval` means this is it), then run `/mcp` or restart `claude` interactively to approve it.

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
