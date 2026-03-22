# Tipos de Prompt - Versões Genéricas

Esta pasta reúne versões genéricas das técnicas apresentadas no capítulo 1. Os scripts foram pensados para reaproveitamento com tarefas diferentes, com menos acoplamento aos exemplos originais e com uma implementação mais fiel quando a técnica exige múltiplas etapas.

## Visão geral

| Tipo                       | Script                           |
| -------------------------- | -------------------------------- |
| Role Prompting             | `0-role-prompting.py`            |
| Zero-shot                  | `1-zero-shot.py`                 |
| One-shot / Few-shot        | `2-one-few-shot.py`              |
| Chain of Thought           | `3-cot.py`                       |
| Self-Consistency           | `3.1-self-consistency.py`        |
| Tree of Thought            | `4-tot.py`                       |
| Skeleton of Thought        | `5-sot.py`                       |
| ReAct                      | `6-react.py`                     |
| Prompt Chaining            | `7-prompt-chaining.py`           |
| Least-to-Most              | `8-least-to-most.py`             |
| Runner                     | `prompt_runner.py`               |
| Sugeridor                  | `suggest_prompt_technique.py`    |
| Utilitários compartilhados | `common.py`, `prompt_advisor.py` |

## Como usar

### 1. Executar um script diretamente

```powershell
.\venv\Scripts\python.exe .\1-tipos-de-prompts\generic\1-zero-shot.py `
  --task "Explique recursão em termos simples."
```

### 2. Executar via runner

```powershell
.\venv\Scripts\python.exe .\1-tipos-de-prompts\generic\prompt_runner.py run `
  --technique zero-shot `
  --task "Explique recursão em termos simples."
```

### 3. Pedir sugestões antes de rodar

```powershell
.\venv\Scripts\python.exe .\1-tipos-de-prompts\generic\suggest_prompt_technique.py `
  --task "Preciso comparar três arquiteturas para um serviço com alto volume e escolher a melhor."
```

### 4. Pedir sugestões pelo runner

```powershell
.\venv\Scripts\python.exe .\1-tipos-de-prompts\generic\prompt_runner.py suggest `
  --task "Preciso depurar uma API e analisar evidências passo a passo."
