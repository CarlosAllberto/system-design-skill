# Fluxos de código

O mapa de nós mostra a infraestrutura (banco, CDN, VPS, filas). Os fluxos de código mostram, para cada rota ou job importante, o caminho que a requisição faz dentro do código: rota, middlewares, validação, controller, action ou service, repositório, chamadas externas e resposta. Cada passo aponta para o arquivo real, mostra o código e tem um resumo do que faz.

Os fluxos ficam em `flows` no `map.json` (formato em `map-schema.md`) e aparecem na aba **Fluxo de código** da página.

## Quais fluxos mapear

Mapeie as rotas que importam, não todas:

1. Escrita de dinheiro ou de dados críticos: pagamento, pedido, cadastro, webhook.
2. Autenticação: login, cadastro, refresh de token, recuperação de senha.
3. As 2 ou 3 rotas mais chamadas (listagem principal, busca, feed).
4. Jobs, crons e consumidores de fila que mexem em dados.
5. Qualquer rota que o usuário citar.

Num projeto grande, comece com 3 a 6 fluxos e pergunte se ele quer mais (na rodada única de perguntas).

## Como rastrear um fluxo

1. Ache onde a rota é registrada: `app/api/**/route.ts` e `middleware.ts` (Next.js), `router.get/post` (Express, Fastify, Hono), `@app.get` ou `APIRouter` (FastAPI), `urls.py` e views (Django), `routes/*.php` (Laravel), `@Controller` (NestJS, Spring), server actions (`'use server'`).
2. Siga a ordem real de execução: middlewares globais que se aplicam à rota, middlewares da rota, validação, handler ou controller, e daí as chamadas para actions, services, repositórios, ORM, filas e APIs externas.
3. Para cada passo, anote o arquivo, as linhas (`lines`) do trecho que importa e o símbolo (nome da função ou classe).
4. Termine com o passo `response` (o que volta e com qual status) quando ajudar a entender o fluxo.
5. Ligue o passo ao nó de infraestrutura que ele usa com `node` (ex.: o repositório aponta para `db`, a chamada ao Stripe aponta para `payments`). Na página, o link leva ao nó no mapa.

Não invente passos. Se um middleware global se aplica, ele entra; se a validação não existe, ela não entra no fluxo atual (vira recomendação).

## Código de cada passo

- **Projeto existente**: prefira `file` + `lines` sem `code`. O `sd.py` lê o trecho do disco toda vez que gera a página, então o código mostrado acompanha o arquivo. Ajuste `lines` se o arquivo mudar muito.
- **Passo recomendado ou app novo**: o arquivo ainda não existe, então escreva o código sugerido em `code`.
- Mostre só o trecho que explica o passo (de 5 a 60 linhas). O `sd.py` corta em 400 linhas.
- Nunca coloque segredos, tokens ou valores de `.env` em `code`. O `sd.py` se recusa a ler `.env*`, chaves (`.pem`, `.key`) e arquivos de credenciais.

## Resumo de cada passo (`summary`)

Uma ou duas frases dizendo o que o passo faz e o que acontece quando falha. Exemplo: "Lê o Bearer token, valida no Auth0 e coloca o usuário em req.user. Sem token válido, responde 401." Evite repetir o nome da função.

## Tipos de passo

| type | Uso |
|---|---|
| `route` | Onde a rota é registrada (path e método) |
| `middleware` | Middleware global ou da rota (auth, CORS, rate limit, logs) |
| `validator` | Validação do corpo, da query ou dos parâmetros (Zod, Joi, Pydantic, class-validator) |
| `controller` | Handler HTTP: traduz a requisição para a regra de negócio e monta a resposta |
| `action` | Server action ou caso de uso com a regra de negócio |
| `service` | Serviço de domínio ou de integração |
| `repository` | Acesso a dados (SQL, ORM, query builder) |
| `model` | Schema, entidade ou tipo central do fluxo |
| `database` | Chamada direta ao banco (procedure, RPC, trigger) |
| `external` | Chamada a API de terceiro (Stripe, e-mail, IA) |
| `queue` | Publicação ou consumo de mensagem |
| `job` | Cron, worker ou tarefa em segundo plano |
| `response` | O que volta para o cliente |
| `util`, `config`, `test` | Utilitário, configuração ou teste relevante ao fluxo |

## CVEs do fluxo

O `sd.py build` lê os `import`, `require` (JS/TS) e `import`/`from` (Python) do arquivo de cada passo e cruza com o `cves.json`. Num projeto npm, as dependências indiretas vêm do `package-lock.json`, então uma CVE do `qs` aparece no passo que importa o `express`. Não precisa preencher nada no `map.json`: basta o passo ter `file`. Imports de arquivos do próprio projeto não são seguidos, então o passo que usa um pacote através de um arquivo local (ex.: `lib/db.js` com o `pg`) só mostra a CVE se esse arquivo também for um passo.

## Recomendações de código

Pense como o time de plataforma de um banco revisando a rota. Avalie cada item abaixo e recomende só o que resolve um risco real deste fluxo:

- **Entrada**: validação de corpo, query e parâmetros com schema; limite de tamanho; paginação com limite máximo.
- **Autenticação e autorização**: checagem de dono do recurso (o usuário só mexe no que é dele), papéis, RLS.
- **Idempotência**: `Idempotency-Key` em criação e pagamento; webhooks idempotentes (o provedor reenvia).
- **Consistência**: transação envolvendo as gravações relacionadas; outbox quando grava e publica evento.
- **Chamadas externas**: timeout, retry com backoff só em operação idempotente, circuit breaker, chave de idempotência no provedor.
- **Erros**: error handler central, sem vazar stack ou SQL para o cliente, status corretos (400, 401, 403, 404, 409, 422).
- **Desempenho**: consultas N+1, falta de índice para o filtro usado, `SELECT *` em tabela larga, cache de leitura.
- **Abuso**: rate limit por usuário e por IP nas rotas de login, cadastro, envio de e-mail e IA.
- **Observabilidade**: log estruturado com id de requisição, sem dados pessoais; erros enviados ao monitoramento.
- **Organização**: regra de negócio fora do controller quando ela é reaproveitada ou testada.

Formato:

- **Passo novo** (`recommendations.steps`): o passo inteiro, com `file` sugerido, `code` sugerido, `why`, `priority`, `effort`. Ligue-o com `recommendations.edges` e marque em `remove_edges` as conexões atuais que ele substitui (ex.: um middleware que entra entre `auth` e `validate`).
- **Mudança num passo existente** (`recommendations.changes`): `step`, `label` curto, `why`, `priority`, `effort` e o `code` sugerido completo do trecho (a página mostra "Atual" e "Sugerido" lado a lado).

Prioridade igual à das recomendações de infraestrutura: `alta` para risco de segurança, de perda de dados ou de cobrança duplicada; `media` para robustez e desempenho; `baixa` para organização.

## Manter os fluxos atualizados

- Mudança só dentro de um fluxo (novo middleware, nova action, rota renomeada) não exige proposta: atualize `flows` no `map.json` e rode `sd.py build` ao terminar a tarefa.
- Se a mudança também muda a infraestrutura (novo banco, fila, API externa), ela segue o fluxo de proposta. Inclua os fluxos novos ou alterados em `add_flows` e `change_flows` da mesma proposta.
- Ao implementar uma recomendação de código, tire-a de `recommendations` e passe o passo para `steps`.
