# Checklist de limitações

Para cada componente, procure no código e na configuração os limites abaixo. Registre os que existem, com valor concreto. Use `scope` assim:

- `hosting`: limite da máquina ou da hospedagem onde o nó roda.
- `service`: limite de um serviço gerenciado ou de terceiro.
- `app`: limite criado pelo próprio código ou pela arquitetura.

## Hospedagem ou VPS (`hosting`)
- RAM total e quanto cada processo disputa (Node, Postgres, Redis, workers).
- CPU (vCPUs) e créditos de burst; I/O e espaço em disco; inodes.
- Banda mensal e velocidade da porta; limite de conexões e portas abertas, `ulimit` de arquivos.
- Ponto único de falha (uma máquina, uma zona), janelas de manutenção, snapshots.
- Plano serverless: tempo máximo de execução, memória por função, tamanho do body e do bundle, cold start, invocações simultâneas.

## Banco de dados (`service` ou `app`)
- Máximo de conexões (e se há pooler); tamanho do plano (GB); IOPS.
- Consultas sem índice, tabelas sem partição que crescem sem limite, transações longas.
- Limite de linhas por resposta da API (ex.: 1000 no PostgREST) e tamanho de payload.
- Realtime: canais e conexões simultâneas. Storage: tamanho máximo de arquivo e banda.

## Autenticação (`service` ou `app`)
- MAUs do plano, limite de e-mails de autenticação por hora, rate limit de login e de envio de OTP ou SMS.
- Sessões simultâneas por usuário, duração do token, limite de usuários de um app OAuth não verificado.
- Quantos logins por minuto o serviço aguenta.

## API e backend (`app`)
- Usuários simultâneos estimados contra a capacidade (requisições por segundo por instância, workers, event loop bloqueado).
- Tamanho máximo de body e de upload, timeout de requisição, lista de origens no CORS.
- Operações síncronas pesadas (PDF, imagem, relatório) dentro da requisição.
- Estado em memória (sessões, cache local, WebSocket) que impede escalar na horizontal.

## Dependências (`app`)
- CVE crítica ou alta em pacote usado em produção (veja `sd.py cves`), principalmente sem versão corrigida.
- Framework ou runtime fora do suporte.

## Terceiros (`service`)
- Rate limit e quota de cada API externa (pagamento, e-mail, SMS, mapas, LLM: tokens por minuto e custo).
- Limites do plano gratuito (envios por dia, webhooks, armazenamento).
- Dependência crítica sem alternativa.

## Filas e cache (`service` ou `app`)
- Memória máxima do Redis e política de evicção; tamanho máximo de mensagem; retenção da fila.
- Vazão do consumidor contra a produção; ausência de dead-letter queue.

## IA (`service` ou `app`)
- Janela de contexto, tokens por minuto, custo por usuário, latência p95.
- Tamanho do índice vetorial e tempo de reindexação.

## Severidade
- `crit`: já é gargalo, ou queda provável no próximo crescimento.
- `warn`: vai apertar com 2 a 5 vezes o uso atual.
- `info`: limite conhecido, sem risco próximo.

Se não for possível descobrir o valor (o plano contratado, por exemplo), pergunte ao usuário **antes** de escrever o mapa. Se ele não souber, registre `value: "desconhecido"` com `severity: info`.
