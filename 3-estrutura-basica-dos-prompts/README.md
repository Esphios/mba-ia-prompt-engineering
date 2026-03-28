# Capítulo: Estruturação de Prompts no Desenvolvimento de Software

## Introdução

Estruturar prompts bem não é um detalhe cosmético. É uma habilidade prática que afeta diretamente a qualidade da saída da IA, a previsibilidade do comportamento do modelo, o custo operacional e, no contexto de software, até mesmo o fluxo de trabalho da equipe.

A primeira ideia importante é simples: **não existe uma única estratégia de prompt que resolva todos os problemas**. A estrutura adequada depende do tipo de tarefa que você está executando.

Alguns exemplos deixam isso claro:

- Um prompt para **corrigir bugs** tende a exigir delimitação rígida de escopo.
- Um prompt para **explorar arquitetura de software** pode precisar de mais contexto, liberdade analítica e etapas de raciocínio.
- Um prompt para **gerar documentação** pode exigir padronização de saída, tom e estrutura editorial.
- Um prompt para **um agente que atende clientes** provavelmente exigirá regras mais rígidas de comportamento, segurança e consistência.

O objetivo deste capítulo é construir uma base sólida para pensar prompts de forma estruturada. Não como fórmulas mágicas, mas como **ferramentas de engenharia**.

---

# 1. O problema real não é a IA “errar”: é a ambiguidade

Uma parte significativa da frustração com IA no desenvolvimento de software não vem do fato de ela “ser ruim”, mas do fato de que ela frequentemente recebe **instruções ambíguas, incompletas ou permissivas demais**.

Quando isso acontece, o modelo não necessariamente falha de forma óbvia. Muitas vezes ele faz algo que **parece bom**, mas que é inadequado para o contexto real de trabalho.

Esse tipo de erro é perigoso justamente porque ele pode vir disfarçado de produtividade.

---

## 1.1 O caso clássico: “só corrige esse bug”

Imagine um cenário comum:

- existe um software com uma base de código razoavelmente grande;
- você recebe um bug simples para corrigir;
- você usa IA no fluxo de desenvolvimento;
- a correção em si é pequena, algo como trocar um `>` por `>=`.

A princípio, parece uma tarefa trivial.

Mas aí você faz um pedido genérico para a IA, algo como:

> “Valide essa função, entenda o problema e faça a correção para mim.”

O que pode acontecer?

A IA pode:

- corrigir o bug;
- melhorar os testes;
- reorganizar trechos de código;
- extrair funções menores;
- alterar nomes de variáveis;
- adicionar comentários;
- documentar partes do módulo;
- aplicar “boas práticas” em arquivos adjacentes.

Ou seja: **ela resolve o problema e cria outros problemas de processo**.

### O efeito colateral

Em vez de você abrir uma pull request pequena, com uma alteração objetiva, você acaba com:

- vários arquivos modificados;
- dezenas ou centenas de linhas alteradas;
- um code review muito maior;
- aumento do risco de regressão;
- perda de foco do objetivo original.

No papel, a IA “melhorou” o código. Mas, no fluxo real da equipe, ela **quebrou o processo**.

Em um ambiente profissional, isso pode significar:

- mais tempo de revisão;
- atraso na entrega;
- mais risco de erro humano;
- dificuldade de aprovação;
- aumento de ruído entre times.

O ponto principal é: **nem toda boa alteração é uma boa alteração naquele momento**.

---

## 1.2 O problema não é só o modelo: é a ausência de limites

É muito tentador culpar apenas o modelo quando esse tipo de coisa acontece. Mas, na prática, o problema normalmente é uma combinação de dois fatores:

1. **modelos diferentes têm comportamentos diferentes**;
2. **prompts sem limites explícitos deixam espaço para “criatividade operacional” demais**.

Ao longo do tempo, novos modelos surgem, versões mudam, ajustes internos são feitos e o comportamento do sistema pode variar bastante.

Um modelo mais “obediente” hoje pode virar um modelo mais “proativo” amanhã.

Isso significa que, se você trabalha com prompts “inocentes”, o seu fluxo fica vulnerável à mudança de comportamento do modelo.

### Conclusão prática

Sempre que você for estruturar um prompt, você precisa definir duas coisas com clareza:

- **os limites do que pode ser feito**;
- **o formato do resultado esperado**.

Sem isso, o modelo tende a preencher as lacunas com decisões probabilísticas próprias.

E isso é o oposto do que você quer em engenharia.

---

