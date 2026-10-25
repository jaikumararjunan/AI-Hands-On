#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAYLOAD="$ROOT/source-payload"
DEST="$ROOT/expanded"
TMP_B64="$(mktemp)"
TMP_XZ="$(mktemp --suffix=.tar.xz)"
trap 'rm -f "$TMP_B64" "$TMP_XZ"' EXIT

find "$PAYLOAD" -type f -name 'part-*.b64' | sort | xargs cat > "$TMP_B64"
base64 -d "$TMP_B64" > "$TMP_XZ"
EXPECTED='f41aabe4384d3975d3f98ef76ee503946e2830104975edb0c0295ada1051bbc2'
ACTUAL="$(sha256sum "$TMP_XZ" | awk '{print $1}')"
[[ "$ACTUAL" == "$EXPECTED" ]] || { echo "Checksum mismatch: $ACTUAL" >&2; exit 1; }
rm -rf "$DEST"
mkdir -p "$DEST"
tar -xJf "$TMP_XZ" -C "$DEST"
test -f "$DEST/AI_Commerce_Zero_to_Master/README.md"
echo "Complete source extracted to: $DEST/AI_Commerce_Zero_to_Master"
