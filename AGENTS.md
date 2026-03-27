# AGENTS.md

## Visão Geral

Este repositório reúne exercícios e exemplos da disciplina de Prompt
Engineering. A raiz funciona como guia de navegação do curso, enquanto alguns
capítulos têm instruções mais específicas em `AGENTS.md` próprios.

## Tecnologias Principais

| Categoria            | Tecnologia            | Evidência                                        | Uso                        |
| -------------------- | --------------------- | ------------------------------------------------ | -------------------------- |
| Runtime              | Python                | `requirements.txt`                               | scripts e exemplos         |
| Framework LLM        | LangChain             | `requirements.txt`, capítulos `1`, `5`, `6`, `7` | prompts e workflows        |
| Observabilidade      | LangSmith, Langfuse   | `requirements.txt`, `7-evaluation/`              | avaliação                  |
| Output/CLI           | Rich, PyYAML, pytest  | `requirements.txt`                               | terminal, prompts e testes |
| Materiais auxiliares | `skills/`, `TOSTUDY/` | árvore do repositório                            | conteúdo complementar      |

## Estrutura do Repositório

- `1-tipos-de-prompts/`: técnicas fundamentais de prompting.
- `3-estrutura-basica-dos-prompts/`: estruturação base de prompts.
- `4-prompts-e-workflow-de-agentes/`: workflows e agentes.
- `5-gerenciamento-e-versionamento-de-prompts/`: versionamento e testes de prompts.
- `6-prompt-enriquecido/`: técnicas de enriquecimento.
- `7-evaluation/`: evaluation com LangSmith e Langfuse.
- `skills/`: skills do ecossistema Codex/Gemini usadas como material do curso.
- `venv/`: ambiente virtual local da raiz; não editar nem versionar conteúdo interno.
- `.env.example`: template de variáveis de ambiente compartilhadas na raiz.

## Setup da Raiz

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

- A raiz possui `requirements.txt` e `.env.example`.
- Nem todo capítulo usa exatamente as dependências da raiz.
- Quando existir `requirements.txt` próprio em um capítulo, ele prevalece para aquele escopo.

## Padrões Gerais do Curso

- Trate a raiz como índice do curso; não imponha abstrações compartilhadas sem necessidade.
- Preserve a numeração das aulas e os nomes dos exemplos.
- Cada capítulo tende a ser autocontido em setup, `.env` e fluxo de execução.
- Se um capítulo já tiver `AGENTS.md` próprio, siga o arquivo do capítulo ao trabalhar dentro dele.
- Não edite `venv/` nem `.pytest_cache/`.
- Se adicionar variáveis de ambiente, atualize `.env.example` ou o `.env.example` do capítulo correspondente.
- Materiais e mensagens voltados ao curso devem permanecer em pt-BR.

## Navegação por Capítulo

### Capítulo 1: Tipos de Prompts

Evidência principal: `1-tipos-de-prompts/examples/`, `1-tipos-de-prompts/generic/`, `1-tipos-de-prompts/utils.py`.

Setup observado no material anterior:

```bash
cd .\1-tipos-de-prompts\
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Dependências relevantes já documentadas anteriormente:

- `langchain==0.3.27`
- `langchain-openai==0.3.32`
- `openai==1.102.0`
- `rich==14.1.0`
- `python-dotenv==1.1.1`

Exemplos importantes:

```bash
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

Notas úteis:

- `utils.py` é o utilitário compartilhado de saída formatada com Rich.
- O capítulo contém variantes `examples/` e `generic/`; não assuma que só uma delas é a fonte de verdade sem verificar o contexto da tarefa.
- `7-Prompt-channing.py` gera `prompt_chaining_result.md`.

### Capítulo 4: Prompts e Workflow de Agentes

Evidência principal: `4-prompts-e-workflow-de-agentes/agents/`, `4-prompts-e-workflow-de-agentes/commands/`, `4-prompts-e-workflow-de-agentes/AGENTS.md`.

Características observadas:

- Não há entrypoint Python única observada na raiz do capítulo.
- A pasta funciona como material de referência, prompts e templates de workflows.
- `agents/` contém agentes especializados para análise de código.
- `commands/` contém comandos de orquestração.

Ao trabalhar nesse capítulo:

- Leia primeiro o `AGENTS.md` local.
- Preserve a separação entre agentes e comandos.
- Não invente um fluxo executável único se a pasta estiver sendo usada como referência textual.

### Capítulo 5: Gerenciamento e Versionamento de Prompts

