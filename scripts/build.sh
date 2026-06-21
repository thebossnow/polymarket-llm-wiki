#!/usr/bin/env bash
# Regenerate the Polymarket docs markdown mirror.
# Pulls every English page via Mintlify's per-page .md endpoint and the sitemap.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BASE="https://docs.polymarket.com"

curl -sL "$BASE/sitemap.xml" \
  | grep -oE '<loc>[^<]+</loc>' | sed -E 's/<\/?loc>//g' \
  | grep -vE '/cn(/|$)' > /tmp/poly_en_urls.txt

fetch_one() {
  url="$1"
  path="${url#$BASE/}"; path="${path%/}"; [ -z "$path" ] && path="index"
  out="$ROOT/$path.md"; mkdir -p "$(dirname "$out")"
  src="$url.md"; [ "$path" = "index" ] && src="$BASE/index.md"
  body="$(curl -sL --fail "$src" 2>/dev/null)" || { echo "FAIL $url"; return 0; }
  printf '%s\n' "$body" | awk '
    NR<=5 && /^> ## Documentation Index/ {skip=1}
    skip==1 && /^> / {next}
    skip==1 && /^[[:space:]]*$/ && !printed {next}
    {skip=0; print}' > "$out"
  echo "OK $path.md"
}
export -f fetch_one; export ROOT BASE
xargs -P 8 -I{} bash -c 'fetch_one "$@"' _ {} < /tmp/poly_en_urls.txt
curl -sL "$BASE/llms.txt" > "$ROOT/llms.txt"
echo "Done. $(find "$ROOT" -name '*.md' -not -name README.md | wc -l) pages."
