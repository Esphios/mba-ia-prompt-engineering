# Capítulo 5: Gerenciamento e Versionamento de Prompts

Este capítulo discute prompt como ativo versionável de engenharia. Ele é importante porque conecta autoria de prompts, registry local, testes, colaboração em equipe e integração com plataforma externa.

## Estrutura da pasta

| Caminho | Papel |
| --- | --- |
| `gerenciamento-e-versionamento-de-prompts.md` | aula principal do capítulo |
| `history.md` | memória editorial, contexto removido e decisões de organização |
| `src/` | implementação dos agentes e utilitários de registry/LangSmith |
| `prompts/` | prompts versionados e registry YAML |
| `tests/` | validação automatizada dos prompts |
| `AGENTS.md` | orientações curtas para agentes |

## O que estudar aqui

O capítulo aprofunda:

- diferença entre prompts de produtividade e prompts de produção;
- versionamento com Git;
- organização de repositório de prompts;
- registry local com YAML;
- testes e validação;
- push e pull de prompts com LangSmith.

Para a explicação completa, leia `gerenciamento-e-versionamento-de-prompts.md`.

## Como executar

```powershell
python .\src\agent_code_reviewer.py
python .\src\agent_pull_request.py
python .\src\langsmith_push.py
pytest .\tests\test_prompts.py -v
```

## Setup local

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Variáveis de ambiente mais importantes:

```env
OPENAI_API_KEY=
LANGCHAIN_TRACING_V2=false
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=
LANGCHAIN_PROJECT=prompt-management-system
```

## Importância do capítulo

Este é o capítulo que transforma prompt em artefato com ciclo de vida. Sem ele, o curso explicaria como escrever prompts, mas não como manter, testar e promover versões de forma disciplinada.
