# Contribuindo

Obrigado pelo interesse! Este projeto está sendo construído em aberto e ainda é
alpha — ou seja, é o melhor momento para ajudar a moldar a direção dele.

## Como ajudar

- 💡 **Ideias e discussão** — abra uma _issue_ com a tag `ideia`. A visão está
  no [README](README.md) e no [roadmap](README.md#roadmap); diga o que faria
  isso ser útil para você.
- 🐛 **Bugs** — abra uma _issue_ descrevendo o que fez, o que esperava e o que
  aconteceu. Se for na classificação, diga que tipo de arquivo/zip era.
- 🔧 **Código** — veja abaixo.

## Rodando localmente

```bash
git clone https://github.com/thepingxd/library-agent-ai.git
cd library-agent-ai
./bin/dlib help
# teste rápido sem IA:
echo "<html><body>oi</body></html>" > /tmp/t/index.html   # monte um zip de teste
./bin/dlib ingest --no-ai
```

Requisitos: `python3` + `unzip`. A parte de IA usa o `claude` CLI (opcional).

## Enviando um PR

1. Faça um fork e crie uma branch descritiva.
2. Mantenha os princípios da [arquitetura](docs/ARCHITECTURE.md):
   - **Núcleo sem dependências** (stdlib + parser próprio).
   - **IA é best-effort**: uma falha de IA nunca pode quebrar a ingestão.
   - **Nunca destruir** dados do usuário; **nunca chutar** categoria (use `_review/`).
3. Se adicionar uma **categoria ou tag**, atualize `TAGS.md`, o dicionário
   `TIPO`/`classify()` em `bin/ingest` e `CATEGORIES` em `bin/reindex`.
4. Descreva no PR o comportamento antes/depois e como testou.

## Escopo de conteúdo

O repositório versiona **apenas o framework** (scripts, docs, estrutura). Não
faça commit de assets pessoais (templates/logos baixados) — o `.gitignore` já
os exclui. Cada usuário popula a própria biblioteca localmente.

## Código de conduta

Seja respeitoso e construtivo. Estamos aqui para construir algo útil juntos.