Setup já documentado anteriormente:

```bash
cd .\5-gerenciamento-e-versionamento-de-prompts\
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Variáveis de ambiente úteis já registradas:

```env
OPENAI_API_KEY=
LANGCHAIN_TRACING_V2=false
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your-langsmith-key-here
LANGCHAIN_PROJECT=prompt-management-system
```

Dependências relevantes preservadas da versão anterior:

- `langchain==1.0.0a5`
- `langchain-core==0.3.76`
- `langchain-openai==0.3.33`
- `langgraph==0.6.7`
- `langgraph-prebuilt==0.6.4`
- `langsmith==0.4.29`
- `pytest==8.3.4`
- `Jinja2==3.1.6`

Comandos úteis:

```bash
python .\src\agent_code_reviewer.py
python .\src\agent_pull_request.py
pytest .\tests\test_prompts.py -v
pytest .\tests\ -v
pytest -k "test_name" -v
```

Estrutura importante:

- `src/`: agentes para code review e criação de PRs.
- `tests/`: validação de prompts baseada em pytest.
- `prompts/`: armazenamento versionado de prompts e artefatos YAML/JSON.

### Capítulo 6: Prompt Enriquecido

Setup já documentado anteriormente:

```bash
cd .\6-prompt-enriquecido\
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Dependências relevantes preservadas:

- `langchain==1.0.0a5`
- `langchain-core==0.3.76`
- `langchain-openai==0.3.33`
- `langgraph==0.6.7`
- `langsmith==0.4.29`
- `openai==1.108.0`
- `pytest==8.3.4`

Scripts observados:

```bash
python .\0-No-expansion.py
python .\1-ITER_RETGEN.py
python .\2-query-enrichment.py
```

Notas úteis:

- O capítulo foca em expansão de consulta e enriquecimento contextual.
- A versão anterior também mencionava `repo_langchain_1.0/` como recurso adicional; trate isso como material auxiliar quando presente no capítulo ou em documentação relacionada.

### Capítulo 7: Evaluation

Setup já documentado anteriormente:

```bash
cd .\7-evaluation\
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Variáveis de ambiente úteis já registradas:

```env
LANGSMITH_API_KEY=
LANGCHAIN_TRACING_V2=true
OPENAI_API_KEY=
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0
LANGFUSE_SECRET_KEY=
LANGFUSE_PUBLIC_KEY=
LANGFUSE_HOST=http://localhost:3000
```

Dependências relevantes preservadas:

- `langchain==0.3.27`
- `langchain-openai==0.3.34`
- `langsmith==0.4.32`
- `langfuse==3.6.1`
- `openevals==0.1.0`

Arquitetura utilitária já documentada:

- `shared/clients.py`: clientes LLM e observabilidade.
- `shared/prompts.py`: carregamento e execução de prompts YAML.
- `shared/datasets.py`: upload de datasets com metadata.
- `shared/evaluators.py`: helpers para `prepare_data`.
- `shared/parsers.py`: parsing de JSON com remoção de markdown.

Fluxos úteis:

```bash
python .\1-basic\1-format-eval.py
python .\2-precision\1-conservative-high-precision.py

cd .\3-pairwise
python .\upload_dataset.py
python .\create_prompts.py
python .\run.py

cd ..\4-pairwise-doc
python .\upload_dataset.py
python .\create_prompt.py
python .\run.py

cd ..\5-langfuse
python .\upload_dataset.py
python .\create_prompts.py
python .\run.py
```

## Diferenças Importantes Entre Capítulos

- Capítulos `1` e `7`: baseados em LangChain `0.3.x`, mais próximos de exemplos introdutórios e evaluation.
- Capítulos `5` e `6`: usam stack mais nova com LangGraph e fluxo mais orientado a engenharia de prompts.
- Capítulo `4`: material de workflow e orquestração, com peso maior em arquivos de referência do que em scripts únicos de execução.

## Arquivos e Saídas Relevantes

- Capítulo 1: `prompt_chaining_result.md` pode ser gerado por `7-Prompt-channing.py`.
- Capítulo 5: artefatos `.json` e `.yaml` em `prompts/` são parte do fluxo de versionamento.

## Peculiaridades do Projeto

- O repositório tem formato de curso e evolui por capítulos, não por uma aplicação única.
- Há mistura de conteúdo didático, workflows de agentes e skills exportadas.
- O histórico recente mostra evolução contínua do material, com capítulos novos e reestruturações.
