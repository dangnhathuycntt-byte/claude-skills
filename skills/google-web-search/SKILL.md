---
name: google-web-search
description: Use when needing up-to-date facts, documentation, live web search, library versions, or current information beyond model knowledge cutoff
---

# Google Web Search

## Overview
Provides live internet search and web page extraction for Claude across environments (Claude Code, Claude Desktop, Cowork, and headless runners). Ensures Claude operates with current information, accurate links, and verifiable sources.

## When to Use
- Looking up current documentation, APIs, or software release notes.
- Verifying recent breaking changes, library versions, or deprecations.
- Fact-checking technical specifications or error codes.
- Answering user queries that explicitly ask to search Google or the web.

## When NOT to Use
- Information already firmly established in local codebase files or git history.
- Pure logic, algorithmic design, or refactoring existing internal code.
- Checking local system status (use Bash, lsof, git, etc.).

## Tool Execution Hierarchy

Choose the highest available search method in the current environment:

| Priority | Method / Tool | Context / Availability |
|---|---|---|
| **1 (Primary)** | `mcp__exa__web_search_exa` + `web_fetch_exa` | When Exa MCP is active in the session (fastest semantic search + clean markdown extraction). |
| **2 (Built-in)** | `WebSearch` + `WebFetch` | Built-in Claude Code harness tools. |
| **3 (Universal CLI)** | `search.py` script | Works anywhere with Python 3 (0 dependencies, 0 API keys). |

### Universal CLI Script Usage (`search.py`)

If MCP or harness web tools are unavailable or restricted, invoke the bundled standalone search utility:

```bash
# Basic web search (returns titles, URLs, snippets)
python3 ~/.claude/skills/google-web-search/search.py "query here" -n 6

# JSON output for machine parsing
python3 ~/.claude/skills/google-web-search/search.py "query here" --json

# Deep-read content of a specific webpage
python3 ~/.claude/skills/google-web-search/search.py --fetch "https://example.com/page"
```

## Search Query Formulation

1. **Describe the ideal target page**:
   - ❌ Bad: `"react error"`
   - ✅ Good: `"react 19 useActionState migration guide and typescript example"`
2. **Include library name and version**:
   - ❌ Bad: `"FastAPI lifespan"`
   - ✅ Good: `"FastAPI asynccontextmanager lifespan example official docs"`
3. **Target authoritative domains when applicable**:
   - Use site modifiers: `site:github.com`, `site:docs.python.org`, `site:anthropic.com`.

## Response Citation Rule

After answering with search results, **always** include a `Sources:` section with markdown hyperlinks:

```markdown
Sources:
- [Claude 3.7 Sonnet Announcement](https://www.anthropic.com/news/claude-3-7-sonnet)
- [Anthropic Documentation](https://docs.anthropic.com)
```

## Common Mistakes

| Mistake | Reality |
|---|---|
| Relying on stale training memory for recent versions | Versions change constantly. Search takes 2 seconds and guarantees accuracy. |
| Quoting bare URLs without markdown links | Always format as `[Title](URL)` so the user can click directly. |
| Stopping at search snippets when details matter | Use `web_fetch_exa`, `WebFetch`, or `search.py --fetch` to read the full page text. |
