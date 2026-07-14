"""Utilitários compartilhados: leitura/escrita de metadados (_meta.yaml).

Formato YAML propositalmente restrito (escalares + listas de bloco) para não
depender de pyyaml. Nós escrevemos e lemos, então o subconjunto basta.
"""
from __future__ import annotations
import re
from pathlib import Path

META_NAME = "_meta.yaml"

# Ordem canônica dos campos no arquivo
FIELD_ORDER = [
    "nome", "tipo", "origem", "data_ingestao", "formato",
    "dominio", "tags", "estilo", "descricao", "licenca",
    "arquivo_original", "confianca", "obs",
]


def normalize(s: str) -> str:
    """minúsculas sem acento — para busca tolerante."""
    import unicodedata
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def _quote(v) -> str:
    if v is None:
        return '""'
    s = str(v)
    s = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    return f'"{s}"'


def _unquote(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        s = s[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return s


def dump(meta: dict) -> str:
    keys = [k for k in FIELD_ORDER if k in meta] + \
           [k for k in meta if k not in FIELD_ORDER]
    lines = []
    for k in keys:
        v = meta[k]
        if isinstance(v, (list, tuple)):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f"  - {_quote(item)}")
            if not v:
                lines[-1] = f"{k}: []"
        else:
            lines.append(f"{k}: {_quote(v)}")
    return "\n".join(lines) + "\n"


def load(text: str) -> dict:
    meta: dict = {}
    cur = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^(\s*)-\s+(.*)$", line)
        if m and cur is not None:
            meta.setdefault(cur, [])
            if not isinstance(meta[cur], list):
                meta[cur] = []
            meta[cur].append(_unquote(m.group(2)))
            continue
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            cur = key
            if val == "":
                meta[key] = []          # início de lista de bloco
            elif val == "[]":
                meta[key] = []
            elif val.startswith("[") and val.endswith("]"):
                inner = val[1:-1]        # lista inline: [a, b, c]
                meta[key] = [_unquote(x.strip()) for x in inner.split(",")
                             if x.strip()]
            else:
                meta[key] = _unquote(val)
    return meta


def read_meta(item_dir: Path) -> dict | None:
    f = item_dir / META_NAME
    if not f.exists():
        return None
    return load(f.read_text(encoding="utf-8"))


def write_meta(item_dir: Path, meta: dict) -> None:
    (item_dir / META_NAME).write_text(dump(meta), encoding="utf-8")
