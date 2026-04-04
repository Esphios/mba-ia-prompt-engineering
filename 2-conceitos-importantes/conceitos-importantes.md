# Capítulo 2: Conceitos Importantes para Prompt Engineering

## Visão geral

Antes de falar de técnicas de prompting, é importante entender alguns conceitos que afetam diretamente custo, latência, qualidade de resposta e arquitetura das aplicações com IA. Este capítulo revisita esses fundamentos para que decisões de prompt não sejam tomadas de forma ingênua.

O ponto central é simples: Prompt Engineering não é apenas escrever instruções para a IA. Também envolve entender limites do modelo, estratégias para lidar com contexto longo e formas de reduzir desperdício operacional.

## Exemplos deste capítulo

Os conceitos abaixo são acompanhados por scripts em `examples/`:

- `1-context-window-budget.py`
- `2-context-management-strategies.py`
- `3-cache-and-batch-patterns.py`
- `4-model-choice-tradeoffs.py`

Esses exemplos não chamam LLMs reais. Eles servem para tornar visível a lógica por trás de orçamento de contexto, truncamento, sumarização, cache, lote e escolha de modelo.

## 1. Por que esses conceitos importam

Quando você entende como o modelo consome contexto, reutiliza informação e responde em escala, muda a forma como você:

- escreve prompts;
- organiza conversas longas;
- escolhe entre modelos maiores ou menores;
- decide quando resumir, truncar ou cachear;
- estrutura fluxos em lote.

Esses conceitos valem tanto para produtividade no desenvolvimento quanto para agentes e aplicações em produção.

## 2. Janela de contexto

Janela de contexto é a quantidade de tokens que o modelo consegue considerar de uma vez para produzir a próxima resposta. Esses tokens podem vir de:

- mensagem de sistema;
- mensagem do usuário;
- respostas anteriores;
- documentos anexados;
- trechos de código;
- instruções adicionais inseridas pela aplicação.

Se o volume total ultrapassa o limite do modelo, parte da informação deixa de caber. Isso afeta diretamente a qualidade da resposta e impõe restrições reais sobre como arquitetar prompts, conversas e pipelines com IA.

### Por que isso importa

- Um prompt isolado pode ser pequeno, mas uma conversa longa pode estourar a janela.
- Um agente pode funcionar bem em tarefas curtas e falhar quando acumula contexto demais.
- Estratégias de sumarização, truncamento e janela deslizante existem justamente para lidar com esse limite.

Veja também: `examples/1-context-window-budget.py`.

## 3. Janela de contexto, memória, custo e latência

Quanto mais tokens entram no processamento, maior tende a ser:

- o uso de memória;
- o custo computacional;
- a latência da resposta.

Em termos práticos, mais contexto não é grátis. Mesmo quando o modelo consegue processar tudo, isso normalmente custa mais e demora mais.

Por isso, um dos objetivos do Prompt Engineering é buscar o melhor resultado possível sem inflar desnecessariamente a quantidade de tokens. O problema não é usar contexto, e sim usar contexto sem intenção.

## 4. Janela de contexto não é a mesma coisa que parâmetros

Esses conceitos costumam ser confundidos, mas são diferentes.

### Janela de contexto

É o quanto o modelo consegue processar simultaneamente em uma interação.

### Parâmetros

São os pesos do modelo, isto é, a estrutura interna que representa o que ele aprendeu no treinamento.

Em termos práticos:

- a janela de contexto define quanto cabe na conversa atual;
- os parâmetros definem a capacidade do modelo de representar padrões e conhecimento.

Um modelo pode ter muitos parâmetros e ainda assim uma janela de contexto menor. Também pode existir um modelo com janela grande, mas menos sofisticado em outros aspectos. Portanto, escolher um modelo exige olhar para o caso de uso, não apenas para um número isolado.

## 5. Truncamento

Truncamento é a estratégia de cortar partes do contexto quando ele fica grande demais.

Na prática, isso significa remover trechos de mensagem para fazer o conteúdo caber na janela disponível. Muitas vezes o corte ocorre nas partes mais antigas, mas essa não é a única possibilidade. Dependendo da estratégia, você pode preservar blocos obrigatórios e truncar apenas regiões menos relevantes.

### Vantagem

- É simples e barato de implementar.

### Risco

- O modelo perde parte do contexto original e pode passar a responder com menos coerência.

Truncar resolve o problema de espaço, mas não preserva necessariamente o significado do que foi perdido.

Veja também: `examples/2-context-management-strategies.py`.