# 2. “A IA produziu um lixo”: como transformar frustração em melhoria operacional

Existe uma reclamação muito comum entre desenvolvedores:

> “O código que a IA gerou é um lixo.”

Essa reação é compreensível. Muitas vezes, ela vem depois de várias tentativas frustradas, especialmente em projetos com:

- dependências antigas;
- mudanças frequentes de versão;
- padrões inconsistentes;
- front-end sensível a detalhes;
- múltiplas bibliotecas e convenções.

O problema é que parar nessa conclusão não resolve nada.

A pergunta útil não é:

> “A IA é ruim?”

A pergunta útil é:

> “O que exatamente tornou essa saída ruim?”

Essa mudança de perspectiva é importante porque ela transforma frustração em **material de refinamento**.

---

## 2.1 Faça code review da saída da IA

Quando a IA gera algo ruim, o melhor caminho não é apenas descartar o resultado. É fazer um **code review estruturado da própria saída**.

Alguns exemplos de problemas que podem aparecer:

- usou bibliotecas antigas ou inadequadas;
- criou arquivos grandes demais;
- adicionou funções desnecessárias;
- interrompeu uma implementação no meio;
- corrigiu uma coisa e quebrou outra;
- mudou padrões do projeto sem necessidade;
- começou a trabalhar no arquivo errado;
- fez uma correção parcial e deixou o resto inconsistente.

Cada um desses erros pode ser transformado em **uma nova diretriz de prompt**.

---

## 2.2 Trate a IA como um novo integrante da equipe

Uma analogia útil é pensar na IA como um novo funcionário no primeiro dia de trabalho.

Não no sentido sentimental, mas no sentido operacional.

Ela pode ser capaz, rápida e produtiva, mas:

- não conhece seu contexto;
- não conhece suas convenções;
- não conhece suas prioridades;
- não conhece seus limites de processo;
- não conhece o “jeito certo” da sua equipe trabalhar.

Se você parte desse princípio, fica mais fácil entender por que ela erra e, principalmente, como reduzir esses erros.

### Exemplo de refinamento

Se a IA usou uma biblioteca antiga, você pode adicionar algo como:

> “Antes de utilizar bibliotecas dessa família, verifique a documentação atual e utilize a versão mais recente compatível com o projeto.”

Se ela criou arquivos grandes demais:

> “Não crie arquivos com mais de 100 linhas sem justificativa clara. Prefira separar responsabilidades quando isso melhorar legibilidade e manutenção.”

Se ela criou funções desnecessárias:

> “Antes de criar uma nova função, verifique se já existe uma implementação equivalente ou se a abstração é realmente necessária.”

Se ela interrompeu um fluxo e deixou um arquivo incompleto:

> “Se precisar mudar de direção durante a implementação, finalize o estado consistente do arquivo atual antes de continuar.”

Perceba o padrão: você está transformando erro em **regra operacional reutilizável**.

---

## 2.3 O que era só irritação vira ativo de projeto

Essa é uma das ideias mais valiosas deste tema:

**cada erro recorrente da IA pode virar uma melhoria permanente do seu sistema de prompts**.

Isso significa que, com o tempo, você pode construir:

- diretrizes reutilizáveis;
- instruções padrão;
- blocos de comportamento;
- templates por tipo de tarefa;
- critérios de revisão;
- exemplos esperados.

Em vez de tratar cada conversa como um improviso, você passa a tratar prompt como **infraestrutura cognitiva do projeto**.

---

# 3. Prompts também são ativos de engenharia

Times maduros tratam várias coisas como ativos de longo prazo:

- testes automatizados;
- documentação;
- convenções de código;
- pipelines;
- observabilidade;
- padrões arquiteturais.

Prompts devem entrar nessa lista.

Porque, no fim das contas, um prompt bem estruturado é uma forma de **codificar intenção operacional**.

Ele carrega:

- restrições;
- contexto;
- critérios de qualidade;
- forma de resposta;
- comportamento esperado.

Se você cria prompts de forma desestruturada, o que acontece é previsível:

- eles crescem sem padrão;
- ficam difíceis de manter;
- começam a se contradizer;
- aumentam a ambiguidade;
- pioram a qualidade da saída.

Ou seja: **mais informação nem sempre significa melhor instrução**.

Sem estrutura, o prompt vira um amontoado de contexto.

Com estrutura, ele vira uma ferramenta.

---

# 4. Quando economizar tokens e quando não economizar

Uma dúvida recorrente quando se fala em prompts mais elaborados é:

