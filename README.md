# 🧠 GHL MCP Server – Anthropic LangGraph Agent Integration

## 🧭 Purpose

This project exposes GoHighLevel (GHL) sub-account tools to an Anthropic-powered LangGraph agent using the **Model Connection Protocol (MCP)**. It acts as a secure intermediary layer between the LangChain ecosystem and GHL APIs—designed for clean modular separation and zero-handoff latency.

This repo is built to support:
- 🔹 Claude-based LangGraph Agents as MCP clients
- 🔹 FastAPI MCP Server exposing GHL sub-account tools (contacts, pipelines, automations)
- 🔹 Secure credential loading via `.env`
- 🔹 Dynamic tool registration using LangChain MCP adapters

---

## 🧱 Architecture

```text
 ┌────────────────────────────────────┐
 │          LangGraph Agent           │
 │  (Claude, Anthropic, LangChain)    │
 └────────────────────────────────────┘
                │
         MCP Client (HTTP)
                │
 ┌────────────────────────────────────┐
 │         GHL MCP Server (This)      │
 │   FastAPI + LangChain Tools        │
 └────────────────────────────────────┘
                │
        REST API → GHL Sub-Account
```

* **MCP Server** = `FastAPI` server exposing LangChain-compatible tools from GHL
* **LangGraph Agent** = Claude-powered LangChain graph calling `MCPClient.load_tools()`
* **Secure Comm** = All tool usage routed over HTTP via LangChain's MCP standard

---

## 📦 Tool Endpoints to Expose

Each tool is implemented using `@mcp_tool` and automatically discoverable by any LangChain-compatible MCP client.

| Tool Name            | GHL Endpoint            | Description                        |
| -------------------- | ----------------------- | ---------------------------------- |
| `get_contact_info`   | `/contacts/{id}`        | Fetch contact details              |
| `list_opportunities` | `/opportunities/`       | List all open opps                 |
| `trigger_webhook`    | Custom workflow trigger | Hit custom workflow webhook        |
| `get_pipeline_info`  | `/funnels/`             | Retrieve funnel/pipeline structure |
| `create_note`        | `/contacts/{id}/notes`  | Create a note on contact           |

---

## 🔐 ENV VARS (.env)

Set the following variables in `.env` at the root of `ghl_mcp_server/`:

```env
GHL_API_BASE_URL=https://rest.gohighlevel.com/v1
GHL_API_KEY=sk_your_primary_api_key_here
GHL_SUB_ACCOUNT_ID=abc123456789
ALLOWED_ORIGINS=*
```

---

## 🕵️ GHL SCAVENGER HUNT CHECKLIST

To go live, collect these credentials:

| 🧩 What                    | 📍 Where to Find It                                |
| -------------------------- | -------------------------------------------------- |
| `GHL_API_KEY`              | GHL → Settings → API Keys (create or use existing) |
| `GHL_SUB_ACCOUNT_ID`       | URL bar while inside the sub-account dashboard     |
| `Webhook Trigger URLs`     | Automations → Webhook → Copy full URL              |
| `Funnel / Pipeline IDs`    | Funnels → Click → Copy from URL                    |
| `Contact ID` (for testing) | Contacts → Click any → Copy ID from URL            |

---

## 🚀 Dev Startup

```bash
# 1. Create .env file with your real credentials
# Copy the template below and save as .env in the project root:
#
# GHL_API_BASE_URL=https://rest.gohighlevel.com/v1
# GHL_API_KEY=sk_your_primary_api_key_here
# GHL_SUB_ACCOUNT_ID=abc123456789
# ALLOWED_ORIGINS=*
# ANTHROPIC_API_KEY=your_anthropic_api_key_here

# 2. Install deps
pip install -r requirements.txt

# 3. Run server
uvicorn mcp_server:app --host 0.0.0.0 --port 8000
# OR use the startup script:
python scripts/start_server.py

# 4. Test the server
python examples/simple_client.py

# 5. Try interactive mode
python examples/simple_client.py interactive
```

---

## 🧰 Stack

* Python 3.11+
* FastAPI
* `langchain-mcp-adapters`
* MCPServer + Claude LangGraph agent
* Optional: NGROK or Azure App Service for public MCP endpoint

---

## 🎯 Goal

By running this repo, your Claude-powered agent can query GHL data and trigger workflows **through MCP** with zero coupling. Extend this to include new GHL tools as needed.

> "Modular tools. Global reach. Absolute power."

⚡ Ready to connect your Claude agent to GoHighLevel! 