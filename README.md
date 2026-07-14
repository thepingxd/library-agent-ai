# library-agent-ai

> Uma biblioteca de referências de desenvolvimento **pesquisável por IA**: você
> alimenta com templates, logos, ilustrações e snippets; a ferramenta
> classifica, documenta e transforma cada item em **material de estudo** que um
> agente encontra por tema e usa como referência de design.

*An AI-searchable library of development references. Drop in templates, logos,
illustrations and snippets — the tool classifies, documents and turns each item
into study material an agent can find by theme and reuse as a design reference.*

**Status:** alpha · construído em aberto, buscando comunidade. Contribuições e
ideias são bem-vindas — veja [CONTRIBUTING.md](CONTRIBUTING.md).

---

## A ideia

Quando você vai desenvolver algo — digamos, **um site de academia** — normalmente
tem uma pasta cheia de templates e assets baixados que você mal lembra que
existem. Esta ferramenta resolve isso:

1. Você baixa um `.zip` (do Envato, Figma, onde for) e joga na `_inbox/`.
2. `dlib ingest` **extrai, classifica pelo conteúdo** (não pelo nome), gera
   metadados e uma **ficha de estudo** (`CARD.md`) descrevendo estrutura,
   paleta, tipografia e como reutilizar.
3. Depois, ao criar algo do mesmo tema, `dlib find academia` **encontra** o
   item — e a IA lê o `CARD.md` e **já tem um modelo de referência de design**,
   sem precisar reengenheirar o material do zero toda vez.

## Como funciona

```
_inbox/            você solta o .zip aqui
   │  dlib ingest
   ▼
extrai → classifica (heurística por conteúdo) → gera _meta.yaml
       → enriquece com IA: descrição, domínio, tags + CARD.md (ficha de estudo)
   ▼
templates/ · brand/ · assets/ · snippets/ · …   arquiva na categoria certa
   │                                            (incerto → _review/, nunca chuta)
   ▼
INDEX.md  (catálogo, regenerado)     .zip original → _archive/ (nada é apagado)

   dlib find <tema>   →  busca ranqueada (domínio/tags > descrição; alcança o CARD)
```

## Requisitos

- **Python 3** e **unzip** (sem libs extras — parser de metadados é próprio).
- **Opcional:** o [Claude Code CLI](https://claude.com/claude-code) (`claude`)
  para o enriquecimento por IA (descrições ricas + `CARD.md` + busca `--ai`).
  Sem ele, tudo funciona em modo heurístico; a descrição fica `[pendente-ia]`.

## Instalação

```bash
git clone https://github.com/thepingxd/library-agent-ai.git ~/dev-library
cd ~/dev-library

# atalho global (opcional, mas recomendado)
ln -sf "$PWD/bin/dlib" ~/.local/bin/dlib   # garanta que ~/.local/bin está no PATH
dlib help
```

A biblioteca vive por padrão na raiz do checkout. Para apontar para outro lugar,
defina `DEV_LIBRARY_HOME=/caminho/para/sua/biblioteca`.

## Uso

```bash
# catalogar
dlib ingest                                  # processa tudo em _inbox/
dlib ingest ~/Downloads/template-gym.zip     # um arquivo específico
dlib ingest --no-ai                          # só heurística, sem IA

# buscar / estudar
dlib find academia fitness                   # busca por tema
dlib find "loja de roupa" --tipo templates   # filtra por tipo
dlib find crossfit --ai                      # reordena por semelhança (IA)

# acompanhar
dlib status                                  # panorama: fila, catálogo, última run
dlib log                                     # histórico legível de ingestões
dlib log --json                              # histórico estruturado (ledger)

# manutenção
dlib reindex                                 # regenera INDEX.md
```

Cada resultado aponta para a pasta do item e seu `CARD.md` — a leitura de design
já pronta para a IA (ou você) estudar.

## Automação (opcional): catalogar sozinho

Para que qualquer arquivo solto na `_inbox/` seja catalogado automaticamente,
há um watcher que roda como **serviço systemd de usuário** (zero dependências,
detecta em segundos, serializa via lock, persiste após logout):

```bash
mkdir -p ~/.config/systemd/user
cp systemd/dev-library-watch.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now dev-library-watch.service
loginctl enable-linger "$USER"        # roda mesmo deslogado (pode pedir sudo)

systemctl --user status dev-library-watch.service   # ver estado
journalctl --user -u dev-library-watch -f           # acompanhar ao vivo
```

Para testar em primeiro plano, sem serviço: `dlib watch`. O passo de IA pode
ser adiado no automático definindo `INGEST_NO_AI=1` no arquivo do serviço.

> Alternativas ao serviço: um `cron`/systemd-timer chamando `dlib ingest` a cada
> N minutos, ou o agendador do seu próprio agente. A ação é sempre `dlib ingest`.

## Estrutura

```
templates/  boilerplates/  components/  snippets/
brand/{logos,colors,fonts}
assets/{images,illustrations,icons}
references/  prompts/
_inbox/  _processing/  _review/  _archive/  _logs/   ← pastas de sistema
bin/        AGENTS.md  TAGS.md  INDEX.md
```

Cada ingestão é registrada em `_logs/`: `ingest.log` (legível) e `ledger.jsonl`
(um JSON por item, com sha256 para detectar duplicatas). Veja com `dlib log`.

- **[AGENTS.md](AGENTS.md)** — como um agente deve buscar e estudar aqui.
- **[TAGS.md](TAGS.md)** — vocabulário controlado de tags e tipos.
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** — como as peças funcionam por dentro.

> O `.gitignore` versiona só o framework: **seus assets ficam locais**. Ao clonar,
> você recebe a ferramenta e a estrutura vazia para popular com o seu conteúdo.

## Roadmap

- [ ] Busca semântica local (embeddings) sem depender de CLI externo
- [ ] Backend de IA plugável (Claude / OpenAI / local)
- [ ] Watcher opcional da `_inbox/` (ingestão automática)
- [ ] Suporte a mais formatos de arquivo (`.rar`, `.7z`)
- [ ] Integração como ferramenta de agentes (MCP / function calling)
- [ ] Deduplicação e detecção de itens semelhantes

## Contribuindo

Este projeto está sendo construído em aberto. Veja [CONTRIBUTING.md](CONTRIBUTING.md)
para como propor ideias, abrir issues e enviar PRs.

## Licença

[MIT](LICENSE) — use, modifique e compartilhe livremente.
