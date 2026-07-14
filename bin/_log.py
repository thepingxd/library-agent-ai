"""Logging e ledger da dev-library.

- _logs/ingest.log   : legível por humano, append-only, timestamps.
- _logs/ledger.jsonl : uma linha JSON por item ingerido (histórico/auditoria).
"""
from __future__ import annotations
import json
import hashlib
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT / "_logs"
INGEST_LOG = LOG_DIR / "ingest.log"
LEDGER = LOG_DIR / "ledger.jsonl"


def _ts() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _fmt(fields: dict) -> str:
    parts = []
    for k, v in fields.items():
        if isinstance(v, dict):
            v = ",".join(f"{a}:{b}" for a, b in v.items())
        parts.append(f'{k}={v}')
    return " ".join(parts)


def event(kind: str, echo: bool = False, **fields) -> None:
    """Registra uma linha estruturada em ingest.log (e opcionalmente ecoa)."""
    LOG_DIR.mkdir(exist_ok=True)
    line = f"{_ts()}  {kind:<9} {_fmt(fields)}".rstrip()
    with INGEST_LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    if echo:
        print(f"  · {line}")


def ledger_append(record: dict) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    record = {"ts": _ts(), **record}
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def ledger_records() -> list[dict]:
    if not LEDGER.exists():
        return []
    out = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def find_by_hash(sha: str) -> dict | None:
    for rec in reversed(ledger_records()):
        if rec.get("sha256") == sha and rec.get("acao") == "ingest":
            return rec
    return None


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()
