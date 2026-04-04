# Capítulo 4: Prompts e Workflow de Agentes

Este capítulo mostra como transformar prompts em especificações de workflow multiagente. Ele é importante porque conecta estruturação de prompts com separação de responsabilidades, coordenação por fases e geração de relatórios auditáveis.

## Estrutura da pasta

| Caminho | Papel |
| --- | --- |
| `prompts-e-workflow-de-agentes.md` | aula principal do capítulo |
| `history.md` | memória editorial, contexto removido e nomenclaturas antigas |
| `agents/` | especificações dos agentes especialistas |
| `commands/` | especificação do fluxo coordenador |
| `AGENTS.md` | orientações curtas para agentes |

## O que estudar aqui

O capítulo aprofunda:

- estrutura de prompts para agentes especialistas;
- separação entre coordenador, orquestrador e especialistas;
- fases de um workflow multiagente;
- uso de manifesto como fonte de verdade;
- disciplina de caminhos, outputs e cobertura.

Para a explicação completa, leia `prompts-e-workflow-de-agentes.md`.

## Como usar a pasta

Esta pasta é specification-driven. Ela não contém uma aplicação única para execução local; ela contém artefatos textuais que definem como um coordenador deve operar os agentes.

O fluxo prático do capítulo passa por:

1. `commands/run-project-state-full-report.md`
2. arquivos em `agents/`
3. regras cruzadas em `AGENTS.md`

## Importância do capítulo

Este é o capítulo que mostra como Prompt Engineering deixa de ser apenas instrução para um modelo e passa a virar protocolo entre múltiplos agentes, com estado, cobertura e auditabilidade.
