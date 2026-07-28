# Metis FCA Handbook AI Harness — MCP Server

An MCP (Model Context Protocol) server that integrates the Metis FCA Handbook AI Harness into Claude Desktop and other MCP-compatible agents.

**Tool name:** `evaluate_fca_handbook_applicability`

Use this tool to analyze FCA Handbook applicability for a product, service, or firm. Returns structured compliance reasoning with verbatim handbook citations.

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

### 2. Install Dependencies

```bash
pip install -r requirements.txt
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
      "command": "python",
      "args": ["/path/to/mcp_server.py"],
      "env": {
        "METIS_API_KEY": "sk_live_..."
      }
    }
  }
}
```

Replace `/path/to/mcp_server.py` with the actual path to the file.

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
- Check that `mcp_server.py` path is absolute and correct
- Restart Claude Desktop (not just reload)

**401 Unauthorized:**
- Verify `METIS_API_KEY` is set in the config `env`
- Check the key is correct (copy from dashboard again)
- Ensure no extra spaces or newlines in the key

**Connection timeout:**
- The analysis can take 60-120 seconds (quick mode) or longer (full mode)
- Ensure you have internet access to fcahandbookharnessimplementation.onrender.com

## Files

- **mcp_server.py** — MCP server implementation
- **requirements.txt** — Python dependencies (`mcp`, `requests`)
- **__init__.py** — Python package marker
- **LICENSE** — MIT License

## Support

For questions or issues, contact: `the-metis-fca-handbook-ai-harness@jbmd.co.uk`

---

**Product:** Metis FCA Handbook AI Harness  
**Version:** 3.0.0  
**License:** MIT
