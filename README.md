# AI Guest Post & Backlink Outreach MCP (`ai-guestpost-outreach-mcp`)

An open-source **Model Context Protocol (MCP) server** that lets AI assistants (Claude Desktop, Claude Code CLI, Gemini, OpenAI Codex, Cursor) automate end-to-end guest post discovery, duplicate verification, and dual-draft email preparation directly in Gmail for **any niche**—with **zero Google Cloud Console setup required**.

## Core Features

- **All-Niche Prospect Discovery (`find_niche_guest_post_prospects`):** Searches the web for blogs and publications accepting guest posts in any industry (SaaS, Travel, UI/UX, Recruitment, E-commerce, Tech) and automatically extracts public editor/contact emails.
- **Duplicate Outreach Protection (`check_duplicate_outreach`):** Scans your Gmail `Sent` and `Drafts` folders before pitching so you never double-pitch the same domain or editor.
- **Simultaneous Dual-Draft Pipeline (`prepare_dual_outreach_drafts`):**
  1. **Draft 1 (The Cold Pitch):** Creates a clean, minimalist HTML pitch card offering 3 tailored article concepts.
  2. **Draft 2 (The Pre-Written Article):** Simultaneously creates a second Gmail draft addressed to the exact same recipient containing the complete, publication-ready HTML guest post—ready to hit send the moment the editor accepts your pitch.

---

## Quick Start (No Google Cloud / OAuth Needed)

### 1. Clone & Install Dependencies

    git clone https://github.com/Abdell1111/ai-guestpost-outreach-mcp.git
    cd ai-guestpost-outreach-mcp
    pip install -r requirements.txt

### 2. Add to Your AI Client (With Your Gmail App Password)

1. Go to your [Google Account App Passwords](https://myaccount.google.com/apppasswords) page and generate a 16-letter App Password.
2. Add this block to your local `claude_desktop_config.json`, `.mcp.json`, or Cursor/Codex MCP settings:

    {
      "mcpServers": {
        "outreach-engine": {
          "command": "python",
          "args": ["/absolute/path/to/ai-guestpost-outreach-mcp/server.py"],
          "env": {
            "GMAIL_ADDRESS": "your.email@gmail.com",
            "GMAIL_APP_PASSWORD": "xxxx xxxx xxxx xxxx"
          }
        }
      }
    }

---

## Example Prompts in AI Chat

Once connected, prompt your AI assistant in plain English:

- *"Find 5 UI/UX design blogs accepting guest posts, check if I have ever emailed them in Gmail, and prepare the dual drafts (pitch + full article) linking to my website."*
- *"Check if we ever pitched editor@exampleblog.com. If not, prepare a guest post pitch with 3 topic ideas and simultaneously prepare the second draft with the full 1,000-word HTML article for Topic #1."*

## License

MIT License
