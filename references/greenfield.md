# Aplicação nova: perguntas e escolhas

Use no Modo 2 (projeto sem backend). Faça as perguntas numa rodada só, antes de desenhar qualquer coisa. Pule as que o pedido ou o código já respondem.

## Perguntas

1. **Produto**: o que o app faz, em uma frase, e quais são as 3 ações principais do usuário?
2. **Usuários**: quantos usuários ativos no primeiro mês e daqui a um ano? Há picos previsíveis (campanha, horário comercial)?
3. **Dados**: que dados o app guarda? Há dado sensível (saúde, financeiro, documento pessoal) ou exigência da LGPD?
4. **Contas**: como o usuário entra (e-mail e senha, Google, link mágico, SSO de empresa)? Há multiempresa (workspaces, times)?
5. **Arquivos**: o usuário envia arquivos? De que tamanho e quantos?
6. **Tempo real e tarefas em segundo plano**: precisa de chat, notificações ao vivo, e-mails, relatórios ou integrações agendadas?
7. **Integrações**: pagamento, e-mail, WhatsApp, IA, calendário, mapas?
8. **Hospedagem e orçamento**: já tem preferência (Vercel, VPS, AWS, Supabase, Firebase)? Quanto pode gastar por mês no início?
9. **Equipe**: quem vai manter o sistema e em que linguagem a equipe trabalha melhor?

## Escolhas padrão (quando o usuário não tiver preferência)

| Situação | Escolha inicial | Quando trocar |
|---|---|---|
| Frontend web com SSR | Next.js na Vercel | Custo de banda ou de functions alto: VPS com Node |
| Banco relacional e autenticação | Supabase (Postgres, Auth, RLS, Storage) | Regra de negócio pesada no servidor: API própria em Node ou Python |
| E-mail transacional | Resend ou Postmark | Volume alto: Amazon SES |
| Pagamento no Brasil | Stripe (cartão) ou Mercado Pago (Pix) | Pix recorrente: provedor com Pix Automático |
| Tarefas em segundo plano | Cron da hospedagem e fila no Postgres (pgmq) | Mais de alguns milhares de jobs por hora: fila dedicada |
| Arquivos | Object storage com URL assinada | Nunca no disco do servidor |
| IA | API do provedor chamada no servidor, com limite por usuário | Custo alto: cache de respostas e modelo menor |
| Observabilidade | Sentry e logs da hospedagem | Muitos serviços: OpenTelemetry |

## Como montar a proposta

- Comece pelo menor conjunto de peças que cobre as respostas. Cada peça a mais precisa de um motivo escrito no `description`.
- Registre os limites do plano escolhido já na proposta (`add_limits`), com o valor do plano gratuito ou do plano inicial.
- Coloque em `recommendations` (direto no `map.json`, depois do `finalize`) o que só vale após crescer, com o gatilho no `why`.
- Desenhe também os fluxos de código das 2 a 4 rotas principais em `add_flows` (veja `code-flows.md`): pastas e arquivos, ordem de rota, middlewares, validação, action e repositório, com o código inicial sugerido em `code`. Isso vira o esqueleto que a implementação segue.
- Quebre a implementação em `tasks` pequenas, na ordem em que vão acontecer: criar o projeto no provedor, schema e RLS, autenticação, primeira rota, deploy, monitoramento.
