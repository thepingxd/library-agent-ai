# AGENTS.md — Como usar esta biblioteca

Esta pasta é uma **base de consulta de referências para desenvolvimento**.
Se você é um agente e vai buscar um recurso aqui (template, logo, ilustração,
snippet…), **leia este arquivo e o `INDEX.md` primeiro** — não saia varrendo
os binários.

## Ordem de leitura

1. **`INDEX.md`** — catálogo textual de tudo que existe, com descrição e tags.
   É gerado automaticamente; é a sua fonte de busca primária.
2. **`TAGS.md`** — vocabulário fechado de tags. Use só estas tags ao filtrar.
3. Só então abra o item específico na sua pasta.

## Como as coisas estão organizadas

- **Pasta = tipo principal** (ver tabela em `TAGS.md`).
- Cada item é uma **pasta própria** dentro da categoria, contendo os arquivos
  originais + um `_meta.yaml` com descrição, tags, origem e licença.
- Imagens/ilustrações têm **descrição textual** no `_meta.yaml` — é assim que
  você "encontra" um visual sem abrir cada arquivo.

## Buscando um recurso e ESTUDANDO (fluxo principal)

O objetivo desta biblioteca é servir de **material de referência**: você acha
um item pelo tema e estuda como ele foi feito antes de construir algo parecido.

```
# 1. Busque pelo tema (palavra-chave, tolera acento; --ai reordena por semelhança)
bin/find academia fitness
bin/find "loja de roupa" --tipo templates --ai

# 2. Abra o item retornado e ESTUDE:
#    - CARD.md  → ficha de estudo (propósito, seções, paleta, tipografia, reuso)
#    - _meta.yaml → tags, domínio, licença
#    - os arquivos reais (HTML/CSS/imagens) → como foi construído

# 3. Use como modelo de referência de design ao desenvolver o novo projeto.
```

Regras de busca:
- `dominio` e `tags` pesam mais que a descrição no ranqueamento.
- Sem resultado bom? Tente sinônimos ou `--ai` para semelhança semântica.
- Alternativa manual: filtrar direto no `INDEX.md` (coluna Domínio/Tags).

O **`CARD.md`** é o coração do reuso: é a leitura de design já feita na
ingestão, então você não precisa reengenheirar o item do zero toda vez.

## Adicionando um recurso (NÃO faça manualmente)

Não arraste arquivos direto pras pastas. Use o pipeline:

```
# solte o .zip (ou arquivo) em _inbox/ e rode:
bin/ingest                 # processa tudo que estiver em _inbox/
bin/ingest arquivo.zip     # processa um arquivo específico
```

O pipeline extrai, classifica pelo conteúdo, gera `_meta.yaml`, enriquece a
descrição com IA e arquiva no lugar certo. Se não tiver certeza da categoria,
ele joga em `_review/` em vez de chutar. O `.zip` original vai pro `_archive/`.

Depois de mexer à mão em qualquer `_meta.yaml`, rode `bin/reindex` pra
regenerar o `INDEX.md`.

## Pastas de sistema (não são conteúdo)

`_inbox/` entrada · `_processing/` staging temporário · `_review/` itens que
precisam de decisão manual · `_archive/` zips originais processados · `bin/`
scripts.
