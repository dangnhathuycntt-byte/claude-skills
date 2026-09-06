#!/usr/bin/env python3
"""Standalone Web Search & Content Fetcher for Claude.

Zero dependencies (Python 3 standard library only).
Provides fast web search and clean markdown/text extraction.
"""

import argparse
import html
import json
import re
import sys
import urllib.parse
import urllib.request

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)


def search_web(query: str, max_results: int = 8) -> list[dict]:
    """Search the web and return a list of {title, url, snippet} dicts."""
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote_plus(query)}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            content = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        sys.stderr.write(f"Search request failed: {e}\n")
        return []

    # Parse result blocks
    results = []
    # Pattern to match each result block
    blocks = re.findall(r'<div class="result results_links[^"]*".*?</div>\s*</div>\s*</div>', content, re.DOTALL)
    if not blocks:
        # Fallback to broader regex
        blocks = re.findall(r'<a[^>]+class="result__snippet[^"]*"[^>]*href="([^"]+)".*?>(.*?)</a>', content, re.DOTALL)
        for href, snip in blocks:
            dest_url = _extract_real_url(href)
            clean_snip = html.unescape(re.sub(r"<[^>]+>", "", snip).strip())
            if dest_url:
                results.append({"title": dest_url, "url": dest_url, "snippet": clean_snip})
                if len(results) >= max_results:
                    break
        return results

    for block in blocks:
        # Extract title & link
        title_match = re.search(r'<a[^>]+class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', block, re.DOTALL)
        if not title_match:
            continue
        raw_href = title_match.group(1)
        raw_title = title_match.group(2)
        clean_title = html.unescape(re.sub(r"<[^>]+>", "", raw_title).strip())
        dest_url = _extract_real_url(raw_href)
        if not dest_url:
            continue

        # Extract snippet
        snippet_match = re.search(r'<a[^>]+class="result__snippet[^"]*"[^>]*>(.*?)</a>', block, re.DOTALL)
        if snippet_match:
            clean_snippet = html.unescape(re.sub(r"<[^>]+>", "", snippet_match.group(1)).strip())
        else:
            clean_snippet = ""

        results.append({
            "title": clean_title,
            "url": dest_url,
            "snippet": clean_snippet,
        })
        if len(results) >= max_results:
            break

    return results


def _extract_real_url(raw_href: str) -> str:
    """Decode real destination URL from search redirect wrapper."""
    if "uddg=" in raw_href:
        parsed = urllib.parse.urlparse(raw_href)
        qs = urllib.parse.parse_qs(parsed.query)
        extracted = qs.get("uddg", [""])[0]
        if extracted:
            return extracted
    if raw_href.startswith("//"):
        return f"https:{raw_href}"
    if raw_href.startswith("http://") or raw_href.startswith("https://"):
        return raw_href
    return ""


def fetch_url(url: str, max_chars: int = 4000) -> str:
    """Fetch URL and return clean text content."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,text/plain;q=0.9,*/*;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"Error fetching URL: {e}"

    # Strip style, script, noscript, svg
    content = re.sub(r"<(script|style|noscript|svg)[^>]*>.*?</\1>", "", content, flags=re.DOTALL | re.IGNORECASE)
    # Convert common block tags to newlines
    content = re.sub(r"<(p|br|div|h[1-6]|li|tr)[^>]*>", "\n", content, flags=re.IGNORECASE)
    # Strip remaining HTML tags
    content = re.sub(r"<[^>]+>", "", content)
    # Unescape HTML entities
    content = html.unescape(content)
    # Collapse multiple whitespaces and blank lines
    content = re.sub(r"[ \t]+", " ", content)
    content = re.sub(r"\n\s*\n+", "\n\n", content).strip()

    if len(content) > max_chars:
        content = content[:max_chars] + f"\n\n... [Truncated at {max_chars} chars] ..."

    return content


def main():
    parser = argparse.ArgumentParser(description="Web search and content fetcher for Claude")
    parser.add_argument("query", nargs="?", help="Search query or URL to fetch")
    parser.add_argument("-n", "--num", type=int, default=6, help="Maximum search results (default: 6)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--fetch", metavar="URL", help="Fetch and display clean text of a specific URL")

    args = parser.parse_args()

    if args.fetch:
        text = fetch_url(args.fetch)
        print(text)
        return

    if not args.query:
        parser.print_help()
        sys.exit(1)

    # If query is a URL, fetch directly
    if args.query.startswith("http://") or args.query.startswith("https://"):
        text = fetch_url(args.query)
        print(text)
        return

    results = search_web(args.query, max_results=args.num)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return

    if not results:
        print(f"No search results found for '{args.query}'.")
        return

    print(f"### Web Search Results for: {args.query}\n")
    for idx, item in enumerate(results, 1):
        print(f"**{idx}. [{item['title']}]({item['url']})**")
        if item["snippet"]:
            print(f"> {item['snippet']}")
        print()


if __name__ == "__main__":
    main()
