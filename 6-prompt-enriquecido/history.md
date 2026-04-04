# Histórico do Capítulo 6

Este arquivo preserva divergências antigas da pasta, observações editoriais e contexto removido da documentação principal.

## Divergências corrigidas

Durante a reorganização da documentação, foram corrigidas referências que não refletiam a árvore real da pasta:

- a aula principal é `prompt-enriquecido.md`, não `lessons.md`;
- o histórico do capítulo é `history.md`, não `lessons.history.md`;
- não existe pasta `examples/` neste diretório;
- os nomes válidos dos scripts continuam sendo:
  - `0-No-expansion.py`
  - `1-ITER_RETGEN.py`
  - `2-query-enrichment.py`

Os logs do Codex mostram que, antes da normalização final, este capítulo chegou a ser documentado como se tivesse:

- `lessons.md` como aula principal;
- `lessons.history.md` como histórico;
- uma pasta `examples/`.

Nenhuma dessas três premissas correspondia à árvore real do capítulo.

## Conteúdo removido da documentação principal

Foram movidos para `history.md`:

- menções a execuções específicas de modelos;
- números de iteração e crescimento de resposta tratados como se fossem invariantes;
- referências a estruturas que não existiam mais na pasta;
- descrições que misturavam teoria de retrieval com a implementação didática atual.

## Estrutura anterior preservada pelo git

Pelo histórico do git, o capítulo foi adicionado em `2025-09-29` com:

- `.env.example`
- `.gitignore`
- `requirements.txt`
- `0-No-expansion.py`
- `1-ITER_RETGEN.py`
- `2-query-enrichment.py`

Depois, em `2026-03-21`, o commit `b279f5d` removeu:

- `.env.example`
- `.gitignore`
- `requirements.txt`

Esse detalhe é relevante porque parte da documentação antiga foi escrita como se esse setup local ainda existisse.

## Ajuste entre teoria e implementação

O capítulo continua explicando `Query2Doc`, `HyDE` e `ITER-RETGEN`, mas a implementação local permanece mais simples:

- `1-ITER_RETGEN.py` demonstra o loop iterativo;
- a etapa de preenchimento é feita pelo próprio LLM;
- não há integração explícita com web, Elastic ou banco vetorial.

O `AGENTS.md` original do capítulo também mencionava explicitamente:

- LangChain `1.0.0a5`, `langgraph`, `langsmith` e `pytest` como stack local;
- um diretório `repo_langchain_1.0/` como repositório de referência;
- notas de troubleshooting e migração entre capítulos.

Como esses pontos misturavam setup antigo, referência auxiliar e instrução operacional, eles foram retirados dos arquivos principais e preservados aqui.

## Reorganização documental

A documentação foi normalizada para seguir o padrão do restante do curso:

- `README.md`: estrutura, execução e importância;
- `prompt-enriquecido.md`: explicação aprofundada;
- `history.md`: contexto histórico e divergências antigas;
- `AGENTS.md`: orientações curtas para agentes.