> “Não vai gastar tokens demais?”

A resposta correta é: **depende do contexto de uso**.

Essa decisão não deve ser ideológica. Ela deve ser **estrutural e econômica**.

---

## 4.1 Em desenvolvimento, geralmente não vale a pena economizar tokens

Quando você está usando IA em tarefas como:

- corrigir bugs;
- gerar testes;
- explorar arquitetura;
- documentar código;
- revisar fluxos;
- entender dependências;
- mapear impacto de mudanças;

... normalmente você está em um cenário de **baixa escala e alto valor por interação**.

Nesses casos, economizar tokens cedo demais pode ser um falso ganho.

### Por quê?

Porque desenvolvimento de software é um domínio complexo. E, em muitos casos, menos contexto significa:

- mais interpretação errada;
- mais retrabalho;
- mais correções manuais;
- mais bugs;
- mais ruído.

Se a tarefa não vai rodar milhares ou milhões de vezes, faz sentido priorizar:

- clareza;
- contexto;
- previsibilidade;
- qualidade de saída.

### Regra prática

Se a tarefa é:

- pontual,
- humana,
- iterativa,
- de exploração,
- ou de alto impacto local,

... normalmente **não faz sentido ser obcecado por economia de tokens**.

O importante é evitar desperdício estrutural, não amputar contexto útil.

---

## 4.2 Em larga escala, cada token importa

O cenário muda completamente quando a IA está dentro de uma aplicação que roda em produção em escala.

Exemplos:

- atendimento automatizado;
- classificação em massa;
- sumarização em lote;
- validação de entradas;
- processamento recorrente de documentos;
- agentes que atendem usuários finais em alto volume.

Nesse contexto:

- mais token = mais custo;
- mais regras = mais latência;
- mais raciocínio = mais tempo de resposta;
- mais contexto = maior chance de inviabilidade econômica.

Aqui, o problema não é apenas técnico. É de produto e negócio.

### Em larga escala, você precisa otimizar:

- custo;
- latência;
- previsibilidade;
- throughput;
- taxa de acerto aceitável.

E isso muda a forma de estruturar o prompt.

---

# 5. Trade-offs reais: custo, latência e qualidade

Prompt engineering não é só “escrever instruções melhores”. Em muitos cenários, ele é um problema clássico de trade-off.

Toda decisão de prompt afeta, em algum nível:

- **qualidade do resultado**;
- **latência**;
- **custo operacional**.

E, na prática, você raramente maximiza os três ao mesmo tempo.

---

## 5.1 O raciocínio correto não é “melhor ou pior”, e sim “vale a pena?”

Imagine um cenário hipotético:

- com uma estratégia mais simples, você tem **86% de assertividade**;
- com uma estratégia mais elaborada, você chega a **90% de assertividade**;
- o custo mensal sobe significativamente.

A pergunta não é:

> “90% é melhor que 86%?”

Claro que é.

A pergunta correta é:

> “Quanto custa cada ponto percentual adicional de qualidade?”

Essa é uma pergunta de produto, operação e engenharia, não apenas de desenvolvimento.

---

## 5.2 O desenvolvedor nem sempre decide sozinho

Em muitos casos, a decisão não cabe só ao desenvolvedor.

Porque o trade-off pode envolver:

- orçamento;
- SLA;
- experiência do usuário;
- risco regulatório;
- criticidade da tarefa;
- tolerância a erro.

Seu papel técnico, muitas vezes, é tornar o trade-off explícito.

Por exemplo:

- “Com esse prompt simples, temos menor custo e menor latência, mas maior erro.”
- “Com esse prompt mais robusto, ganhamos qualidade, mas o custo sobe e a resposta fica mais lenta.”

Isso é engenharia madura.

---

# 6. Guidelines práticas: zero-shot e few-shot

Nem toda tarefa exige o mesmo nível de elaboração.

Uma boa forma de pensar nisso é entender quando usar abordagens mais simples e quando usar abordagens mais guiadas.

---

## 6.1 Zero-shot: quando a tarefa é simples, comum ou volumosa

**Zero-shot** é quando você pede algo sem dar exemplos.

Você apenas descreve a tarefa.

Isso costuma funcionar bem quando a tarefa é:

- simples;
- de senso comum;
- bem conhecida;
- pouco ambígua;
- altamente repetitiva;
- ou de grande volume.

### Exemplos de tarefas que tendem a funcionar bem com zero-shot

- validar uma estrutura;
- classificar algo simples;
- resumir um pequeno trecho;
- identificar um elemento específico;
- fazer uma transformação direta.

