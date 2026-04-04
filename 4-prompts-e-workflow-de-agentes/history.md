# Histórico do Capítulo 4

Este arquivo preserva contexto editorial, formulações antigas do workflow e informações removidas da documentação operacional.

## Reorganização documental

O capítulo foi consolidado com a seguinte divisão:

- `README.md`: visão geral, estrutura e forma de uso;
- `prompts-e-workflow-de-agentes.md`: explicação aprofundada do capítulo;
- `history.md`: memória editorial e contexto histórico;
- `AGENTS.md`: orientações curtas para agentes.

## Estruturas anteriores preservadas

Pelo histórico do git:

- em `2025-09-22`, foram adicionados `agents/` e `commands/`, formalizando o capítulo como material specification-driven;
- em `2025-10-10`, foi adicionado um `AGENTS.md` amplo e centralizador;
- em `2026-03-27`, o commit `0bb1fd3` adicionou `prompts-e-workflow-de-agentes.md` e `workflow-e-historico.md`.

Ou seja, por um período o capítulo teve como estrutura principal:

- `AGENTS.md`
- `prompts-e-workflow-de-agentes.md`
- `workflow-e-historico.md`
- `agents/`
- `commands/`

## Contexto preservado do workflow

O desenho original do capítulo enfatizava:

- coordenador principal responsável por sequenciar fases e paralelismo;
- orquestrador responsável apenas por registrar estado;
- `MANIFEST.md` como fonte única da verdade;
- cobertura completa de componentes antes do encerramento;
- geração de README final a partir do manifesto.

## Nome antigo do arquivo histórico

Antes da normalização atual, o arquivo de memória histórica do capítulo se chamava `workflow-e-historico.md`.

Esse nome é importante para rastreabilidade porque:

- ele aparece em referências internas antigas;
- ele foi parte explícita da organização do capítulo;
- a consolidação para `history.md` aconteceu depois, para alinhar este capítulo ao padrão dos demais.

## Observações históricas

- O capítulo foi pensado para ambientes com coordenação explícita de agentes.
- Parte das referências antigas citava Claude Code como coordenador principal, mas o padrão conceitual é adaptável a outros ambientes.
- O uso de validação externa, como MCPs, sempre foi opcional e subordinado às especificações dos agentes.

## Contexto removido do AGENTS

O `AGENTS.md` anterior acumulava documentação de estudo, regras operacionais e histórico no mesmo arquivo. A reorganização atual separa essas funções para reduzir redundância e tornar a leitura mais clara.

O histórico do git também preserva outra fase relevante:

- em `2026-03-21`, o commit `b279f5d` revisou `commands/run-project-state-full-report.md` e vários arquivos em `agents/`;
- em `2026-03-22`, o commit `f995a50` fez nova rodada de ajustes nesses agentes.

Essas mudanças indicam que o workflow e as especificações dos agentes evoluíram ativamente antes da normalização documental final.
