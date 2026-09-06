# Claude Skills 🧠⚡

A curated collection of modular, production-ready skills for **Claude Code**, **Claude Desktop**, and **Claude Cowork**.

---

## 📦 Included Skills

| Skill | Purpose | Features |
|---|---|---|
| **[`google-web-search`](skills/google-web-search/)** | Real-time web search & content fetching | 0-dependency Python script, automatic markdown link generation, full-page clean text extraction. |
| **[`cowork-antigravity`](skills/cowork-antigravity/)** | Antigravity Pool integration for Cowork | Multi-account gateway setup, thinking model aliases (`claude-cowork`, `claude-combo`), zero-downtime configuration. |

---

## 🚀 Quick Install

### Option 1: One-Line Installer
```bash
git clone https://github.com/dangnhathuycntt-byte/claude-skills.git /tmp/claude-skills \
  && /tmp/claude-skills/install.sh \
  && rm -rf /tmp/claude-skills
```

### Option 2: Clone Directly into Skills Directory
```bash
git clone https://github.com/dangnhathuycntt-byte/claude-skills.git ~/claude-skills
~/claude-skills/install.sh
```

---

## 🛠️ Usage

Once installed, Claude automatically detects the skills in `~/.claude/skills/`.

### 1. Google Web Search
Prompt Claude naturally:
- *"Tìm kiếm thông tin về bản phát hành mới nhất của Claude 3.7"*
- *"Search for FastAPI lifespan asynccontextmanager documentation"*

Or run the bundled standalone CLI script directly in your terminal:
```bash
# Search query
python3 ~/.claude/skills/google-web-search/search.py "Claude 3.7 Sonnet Anthropic" -n 5

# Deep-read page text
python3 ~/.claude/skills/google-web-search/search.py --fetch "https://www.anthropic.com/news/claude-3-7-sonnet"
```

### 2. Cowork & Antigravity Pool Setup
Follow instructions in [`skills/cowork-antigravity/SKILL.md`](skills/cowork-antigravity/SKILL.md) to route Claude Desktop or Cowork through your pooled upstream node.

---

## 📄 License
MIT License. Free to use, adapt, and share.
