# Arquitetura

Visão de como o `library-agent-ai` funciona por dentro. Se você vai contribuir,
comece por aqui.

## Princípios

1. **Pasta = tipo, tags = busca transversal.** Modelo híbrido: a categoria
   (pasta) define o tipo principal; as tags (vocabulário fechado em `TAGS.md`)
   permitem filtrar por tema/tecnologia sem duplicar itens.
2. **Documentar para reuso, não só armazenar.** O valor está no `CARD.md` —
   a ficha de estudo gerada uma vez na ingestão, para a IA não reengenheirar
   o item toda vez.
3. **Nunca chutar.** Se a classificação é ambígua, o item vai para `_review/`.
4. **Nada é destruído.** O arquivo original vai para `_archive/`.
5. **Zero dependências pesadas.** Só `python3` + `unzip`; a IA é opcional.

## Componentes

| Arquivo          | Papel                                                        |
|------------------|-------------------------------------------------------------|
| `bin/dlib`       | Front-end (dispatcher) global. Resolve a raiz e delega.     |
| `bin/ingest`     | Pipeline: extrai → classifica → metadados → IA → arquiva.   |
| `bin/find`       | Busca ranqueada por palavra-chave (+ rerank opcional por IA).|
| `bin/reindex`    | Regenera `INDEX.md` a partir dos `_meta.yaml`.              |
| `bin/status`     | Panorama atual: fila, catálogo por categoria, última run.   |
| `bin/log`        | Histórico de ingestões (`ingest.log` ou `ledger.jsonl`).    |
| `bin/_lib.py`    | Leitura/escrita dos `_meta.yaml` (parser YAML mínimo próprio).|
| `bin/_log.py`    | Log (`_logs/ingest.log`) e ledger (`_logs/ledger.jsonl`) + sha256.|

## Pipeline de ingestão (`bin/ingest`)

```
1. extract()   descompacta (ou copia) para _processing/, remove lixo (__MACOSX),
               desembrulha pasta-raiz única.
2. classify()  conta extensões e usa palavras-chave (nome + paths) numa cadeia
               de regras priorizadas → (categoria, confiança, formatos, estilo).
               Sem match forte → _review/.
3. place       move para <categoria>/<slug>/ (unique_dir evita colisão).
4. enrich_ai() (opcional) chama `claude -p` pedindo DOIS blocos:
               ```yaml (descricao, dominio, tags, estilo, licenca)
               ```markdown (a ficha CARD.md).
5. write_meta  grava _meta.yaml; move o original para _archive/.
6. reindex     regenera INDEX.md.
```

### Estender a classificação

As regras estão em `classify()` em `bin/ingest`, como grupos de extensões
(`FONT`, `RASTER`, `VECTOR`, `WEB`, …) e uma cadeia `if/elif` ordenada. Para
suportar um novo tipo: adicione o grupo de extensões, uma regra na cadeia e a
entrada no dicionário `TIPO` (categoria → tag singular). Documente a tag em
`TAGS.md` e a pasta em `bin/reindex` (`CATEGORIES`).

## Metadados (`_meta.yaml`)

Formato YAML propositalmente restrito (escalares + listas de bloco **e** inline
`[a, b]`) para dispensar `pyyaml`. `bin/_lib.py` é a única fonte de leitura/
escrita — se mudar o formato, mude só ali. Campos em `FIELD_ORDER`.

## Busca (`bin/find`)

Monta um "blob" pesquisável por item juntando `nome`, `dominio`, `tags`,
`estilo`, `descricao`, `tipo` e o texto do `CARD.md`, cada campo com um peso
(`WEIGHTS`). A pontuação é a soma das ocorrências dos termos (normalizados, sem
acento). `--ai` envia os melhores candidatos ao `claude` para reordenar por
semelhança semântica. `--tipo` tolera singular/plural.

## O que a IA vê

Na ingestão, o `claude -p` roda com `--allowedTools Read Glob` **dentro da pasta
do item**, então ele realmente abre o HTML/CSS e inspeciona as imagens antes de
escrever a ficha — não descreve só pelo nome do arquivo.

## Logs e ledger (`_logs/`, `bin/_log.py`)

Cada ingestão emite **dois registros** (a pasta `_logs/` é ignorada pelo git —
é histórico pessoal):

- `ingest.log` — linhas legíveis com timestamp e tipo de evento
  (`start`, `extract`, `classify`, `duplicate`, `done`, `error`).
- `ledger.jsonl` — um JSON por item: `source`, `sha256`, `size_bytes`,
  `n_files`, `ext_top`, `categoria`, `confianca`, `destino`, `ai`, `card`,
  `duracao_s`, `erro`.

O `sha256` habilita **deduplicação**: antes de processar, `ingest` consulta o
ledger (`find_by_hash`) e avisa se aquele arquivo já foi ingerido. `bin/status`
e `bin/log` leem esses registros para reportar o estado.

## Convenções para PRs

- Mantenha o **zero-dependency** no núcleo (parser próprio, stdlib).
- IA sempre **best-effort**: falha de IA nunca deve quebrar a ingestão.
- Toda nova categoria/tag precisa aparecer em `TAGS.md` **e** `bin/reindex`.