## 6. Sumarização

Sumarização é uma alternativa ao truncamento puro. Em vez de simplesmente cortar o histórico, você pede a outro processo ou modelo que resuma o conteúdo anterior, liberando espaço na janela de contexto.

### Vantagens

- preserva melhor a linha geral da conversa;
- reduz o risco de perda total de contexto;
- pode ser reutilizada como memória de curto prazo.

### Limites

- um resumo sempre perde detalhes;
- um resumo ruim pode distorcer o que aconteceu antes;
- o prompt de sumarização também precisa ser bem pensado.

Na prática, a sumarização é muito útil, mas não elimina totalmente o risco de perda de nuance.

Veja também: `examples/2-context-management-strategies.py`.

## 7. Sliding Window

Sliding window, ou janela deslizante, é tratar o histórico como uma janela móvel. O sistema mantém dentro do contexto apenas a parte mais recente e vai deslocando essa janela conforme novos dados entram.

O que fica fora da janela pode:

- ser descartado;
- ser arquivado;
- ser resumido;
- ser armazenado para recuperação posterior.

Essa estratégia é comum quando o histórico cresce continuamente e não faz sentido manter tudo ativo ao mesmo tempo.

Veja também: `examples/2-context-management-strategies.py`.

## 8. Prompt Caching

Prompt caching é uma estratégia para evitar reprocessamento de partes do prompt que se repetem com frequência.

Isso importa porque muitos fluxos reutilizam blocos fixos, como:

- instruções de sistema;
- documentos base;
- políticas da empresa;
- schemas de saída;
- exemplos recorrentes.

Quando esse conteúdo pode ser reutilizado via cache, o sistema tende a:

- gastar menos;
- responder mais rápido;
- evitar trabalho repetido.

### Observação importante

Nem todo provedor trata cache da mesma forma. Alguns fazem isso automaticamente; outros exigem cache explícito. Em qualquer caso, a consequência para Prompt Engineering é a mesma: prompts recorrentes devem ser desenhados com intenção, e não montados de forma totalmente diferente a cada chamada.

Veja também: `examples/3-cache-and-batch-patterns.py`.

## 9. Batch Prompting

Batch prompting é a estratégia de enviar múltiplos itens semelhantes em uma mesma chamada, em vez de executar uma chamada por item.

Isso costuma fazer sentido quando:

- as tarefas são parecidas;
- o formato de resposta é o mesmo;
- o contexto geral compartilhado é útil para todos os itens;
- existe alto volume de processamento.

### Benefícios

- reduz overhead por requisição;
- melhora consistência entre respostas;
- pode reduzir custo total;
- pode aumentar throughput.

### Cuidados

- os itens do lote precisam ser compatíveis entre si;
- a resposta precisa ser fácil de mapear de volta para cada item;
- nem toda tarefa deve ser agrupada.

Se você mistura objetivos muito diferentes no mesmo lote, tende a aumentar ruído e ambiguidade.

Veja também: `examples/3-cache-and-batch-patterns.py`.

## 10. Pensar em Prompt Engineering de forma estratégica

Esses conceitos mostram que Prompt Engineering também envolve decisões de arquitetura e operação. Em muitos casos, o trabalho não é apenas escolher entre zero-shot ou few-shot, mas decidir:

- qual modelo usar;
- quanto contexto realmente vale a pena enviar;
- quando resumir;
- quando truncar;
- quando cachear;
- quando processar em lote.

Em outras palavras, prompt bem feito não é só bem escrito. Ele também é economicamente e operacionalmente coerente com o sistema em que está inserido.

Veja também: `examples/4-model-choice-tradeoffs.py`.

## 11. Checklist mental deste capítulo

Ao desenhar um fluxo com IA, vale revisar:

- a quantidade de contexto cabe confortavelmente na janela do modelo?
- existe risco de custo ou latência excessivos por excesso de tokens?
- o caso pede truncamento, sumarização ou janela deslizante?
- há blocos recorrentes que justificam cache?
- existe volume suficiente para pensar em batch prompting?
- o modelo escolhido faz sentido para a tarefa, em vez de ser apenas o “maior”?

## Conclusão

Os conceitos deste capítulo servem como base para capítulos mais práticos. Sem eles, é fácil cair em duas armadilhas:

- achar que prompt engineering é só redação;
- ignorar custo, latência e limites operacionais até o sistema começar a falhar.

Entender contexto, memória operacional, cache e batch não substitui técnicas de prompt, mas muda completamente a qualidade das decisões que você toma ao aplicá-las.
