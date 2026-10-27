import os
import re
import time
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
import httpx
from bs4 import BeautifulSoup
from ddgs import DDGS
from mcp.server.fastmcp import FastMCP

# Initialize MCP Server for Claude, Gemini, OpenAI Codex, and Cursor
mcp = FastMCP("GuestPost-Outreach-Engine")

IMAP_HOST = "imap.gmail.com"


def get_imap_connection():
    """Connect to Gmail via built-in IMAP using simple environment variables."""
    gmail_user = os.environ.get("GMAIL_ADDRESS")
    gmail_pass = os.environ.get("GMAIL_APP_PASSWORD")

    if not gmail_user or not gmail_pass:
        raise ValueError(
            "Missing GMAIL_ADDRESS or GMAIL_APP_PASSWORD in your MCP config env!"
        )

    mail = imaplib.IMAP4_SSL(IMAP_HOST)
    mail.login(gmail_user, gmail_pass.replace(" ", ""))
    return mail, gmail_user


def get_gmail_folder(mail, keyword: str) -> str:
    """Auto-detect Sent or Drafts folder name across any Gmail language."""
    status, folders = mail.list()
    for f in folders:
        decoded = f.decode("utf-8", errors="ignore")
        if keyword.lower() in decoded.lower():
            parts = decoded.split(' "/" ')
            if len(parts) == 2:
                return parts[1].strip('"')
    return f'"[Gmail]/{keyword.capitalize()}"'


def render_pitch_html(recipient_name: str, site_name: str, topics: List[Dict[str, str]], sender_name: str, sender_url: str) -> str:
    """Format the initial cold outreach pitch into a clean minimalist HTML card."""
    topics_html = ""
    for idx, t in enumerate(topics, 1):
        topics_html += f"""
        <div style="margin-bottom: 14px; padding: 12px 16px; background-color: #f9fafb; border-left: 3px solid #111827; border-radius: 4px;">
            <strong style="color: #111827; font-size: 15px;">Option {idx}: {t.get('title')}</strong>
            <p style="margin: 6px 0 0 0; color: #4b5563; font-size: 14px; line-height: 1.5;">{t.get('summary')}</p>
        </div>
        """

    return f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #1f2937; line-height: 1.6;">
        <p>Hi {recipient_name},</p>
        <p>I've been following <strong>{site_name}</strong> and wanted to pitch a few original, data-backed guest article ideas tailored for your readers:</p>
        {topics_html}
        <p>I already have the first draft outlined and ready to adapt to your editorial guidelines. Let me know which angle fits your upcoming schedule best, and I will send the full piece right over.</p>
        <p style="margin-top: 24px;">Best regards,<br>
        <strong>{sender_name}</strong><br>
        <a href="{sender_url}" style="color: #2563eb; text-decoration: none;">{sender_url}</a></p>
    </div>
    """


def render_article_delivery_html(recipient_name: str, article_title: str, article_body_html: str, sender_name: str, sender_url: str) -> str:
    """Format the second companion draft containing the full article for immediate follow-up."""
    return f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 680px; margin: 0 auto; color: #1f2937; line-height: 1.6;">
        <p>Hi {recipient_name},</p>
        <p>Thanks for getting back to me! As promised, here is the complete draft for <strong>{article_title}</strong>.</p>
        <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 24px 0;">
        <div style="padding: 20px; background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 6px;">
            <h1 style="font-size: 22px; color: #111827; margin-top: 0;">{article_title}</h1>
            {article_body_html}
        </div>
        <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 24px 0;">
        <p>Feel free to adjust any headings or links to match your style guide. Let me know once it's scheduled for publication!</p>
        <p>Best regards,<br>
        <strong>{sender_name}</strong><br>
        <a href="{sender_url}" style="color: #2563eb; text-decoration: none;">{sender_url}</a></p>
    </div>
    """