```

### 5. Listar as técnicas disponíveis

```powershell
.\venv\Scripts\python.exe .\1-tipos-de-prompts\generic\prompt_runner.py list
```

## Princípios gerais

Os pontos abaixo vieram do material original e valem para todas as técnicas:

- Seja intencional: antes de escolher a técnica, defina contexto, saída desejada e como a resposta será auditada.
- Nem toda tarefa precisa raciocínio detalhado. Pedir passo a passo em excesso aumenta custo e latência.
- Em cenários de alta escala, técnicas mais simples como zero-shot costumam ser preferíveis quando a tarefa permite.
- A escolha do modelo muda bastante o comportamento, o custo em tokens, a latência e o ganho real de cada técnica.
- Mais exemplos não significa automaticamente melhor resultado. Muitos exemplos podem introduzir ambiguidade.
- Quando a saída de uma etapa alimenta outra, estrutura e parsing deixam de ser detalhe e passam a ser requisito.
- A IA ainda pode errar ou alucinar. O trabalho de refinar o prompt continua sendo parte central do resultado.

## Argumentos mais usados por script

| Script                    | Argumentos principais                                                                                                                     |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `0-role-prompting.py`     | `--task`, `--task-file`, `--role`, `--role-file`, `--model`, `--temperature`                                                              |
| `1-zero-shot.py`          | `--task`, `--task-file`, `--model`, `--temperature`                                                                                       |
| `2-one-few-shot.py`       | `--task`, `--task-file`, `--instruction`, `--example`, `--example-file`, `--model`, `--temperature`                                       |
| `3-cot.py`                | `--task`, `--task-file`, `--answer-label`, `--model`, `--temperature`                                                                     |
| `3.1-self-consistency.py` | `--task`, `--task-file`, `--samples`, `--answer-label`, `--model`, `--temperature`                                                        |
| `4-tot.py`                | `--problem`, `--problem-file`, `--criterion`, `--max-depth`, `--branch-factor`, `--beam-width`, `--finalists`, `--model`, `--temperature` |
| `5-sot.py`                | `--task`, `--task-file`, `--bullet-range`, `--model`, `--temperature`                                                                     |
| `6-react.py`              | `--task`, `--task-file`, `--context`, `--context-file`, `--model`, `--temperature`                                                        |
| `7-prompt-chaining.py`    | `--task`, `--task-file`, `--step`, `--step-model`, `--output-file`, `--temperature`                                                       |
| `8-least-to-most.py`      | `--task`, `--task-file`, `--model`, `--temperature`                                                                                       |

## 0. Role Prompting

**Script equivalente:** `0-role-prompting.py`

**Nome:** Role Prompting

**Descrição:** define explicitamente o papel, a persona, o contexto ou o estilo que o modelo deve assumir antes de responder.

**Quando utilizar**

- Quando você precisa ajustar tom, profundidade técnica ou público-alvo.
- Quando deseja respostas consistentes em um agente com persona fixa.
- Quando quer reduzir ambiguidades de contexto, como "Go" linguagem versus verbo.
- Quando precisa simular papéis distintos em revisão de arquitetura, suporte ou ensino.

**Limitações**

- O papel pode perder força ao longo de conversas longas.
- Instruções posteriores podem sobrescrever a persona inicial.
- Em tarefas simples, o ganho pode não justificar o custo adicional de tokens.
- Em modelos mais fortes, o contraste entre usar ou não role prompting pode ser pequeno.

**Exemplos (pseudo-código)**

```text
system = "Você é um professor universitário de computação, técnico e objetivo."
user = "Explique recursão em 50 palavras."
response = llm(system, user)
```

```text
role = "Você é um revisor de código pragmático e rigoroso."
task = "Analise este diff e aponte regressões."
response = llm(role, task)
```

**Cuidados:** role prompting não precisa ficar apenas no `system prompt`, embora isso seja comum. O importante é definir um papel que realmente ajude a tarefa. Em modelos menores, o impacto costuma ser mais perceptível do que em modelos mais fortes.

## 1. Zero-shot

**Script equivalente:** `1-zero-shot.py`

**Nome:** Zero-shot Prompting

**Descrição:** o modelo recebe apenas a instrução da tarefa, sem exemplos demonstrando como responder.

**Quando utilizar**

- Quando a tarefa é simples, direta ou muito conhecida pelo modelo.
- Quando latência e custo importam e você quer prompts menores.
- Quando deseja testar a capacidade base de generalização do modelo.
- Quando precisa de respostas rápidas para resumo, tradução, classificação ou explicação curta.

**Limitações**

- Oferece pouco controle sobre formato e estilo da saída.
- Pode falhar com mais frequência em tarefas complexas.
- Pequenas mudanças no enunciado podem alterar bastante o resultado.
- A escolha do modelo e da temperatura influencia bastante o comportamento.

**Exemplos (pseudo-código)**

```text
prompt = "Qual é a capital do Brasil? Responda apenas com o nome da cidade."
response = llm(prompt)
```

```text
prompt = "Descubra a intenção do usuário: 'Estou procurando um restaurante japonês perto de São Paulo.'"
response = llm(prompt)
```

**Cuidados:** zero-shot é definido pela ausência de exemplos, não pelo tamanho do prompt. Você pode escrever um prompt longo e ainda assim continuar em zero-shot. Para produção em escala, costuma ser um ótimo ponto de partida.

## 2. One-shot / Few-shot

**Script equivalente:** `2-one-few-shot.py`

**Nome:** One-shot / Few-shot Prompting

**Descrição:** a tarefa é acompanhada de um ou mais exemplos para ensinar ao modelo o padrão esperado de entrada e saída.

**Quando utilizar**

- Quando o modelo precisa aprender um formato de resposta específico.
- Quando a tarefa depende de padronização de estilo, classificação ou template.
- Quando você quer reduzir variação entre respostas.
- Quando o padrão fica mais claro por demonstração do que por instrução abstrata.

**Limitações**

- A qualidade final depende fortemente da qualidade dos exemplos.
- O custo de tokens sobe com facilidade.
- Exemplos muito rígidos podem enviesar demais a resposta.
- Muitos exemplos também podem introduzir ambiguidade em vez de clareza.

**Exemplos (pseudo-código)**

```text
instruction = "Use os exemplos para inferir o padrão esperado."
examples = [
  "Input: 'Database connection lost' -> Output: ERROR",
  "Input: 'Disk usage at 85%' -> Output: WARNING"
]
task = "Input: 'CPU usage at 95%' -> Output:"
response = llm(instruction + examples + task)
```

```text
example = "Pergunta: Capital da França\nResposta: Paris"
task = "Pergunta: Capital do Japão\nResposta:"
response = llm(example + task)
```

**Cuidados:** mais exemplos nem sempre significam melhor qualidade. Se você fornecer exemplos demais, com sinais conflitantes, o modelo pode oscilar mais entre execuções.

## 3. Chain of Thought

**Script equivalente:** `3-cot.py`

**Nome:** Chain of Thought (CoT)

**Descrição:** instrui o modelo a raciocinar passo a passo antes de apresentar a resposta final.

**Quando utilizar**

- Quando o problema exige decomposição lógica, cálculo ou análise intermediária.
- Quando você quer auditar como o modelo chegou à conclusão.
- Quando o modelo erra por pular etapas.
- Quando a tarefa envolve investigação, comparação ou planejamento.

**Limitações**

- Aumenta custo, latência e tamanho da resposta.
- O raciocínio pode soar convincente e ainda assim estar errado.
- Em tarefas simples, o benefício costuma ser pequeno.
- Modelos de reasoning já podem gastar muitos tokens internamente mesmo sem expor o passo a passo.

**Exemplos (pseudo-código)**

```text
prompt = """
Resolva a tarefa abaixo.
Pense passo a passo.
Ao final, escreva a resposta depois de 'Answer:'.
"""
response = llm(prompt + task)
```

```text
task = "Se uma API recebe 200 req/s e cada instância suporta 50 req/s, quantas instâncias são necessárias?"
response = llm("Raciocine passo a passo e finalize com 'Answer:'" + task)
```

**Cuidados:** use CoT quando realmente houver algo para auditar. Em alta escala, pedir passo a passo para tudo costuma ser desperdício.

## 3.1 Self-Consistency

**Script equivalente:** `3.1-self-consistency.py`

**Nome:** Self-Consistency

**Descrição:** executa múltiplas amostras independentes de raciocínio e escolhe a resposta mais consistente entre elas.

**Quando utilizar**

- Quando a tarefa tem resposta objetiva e você quer mais confiança.
- Quando uma única cadeia de raciocínio oscila muito entre execuções.
- Quando faz sentido comparar caminhos alternativos e votar na saída final.
- Quando o problema envolve lógica, matemática ou análise objetiva.

**Limitações**

- Multiplica custo e latência.
- Nem sempre converge para a resposta correta.
- Pode repetir respostas redundantes.
- Exige um marcador claro para extrair a resposta final.

**Exemplos (pseudo-código)**

```text
answers = []
repeat 5 times:
  sample = llm("Resolva passo a passo e finalize com 'Answer:'")
  answers.append(extract_final_answer(sample))
