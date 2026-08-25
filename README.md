# MED-RAG-ASSISTANT

Assistente médico com RAG (Retrieval-Augmented Generation) e Agentes, 100% open source.

> ⚠️ **Aviso de escopo:** este é um projeto educacional/de portfólio. Não substitui orientação médica profissional. As respostas do bot e da API sempre exibirão este aviso.

---

## Visão Geral

O projeto é dividido em duas fases evolutivas:

- **Fase 1 — Assistente de Consulta:** responde perguntas livres sobre medicamentos e literatura médica pública (bulas da Anvisa e artigos do PubMed/PMC), sempre citando a fonte.
- **Fase 2 — Verificador de Interações Medicamentosas:** dado uma lista de medicamentos, identifica interações conhecidas entre eles, com nível de severidade e fontes, usando múltiplos agentes especializados.

A interação com o usuário final acontece via **Telegram Bot** (gratuito, sem trial, sem cartão de crédito), enquanto o backend expõe tudo também via **FastAPI**, permitindo testar a API diretamente pelo Swagger.

---

## Stack Tecnológica (100% Open Source)

| Camada | Tecnologia | Função |
|---|---|---|
| LLM | Llama 3.x via **Ollama** | Geração de respostas, rodando localmente e de graça |
| Embeddings | nomic-embed-text ou bge-m3 (via Ollama) | Vetorização de texto |
| Banco vetorial | **Qdrant** (ou pgvector) | Busca semântica |
| Banco relacional | **PostgreSQL** | Metadados, histórico de conversas, usuários |
| API | **FastAPI** | Exposição dos endpoints |
| Orquestração de agentes | **Strands Agents SDK** | Coordenação dos agentes na Fase 2 |
| Canal de mensagens | **Telegram Bot API** (python-telegram-bot) | Interface gratuita com o usuário final |
| Fila/Assíncrono | Celery + Redis | Ingestão de dados em background |
| Infra | Docker Compose | Orquestração de todos os serviços localmente |

---

## Fase 1 — Assistente de Consulta (RAG aberto)

### Objetivo
Responder perguntas livres sobre medicamentos e literatura médica pública, sempre citando a fonte.

### Fontes de dados
- Bulas públicas da **Anvisa**
- Artigos abertos do **PubMed/PMC** (API gratuita)

### Fluxo

```
Usuário (Telegram) → Bot → FastAPI (/perguntar)
        ↓
   Busca vetorial no Qdrant (top-k chunks relevantes)
        ↓
   Monta contexto + pergunta → Llama (Ollama)
        ↓
   Resposta com citação da fonte → Bot → Usuário
```

### Pipeline de ingestão (roda uma vez / periodicamente)
1. Coleta de bulas/artigos (scraping ou API)
2. Limpeza e chunking do texto
3. Geração de embeddings
4. Persistência no Qdrant (vetores) + PostgreSQL (metadados: fonte, data, tipo de documento)

### Endpoints principais (FastAPI)
- `POST /perguntar` — pergunta livre, retorna resposta + fontes
- `POST /ingestao` — dispara ingestão de novos documentos (uso interno/admin)
- `GET /documentos` — lista o que já está indexado

### Comando no Telegram

```
/perguntar Quais os efeitos colaterais da dipirona?
```

→ Bot responde com o resumo gerado + trecho da fonte citada.

### Entregável da Fase 1
Sistema de perguntas e respostas funcional, com RAG completo (ingestão → vetorização → geração), testável via Telegram e via Swagger.

---

## Fase 2 — Verificador de Interações Medicamentosas (RAG + Agentes)

### Objetivo
Dado uma lista de medicamentos informada pelo usuário, identificar interações conhecidas entre eles, com nível de severidade e fontes.

### Por que precisa de agentes (e não só RAG simples)
A tarefa não é uma pergunta única — é uma lógica combinatória: para uma lista de N medicamentos, é preciso analisar todos os pares possíveis, cruzar informações e agregar num veredito único. Isso é dividido entre agentes especializados:

- **Agente Buscador:** para cada par de medicamentos, busca no mesmo Qdrant da Fase 1 se há registro de interação
- **Agente Agregador:** recebe os resultados de todos os pares, classifica a severidade geral e monta a resposta final
- **Agente Explicador:** transforma o resultado técnico em linguagem clara para o usuário, sempre citando a fonte

