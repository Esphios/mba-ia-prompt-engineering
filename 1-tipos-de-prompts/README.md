# Capítulo 1: Tipos de Prompts

Este capítulo apresenta o repertório base de técnicas de prompting usado ao longo do restante do curso. Ele estabelece a linguagem comum das aulas seguintes: como orientar o modelo, quando usar exemplos, quando explicitar raciocínio e quando dividir o problema em etapas.

## Como este capítulo está organizado

| Caminho               | Papel                                                                           |
| --------------------- | ------------------------------------------------------------------------------- |
| `tipos-de-prompts.md` | aula principal, com explicação conceitual das técnicas                          |
| `examples/`           | trilha didática, mais próxima da sequência original da aula                     |
| `generic/`            | trilha reutilizável, com CLI, advisor e scripts parametrizados                  |
| `utils.py`            | utilitário compartilhado da trilha `examples/`                                  |
| `history.md`          | contexto editorial, nomes antigos e conteúdo retirado dos documentos principais |
| `AGENTS.md`           | instruções operacionais curtas para agentes                                     |

## O que estudar aqui

O capítulo cobre:

- role prompting;
- zero-shot;
- one-shot e few-shot;
- chain of thought;
- self-consistency;
- tree of thought;
- skeleton of thought;
- ReAct;
- prompt chaining;
- least-to-most.

Comece por `tipos-de-prompts.md` para entender as técnicas. Depois escolha a trilha prática adequada:

- `examples/` para acompanhar a progressão didática do capítulo;
- `generic/` para reaproveitar as técnicas em problemas novos.

## Como navegar entre as trilhas

As duas pastas não são duplicatas simples.

- `examples/` prioriza clareza pedagógica, nomes históricos dos scripts e execução direta.
- `generic/` prioriza reuso, parametrização e uma interface central para listar, sugerir e executar técnicas.

Essa distinção precisa ficar explícita porque o mesmo nome conceitual aparece em ambas as trilhas, mas com intenções diferentes.

## Referência das técnicas

Esta seção preserva o resumo operacional das técnicas do capítulo em um ponto único da documentação. A explicação mais conceitual continua em `tipos-de-prompts.md`, enquanto as instruções de execução detalhadas ficam nos READMEs internos.

## Princípios gerais

Os pontos abaixo valem para todas as técnicas:

- seja intencional: defina contexto, saída desejada e como a resposta será auditada;
- nem toda tarefa precisa raciocínio detalhado;
- em alta escala, técnicas mais simples costumam ser preferíveis quando a tarefa permite;
- a escolha do modelo muda custo, latência e ganho real de cada técnica;
- mais exemplos não significam automaticamente melhor resultado;
- quando uma etapa alimenta a próxima, estrutura e parsing deixam de ser detalhe e passam a ser requisito;
- a IA ainda pode errar ou alucinar, então o refinamento do prompt continua sendo parte central do resultado.

## Como executar

Para seguir a trilha didática:

```powershell
python .\examples\0-Role-prompting.py
python .\examples\1-zero-shot.py
python .\examples\2-one-few-shot.py
python .\examples\3-CoT.py
python .\examples\3.1-CoT-Self-consistency.py
python .\examples\4-ToT.py
python .\examples\5-SoT.py
python .\examples\6-ReAct.py
python .\examples\7-Prompt-channing.py
python .\examples\8-Least-to-most.py
```

Para reaproveitar a trilha genérica, o ponto de entrada principal é:

```powershell
python .\generic\prompt_runner.py list
python .\generic\prompt_runner.py suggest --task "Explique recursão em termos simples."
python .\generic\prompt_runner.py run --technique zero-shot --task "Explique recursão em termos simples."
```

## Importância do capítulo

Sem este capítulo, os demais tendem a parecer apenas coleções de scripts ou prompts isolados. Ele fornece o vocabulário técnico que sustenta capítulos sobre estruturação, workflows, versionamento e enriquecimento.
