# API Setup Guide — FCA Handbook Compliance Analysis HTTP API

## Overview

Once you have your API key from your account dashboard, follow these instructions to set it up in your environment and start making requests.

**Before you start:** You should have:
- A paid (Stripe) account, created via the "Create Account" flow at `https://fcahandbookharnessimplementation.onrender.com` (there is no separate `/signup` page — it is a modal on the main page)
- An API key generated from the admin dashboard's API Keys section (shown once, then hidden)
- The API key copied and saved somewhere secure

---

## Step 0: Install Dependencies (if using the MCP server)

If you are integrating via MCP with Claude Desktop, first install the Python dependencies:

```bash
pip install -r requirements.txt
```

This installs `mcp` (the Model Context Protocol server) and `requests` (for HTTP calls).

---

## Step 1: Store Your API Key Securely

**Never commit API keys to git or hardcode them in source files.** Always use environment variables.

### Option A: Export to current shell session (temporary)

**Bash/Zsh:**
```bash
export METIS_API_KEY="sk_live_abc123xyz..."
```

This only lasts for the current terminal session. Useful for testing.

### Option B: Add to shell profile (persistent, per-machine)

**Bash** (`~/.bashrc` or `~/.bash_profile`):
```bash
export METIS_API_KEY="sk_live_abc123xyz..."
```

**Zsh** (`~/.zshrc`):
```bash
export METIS_API_KEY="sk_live_abc123xyz..."
```

**Fish** (`~/.config/fish/config.fish`):
```fish
set -x METIS_API_KEY "sk_live_abc123xyz..."
```

Then reload your shell:
```bash
source ~/.bashrc  # or ~/.zshrc, etc.
```

### Option C: Use a `.env` file (project-specific)

Create a `.env` file in your project root:
```
METIS_API_KEY=sk_live_abc123xyz...
```

Then load it before running your code:
```bash
source .env
python your_script.py
```

Or use a library like `python-dotenv` to load it automatically (see Python example below).

**Important:** Add `.env` to `.gitignore` so it is never committed:
```bash
echo ".env" >> .gitignore
```

### Option D: Windows PowerShell

```powershell
$env:METIS_API_KEY = "sk_live_abc123xyz..."
```

Or persistently, add to your PowerShell profile:
```powershell
$PROFILE  # Shows your profile location
# Then edit that file and add:
$env:METIS_API_KEY = "sk_live_abc123xyz..."
```

---

## Step 2: Use Your API Key in Code

### Python

**Simple approach (environment variable):**
```python
import os
import requests

api_key = os.getenv("METIS_API_KEY")

response = requests.post(
    "https://fcahandbookharnessimplementation.onrender.com/v1/analyze",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "user_input": "Robo-advisor platform, £500k-£1M portfolios, retail investors. Question: What FCA authorisation and permissions do we need?"
    },
    stream=True
)

for line in response.iter_lines():
    if line and line.startswith(b'data:'):
        import json
        data = json.loads(line[5:].decode('utf-8'))
        print(f"[{data['type']}] {data['content']}")
```

**With `.env` file (using `python-dotenv`):**
```python
from dotenv import load_dotenv
import os
import requests

load_dotenv()  # Loads .env file automatically
api_key = os.getenv("METIS_API_KEY")

# Rest of code same as above
```

Install `python-dotenv`:
```bash
pip install python-dotenv
```

### JavaScript/Node.js

**Simple approach (environment variable):**
```javascript
const apiKey = process.env.METIS_API_KEY;

const response = await fetch(
    "https://fcahandbookharnessimplementation.onrender.com/v1/analyze",
    {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${apiKey}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_input: "Robo-advisor platform, £500k-£1M portfolios, retail investors. Question: What FCA authorisation and permissions do we need?"
        })
    }
);

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const text = decoder.decode(value);
    console.log(text);
}
```

**With `.env` file (using `dotenv`):**
```javascript
require('dotenv').config();
const apiKey = process.env.METIS_API_KEY;

// Rest of code same as above
```

Install `dotenv`:
```bash
npm install dotenv
```

### Go

```go
package main

import (
    "fmt"
    "io"
    "net/http"
    "os"
    "bytes"
    "encoding/json"
)

func main() {
    apiKey := os.Getenv("METIS_API_KEY")
    
    payload := map[string]string{
        "user_input": "Robo-advisor platform, £500k-£1M portfolios, retail investors. Question: What FCA authorisation and permissions do we need?",
    }
    
    jsonData, _ := json.Marshal(payload)
    
    req, _ := http.NewRequest(
        "POST",
        "https://fcahandbookharnessimplementation.onrender.com/v1/analyze",
        bytes.NewBuffer(jsonData),
    )
    
    req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", apiKey))
    req.Header.Set("Content-Type", "application/json")
    
    client := &http.Client{}
    resp, _ := client.Do(req)
    defer resp.Body.Close()
    
    io.Copy(os.Stdout, resp.Body)
}
```

