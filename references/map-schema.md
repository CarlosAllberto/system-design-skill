# Schema do map.json

```json
{
  "project": {
    "name": "Meu App",
    "description": "O que o sistema faz em uma frase.",
    "hosting": { "provedor": "VPS Hetzner CX22", "recursos": "2 vCPU, 4 GB de RAM, 40 GB de SSD", "região": "Nuremberg" },
    "logos": true
  },
  "version": 1,
  "nodes": [
    {
      "id": "web",
      "label": "Frontend",
      "type": "frontend",
      "tech": "Next.js 15",
      "logo": "nextdotjs",
      "description": "Interface do usuário e SSR.",
      "host": "VPS"
    }
  ],
  "edges": [
    { "from": "web", "to": "api", "label": "HTTPS/JSON" }
  ],
  "limits": [
    {
      "id": "api-ram",
      "node": "api",
      "scope": "hosting",
      "severity": "warn",
      "label": "Memória",
      "value": "4 GB compartilhados com o Postgres",
      "note": "Node e Postgres na mesma máquina."
    }
  ],
  "recommendations": {
    "nodes": [
      {
        "id": "lb",
        "label": "Load balancer",
        "type": "loadbalancer",
        "tech": "Nginx / HAProxy",
        "logo": "nginx",
        "why": "Remove o ponto único de falha da API e permite escalar na horizontal.",
        "priority": "alta",
        "effort": "médio",
        "cost": "baixo",
        "resolves": ["api-ram"],
        "improves": ["api"]
      }
    ],
    "edges": [ { "from": "web", "to": "lb", "label": "HTTPS" }, { "from": "lb", "to": "api" } ],
    "remove_edges": [ { "from": "web", "to": "api" } ]
  }
}
```

## Campos

**node**: `id` (a-z, 0-9, `-`, `_`), `label`, `type`, `tech`, `description`, `host` (onde roda) e `logo` (opcional). Tipos: `client`, `frontend`, `api`, `service`, `database`, `cache`, `queue`, `storage`, `auth`, `external`, `loadbalancer`, `worker`, `ai`, `monitoring`, `cdn`, `gateway`.

**logo**: slug do [Simple Icons](https://simpleicons.org) (só `a-z` e `0-9`, ex.: `supabase`, `postgresql`, `stripe`, `vercel`, `googledrive`, `redis`), ou uma URL `https://` de imagem. Qualquer outro valor (`javascript:`, `data:`, `http:`) é rejeitado pelo `validate`. Use `false` para forçar o ícone do tipo. Sem o campo, a página tenta adivinhar o logo pelo `label` e pela `tech`.

**project.logos**: `true` por padrão. Com `false`, a página não faz nenhuma requisição ao Simple Icons, ignora também as URLs `https` de `logo` e usa o ícone do tipo em todos os nós.

**edge**: `from`, `to` (ids de nós) e `label` opcional (protocolo ou o que trafega).

**limit**:
- `id` único, `node` (o nó afetado), `label`, `value` e `note` opcional.
- `scope`: `hosting` = limite da hospedagem; `service` = limite de um serviço gerenciado ou de terceiro; `app` = limite do próprio código ou da arquitetura.
- `severity`: `info` (conhecido, sem risco próximo), `warn` (vai apertar com o crescimento), `crit` (já é gargalo ou risco de queda).
- Na página, o nó só ganha o estilo de alerta quando o usuário clica no limite na lista.

**recommendation node**: igual a um node, mais `why`, `priority` (`alta`, `media` ou `baixa`), `effort`, `cost`, `resolves` (ids dos limites que ela resolve) e `improves` (ids dos nós existentes que ela melhora). Os ids não podem repetir ids de nós existentes.

**recommendations.edges**: conexões do mapa recomendado (podem ligar nós existentes e recomendados). **remove_edges**: conexões atuais que a recomendação substitui (aparecem tracejadas em vermelho).

## Proposta (entrada do `sd.py propose`)

```json
{
  "title": "Adicionar Redis para cache de sessões",
  "summary": "Sessões e consultas frequentes saem do Postgres.",
  "reason": "Resolve o limite de 60 conexões do banco nos horários de pico.",
  "add_nodes": [
    { "id": "redis", "label": "Redis", "type": "cache", "tech": "Redis 7", "logo": "redis", "description": "Cache de sessão e rate limit." }
  ],
  "change_nodes": [
    { "id": "api", "patch": { "description": "API com cache de leitura." }, "note": "Passa a ler do Redis antes do banco." }
  ],
  "remove_nodes": [],
  "add_edges": [ { "from": "api", "to": "redis", "label": "TCP 6379" } ],
  "remove_edges": [],
  "add_limits": [
    { "id": "redis-mem", "node": "redis", "scope": "hosting", "severity": "info", "label": "Memória", "value": "256 MB reservados" }
  ],
  "remove_limits": [],
  "implements_recommendations": ["redis"],
  "tasks": [ { "id": "migrar-sessoes", "label": "Migrar as sessões para o Redis" } ]
}
```

Cada nó em `add_nodes`, `change_nodes` e `remove_nodes` e cada item de `tasks` vira um item rastreável (`sd.py set <id> <estado>`). Estados: `waiting`, `in_progress`, `done` e `blocked`. Se o `id` de um item de `add_nodes` for o de uma recomendação, ela vira nó real e sai das recomendações ao finalizar.

Num projeto novo (Modo 2), a proposta inicial costuma ter só `add_nodes`, `add_edges`, `add_limits` e `tasks`.

## Ciclo de status da atualização

`proposed` (aguardando aprovação) -> `approved` -> `in_progress` -> `finalize` (a atualização some). Desvio: `rejected`.