def save_imap_draft(mail, from_email: str, to_email: str, subject: str, html_content: str):
    """Save an HTML email directly into Gmail's Drafts folder via IMAP."""
    msg = MIMEMultipart("alternative")
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    drafts_folder = get_gmail_folder(mail, "Drafts")
    mail.append(
        f'"{drafts_folder}"',
        "\\Draft",
        imaplib.Time2Internaldate(time.time()),
        msg.as_bytes()
    )


@mcp.tool()
def find_niche_guest_post_prospects(niche: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Search the web for blogs and websites accepting guest posts in ANY niche,
    and automatically scrape their public contact emails.
    """
    queries = [
        f'{niche} "write for us"',
        f'{niche} "guest post guidelines"',
        f'{niche} "submit a guest post"'
    ]

    prospects = []
    seen_urls = set()
    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    with DDGS() as ddgs:
        for q in queries:
            for r in ddgs.text(q, max_results=max_results):
                url = r.get("href") or r.get("url")
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)

                found_emails = []
                try:
                    resp = httpx.get(url, timeout=8.0, follow_redirects=True)
                    if resp.status_code == 200:
                        soup = BeautifulSoup(resp.text, "html.parser")
                        raw_emails = set(re.findall(email_regex, soup.get_text()))
                        found_emails = [
                            e for e in raw_emails
                            if not e.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"))
                        ]
                except Exception:
                    pass

                prospects.append({
                    "niche": niche,
                    "title": r.get("title", ""),
                    "url": url,
                    "snippet": r.get("body", ""),
                    "emails_found": found_emails[:5]
                })

                if len(prospects) >= max_results:
                    return prospects

    return prospects


@mcp.tool()
def check_duplicate_outreach(email_or_domain: str) -> dict:
    """
    Check Gmail Sent and Drafts folders via IMAP to verify if a blog domain
    or editor email has already been pitched.
    """
    mail, _ = get_imap_connection()
    matches = 0

    for folder_key in ["Sent", "Drafts"]:
        try:
            folder_name = get_gmail_folder(mail, folder_key)
            mail.select(f'"{folder_name}"', readonly=True)
            _, data = mail.search(None, f'(TO "{email_or_domain}")')
            if data and data[0]:
                matches += len(data[0].split())
        except Exception:
            pass

    mail.logout()
    return {
        "target": email_or_domain,
        "already_contacted": matches > 0,
        "matching_messages_count": matches
    }


@mcp.tool()
def prepare_dual_outreach_drafts(
    recipient_email: str,
    recipient_name: str,
    site_name: str,
    pitch_subject: str,
    topics: List[Dict[str, str]],
    selected_article_title: str,
    full_article_html: str,
    sender_name: str,
    sender_url: str
) -> dict:
    """
    Verify Gmail history and simultaneously create TWO Gmail drafts for the same recipient:
    1. Draft 1: The initial guest post pitch with 3 topic ideas.
    2. Draft 2: The ready-to-send full guest post article for when they accept the pitch.
    """
    history = check_duplicate_outreach(recipient_email)
    if history["already_contacted"]:
        return {
            "status": "SKIPPED_DUPLICATE",
            "message": f"Found {history['matching_messages_count']} existing message(s)/draft(s) for {recipient_email}."
        }

    mail, from_email = get_imap_connection()

    # Draft 1: Cold Pitch
    pitch_html = render_pitch_html(recipient_name, site_name, topics, sender_name, sender_url)
    save_imap_draft(mail, from_email, recipient_email, pitch_subject, pitch_html)

    # Draft 2: Full Article Ready to Send
    article_subject = f"Re: {pitch_subject} [Full Draft: {selected_article_title}]"
    article_html = render_article_delivery_html(
        recipient_name, selected_article_title, full_article_html, sender_name, sender_url
    )
    save_imap_draft(mail, from_email, recipient_email, article_subject, article_html)

    mail.logout()

    return {
        "status": "SUCCESS",
        "recipient": recipient_email,
        "summary": "Saved both the initial pitch draft and the full article delivery draft directly in Gmail Drafts."
    }


if __name__ == "__main__":
    mcp.run()
