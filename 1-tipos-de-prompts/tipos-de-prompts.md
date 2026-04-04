# Capítulo 1: Tipos de Prompts

Este capítulo apresenta o conjunto base de técnicas de prompt engineering usado ao longo do restante do curso. A ideia central é simples: cada técnica aumenta o nível de controle sobre a resposta do modelo por um mecanismo diferente.

## Progressão conceitual do capítulo

O capítulo parte de técnicas simples, como `Role Prompting` e `Zero-shot`, e avança até estruturas mais elaboradas, como `Tree of Thought`, `ReAct`, `Prompt Chaining` e `Least-to-Most`.

Em termos pedagógicos, a progressão faz sentido porque cada técnica introduz um novo tipo de controle:

- definir papel e contexto;
- fornecer ou não exemplos;
- tornar o raciocínio intermediário mais explícito;
- explorar múltiplos caminhos antes de decidir;
- encadear etapas;
- decompor problemas maiores em partes menores.

## Mapa conceitual das técnicas

| Técnica | Mecanismo principal | Quando tende a ajudar |
| --- | --- | --- |
| Role Prompting | define papel, especialidade, tom ou contexto | quando a resposta depende muito de perspectiva ou público |
| Zero-shot | usa apenas instrução, sem exemplos | quando a tarefa é simples ou barata de testar |
| One-shot / Few-shot | ensina por demonstração | quando formato e padrão importam |
| Chain of Thought | explicita raciocínio passo a passo | quando há lógica intermediária ou auditoria |
| Self-Consistency | compara múltiplas cadeias de raciocínio | quando existe resposta objetiva e alta variância |
| Tree of Thought | explora alternativas em árvore | quando há trade-offs e múltiplos caminhos plausíveis |
| Skeleton of Thought | estrutura antes de expandir | quando a resposta longa precisa de organização |
| ReAct | alterna raciocínio, ação e observação | quando a tarefa exige investigação iterativa |
| Prompt Chaining | divide a solução em etapas sequenciais | quando há pipeline natural com saídas intermediárias |
| Least-to-Most | resolve do mais simples ao mais complexo | quando a decomposição progressiva ajuda o modelo |

## Como pensar a escolha de técnica

Há quatro perguntas úteis antes de escolher uma abordagem:

1. A tarefa precisa de contexto ou persona específica?
2. O formato da saída pode ser aprendido só por instrução, ou precisa de exemplos?
3. O problema exige raciocínio intermediário auditável?
4. A solução precisa ser linear, em árvore ou em várias etapas encadeadas?

Essas perguntas não substituem experimento, mas ajudam a evitar dois erros comuns:

- usar técnicas complexas demais para tarefas simples;
- pedir raciocínio detalhado quando o ganho real é pequeno diante do custo.

## Técnicas baseadas em instrução e exemplo

### Role Prompting

Define papel, persona, tom ou especialidade do modelo antes da tarefa principal.

Funciona melhor quando a perspectiva muda a qualidade da resposta, como em docência, revisão técnica, atendimento ou análise de arquitetura. O ganho costuma estar menos em "dar inteligência" ao modelo e mais em reduzir ambiguidade de contexto.

Quando usar:

- para ajustar tom, profundidade técnica ou público-alvo;
- para manter respostas consistentes em agentes com persona fixa;
- para reduzir ambiguidades de contexto;
- para simular papéis distintos em revisão, suporte, ensino ou análise.

Limitações:

- o papel pode perder força em interações longas;
- instruções posteriores podem sobrescrever a persona inicial;
- em tarefas simples, o ganho pode não compensar o custo extra de tokens.

### Zero-shot

Executa a tarefa sem exemplos, confiando apenas na instrução e no conhecimento prévio do modelo.

É o melhor ponto de partida quando a tarefa já é bem conhecida pelo modelo e quando custo e latência importam. Também é a forma mais clara de medir a capacidade base do modelo para aquele problema.

Quando usar:

- para tarefas simples, diretas ou muito conhecidas pelo modelo;
- quando latência e custo importam;
- para medir a capacidade base do modelo;
- para resumos, classificações, explicações curtas e tarefas similares.

Limitações:

- oferece menos controle sobre formato e estilo;
- tende a oscilar mais em tarefas complexas;
- pequenas mudanças no enunciado podem alterar bastante o resultado.

### One-shot / Few-shot

Ensina o padrão esperado com um ou mais exemplos.

É útil quando o modelo precisa aprender formato, tom ou regra de classificação por demonstração. O risco aqui é confundir o modelo com exemplos ruins, excessivos ou inconsistentes.

Quando usar:

- quando o formato da saída precisa ser aprendido por demonstração;
- quando a tarefa depende de padronização de estilo ou classificação;
- quando você quer reduzir variação entre respostas.

Limitações:

- a qualidade depende fortemente da qualidade dos exemplos;
- o custo em tokens cresce rápido;
- exemplos excessivos ou conflitantes podem introduzir ambiguidade.

## Técnicas baseadas em raciocínio explícito

### Chain of Thought

Pede raciocínio passo a passo para melhorar tarefas com lógica intermediária.

