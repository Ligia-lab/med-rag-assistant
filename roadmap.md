# Roadmap — MED-RAG-ASSISTANT

Checklist geral do projeto, em ordem. Marca o que for concluindo.

---

## Fase 0 — Setup

- [x] Definir arquitetura e stack do projeto
- [x] Criar esqueleto de pastas (`src/`)
- [x] Configurar `.env`, `.example.env` e `.gitignore`
- [x] Criar `docker-compose.yml` (Postgres, Qdrant)
- [x] Validar infra (Postgres, Qdrant e Ollama respondendo)
- [x] Configurar venv e `requirements.txt`

---

## Fase 1 — Assistente de Consulta (RAG aberto)

### Ingestão
- [x] Extrair texto de bulas em PDF
- [x] Implementar chunking (por seção)
- [x] Limpar ruídos do texto extraído (rodapés, repetições)
- [ ] Gerar embeddings dos chunks (Ollama / nomic-embed-text)
- [ ] Gravar chunks + embeddings no Qdrant
- [ ] Validar busca manual (pergunta → chunk certo retorna)
- [ ] Automatizar ingestão para múltiplas bulas (loop pela pasta `bulas/`)
- [ ] (Opcional) Ingestão de artigos do PubMed/PMC

### API
- [ ] Definir schemas de request/response (`/perguntar`)
- [ ] Implementar service de RAG (busca + prompt + geração)
- [ ] Criar endpoint `POST /perguntar`
- [ ] Criar endpoint `GET /documentos`
- [ ] Criar endpoint `POST /ingestao` (uso interno)
- [ ] Testar tudo via Swagger

### Telegram Bot
- [ ] Criar bot via BotFather e configurar token
- [ ] Implementar handler `/perguntar`
- [ ] Testar fluxo completo (Telegram → API → resposta)

### Fechamento da Fase 1
- [ ] Escrever testes básicos (pytest)
- [ ] Gravar GIF/demo do bot funcionando
- [ ] Atualizar README com o que foi entregue

---

## Fase 2 — Verificador de Interações Medicamentosas (RAG + Agentes)

- [ ] Definir arquitetura dos agentes com LangChain/LangGraph
- [ ] Implementar Agente Buscador (busca pares de medicamentos no Qdrant)
- [ ] Implementar Agente Agregador (classifica severidade)
- [ ] Implementar Agente Explicador (gera resposta legível)
- [ ] Orquestrar o fluxo entre os 3 agentes
- [ ] Criar endpoint `POST /verificar-interacoes`
- [ ] Implementar comando `/interacoes` no Telegram Bot
- [ ] Testar fluxo completo ponta a ponta
- [ ] (Opcional) Expor lógica de busca de interação como tool MCP

### Fechamento da Fase 2
- [ ] Escrever testes
- [ ] Atualizar README e documentação final

---

## Encerramento do Projeto

- [ ] Revisão geral do código
- [ ] README final com GIFs de demonstração
- [ ] Aviso legal revisado e visível em todos os canais (README, bot, API)
- [ ] Publicar/divulgar o repositório