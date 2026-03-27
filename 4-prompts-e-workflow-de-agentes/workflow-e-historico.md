# Workflow e Histórico

Este arquivo preserva informações de contexto, histórico editorial e descrições complementares de workflow que estavam concentradas no `AGENTS.md` anterior.

Ele existe para manter rastreabilidade do material sem misturar, no mesmo arquivo, dois objetivos diferentes:

- instrução operacional para agentes
- contexto histórico e explicativo do capítulo

Para execução, priorize `AGENTS.md`.
Para estudo, priorize `prompts-e-workflow-de-agentes.md`.
Para contexto complementar e memória editorial do capítulo, consulte este arquivo.

## Contexto do capítulo

Este capítulo demonstra workflows baseados em agentes para análise abrangente de projetos por meio de especificações especializadas. Em vez de trazer uma implementação tradicional em código, ele usa especificações em Markdown para definir papéis, responsabilidades e padrões de coordenação para análise de projetos de software.

A arquitetura modelada é uma arquitetura multiagente liderada por um coordenador, na qual o coordenador principal orquestra agentes especialistas que produzem relatórios estruturados sobre arquitetura, componentes e dependências.

## Estrutura resumida da pasta

```text
4-prompts-e-workflow-de-agentes/
├── AGENTS.md
├── prompts-e-workflow-de-agentes.md
├── workflow-e-historico.md
├── agents/
│   ├── orchestrator.md
│   ├── architectural-analyzer.md
│   ├── component-deep-analyzer.md
│   └── dependency-auditor.md
└── commands/
    └── run-project-state-full-report.md
```

## Histórico de consolidação

Ao longo da reorganização deste capítulo:

- o conteúdo operacional foi concentrado em `AGENTS.md`
- o conteúdo didático foi concentrado em `prompts-e-workflow-de-agentes.md`
- este arquivo passou a preservar observações históricas, contexto editorial e descrições complementares de workflow

Essa separação evita duplicação excessiva e reduz conflito entre instruções normativas e material de estudo.

## Informações históricas de workflow

O desenho original do capítulo enfatizava os seguintes pontos:

- o coordenador principal é responsável por sequenciar fases e controlar paralelismo
- o orquestrador não deve criar subagentes
- o `MANIFEST.md` é a fonte única da verdade do workflow
- a atualização do manifesto deve acontecer após cada agente concluído
- a cobertura de componentes deve ser validada antes do encerramento do fluxo
- o README final deve ser gerado a partir do manifesto

## Fluxo histórico resumido

### Fase 1

- Ler flags de entrada, como pasta do projeto, pasta de saída e listas de exclusão
- Normalizar caminhos
- Criar a estrutura mínima necessária
- Inicializar `MANIFEST.md`

### Fase 2

- Executar `dependency-auditor`
- Executar `architectural-analyzer`
- Rodar ambos em paralelo quando possível
- Registrar cada resultado no manifesto por meio do orquestrador

### Fase 3

- Ler o relatório de arquitetura
- Extrair a lista de componentes críticos
- Executar `component-deep-analyzer` uma vez para cada componente
- Validar cobertura total dos componentes

### Fase 4

- Consolidar relatórios
- Validar caminhos
- Remover duplicações
- Finalizar `MANIFEST.md`

### Fase 5

- Ler o manifesto consolidado
- Validar links
- Gerar o README final com índice dos relatórios

## Observações históricas importantes

- O capítulo foi pensado para ambientes com suporte a coordenação explícita de agentes.
- Parte das referências originais mencionava Claude Code como coordenador principal, mas o padrão conceitual pode ser adaptado para outros ambientes semelhantes.
- O uso de MCPs para validação de dependências era opcional, com destaque para Context7 e Firecrawl nos exemplos.
- O capítulo sempre tratou os relatórios como artefatos descritivos, não prescritivos.

## Relação com os outros arquivos

- `AGENTS.md`: contrato operacional da pasta
- `prompts-e-workflow-de-agentes.md`: guia de estudo do capítulo
- `workflow-e-historico.md`: memória editorial, contexto complementar e resumo histórico de workflow