final = majority_vote(answers)
```

```text
task = "Quantas queries existem em um padrão N+1 com 100 usuários?"
final = vote(run_multiple_reasoning_paths(task))
```

**Cuidados:** essa técnica é útil para reduzir variância, não para corrigir automaticamente um prompt ruim. Se o raciocínio base estiver enviesado, você pode apenas votar na resposta errada mais frequente.

## 4. Tree of Thought

**Script equivalente:** `4-tot.py`

**Nome:** Tree of Thought (ToT)

**Descrição:** explora alternativas em forma de árvore, avalia os ramos com critérios e escolhe uma decisão final.

**Quando utilizar**

- Quando há várias alternativas plausíveis e trade-offs relevantes.
- Quando o problema pede brainstorming com seleção da melhor opção.
- Quando você quer comparar estratégias, arquiteturas ou decisões técnicas.
- Quando uma resposta linear tende a ficar superficial.

**Limitações**

- É mais caro e mais lento do que CoT simples.
- Exige critérios de avaliação bem definidos.
- Os ramos podem acabar ficando parecidos demais.
- Pode virar complexidade desnecessária em problemas pequenos.

**Exemplos (pseudo-código)**

```text
candidates = generate_candidates(problem, n=3)
scored = evaluate_each(candidates, criteria)
best = select_top_k(scored, k=2)
children = expand(best)
winner = choose_finalist(children, criteria)
```

```text
problem = "Escolher arquitetura para um chatbot com 50 mil usuários por dia"
criteria = ["qualidade", "custo", "latência", "operação"]
decision = tree_search(problem, criteria)
```

**Cuidados:** o critério que define o "melhor" precisa estar explícito. Sem isso, o resultado vira apenas exploração de alternativas sem mecanismo claro de decisão.

## 5. Skeleton of Thought

**Script equivalente:** `5-sot.py`

**Nome:** Skeleton of Thought (SoT)

**Descrição:** primeiro produz um esqueleto enxuto da resposta e depois expande esse esqueleto em uma versão final.

**Quando utilizar**

- Quando você quer respostas longas mais organizadas.
- Quando precisa controlar a estrutura antes de detalhar o conteúdo.
- Quando a tarefa envolve artigos, ADRs, planos, checklists ou documentação.
- Quando deseja evitar que o modelo se perca em respostas extensas.

**Limitações**

- Um esqueleto ruim leva a uma expansão ruim.
- Se os tópicos forem ambíguos, a segunda etapa pode perder contexto.
- Introduz mais custo e mais latência.
- O modelo pode tentar pular direto para os detalhes se o prompt for frouxo.

**Exemplos (pseudo-código)**

```text
skeleton = llm("Crie apenas um esqueleto de 4 a 6 bullets")
final = llm("Expanda o esqueleto abaixo em uma resposta final" + skeleton)
```

```text
task = "Escreva uma ADR justificando PostgreSQL em vez de MongoDB"
outline = generate_outline(task)
answer = expand_outline(task, outline)
```

**Cuidados:** não é obrigatório exibir o esqueleto ao usuário, mas mostrá-lo ajuda tanto na auditoria quanto na própria expansão da resposta.

## 6. ReAct

**Script equivalente:** `6-react.py`

**Nome:** ReAct

**Descrição:** alterna ciclos de `Thought`, `Action` e `Observation`, permitindo investigação iterativa antes da conclusão.

**Quando utilizar**

- Quando a tarefa exige investigação, verificação ou depuração.
- Quando você quer explicitar o processo de decisão do agente.
- Quando o problema depende de observar evidências intermediárias.
- Quando faz sentido separar hipótese, ação concreta e observação obtida.

**Limitações**

- Consome muitos tokens e pode ficar lento.
- Pode gerar respostas longas e verbosas.
- O modelo pode simular ações inexistentes ou inventar observações.
- Em produção, exige mais cuidado com pontos de parada e ferramentas disponíveis.

**Exemplos (pseudo-código)**

```text
prompt = """
Use ReAct.
Alterne entre Thought, Action e Observation.
Não invente dados ausentes.
Finalize com 'Final Answer:'.
"""
response = llm(prompt + context + task)
```

```text
Thought: "Preciso comparar custo e tempo."
Action: "Avaliar a opção de voo."
Observation: "Custa 960 e leva cerca de 3 horas."
Final Answer: "Escolha o voo."
```

**Cuidados:** deixe claro de onde vêm as evidências e como o processo deve parar. Sem isso, o modelo pode entrar em loops desnecessários ou alucinar observações.

## 7. Prompt Chaining

**Script equivalente:** `7-prompt-chaining.py`

**Nome:** Prompt Chaining

**Descrição:** organiza a solução em etapas sequenciais, em que a saída de uma etapa se torna a entrada da próxima.

**Quando utilizar**

- Quando a tarefa tem pipeline natural com fases distintas.
- Quando você precisa extrair, estruturar, gerar e resumir em sequência.
- Quando etapas diferentes pedem prompts ou modelos diferentes.
- Quando a saída intermediária precisa ser auditável.

**Limitações**

- Aumenta latência e custo.
- Erros podem se propagar pela cadeia.
- Parsing ruim entre etapas quebra o fluxo.
- A orquestração fica mais complexa de manter.

**Exemplos (pseudo-código)**

```text
step1 = llm("Extraia os requisitos", input=task)
step2 = llm("Com base nos requisitos, proponha a solução", input=step1)
step3 = llm("Transforme a solução em plano de implementação", input=step2)
result = step3
```

```text
spec -> schema JSON -> rotas REST -> mensagem de commit
```

**Cuidados:** padronize bem a saída intermediária. Esse é o tipo de técnica em que usar modelos diferentes por etapa pode fazer muito sentido.

## 8. Least-to-Most

**Script equivalente:** `8-least-to-most.py`

**Nome:** Least-to-Most Prompting

**Descrição:** quebra um problema maior em subproblemas ordenados do mais simples para o mais complexo, resolvendo cada um com apoio dos anteriores.

**Quando utilizar**

- Quando o problema é grande demais para ser resolvido corretamente de uma vez.
- Quando existe dependência natural entre etapas de complexidade crescente.
- Quando você quer construir contexto progressivamente.
- Quando a tarefa envolve design, planejamento ou implementação de sistemas.

**Limitações**

- A decomposição inicial pode sair ruim.
- Erros nas primeiras etapas contaminam as seguintes.
- Exige mais chamadas e mais coordenação.
- Pode ser excessivo para tarefas pequenas.

**Exemplos (pseudo-código)**

```text
subproblems = llm("Quebre a tarefa do mais fácil para o mais difícil")
for each subproblem in subproblems:
  solution = llm("Resolva usando as respostas anteriores como contexto")
final = llm("Combine tudo em uma resposta integrada")
```

```text
task = "Projetar um encurtador de URL"
1. Definir requisitos
2. Definir modelo de dados
3. Definir API
4. Definir estratégia de escalabilidade
5. Consolidar arquitetura final
```

**Cuidados:** revise a decomposição antes de confiar na execução inteira. A técnica depende muito da qualidade da ordem proposta.

## Notas sobre estas versões

- `3.1-self-consistency.py` faz múltiplas amostras independentes e votação, em vez de apenas pedir para o modelo "simular" consistência.
- `4-tot.py` executa busca em árvore com geração, avaliação, expansão, beam pruning e decisão final.
- `5-sot.py` separa explicitamente esqueleto e expansão em duas chamadas.
- `7-prompt-chaining.py` executa etapas reais em sequência.
- `8-least-to-most.py` decompõe o problema e resolve os subproblemas iterativamente.
- `prompt_runner.py` serve como interface única para listar, sugerir e executar as técnicas.
- `suggest_prompt_technique.py` sugere técnica, parâmetros iniciais e comandos prontos para cada caso.
