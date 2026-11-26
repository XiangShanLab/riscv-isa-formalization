#!/usr/bin/env bash
# Validate the formalization document. Usage: tools/validate.sh [file.md]
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
doc="${1:-$root/riscv-fp-compact.md}"
python3 -I "$root/tools/check_md.py" "$doc"
echo "--- formula audit ---"
python3 -I "$root/tools/audit_formulas.py" "$doc"
echo "OK: $doc"
