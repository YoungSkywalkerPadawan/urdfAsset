"""Build actual-content checksums, excluding self-referential and local-only files."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", "__pycache__", "exports", ".DS_Store", "FILES.sha256.jsonl", "IMPORT_REPORT.json", "local_config.json"}


def main():
    count, total = 0, 0
    with (ROOT / "FILES.sha256.jsonl").open("w", encoding="utf-8") as output:
        for path in sorted(ROOT.rglob("*")):
            relative = path.relative_to(ROOT)
            if set(relative.parts) & EXCLUDED or path.suffix in {".pyc", ".log"} or not path.is_file():
                continue
            with path.open("rb") as stream:
                sha = hashlib.file_digest(stream, "sha256").hexdigest()
            size = path.stat().st_size
            output.write(json.dumps({"path": relative.as_posix(), "bytes": size, "sha256": sha}, ensure_ascii=False) + "\n")
            count += 1; total += size
    print(json.dumps({"files": count, "bytes": total}))


if __name__ == "__main__":
    main()
