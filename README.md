# AI Guest Post & Backlink Outreach MCP (`ai-guestpost-outreach-mcp`)

An open-source **Model Context Protocol (MCP) server** that allows AI assistants (Claude Desktop, Claude Code CLI, Gemini, OpenAI Codex, Cursor) to automate end-to-end guest post discovery, duplicate verification, and dual-draft email preparation directly in Gmail for **any niche**.

## Core Features

- **All-Niche Prospect Discovery (`find_niche_guest_post_prospects`):** Searches the web for blogs and publications accepting guest posts in any industry (SaaS, Travel, UI/UX, Recruitment, E-commerce, Tech) and automatically extracts public editor/contact emails.
- **Duplicate Outreach Protection (`check_duplicate_outreach`):** Scans Gmail `SENT` and `DRAFTS` before pitching to ensure you never double-pitch the same domain or editor.
- **Simultaneous Dual-Draft Pipeline (`prepare_dual_outreach_drafts`):**
  1. **Draft 1 (The Cold Pitch):** Creates a clean, minimalist HTML pitch card offering 3 tailored article concepts.
  2. **Draft 2 (The Pre-Written Article):** Simultaneously creates a second Gmail draft addressed to the exact same recipient containing the complete, publication-ready HTML guest post—ready to hit send the moment the editor accepts your pitch.

---

## Quick Start

### 1. Clone & Install Dependencies
```bash
git clone [https://github.com/Abdell1111/ai-guestpost-outreach-mcp.git](https://github.com/Abdell1111/ai-guestpost-outreach-mcp.git)
cd ai-guestpost-outreach-mcp
pip install -r requirements.txt
