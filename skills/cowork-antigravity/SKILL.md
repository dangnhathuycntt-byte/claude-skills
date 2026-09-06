---
name: cowork-antigravity
description: Use when setting up or connecting Claude Desktop, Cowork, or Cockpit Tools to an Antigravity Pool API server
---

# Claude Cowork & Antigravity Pool Integration

## Overview
Reference guide and step-by-step instructions for connecting Claude Desktop, Claude Cowork, or Cockpit tools to an OpenAI-compatible Antigravity Pool API (`inf_quota`).

## Prerequisites
- Running Antigravity Pool instance (default: `http://localhost:8000`)
- Valid `API_KEY` configured on the pool server
- Claude Desktop or Cowork application

## Recommended Model Configurations

| Role / Intent | Pool Model Alias | Upstream Target | Features |
|---|---|---|---|
| **Coding & Reasoning** | `claude-cowork` | `claude-opus-4-6-thinking` | Native Claude thought signatures, 1M context window, high reasoning effort. |
| **Fast Agentic Tasks** | `claude-combo` | `gemini-3.8-flash-high` | Ultra-low latency, high token throughput, thinking enabled. |
| **General Assistance** | `claude-sonnet-4-6` | `claude-sonnet-4-6` | Balanced speed, intelligence, and 200k context. |

## Claude Desktop Configuration

Add the custom endpoint to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "api_endpoint": "http://localhost:8000/v1",
  "api_key": "YOUR_POOL_API_KEY",
  "default_model": "claude-cowork"
}
```

Or via environment variables when launching Claude Desktop / Cowork:

```bash
export ANTHROPIC_BASE_URL="http://localhost:8000/v1"
export ANTHROPIC_API_KEY="YOUR_POOL_API_KEY"
```

## Troubleshooting & Verification

1. **Verify Pool Health**:
   ```bash
   curl http://localhost:8000/health
   ```
   Ensure `"ok": true` and `"accounts"` count > 0.

2. **Verify Models List**:
   ```bash
   curl http://localhost:8000/v1/models -H "Authorization: Bearer YOUR_POOL_API_KEY"
   ```
   Check that `claude-cowork` and `claude-combo` are present in the returned list.

3. **429 Handling**:
   The pool automatically failovers exhausted accounts silently. If multiple consecutive accounts hit rate limits, 429 dampening protects the pool from cascading lockouts.