Em cenários de alto volume, zero-shot tende a ser a escolha natural porque:

- usa menos tokens;
- responde mais rápido;
- custa menos;
- é mais simples de operar.

---

## 6.2 Few-shot: quando o formato e o domínio importam muito

**Few-shot** é quando você inclui exemplos no prompt para mostrar ao modelo como deve ser o comportamento ou a saída.

Isso tende a ser útil quando você trabalha com:

- domínio muito específico;
- formato de resposta muito rígido;
- linguagem especializada;
- regras contextuais delicadas;
- tarefas em que “acertar o estilo” importa tanto quanto “acertar o conteúdo”.

### Exemplos típicos de uso

- documentação padronizada;
- saídas estruturadas específicas;
- domínios sensíveis ou altamente técnicos;
- tarefas onde a forma da resposta precisa ser muito consistente.

### Custo do few-shot

Few-shot tende a ser:

- mais caro;
- mais lento;
- mais pesado em tokens;
- mais complexo de manter.

Mas, em compensação, pode aumentar muito a consistência da saída.

---

## 6.3 O exemplo ensina comportamento

Uma observação importante: quando você dá exemplos, você não está apenas “ajudando a IA”.

Você está ensinando:

- forma;
- padrão;
- expectativa;
- nível de detalhe;
- comportamento de saída.

Por isso, few-shot é poderoso.

Mas exatamente por isso ele também é caro: **você está pagando contexto para comprar previsibilidade**.

---

# 7. System Prompt vs User Prompt

Para estruturar prompts de forma profissional, é essencial entender uma separação conceitual importante: **System Prompt** e **User Prompt**.

---

## 7.1 O que é o System Prompt

O **System Prompt** define as regras do jogo.

Ele estabelece, por exemplo:

- comportamento geral;
- tom;
- especialização;
- limites;
- prioridades;
- restrições permanentes daquela interação.

Você pode pensar nele como um **manual de operação do modelo dentro daquele contexto**.

Ele costuma responder perguntas como:

- Quem esse modelo é?
- Como ele deve se comportar?
- O que ele nunca deve fazer?
- Quais princípios ele deve priorizar?

### Exemplo conceitual

Um System Prompt pode dizer algo como:

- você é um assistente especializado em backend;
- seja direto e técnico;
- não invente APIs;
- não modifique código sem justificativa;
- não refatore fora do escopo solicitado.

Isso não define a tarefa em si. Isso define **o comportamento esperado durante qualquer tarefa**.

---

## 7.2 O que é o User Prompt

O **User Prompt** é o pedido específico que chega em uma interação.

Ele responde à pergunta:

> “O que eu quero que você faça agora?”

Por exemplo:

- corrigir um bug;
- gerar testes;
- documentar uma função;
- revisar uma implementação;
- comparar duas abordagens.

Ou seja:

- o **System Prompt** define o comportamento global;
- o **User Prompt** define a tarefa local.

Essa separação é muito importante porque evita que você misture:

- regras permanentes;
- com pedidos pontuais.

---

## 7.3 Por que essa separação importa

Quando você não separa essas duas camadas, vários problemas aparecem:

- regras de comportamento ficam perdidas no meio da tarefa;
- o modelo pode ignorar restrições importantes;
- o prompt cresce de forma confusa;
- a manutenção fica ruim;
- o reaproveitamento se torna difícil.

Pensar em System Prompt e User Prompt é, no fundo, pensar em **arquitetura de instrução**.

---

# 8. A estrutura base de um bom prompt

Agora que os conceitos principais estão claros, podemos consolidar uma estrutura prática para prompts mais robustos.

Essa estrutura não é uma regra absoluta, mas funciona como uma base muito útil para tarefas técnicas, especialmente no desenvolvimento de software.

---

## 8.1 Persona e escopo

A primeira parte do prompt deve definir **quem o modelo é** e **até onde ele pode ir**.

Essa seção serve para reduzir improviso e alinhar o comportamento.

Ela responde perguntas como:

- Qual papel ele deve assumir?
- Em que ele é especializado?
- O que está fora de escopo?
- O que ele não deve fazer?

### Exemplo conceitual

> Você é um assistente especializado em Node.js e testes com Jest.
> Não faça refatorações no código original.

Esse bloco já faz duas coisas ao mesmo tempo:

- especializa o comportamento;
- restringe a atuação.

E isso, na prática, reduz bastante a chance de “proatividade indevida”.

---