### Fluxo

```
Usuário (Telegram): /interacoes dipirona, warfarina, ibuprofeno
        ↓
Bot → FastAPI (/verificar-interacoes)
        ↓
Agente Buscador → gera todos os pares → busca vetorial por par
        ↓
Agente Agregador → classifica severidade (baixo/médio/alto risco)
        ↓
Agente Explicador → gera resposta final legível
        ↓
Bot → Usuário (com aviso de severidade + fontes)
```

### Reaproveitamento da Fase 1
Nenhuma infraestrutura nova de dados é necessária — a Fase 2 usa a mesma base vetorial de bulas já construída na Fase 1. O trabalho novo é a camada de agentes e orquestração, não a base de conhecimento.

### Endpoints principais (novos)
- `POST /verificar-interacoes` — recebe lista de medicamentos, retorna veredito + severidade + fontes

### Extensão opcional: MCP
A lógica de "buscar interação entre dois medicamentos" pode ser exposta como uma **tool MCP**, permitindo que o Agente Buscador (e futuramente outros agentes ou até outros projetos) a consuma via protocolo padrão, em vez de chamada de função direta. Isso demonstra arquitetura desacoplada e reutilizável.

### Entregável da Fase 2
Sistema de verificação estruturada, com múltiplos agentes colaborando, reaproveitando 100% dos dados da Fase 1.

---

## Por que o Telegram (e não Twilio)

O Twilio oferece apenas um trial temporário (30 dias, unidades limitadas, só envia para números verificados, sem mensagens customizadas). Não é gratuito de fato para uso contínuo.

O **Telegram Bot API** é:
- Totalmente gratuito, sem trial, sem cartão de crédito
- Sem limite artificial de mensagens
- Fácil de integrar via `python-telegram-bot` (biblioteca open source)
- Coerente com a proposta do projeto de ser 100% open source e gratuito, de ponta a ponta

---

## Estrutura de Pastas

```
med-rag-assistant/
├── src/
│   ├── agents/          # Agente Buscador, Agregador, Explicador (Fase 2)
│   ├── app/             # bootstrap/inicialização da aplicação
│   ├── config/          # configurações e variáveis de ambiente
│   ├── prompt/          # templates e engenharia de prompt
│   ├── schemas/         # modelos Pydantic (request/response)
│   ├── services/        # regras de negócio (RAG, ingestão, interações)
│   ├── tools/           # tools utilizadas pelos agentes (inclui MCP)
│   └── utils/           # funções auxiliares
├── .env
├── .example.env
├── requirements.txt
└── README.md
```

---

## Como Rodar

```bash
# 1. Clone o repositório
git clone https://github.com/<seu-usuario>/med-rag-assistant.git
cd med-rag-assistant

# 2. Configure as variáveis de ambiente
cp .example.env .env
# edite o .env com suas configurações (tokens, URLs de banco, etc.)

# 3. Suba a infraestrutura (Postgres, Qdrant, Ollama etc.)
docker compose up -d

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Rode a API
uvicorn src.app.main:app --reload

# 6. Rode o bot do Telegram
python -m src.app.telegram_bot
```

A documentação interativa da API estará disponível em `http://localhost:8000/docs` (Swagger).

---

## Roadmap

| Etapa | Entrega |
|---|---|
| 1 | Setup de infra (Docker Compose: Postgres, Qdrant, Ollama) |
| 2 | Pipeline de ingestão de bulas/PubMed |
| 3 | Endpoint `/perguntar` + bot Telegram básico |
| 4 | Testes e documentação da Fase 1 |
| 5 | Agentes Buscador/Agregador/Explicador |
| 6 | Endpoint `/verificar-interacoes` + comando no bot |
| 7 | (Opcional) Exposição via MCP server |
| 8 | Documentação final, README com GIFs de demonstração |

---

## Aviso Legal

Este projeto tem fins **educacionais e de portfólio**. As informações fornecidas não substituem a orientação de um profissional de saúde qualificado. Sempre consulte um médico ou farmacêutico antes de tomar decisões sobre medicamentos.