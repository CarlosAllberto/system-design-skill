<div align="center">

<img src="docs/screenshots/mapa-detalhado.png" alt="Mapa de arquitetura no modo detalhado, com logos" width="100%">

# system-design-skill

**O mapa de arquitetura do seu projeto, vivo e revisável, para você e para a sua IA.**

![Python 3](https://img.shields.io/badge/Python-3-blue)
![Sem dependências](https://img.shields.io/badge/depend%C3%AAncias-nenhuma-lightgrey)
[![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-blue)](LICENSE)

[Capturas](#capturas) • [Instalação](#instalação) • [Uso](#uso) • [O que o init altera](#o-que-o-init-altera-no-projeto) • [Confidencialidade](#confidencialidade) • [O que sai da sua máquina](#o-que-sai-da-sua-máquina)

<a href="README.md">English</a> • Português

</div>

O system-design é uma skill para agentes de IA. Ela guarda a arquitetura do projeto em `.system-design/` (componentes, conexões, limites de capacidade, recomendações e vulnerabilidades das dependências) e mostra tudo numa página local no estilo n8n.

Ela também mapeia **fluxos de código**: para cada rota importante (por exemplo `POST /api/orders`), o caminho que a requisição faz no código (rota, middlewares, validação, controller, action, repositório, resposta), com o código de cada arquivo e um resumo do que ele faz. O botão **Com recomendações** mostra os passos novos sugeridos e as mudanças de código sugeridas.

A IA lê um resumo do mapa antes de mexer em backend. Quando uma tarefa muda o fluxo (novo banco, fila, API externa, deploy), ela propõe a mudança, você aprova na página e só então ela implementa, marcando o progresso em tempo real.

## Capturas

O mapa mostra os componentes e as conexões. O botão do canto inferior alterna entre o modo simplificado (ícones por tipo) e o detalhado (logos e tecnologias). O tema claro e o escuro seguem o sistema.

<p align="center">
  <img src="docs/screenshots/mapa-simplificado.png" alt="Mapa no modo simplificado" width="49%">
  <img src="docs/screenshots/mapa-claro.png" alt="Mapa no tema claro" width="49%">
</p>

A aba **Com recomendações** desenha a arquitetura sugerida sobre a atual: o que entra fica tracejado em roxo e o que sai, em vermelho.

<p align="center">
  <img src="docs/screenshots/recomendacoes-mapa.png" alt="Mapa com recomendações, modo detalhado" width="100%">
</p>

<p align="center">
  <img src="docs/screenshots/recomendacoes-mapa-simplificado.png" alt="Mapa com recomendações, modo simplificado" width="49%">
  <img src="docs/screenshots/recomendacoes-lista.png" alt="Lista de recomendações com prioridade, esforço e custo" width="49%">
</p>

Abaixo do mapa ficam as listas de limitações e de vulnerabilidades das dependências. Clicar numa limitação destaca o componente afetado no mapa.

<p align="center">
  <img src="docs/screenshots/limitacoes.png" alt="Lista de limitações por severidade" width="100%">
</p>

<p align="center">
  <img src="docs/screenshots/cves.png" alt="Lista de CVEs com a versão corrigida" width="100%">
</p>

A aba **Fluxo de código** desenha uma rota por vez. Escolha a rota no topo; cada passo vira um nó com o seu arquivo. Clicar num passo abre o resumo, o arquivo com as linhas e o código com realce de sintaxe. Sem código no JSON, o `sd.py` lê o trecho do arquivo no disco, então a página acompanha o código.

<p align="center">
  <img src="docs/screenshots/fluxo-codigo.png" alt="Fluxo de código do POST /api/orders: rota, middlewares, validação, controller, action, repositório e resposta" width="100%">
</p>

<p align="center">
  <img src="docs/screenshots/fluxo-codigo-arquivo.png" alt="Painel do passo com resumo, arquivo, componente ligado e código" width="100%">
</p>

O botão **Com recomendações** acrescenta os passos sugeridos (tracejado roxo, como um middleware de idempotência), marca os passos cujo código deve mudar (azul, com as visões *Atual* e *Sugerido*) e as conexões que saem (tracejado vermelho). Cada recomendação tem um botão que copia um pedido pronto, com o código sugerido, para colar no agente.

<p align="center">
  <img src="docs/screenshots/fluxo-codigo-recomendacoes.png" alt="Fluxo de código com passos recomendados" width="49%">
  <img src="docs/screenshots/fluxo-codigo-sugerido.png" alt="Código atual e sugerido de um passo" width="49%">
</p>

> [!NOTE]
> Os dados das capturas vêm de [`examples/`](examples) e são fictícios.

> [!NOTE]
> Projeto independente. A skill usa só a biblioteca padrão do Python 3.

## Instalação

```bash
npx skills add CarlosAllberto/system-design-skill
```

O comando instala a skill nos agentes compatíveis que você usa. O repositório se chama `system-design-skill`, mas a skill instalada se chama `system-design`, nome definido no `SKILL.md`. Requisito: Python 3 (no Windows o comando pode ser `python`).

## Uso

Peça ao agente algo como "mapeie o system design deste projeto". A skill tem 4 modos:

| Modo | Quando | O que acontece |
| --- | --- | --- |
| 1. Mapear um projeto existente | O projeto já tem código | A IA lê o código, faz todas as perguntas numa rodada só e escreve o `map.json` com nós, conexões, limites, recomendações e os fluxos de código das rotas principais |
| 2. Desenhar um backend novo | App novo, sem backend | A arquitetura alvo e os fluxos de código planejados (com código inicial) viram uma proposta com tarefas de implementação |
| 3. Propor antes de mudar o fluxo | Novo componente, banco, fila, cache, API externa, autenticação ou deploy | A IA registra a proposta e espera você aprovar na aba Atualização |
| 4. Executar a atualização aprovada | Depois da aprovação | Cada item passa por `waiting`, `in_progress` e `done`; no fim o `finalize` atualiza o mapa |

Para mapear só o código de uma rota, peça algo como "mapeie o fluxo de código de api/users" ou "mostre o fluxo de código do POST /api/orders com recomendações".

Comandos úteis, a partir da raiz do projeto:

```bash
python3 .system-design/sd.py serve --open
python3 .system-design/sd.py cves
python3 .system-design/sd.py build
```

Um exemplo para testar fica em [`examples/map.example.json`](examples/map.example.json). Para ver a aba de vulnerabilidades, copie também [`examples/cves.example.json`](examples/cves.example.json) para `.system-design/cves.json` (os dados são fictícios) e rode `build`.

## O que o init altera no projeto

O `sd.py init` cria a pasta `.system-design/` e mexe só nisto:

- **`AGENTS.md`:** acrescenta um bloco entre `<!-- system-design:start -->` e `<!-- system-design:end -->` com uma linha condicional ("se existir `.system-design/AI-MAP.md`, leia"). O resto do arquivo não é tocado, e rodar o `init` de novo não duplica nada.
- **`CLAUDE.md`:** só remove o bloco do system-design, se existir. Se o arquivo não importar o `AGENTS.md`, o `init` avisa.
- **`.gitignore`:** adiciona `.system-design/`.

## Confidencialidade

A pasta `.system-design/` descreve a arquitetura, os limites e as vulnerabilidades do projeto. Se vazar, vira um roteiro de ataque.

- Não faça commit dela nem cole o conteúdo em issue, PR, chat público ou serviço externo. O `index.html` gerado também embute o código dos passos dos fluxos.
- O `init` põe a pasta no `.gitignore` e avisa se o git já rastreia algum arquivo dela.
- Para backup, guarde a pasta num lugar privado.

## O que sai da sua máquina

Só isto:

1. `sd.py cves` envia nomes e versões de pacotes ao [OSV](https://osv.dev).
2. A página pede ao [Simple Icons](https://simpleicons.org) os logos pelo slug da marca. Para desligar, ponha `"logos": false` em `project` no `map.json`.
3. A página pede a fonte Inter ao Google Fonts.

Nenhum conteúdo do `map.json` (nomes de projeto, limites, descrições) é enviado a terceiros.

## Estrutura

```
system-design-skill/
├── SKILL.md          Instruções para o agente
├── scripts/sd.py     CLI do ciclo de vida (propose, approve, set, finalize, cves, serve)
├── assets/viewer.html Página do mapa
├── docs/screenshots/ Capturas do README
├── references/       Esquema do map.json, fluxos de código, limites, recomendações, app novo
└── examples/         Mapa de exemplo
```

## Licença

[MIT](LICENSE)