## 8.2 Objetivo

Depois de definir quem o modelo é, você precisa dizer **o que ele deve fazer agora**.

Essa seção deve ser:

- direta;
- específica;
- sem ambiguidade desnecessária.

### Exemplo ruim

> Descreva testes para o código abaixo.

Isso é amplo demais.

### Exemplo melhor

> Gere testes unitários para a função abaixo usando Jest, cobrindo casos válidos e inválidos.

O ponto aqui não é “achar a frase perfeita”, mas **reduzir o espaço de interpretação solta**.

---

## 8.3 Entrada

Depois do objetivo, você precisa mostrar claramente **qual é a entrada da tarefa**.

Essa seção existe para separar:

- instrução;
- contexto;
- material de trabalho.

Isso é importante porque, quando tudo vem misturado, o modelo pode confundir:

- o que é regra;
- o que é dado;
- o que é código;
- o que é comentário.

### Boas práticas para a entrada

- forneça apenas o necessário;
- separe visualmente os blocos;
- evite colar arquivos inteiros sem necessidade;
- destaque o trecho realmente relevante.

### Exemplo conceitual

> Função:
>
> ```js
> // código aqui
> ```

Essa separação simples já melhora muito a legibilidade do prompt para o modelo.

---

## 8.4 Formato de saída

Esse é um dos blocos mais importantes.

Muita gente sabe o que quer que a IA faça, mas não define claramente **como quer receber a resposta**.

Quando você não define isso, o modelo tende a responder “do jeito dele”.

E isso costuma gerar:

- respostas longas demais;
- explicações desnecessárias;
- formatos inconsistentes;
- dificuldade de automação;
- dificuldade de revisão.

### Exemplo conceitual

> Responda apenas com um objeto JSON contendo:
>
> - `test_file`
> - `coverage_notes`
> - `assumptions`

Isso é muito útil quando você quer:

- previsibilidade;
- integração com outras etapas;
- facilidade de validação;
- menor ruído de resposta.

### JSON é obrigatório?

Não.

Mas formatos estruturados tendem a funcionar melhor quando você precisa de:

- consistência;
- automação;
- comunicação entre agentes ou sistemas;
- validação programática.

---

## 8.5 Critérios de qualidade

Depois de dizer o que quer e como quer a saída, você precisa dizer:

> “O que caracteriza uma boa resposta?”

Essa seção ajuda o modelo a entender **como deve se autoavaliar** durante a geração da resposta.

### Exemplo conceitual

- O teste deve rodar com `npm test` sem ajustes
- Deve cobrir casos válidos e inválidos
- Não deve usar bibliotecas externas além do Jest

Perceba a diferença:

- “gere testes” é um pedido;
- “os testes devem rodar sem ajustes e cobrir casos válidos e inválidos” é um critério de qualidade.

Essa diferença importa muito.

---

## 8.6 Tratamento de ambiguidades e pressupostos

Em muitos casos, a IA não terá todas as informações necessárias.

Nessas situações, você tem duas opções:

1. deixar o modelo improvisar silenciosamente;
2. instruí-lo a **assumir explicitamente certas coisas e declarar isso**.

A segunda opção é muito melhor.

### Exemplo conceitual

> Se faltar a versão do Node.js, assuma Node 18.
> Liste todos os pressupostos no campo `assumptions`.

Esse bloco é extremamente útil porque evita que hipóteses implícitas passem despercebidas.

Isso é importante para revisão, rastreabilidade e confiança operacional.

---

## 8.7 Instruções negativas

Além de dizer o que a IA deve fazer, é importante dizer **o que ela não deve fazer**.

Essa é uma parte subestimada da estruturação de prompts.

### Exemplo conceitual

> Não inclua explicações ou comentários fora do JSON.

Esse tipo de instrução é especialmente útil para controlar a **saída final**.

Ela ajuda a reduzir:

- ruído;
- prolixidade;
- formatação inconsistente;
- comportamento não desejado.

---

## 8.8 Tratamento de erro

Por fim, vale a pena dizer o que o modelo deve fazer **se não conseguir cumprir a tarefa adequadamente**.

Sem esse bloco, a IA pode:

- improvisar;
- mascarar falha;
- entregar algo incompleto como se estivesse certo;
- responder de forma vaga.

### Exemplo conceitual

> Se não for possível cumprir a tarefa, retorne um JSON com:
>
> - `status: error`
> - `reason`

Isso torna a falha legível, tratável e operacionalmente útil.

---

# 9. Exemplo consolidado de prompt estruturado

