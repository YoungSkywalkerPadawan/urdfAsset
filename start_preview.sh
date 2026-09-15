#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python -m http.server 8768 --bind 127.0.0.1
