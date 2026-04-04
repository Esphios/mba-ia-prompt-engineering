# Curso de Prompt Engineering

Este repositório reúne os materiais da disciplina de Prompt Engineering do MBA em Engenharia de Software com IA. A raiz funciona como índice do curso: ela explica a organização geral, aponta o papel de cada capítulo e orienta como navegar entre teoria, exemplos e workflows.

## Como a documentação está organizada

Cada capítulo deve seguir a mesma lógica documental:

- `README.md`: visão geral do capítulo, estrutura da pasta, como estudar e como executar o que existir ali.
- `AGENTS.md`: orientações curtas para agentes de IA que forem editar ou analisar aquele capítulo.
- arquivo principal da aula: explicação aprofundada dos conceitos do capítulo.
- `history.md`: contexto removido, decisões editoriais, nomenclaturas antigas e informações preservadas por rastreabilidade.

Os nomes dos arquivos de aula variam por capítulo, por exemplo:

- `1-tipos-de-prompts/tipos-de-prompts.md`
- `2-conceitos-importantes/conceitos-importantes.md`
- `3-estrutura-basica-dos-prompts/estrutura-basica-dos-prompts.md`
- `4-prompts-e-workflow-de-agentes/prompts-e-workflow-de-agentes.md`
- `5-gerenciamento-e-versionamento-de-prompts/gerenciamento-e-versionamento-de-prompts.md`
- `6-prompt-enriquecido/prompt-enriquecido.md`

## Estrutura do curso

| Capítulo | Foco | Arquivo principal |
| --- | --- | --- |
| `1-tipos-de-prompts/` | técnicas clássicas de prompting | `tipos-de-prompts.md` |
| `2-conceitos-importantes/` | contexto, custo, latência, cache e batch | `conceitos-importantes.md` |
| `3-estrutura-basica-dos-prompts/` | estruturação profissional de prompts | `estrutura-basica-dos-prompts.md` |
| `4-prompts-e-workflow-de-agentes/` | prompts especificados como workflow multiagente | `prompts-e-workflow-de-agentes.md` |
| `5-gerenciamento-e-versionamento-de-prompts/` | versionamento, registry, testes e LangSmith | `gerenciamento-e-versionamento-de-prompts.md` |
| `6-prompt-enriquecido/` | query enrichment e expansão iterativa | `prompt-enriquecido.md` |
| `7-evaluation/` | avaliação com LangSmith e Langfuse | material próprio do capítulo |

Pastas auxiliares relevantes:

- `skills/`: skills usadas como material complementar do curso.
- `TOSTUDY/`: materiais auxiliares de estudo.
- `venv/`: ambiente local da raiz; não editar nem versionar conteúdo interno.

## Como estudar

O fluxo recomendado é:

1. Ler o `README.md` do capítulo para entender escopo e estrutura.
2. Ler o arquivo principal da aula para estudar o conteúdo em profundidade.
3. Consultar `history.md` apenas quando precisar de contexto removido, decisões editoriais ou nomenclaturas antigas.
4. Executar exemplos e scripts do capítulo quando fizer sentido.

## Setup da raiz

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Observações:

- a raiz tem `requirements.txt` e `.env.example`, mas vários capítulos são autocontidos;
- quando um capítulo tiver `requirements.txt` próprio, ele prevalece dentro daquele escopo;
- se um capítulo tiver `.env.example` próprio, use o arquivo local em vez do da raiz.

## Tecnologias principais

| Categoria | Tecnologia | Uso no repositório |
| --- | --- | --- |
| Runtime | Python | scripts, exemplos e utilitários |
| Orquestração LLM | LangChain, LangGraph | capítulos `1`, `5`, `6` e `7` |
| Observabilidade | LangSmith, Langfuse | capítulos `5` e `7` |
| CLI e suporte | Rich, PyYAML, pytest | saída formatada, configuração e testes |

## Regras gerais do repositório

- Preserve a numeração dos capítulos e os nomes dos exemplos.
- Não imponha abstrações compartilhadas sem evidência de que o curso realmente precisa disso.
- Não edite `venv/` nem `.pytest_cache/`.
- Se adicionar variáveis de ambiente, atualize o `.env.example` correspondente.
- Materiais voltados ao curso devem permanecer em pt-BR.

## Importância da raiz

O objetivo da documentação da raiz não é repetir o conteúdo de cada aula em profundidade. Ela existe para manter o curso navegável, consistente e sustentável conforme novos capítulos, exemplos e skills forem sendo adicionados.