É valioso quando o problema tem dependências internas, cálculo, comparação ou planejamento. Em contrapartida, aumenta custo e latência e pode produzir explicações convincentes, mas erradas.

Quando usar:

- em problemas com decomposição lógica, cálculo ou análise intermediária;
- quando o processo precisa ser auditável;
- quando o modelo tende a errar por pular etapas.

Limitações:

- aumenta custo, latência e tamanho da resposta;
- o raciocínio pode parecer convincente e ainda assim estar errado;
- em tarefas simples, o benefício costuma ser pequeno.

### Self-Consistency

Gera várias amostras de raciocínio e escolhe a resposta mais consistente.

O objetivo não é "pensar melhor" em abstrato, e sim reduzir variância quando uma cadeia única oscila demais. É especialmente útil em lógica e matemática, desde que exista um critério claro para extrair e comparar respostas finais.

Quando usar:

- quando a tarefa tem resposta objetiva e você quer mais confiança;
- quando uma cadeia única oscila demais entre execuções;
- quando faz sentido comparar caminhos alternativos e votar na saída final.

Limitações:

- multiplica custo e latência;
- não garante correção;
- exige um marcador ou critério claro para extrair a resposta final.

## Técnicas baseadas em exploração estruturada

### Tree of Thought

Explora caminhos alternativos como ramos de decisão antes de escolher uma solução.

Essa técnica é indicada quando há múltiplas alternativas plausíveis e trade-offs relevantes. Sem critérios explícitos de avaliação, porém, a árvore vira apenas brainstorming mais caro.

Quando usar:

- quando há várias alternativas plausíveis com trade-offs relevantes;
- para brainstorming com seleção estruturada;
- para comparar estratégias, arquiteturas ou decisões técnicas.

Limitações:

- é mais caro e mais lento do que uma cadeia linear;
- depende de critérios de avaliação bem definidos;
- pode virar complexidade desnecessária em problemas pequenos.

### Skeleton of Thought

Cria um esqueleto inicial da resposta e expande depois.

É uma técnica de estruturação, não apenas de raciocínio. Ajuda principalmente em documentos longos, respostas compostas ou materiais que exigem coerência entre seções.

Quando usar:

- em respostas longas que precisam de organização;
- para artigos, ADRs, planos, checklists e documentação;
- quando você quer controlar a estrutura antes de detalhar.

Limitações:

- um esqueleto ruim leva a uma expansão ruim;
- há mais custo e latência por envolver múltiplas etapas;
- tópicos ambíguos podem degradar a expansão final.

## Técnicas baseadas em orquestração

### ReAct

Alterna raciocínio, ação e observação em ciclos sucessivos.

É apropriada quando o agente precisa investigar, testar hipótese, observar evidência e então ajustar o próximo passo. O principal risco é simular ações ou observações que não ocorreram de fato.

Quando usar:

- em tarefas de investigação, verificação ou depuração;
- quando o problema depende de evidências intermediárias;
- quando é útil separar hipótese, ação e observação.

Limitações:

- consome muitos tokens;
- pode gerar respostas verbosas;
- sem controle adequado, o modelo pode simular ações ou observações inexistentes.

### Prompt Chaining

Divide um problema em múltiplas etapas sequenciais, em que a saída de uma etapa alimenta a próxima.

Ajuda quando há fases naturalmente distintas, como extrair, estruturar, gerar e revisar. O ponto crítico é padronizar a saída intermediária para evitar propagação de erro.

Quando usar:

- quando a tarefa já tem pipeline natural com fases distintas;
- quando etapas diferentes pedem prompts ou modelos diferentes;
- quando a saída intermediária precisa ser auditável.

Limitações:

- aumenta latência e custo;
- erros podem se propagar pela cadeia;
- parsing ruim entre etapas quebra o fluxo.

### Least-to-Most

Resolve o problema do mais simples para o mais complexo, acumulando contexto progressivamente.

É especialmente útil quando uma resolução direta falha porque o problema é grande demais ou exige dependências progressivas entre subproblemas.

Quando usar:

- quando o problema é grande demais para ser resolvido corretamente de uma vez;
- quando há dependência natural entre etapas de complexidade crescente;
- quando faz sentido construir contexto progressivamente.

Limitações:

- a decomposição inicial pode sair ruim;
- erros nas primeiras etapas contaminam as seguintes;
- pode ser excessivo para tarefas pequenas.

## Critérios práticos de comparação

As técnicas podem ser comparadas por cinco dimensões recorrentes:

- custo em tokens;
- latência;
- facilidade de auditoria;
- robustez a tarefas complexas;
- necessidade de estruturação explícita.

Não existe técnica universalmente melhor. Em produção, muitas vezes a melhor escolha é a técnica mais simples que ainda entrega qualidade suficiente.

## Síntese

- role e zero-shot aumentam controle com baixo overhead;
- few-shot aumenta aderência a padrões;
- CoT e self-consistency aumentam auditabilidade e robustez em raciocínio;
- ToT, SoT, ReAct, chaining e least-to-most entram quando o problema exige estrutura mais forte;
- o segredo do capítulo não é decorar nomes, e sim entender qual mecanismo cada técnica adiciona.
