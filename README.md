# AI Guest Post Outreach MCP Server

An automated Model Context Protocol (MCP) server built in Python that scrapes the web for niche guest post opportunities, extracts verified contact emails, checks existing Gmail communication to prevent duplicate outreach, and generates dual-draft HTML outreach pitches directly inside your Gmail account.

## Tech Stack
* **Python (v3.12)** with virtual environment support.
* **DuckDuckGo Search (`ddgs`)** & HTTP clients for prospect discovery.
* **IMAP (`imaplib`)** for direct Gmail draft integration and duplicate checking.
* **Model Context Protocol (MCP)** for seamless integration with AI clients (e.g., Claude Desktop).

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Abdell1111/ai-guestpost-outreach-mcp.git](https://github.com/Abdell1111/ai-guestpost-outreach-mcp.git)
   cd ai-guestpost-outreach-mcp
Create and activate a virtual environment:

Bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install "mcp<2"
Connecting to AI Assistants (Claude Desktop MCP)
Add this entry to your claude_desktop_config.json:

JSON
{
  "mcpServers": {
    "guestpost-outreach": {
      "command": "python",
      "args": ["/path/to/ai-guestpost-outreach-mcp/server.py"],
      "env": {
        "GMAIL_ADDRESS": "your-email@gmail.com",
        "GMAIL_APP_PASSWORD": "your-gmail-app-password"
      }
    }
  }
}
Ready-to-Use AI Prompt Template
Copy and paste this template into your AI assistant once connected:

Plaintext
Find [NUMBER] guest post opportunities for the niche "[YOUR_NICHE]" and automatically prepare outreach drafts for each discovered prospect. 

For the outreach emails, ensure the cold pitch and the full article draft include a natural contextual backlink pointing to my website: [YOUR_WEBSITE_URL] ([YOUR_WEBSITE_NAME]).
Example:

"Find 5 guest post opportunities for the niche "Morocco travel & desert tours" and automatically prepare outreach drafts for each discovered prospect. For the outreach emails, ensure the cold pitch and the full article draft include a natural contextual backlink pointing to my website: https://marruecos.cc (Marruecos)."
