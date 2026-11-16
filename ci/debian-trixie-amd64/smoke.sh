#!/usr/bin/env bash
set -euo pipefail
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
printf '%s\n' 'GetPatched curl smoke test' > "$work/input"
curl --silent --show-error --fail --proto '=file' "file://$work/input" --output "$work/output"
cmp "$work/input" "$work/output"
