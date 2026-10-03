"""Portable configuration, immutable metadata, and JSON helpers."""
import hashlib
import json
from pathlib import Path


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False),
                    encoding="utf-8", newline="\n")


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def stable_seed(text):
    return int(hashlib.sha256(text.encode()).hexdigest()[:8], 16)


def _merge(base, update):
    result = dict(base)
    for key, value in update.items():
        result[key] = _merge(result[key], value) if isinstance(value, dict) and isinstance(result.get(key), dict) else value
    return result


def config_from(path, _seen=None):
    path = Path(path).resolve()
    seen = set() if _seen is None else set(_seen)
    if path in seen:
        raise ValueError("Circular config inheritance: " + str(path))
    seen.add(path)
    own = read_json(path)
    parent = own.pop("extends", None)
    base = config_from(path.parent / parent, seen) if parent else {}
    for key in ("prepared_dir", "run_dir", "base_prepared_dir", "cache_root"):
        if key in own:
            own[key] = str((path.parent / own[key]).resolve())
    for source in own.get("data_roots", []):
        source["path"] = str((path.parent / source["path"]).resolve())
    return _merge(base, own)


def read_rows(path):
    return [json.loads(line) for line in Path(path).read_text("utf-8").splitlines() if line.strip()]


def write_rows(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n" for row in rows),
                    encoding="utf-8", newline="\n")


def code_digest():
    root = Path(__file__).parent
    payload = "".join(path.name + ":" + digest(path) + "\n" for path in sorted(root.glob("*.py")))
    return hashlib.sha256(payload.encode()).hexdigest()


def verify_checkpoint_code(state):
    if state.get('code_sha256') != code_digest():
        raise ValueError('Checkpoint source code differs; use its original code version')
