# Metis FCA Handbook AI Harness — MCP Server

<!-- mcp-name: io.github.99blakeD99/the-metis-fca-handbook-ai-harness-mcp -->

An MCP (Model Context Protocol) server for The Metis FCA Handbook AI Harness. MCP is supported by Claude, OpenAI, Gemini and most desktop and IDE clients (Cursor, Windsurf, Cline and others). This README uses Claude Code as the tested example for the recommended remote server, and Claude Code and Claude Desktop for the local fallback; adapt the steps to your own client.

**Source & full documentation:** [github.com/99blakeD99/the-metis-fca-handbook-ai-harness-mcp-files](https://github.com/99blakeD99/the-metis-fca-handbook-ai-harness-mcp-files)

## Tool

The Harness consists of one tool, `evaluate_fca_handbook_applicability`, which evaluates which FCA Handbook entries apply to a described situation. Stateless: nothing is kept between calls, so each refinement run sends the whole input again. A call takes 60-120 seconds; quick mode (the default) is a first pass, and full mode gives more detailed reasoning. Returns a structured result with verbatim citations and refinement suggestions, which identify gaps in the information you provided and how to fill them (see Using the Tool). The Harness is not endorsed by the FCA and does not provide legal, financial or compliance advice: it supports the advisers who work with the Handbook. Your AI assistant gathers what the Harness needs, asking you for anything missing, and proposes further runs when the result suggests refinements. Each call is billed (see Cost); the AI is told that the cost is not significant for a typical professional user, and may remind you if the runs accumulate.

## Why choose The Metis FCA Handbook AI Harness?

- **Efficiency** Multiplies effectiveness of compliance advice. Saves £80+ in token fees per Harness run.

- **Deals with "Hard Problem"**, in which LLMs' token incentives prioritise training data so results are unreliable.

- **Verbatim citations** Quotes verbatim entries from the FCA Handbook. Other AI systems struggle to do this.

- **Matches real-world need** You do not have to start off knowing which sections you are looking for. Carries out structured searches across all 33,000+ FCA Handbook entries.

- **Secure Design** Harness compartmentalisation and statelessness fit natively with emerging AI agent security standards such as OWASP Top 10 for Agentic Applications 2026.

- **AI Accessible** Integrates easily with AI workflows and agents. Your LLM can use it as a tool.

## Try the Harness Live

Experience the Harness interactively before integrating:

```
https://fcahandbookharnessimplementation.onrender.com
```

Email `the-metis-fca-handbook-ai-harness@jbmd.co.uk` and request a free temporary Access Code.

Ask compliance questions in natural language and watch each reasoning step unfold in real-time.

## Design Principles

- **Stateless** — each call is complete in itself and nothing is kept between calls; a refinement run sends the whole input again
- **Documented contract** — a typed input and a documented output (see Using the Tool)
- **Hosted** — the Handbook data and the reasoning live in one place, so results use the current Handbook
- **Updates** — the remote MCP server is updated centrally; the local MCP package (`pip`) can be version-pinned
- **Single point of failure** — if the Harness is down, it is obvious; there are no cascading configuration issues

## Use Cases for the Harness's MCP Server

### Compliance AI Platforms
Embed FCA reasoning as a service within your compliance platform. Your platform or its AI gathers the situation, calls the Harness and presents the structured result.

### AI Agent Workflows
Agents building compliance workflows can include FCA Handbook reasoning as a tool: no custom integration code, just MCP configuration.

### Compliance Review Automation
Integrate into document review or due-diligence pipelines to screen rules for FCA applicability.

## Quick Start

Setup is a one-off task for whoever manages your AI tools. Once connected, your compliance staff simply ask their AI assistant.

**Which setup to use:**

1. Use the **remote server** (step 2) if your client can connect to a remote MCP server and send a custom `Authorization` header. Nothing is installed; you need a URL and your API key. This is the recommended setup.
2. Otherwise use the [local server](#alternative-run-the-server-locally-stdio), which runs on your machine and passes each call on to the hosted Harness.

Both give the same tool and results, billed at the same rate. For Claude Desktop, use the local server.

### If you are an AI assistant setting this up for a user

Follow these rules as well as the steps below:

- **Setup:** for Claude Code, use the remote setup in step 2a with `--scope user` unless the user asks for a project-only setup. For Claude Desktop, use the local setup. For other clients, use the settings in step 2b.
- **The API key** must come from the user's environment variable `METIS_API_KEY`. Never ask the user to paste it into this conversation, never write it to a file in a project or repository, and never put it as a literal value in a configuration file; configuration files use the `${METIS_API_KEY}` reference shown below. To check it is set without printing it, run `[ -n "$METIS_API_KEY" ] && echo set || echo unset`. If it is unset, tell the user how to set it (step 2), wait until they confirm, and change no configuration and use no placeholder meanwhile. If the user pastes their key into the conversation anyway, do not use, repeat or write it anywhere, and suggest they regenerate it on the dashboard.
- **Configuration:** use `claude mcp add`, or `.mcp.json` (one project) or `~/.claude.json` (all projects, where `claude mcp add --scope user` writes). Prefer the CLI: `~/.claude.json` is the route we tested, and a hand-made `~/.mcp.json` is untested. Never put an `mcpServers` entry in `.claude/settings.json`.
- **Verify** that the tool `evaluate_fca_handbook_applicability` is listed. In Claude Code, run `claude mcp list` to see whether the server is connected; `/mcp` lists its tools, but only the user can run it, so ask them. In other clients, check the MCP settings screen. **Do not call the tool to test it:** every call is a real run, billed to the user, and takes a minute or two. Call it only when the user asks a real FCA Handbook question.
- **Success** means the server shows as connected and the tool is listed. Two known failures are `⏸ Pending approval` (the user must approve the server; see step 3) and a 401 on first use (see Troubleshooting).

### 1. Get an API Key

If you already have an API key, skip to step 2. Otherwise:

1. Visit `https://fcahandbookharnessimplementation.onrender.com`.
2. Click **"Create Account"** (modal on the homepage) and complete the Stripe payment flow (accounts are paid).
3. Go to **API Keys**, generate a new key and save it securely.

### 2. Connect your client to the remote server

```
https://fcahandbookharnessimplementation.onrender.com/mcp
```

The remote server uses the Streamable HTTP transport and expects your API key as a bearer token in the `Authorization` header of each request.

**Important:** supply the key from an environment variable or secrets manager, never as a literal value in a configuration file that may be committed to a shared repository. Add this line to your shell startup file (`~/.bashrc`, `~/.zshrc` and so on) and start your client afterwards, so that the variable is in the client's own environment:

```bash
export METIS_API_KEY="sk_live_..."
```

Replace `sk_live_...` with your key. On Windows, run `setx METIS_API_KEY "sk_live_..."` in Command Prompt, then restart your client. Start your client from a terminal if you can: an app launched from the Dock, Spotlight or the Start menu may not see a variable set in a shell startup file.

#### 2a. Claude Code

Use the CLI, which writes the correct file for you. Quote the header exactly as shown (single quotes) so that your shell does not expand `${METIS_API_KEY}`; otherwise your actual key is written to the config file as a literal.

```bash
claude mcp add --transport http --scope user fca-handbook-harness-mcp https://fcahandbookharnessimplementation.onrender.com/mcp --header 'Authorization: Bearer ${METIS_API_KEY}'
```

A `--scope user` entry applies to every Claude Code project on the machine until you run `claude mcp remove`; use `--scope project` for a project-only setup. To edit a file directly, add the entry below under the top-level `mcpServers` key of `~/.claude.json` (all projects; the file also holds your other Claude Code settings, so edit with care) or in `.mcp.json` in your project root (that project only). `.mcp.json` is a standalone file, not inside `.claude/`; Claude Code rejects an `mcpServers` key in `.claude/settings.json`.

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

Claude Code substitutes `${METIS_API_KEY}` from your environment when it starts. If the variable is not set then, it sends the literal text `${METIS_API_KEY}` as your key (and warns), which gives a 401 that is easy to mistake for a bad key. Start Claude Code from a shell where `[ -n "$METIS_API_KEY" ] && echo set` prints `set`. If the tool does not appear, restart Claude Code.

#### 2b. Other clients

Cursor, VS Code (Copilot), Gemini CLI, Cline and other developer tools and agent frameworks can connect to a remote MCP server given a URL and a custom header. They should work with the settings below but have not been tested by us. Field names and file locations differ and are still changing, so follow your client's documentation.

- **URL:** `https://fcahandbookharnessimplementation.onrender.com/mcp`
- **Transport:** Streamable HTTP
- **Header:** `Authorization: Bearer <your API key>`, read from an environment variable if your client supports that. The syntax differs between clients (Cursor documents `${env:METIS_API_KEY}` where Claude Code uses `${METIS_API_KEY}`); use your client's own, and never a literal key.
- **Timeout:** a call takes 60-120 seconds. Raise your client's timeout if its default is shorter.

A client that accepts only no authentication or OAuth for remote servers cannot send a static API key; use the [local server](#alternative-run-the-server-locally-stdio) with it.

### 3. Verify the connection

**Claude Code, first run only:** the first time you launch `claude` (interactively, not with `-p`) in a project with a new or changed project-scoped `.mcp.json`, it shows a one-time approval prompt for that server. Until you accept it, the server stays in a "pending approval" state and its tool is not available (`claude mcp list` shows `⏸ Pending approval`). Accept the prompt, or run `/mcp` in an existing session. This does not apply to user scope (`--scope user`, stored in `~/.claude.json`).

Once connected, `evaluate_fca_handbook_applicability` should be available as a tool. `Connected` in `claude mcp list` only means the server started; it does not prove your key is accepted. A key that was not set when your client started, or was mistyped, appears as a 401 or "Invalid or revoked API key" on the first real call, and can look like a fault in the service. Do not call the tool just to test the connection: every call is a real run, billed to your account.

## Alternative: run the server locally (stdio)

Use this if your client cannot connect to the remote server. A small local server runs on your machine and passes each call on to the hosted Harness, using the same API key. You need Python 3.10 or later.

### Install the local server

```bash
pip install fca-handbook-harness-mcp
```

If `pip` refuses with "externally managed environment" (common on recent Linux and macOS), use `pipx`, which gives the server its own environment and puts the command on your PATH:

```bash
pipx install fca-handbook-harness-mcp
```

### Configure your MCP client (local)

The `mcpServers` JSON below is shared by most desktop and IDE clients, but the file location and restart step vary.

**Important:** supply the API key at runtime from an environment variable or secrets manager, never as a literal value in a configuration file that may be committed to a shared repository. Pick one method; they need different config:

- **Method A — shell profile.** Add `export METIS_API_KEY="sk_live_..."` to your shell startup file before launching your client, so the variable is in the client's own environment. The MCP config then references it:
  ```json
  "env": { "METIS_API_KEY": "${METIS_API_KEY}" }
  ```
- **Method B — `.env` file.** Create a `.env` file in your project directory containing `METIS_API_KEY=sk_live_...`. The server loads it itself at startup, so your client never sees the value. **Omit the `env` block from your MCP config entirely.** Do not copy the Method A snippet: your client's environment will not have the variable, the substitution will fail silently, and the literal text `${METIS_API_KEY}` will be sent as your key, giving a 401 that is easy to mistake for a revoked key.

⚠️ A user-scope config (`~/.claude.json`) applies to every project on the machine, so a stray `${METIS_API_KEY}` placeholder there breaks the MCP server in every project. Prefer a project-local config unless you want a shared, machine-wide key.

#### Claude Code (local)

MCP servers are configured in `.mcp.json` files or `~/.claude.json`, never in `.claude/settings.json`, which rejects an `mcpServers` key (`Unrecognized field: mcpServers`). The easiest route is the CLI. Quote the reference exactly as shown (single quotes) so that your shell does not write your actual key into the file:

```bash
claude mcp add --scope user fca-handbook-harness-mcp -e 'METIS_API_KEY=${METIS_API_KEY}' -- fca-handbook-harness-mcp
```

This is Method A with user scope; use `--scope project` for a project-local setup. To edit files directly:

##### Global configuration (recommended for FS firms)

Use Method A. Add the entry below to the top-level `mcpServers` key of `~/.claude.json` (your home directory, not inside `.claude/`). The file already holds other settings, so do not overwrite it; the CLI command above is the safer route.

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

Then add `export METIS_API_KEY="sk_live_..."` to your shell profile **before** starting Claude Code, replacing `sk_live_...` with your key. Claude Code substitutes the variable when it starts the server; if it is not set then, the server loads with the literal `${METIS_API_KEY}` (with a warning), which causes the 401 described in Troubleshooting. Restart Claude Code; the tool is then available in all projects.

##### Project-level configuration (single project)

The natural fit for Method B. Create `.mcp.json` in your project root (not inside `.claude/`), with no `env` block:

```json
{
  "mcpServers": {
    "fca-handbook-harness-mcp": {
      "command": "fca-handbook-harness-mcp"
    }
  }
}
```

Then create a `.env` file in the project root containing `METIS_API_KEY=sk_live_...`. These files are often checked into version control: ensure `.env` is in `.gitignore` before committing (`.mcp.json` holds no secret, since Method B omits the `env` block), or use the global configuration instead. Claude Code reloads MCP connections automatically, or restart the IDE.

#### Claude Desktop (local)

Config file:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

The config is machine-wide, so Method A is the better fit (see the ⚠️ note above before using Method B). If the file exists, add the `mcpServers` entry to it; do not overwrite it. On Windows, set the variable with `setx` (see step 2).

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

Set `METIS_API_KEY` in your system environment before launching Claude Desktop. For Method B, put `METIS_API_KEY=sk_live_...` in a `.env` file in the directory Claude Desktop runs from and omit the `env` block entirely. Then quit and restart the app.

#### Other clients (local)

These usually use the same `mcpServers` JSON as Claude Desktop. Check your client's documentation for the file location, the restart step, and whether it substitutes `${VAR}` in `env` blocks as Claude Code and Claude Desktop do (some use GUI connectors, or do not substitute at all; check before relying on Method A).

### Verify the local connection

See step 3 above. The same first-run approval gate applies to a project-scoped `.mcp.json`.

## Using the Tool

The tool accepts two parameters:

- **user_input** (required): the situation to evaluate, as one piece of text, ideally no more than 5000 characters: the primary question, the product or service, who provides it, its key features, the target market, and the types of data it handles.
- **analysis_mode** (optional): `"quick"` (default; a first pass) or `"full"` (detailed conditional reasoning)

The tool returns:
- **summary**: 1-2 sentences in quick mode, 2-3 in full mode
- **entry_analysis**: for each retrieved Handbook entry, whether it applies, whether it is conditional, and the reasoning (the Handbook text itself is in `citations`)
- **obligations**: the high-confidence obligations (quick mode returns only these) and, in full mode, the low-confidence or tangential ones, each optionally flagged with the condition under which it applies
- **refinement_suggestions**: each gives a gap (what the Harness could not determine from your input), why it matters, and the edit that would settle it
- **citations**: for each applicable entry, the verbatim Handbook text with its title, precise citation (where there is one), source URL and binding level (R=Rule, G=Guidance)
- **input_reading**: how the Harness read your input (the distilled question, entity name and type, target market), so you can check it understood you
- **glossary_terms_referred**: names only (no definitions) of the Handbook Glossary terms that the applicable entries use, which carry their Handbook meaning
- **tokens**: `input`, `output` and `total` token counts

## Cost

Each call is a live reasoning run, billed to the configured account at £7.95 plus VAT for either mode. Sometimes several runs are needed. The tool description tells the calling AI that the user is normally a compliance professional at a financial institution, for whom this level of cost is not significant, and that it may remind you of the accumulating cost if you ask for many runs; whether it tells you as it goes or asks before a run is left to its judgement. A run that fails, or whose result is never delivered, is not billed.

## Troubleshooting

**"Missing API key" or "Invalid or revoked API key" (remote server), or a 401 with a key you have confirmed on the dashboard:**
- "Missing API key" means the client is not sending an `Authorization: Bearer <key>` header. Check the `headers` entry in your config.
- A message saying the key "looks like an unsubstituted placeholder" means the server received the literal text `${METIS_API_KEY}`: your client did not read the environment variable. Set `METIS_API_KEY` before starting the client (Method A), or use Method B without an `env` block. Start the client from a shell where `[ -n "$METIS_API_KEY" ] && echo set` prints `set`.
- With the local server, check that the key is set in exactly one place: the config `env` block (Method A) or a `.env` file (Method B), not both and not neither. A config that still has an `env` block written for Method A while Method B is in use sends the placeholder. You can inspect the running server's environment (for example `/proc/<pid>/environ` on Linux) to see what it receives.
- Otherwise copy the key again from the dashboard, with no extra spaces or newlines.

**The tool is not listed:**
- In Claude Code, run `claude mcp list`. `⏸ Pending approval` means the server needs approving (see step 3). Restart your client after adding the server.
- Remote server: check that your client supports the Streamable HTTP transport and can send a custom `Authorization` header; if not, use the local server.
- Claude Desktop and most desktop clients: verify the config file path (see above) and restart the client fully, not just reload. Confirm that `fca-handbook-harness-mcp` resolves on the command line (`which fca-handbook-harness-mcp`, or `where` on Windows). Desktop clients often launch with a minimal PATH; if it does not resolve, put the absolute path from that lookup in `"command"`.

**Claude Code: the model seems vaguely aware "an MCP" exists but does not know its name or purpose, and never calls it:**
- This is the first-run approval gate (see step 3), not a tool-description problem: an unapproved project-scoped server never connects, so the model sees only generic MCP-resource tools. Run `claude mcp list` (`⏸ Pending approval` confirms it), then run `/mcp` or restart `claude` interactively to approve.

**Claude Code: "Settings validation failed: Unrecognized field: mcpServers":**
- `mcpServers` was added to `.claude/settings.json` (or `~/.claude/settings.json`), which does not support it. Move the block to `.mcp.json` (project) or `~/.claude.json` (user), or run `claude mcp add --scope project|user ...` to have Claude Code write it.

**The connection drops or times out during a call:**
- A call takes 60-120 seconds. Raise your client's timeout if its default is shorter, and check that you can reach fcahandbookharnessimplementation.onrender.com. If your client or network cannot hold a connection open that long, use the local server.

## Files

- **mcp_server.py** — MCP server implementation (main entry point)
- **tool-description.md** — the single source of the tool description, title and annotations, read by `mcp_server.py` at startup
- **pyproject.toml** — PyPI package manifest
- **server.json** — MCP registry manifest (registry.modelcontextprotocol.io format)
- **manifest.json** — MCPB/Smithery bundle manifest
- **requirements.txt** — Python dependencies (`mcp`, `requests`)
- **uv.lock** — pinned dependency resolution for reproducible `uv run`
- **`__init__.py`** — Python package marker
- **README.md** — this file
- **LICENSE** — MIT License
- **.gitignore** — Git ignore rules
- **.mcpbignore** — files excluded from the MCPB bundle

## Support

For questions or issues, contact: `the-metis-fca-handbook-ai-harness@jbmd.co.uk`

---

**Product:** The Metis FCA Handbook AI Harness  
**License:** MIT
