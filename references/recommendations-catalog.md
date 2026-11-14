# Catálogo de recomendações (visão de um sistema bancário em Java)

Use como lista de verificação. Recomende apenas o que faz sentido para o tamanho e os limites reais do projeto, mas avalie sempre cada linha. Em projetos pequenos, marque itens pesados (Kafka, multirregião) com `priority: baixa` e explique no `why` o gatilho para adotá-los (ex.: "quando passar de 500 requisições por segundo").

## Borda e entrada
- **CDN e WAF** (Cloudflare, CloudFront): cache de arquivos estáticos e proteção contra DDoS e contra o OWASP Top 10. Tipo `cdn`.
- **API Gateway**: autenticação central, rate limit por cliente, versionamento e quotas. Tipo `gateway`.
- **Load balancer** (Nginx, HAProxy, ALB) com health checks e pelo menos 2 instâncias da API. Tipo `loadbalancer`.
- **Rate limit e proteção contra abuso** por IP e por usuário (Redis como contador).

## Aplicação
- **Instâncias stateless** da API atrás do balanceador (sessão fora da memória do processo).
- **Autoscaling** horizontal (container ou orquestrador) quando houver pico previsível.
- **Separar leitura e escrita** (CQRS leve) quando a leitura dominar.
- **Idempotência** em endpoints de pagamento e de criação (chave de idempotência) e retries com backoff.
- **Circuit breaker e timeouts** nas chamadas a APIs externas.
- **Feature flags** e deploy gradual (blue/green ou canary).

## Dados
- **Réplicas de leitura** do banco e failover automático (primário e standby).
- **Connection pooler** (PgBouncer, Supavisor) para não estourar as conexões.
- **Particionamento ou sharding** de tabelas grandes por tempo ou por tenant.
- **Cache em camadas** (Redis para dados frequentes, cache HTTP para respostas públicas). Tipo `cache`.
- **Busca dedicada** (OpenSearch, Meilisearch, pgvector) quando LIKE e filtros ficarem lentos.
- **Backups automáticos com PITR** e teste de restauração periódico.
- **Object storage com CDN** para arquivos, nunca no disco da VPS.

## Assíncrono
- **Fila de mensagens** (RabbitMQ, SQS; Kafka em escala maior) para e-mails, webhooks, relatórios e integrações. Tipo `queue`.
- **Workers** separados da API, com **dead-letter queue** e reprocessamento.
- **Outbox pattern** quando o evento e a gravação no banco precisam ser consistentes.
- **Jobs agendados** isolados, fora do processo da API.

## IA e RAG (quando o produto usa LLM)
- **Pipeline de RAG**: ingestão, chunking, embeddings, vector store (pgvector, Qdrant) e reranker. Tipo `ai`.
- **Gateway de LLM** com cache semântico, alternativa entre provedores e limites de custo e de tokens por usuário.
- **Guardrails**: filtro de entrada e de saída, mascaramento de dados pessoais, log de prompts sem dados sensíveis.
- **Avaliação contínua** (conjunto de perguntas de referência) para detectar regressão.

## Segurança e conformidade
- **Gestão de segredos** (Vault, Secrets Manager, Doppler) e rotação de chaves.
- **Identidade**: provedor central (OIDC), MFA, RBAC ou ABAC, sessões com expiração e revogação.
- **Criptografia** em trânsito e em repouso; campos sensíveis com criptografia por coluna.
- **Auditoria**: trilha imutável de quem fez o quê. **LGPD**: retenção, exclusão e consentimento.
- **Rede**: segmentação (sub-redes privadas para banco e filas), bastion ou VPN, firewall mínimo.
- **Dependências**: varredura de CVEs no CI (`sd.py cves`, Dependabot, Renovate), além de SAST e DAST.

## Observabilidade e operação
- **Logs estruturados** centralizados, **métricas** (Prometheus, Grafana) e **tracing** distribuído (OpenTelemetry). Tipo `monitoring`.
- **Alertas** por SLO (latência, taxa de erro, saturação) e **status page**.
- **Health checks** e probes de readiness e liveness.
- **IaC** (Terraform, Ansible) e CI/CD com testes e rollback automático.
- **Recuperação de desastre**: RPO e RTO definidos, ambiente de recuperação, várias zonas; multirregião só se o negócio exigir.

## Como escolher a prioridade
- `alta`: resolve um limite `crit`, remove um ponto único de falha ou fecha um risco de segurança ou de perda de dados.
- `media`: resolve um limite `warn` ou melhora custo ou operação de forma clara.
- `baixa`: só vale depois do crescimento; descreva o gatilho no `why`.