### cURL

```bash
curl -N -X POST https://fcahandbookharnessimplementation.onrender.com/v1/analyze \
  -H "Authorization: Bearer $METIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Robo-advisor platform, £500k-£1M portfolios, retail investors. Question: What FCA authorisation and permissions do we need?"
  }'
```

(Make sure `METIS_API_KEY` is exported in your shell first.)

---

## Step 3: Handle Streaming Responses

All responses from the API are **Server-Sent Events (SSE) streams** — even
though only three event types actually occur on this endpoint. Parse them
as shown above, watching for:

- `"type": "message"` — Progress notifications, one per reasoning node (7-8 total, including "Analysis complete"). Each contains a human-readable description of what's happening.
- `"type": "analysis"` — The final result (`content` is already a JSON object, not a string to re-parse)
- `"type": "error"` — Terminal error (budget exceeded, out-of-scope question, or any other failure); `content` is a plain string

There's a real 60-120 second gap between the first `message` and the final `analysis`/`error` — this is not a token-by-token reasoning stream. Use the `message` events to show the user progress, rather than waiting silently.

---

## Step 4: Handle Errors

There are two levels of failure. HTTP-level errors happen before the stream
even opens; everything else arrives as an in-stream `"type": "error"` event
over a normal HTTP 200.

### 401 Unauthorized (HTTP-level)

**Problem:** `"Missing or invalid Authorization header"` or `"Invalid or revoked API key"`

**Solutions:**
1. Check your API key is correct (copy from dashboard again)
2. Verify you are exporting it to your environment: `echo $METIS_API_KEY`
3. Check the header is `Authorization: Bearer <key>` (not just `<key>`)
4. Verify no extra spaces or newlines: `export METIS_API_KEY="sk_live_..."` (not `" sk_live_..."`)

### 404 Not Found (HTTP-level)

**Problem:** the account behind your API key no longer exists.

**Solution:** Contact whoever administers the account; the key may need regenerating under a current account.

### 422 Unprocessable Entity (HTTP-level)

**Problem:** the request body is missing `user_input`.

**Solution:** Send `{"user_input": "..."}` — that's the only field this endpoint accepts.

### Budget exceeded (in-stream)

**Problem:** `{"type": "error", "content": "This account has been used up to your budget. The monthly limit needs to be reset."}`

**Solution:** An admin needs to raise `monthly_limit` from the account dashboard.

### Out-of-scope question (in-stream)

**Problem:** the question did not pass the triage gate (Node 1) — it does not
look like it is about financial services regulation. You will see an `error`
event with a message like `"...Please ask a question relating to the
provision of financial services."`

**Solution:** Rephrase `user_input` to make the financial-services angle explicit.

There is currently **no 429 rate limiting** on this endpoint — plan client
concurrency accordingly.

---

## Troubleshooting

### "METIS_API_KEY not found"

Check your environment variable is exported:
```bash
echo $METIS_API_KEY
```

If blank, re-export:
```bash
export METIS_API_KEY="sk_live_..."
source ~/.bashrc  # or ~/.zshrc
```

### API key works locally but fails in CI/CD (GitHub Actions, etc.)

Set your API key as a **secret** in your CI/CD platform (not in code or `.env` file):

**GitHub Actions example:**
```yaml
env:
  METIS_API_KEY: ${{ secrets.METIS_API_KEY }}
```

Go to your repo Settings → Secrets → New secret, add `METIS_API_KEY`.

### "Can't reproduce the token counts"

`tokens.total` in the response is the sum of input and output tokens across
every Claude call in the run (the triage gate plus every Harness node that
calls Claude). It accounts for your `user_input` and Claude's reasoning
output.

Token counts are **not** deterministic — identical input can produce
slightly different token counts (and different reasoning) on different
runs. They're for cost/complexity tracking, not reproducibility. They also
do not determine what is billed — billing is a flat £7.95 per call.

---

## Best Practices

1. **Never hardcode keys** — always use environment variables
2. **Rotate keys** — regenerate from dashboard periodically (old key becomes invalid)
3. **Monitor usage** — check your account dashboard for monthly spend
4. **Use per-user keys** — if your firm has multiple users, each should have their own key (easier to audit, rotate, or revoke)
5. **Log token counts** — store `total_tokens` per request for cost tracking and optimization

---

## Next Steps

- Read [schema.md](./schema.md) for the complete API specification
- See [tool.json](./tool.json) for the tool schema
- Read [README.md](./README.md) for integration methods (HTTP API and MCP)

---