Abaixo está uma forma consolidada de estruturar esse tipo de prompt técnico.

## Persona e escopo

Você é um assistente especializado em Node.js 18 e testes com Jest.
Não faça refatorações no código original.

## Objetivo

Gerar testes unitários para a função abaixo usando Jest.

## Entrada

Função:

```js
// código aqui
```

## Formato de saída

Responda apenas com um objeto JSON contendo:

- `test_file`
- `coverage_notes`
- `assumptions`

## Critérios de qualidade

- O teste deve rodar com `npm test` sem ajustes
- Deve cobrir casos válidos e inválidos
- Não usar bibliotecas externas além do Jest

## Tratamento de ambiguidades

Se faltar a versão do Node.js, assuma Node 18 e registre isso em `assumptions`.

## Instruções negativas

Não inclua explicações ou comentários fora do JSON.

## Tratamento de erro

Se não for possível cumprir a tarefa, retorne um JSON com erro e a explicação do motivo.

---

# 10. Por que essa estrutura funciona

Essa estrutura funciona porque ela reduz um problema muito comum: **misturar intenção, contexto, regra e saída no mesmo bloco mental**.

Quando você separa as camadas, o prompt fica mais fácil de:

- escrever;
- revisar;
- reutilizar;
- manter;
- adaptar para outros casos.

Além disso, ela melhora quatro coisas fundamentais:

## 10.1 Reduz ambiguidade

Cada seção responde a uma pergunta específica:

- quem é o modelo?
- o que ele deve fazer?
- com qual entrada?
- em que formato?
- com quais critérios?
- com quais limites?

Isso reduz a chance de interpretações difusas.

---

## 10.2 Aumenta previsibilidade

Quanto mais explícita a estrutura, menor a chance de o modelo “inventar o estilo da tarefa”.

Você continua lidando com um sistema probabilístico, mas agora com **muito menos liberdade desnecessária**.

---

## 10.3 Facilita reutilização

Um prompt bem estruturado pode ser reaproveitado com pequenas trocas:

- mudar o objetivo;
- trocar a entrada;
- adaptar critérios;
- ajustar formato de saída.

Isso é muito melhor do que reescrever tudo do zero toda vez.

---

## 10.4 Melhora manutenção ao longo do tempo

Conforme você aprende com os erros da IA, você pode ir evoluindo esse template.

Por exemplo:

- adicionando novas restrições;
- incluindo critérios de qualidade;
- refinando instruções negativas;
- formalizando pressupostos.

Isso transforma prompt em **artefato versionável de engenharia**.

---

# 11. Regras de ouro para qualquer prompt

Como fechamento, vale consolidar uma lista de verificação mental.

Sempre que você for criar um prompt mais sério, especialmente em contexto técnico, vale revisar se ele contém os elementos abaixo.

---

## Checklist de estruturação

### 1. Persona e escopo

- O modelo sabe quem ele deve ser?
- O papel está claro?
- Os limites estão claros?

### 2. Objetivo

- A tarefa está descrita de forma direta?
- Existe ambiguidade desnecessária?

### 3. Entrada

- O material necessário está separado da instrução?
- Só o que importa foi incluído?

### 4. Formato de saída

- Está claro como a resposta deve vir?
- O formato é validável e útil?

### 5. Critérios de qualidade

- Está explícito o que define uma boa resposta?

### 6. Ambiguidades e pressupostos

- O modelo sabe como agir se faltar contexto?
- As suposições precisam ser declaradas?

### 7. Instruções negativas

- Está claro o que não pode acontecer?

### 8. Tratamento de erro

- O modelo sabe como responder se falhar?

---

# 12. Conclusão

A principal mudança de mentalidade aqui é a seguinte:

**prompt não é um texto jogado no chat.**
Prompt é uma forma de **projetar comportamento**.

Quando você começa a enxergar isso, várias coisas mudam:

- você para de improvisar;
- começa a escrever com intenção;
- reduz ruído operacional;
- melhora a qualidade das saídas;
- economiza retrabalho;
- constrói ativos reutilizáveis.

Em ambientes de software, isso é ainda mais importante, porque o custo de uma resposta “quase certa” pode ser muito alto.

No fim das contas, estruturar prompts bem é muito parecido com estruturar software bem:

- clareza importa;
- separação de responsabilidades importa;
- contratos importam;
- manutenção importa;
- comportamento previsível importa.

E, exatamente por isso, prompt engineering bem feito não é perfumaria. É engenharia aplicada.
