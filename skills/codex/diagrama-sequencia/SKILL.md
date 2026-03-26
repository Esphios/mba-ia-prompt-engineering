---
name: diagrama-sequencia
description: Analisa um metodo ou fluxo para mapear callers e callees, rastrear o caminho completo desde o ponto de entrada ate persistencia ou integracoes, e gerar diagramas de sequencia Mermaid detalhados. Use quando Codex precisar entender fluxos de negocio, pontos de transformacao de dados ou impacto de mudancas.
---

# Diagrama de Sequencia

Use este skill para rastrear um metodo, caso de uso ou fluxo de negocio e gerar documentacao Mermaid precisa e reutilizavel.
Nao gere o diagrama imediatamente. Primeiro reconstrua o fluxo real a partir do codigo, configuracao e documentacao.

## Quando Usar

- Entender o caminho completo de execucao de um metodo.
- Medir impacto de mudancas em tipos de dados, contratos ou integracoes.
- Documentar fluxos ponta a ponta entre UI, API, services, repositories e banco.
- Descobrir bifurcacoes, fluxos alternativos e automacoes em background.

## Entradas

- Nome do metodo, assinatura, classe, arquivo ou fluxo descrito pelo usuario.
- Stack trace, endpoint, evento, tela ou caso de uso relacionado, quando houver.
- Codigo fonte, configuracao, testes e documentacao relevantes.
- `docs/diagramas-de-sequencia/README.md` e `docs/diagramas-de-sequencia/DIRETRIZES.md`, quando existirem.

## Workflow

1. Confirmar o alvo e o escopo.
Se houver ambiguidade, resolva pelo repositorio e explicite a suposicao adotada.

2. Ler diretrizes antes de diagramar.
Leia `docs/diagramas-de-sequencia/README.md` e `docs/diagramas-de-sequencia/DIRETRIZES.md` quando existirem.
Se os arquivos nao existirem, siga as convencoes do repositorio e boas praticas de Mermaid.

3. Localizar o ponto central de analise.
Mapeie o metodo alvo ou o fluxo principal, incluindo arquivo de origem e assinatura relevante.

4. Mapear dependencias diretas.
Liste explicitamente:
- callers: quem chama o metodo
- callees: o que ele chama
- artefatos relacionados: controllers, handlers, jobs, eventos, repositories, ORMs, integracoes externas e queries

5. Rastrear upstream.
Suba a pilha de chamadas ate o ponto de entrada real, como:
- API controller ou router
- consumer de mensageria
- job ou background service
- frontend ou tela especifica

6. Rastrear downstream.
Siga o fluxo ate persistencia, integracoes externas, publicacao de eventos, arquivos, filas ou qualquer outra saida material.

7. Identificar bifurcacoes e fluxos alternativos.
Se o mesmo metodo for acionado por fluxos distintos, mapeie cada fluxo.
Quando existir um metodo central reutilizado, prefira:
- um diagrama detalhado do fluxo central
- diagramas de alto nivel separados para cada ponto de entrada relevante

8. Sintetizar o fluxo.
Valide se a narrativa ponta a ponta faz sentido tecnico e representa um caso de uso real.
Destaque transformacoes de dados, validacoes, regras de negocio e integracoes sensiveis.

9. Gerar a resposta final.
Produza a analise estruturada e os diagramas Mermaid em conformidade com as diretrizes encontradas.

## Regras de Mermaid

- Use `autonumber`.
- Use aliases curtos e estaveis para participantes.
- Prefira `participant Alias as NomeLegivel`.
- Use `activate` e `deactivate` quando isso melhorar a leitura.
- Nao faca numeracao manual das mensagens quando `autonumber` estiver ativo.
- Evite caracteres de espaco nao padrao.
- Se houver padrao visual no repositorio, preserve-o.

## Estrutura da Resposta

Apresente a resposta final nesta ordem:

1. `Analise de Impacto`
- metodo ou fluxo analisado
- arquivo de origem
- callers identificados
- callees identificados
- resumo do fluxo ponta a ponta

2. `Pontos de Atencao`
- transformacoes de dados
- validacoes criticas
- regras de negocio
- integracoes sensiveis
- lacunas ou incertezas

3. `Diagramas de Sequencia`
- inclua um ou mais blocos `mermaid`
- se houver multiplos fluxos, nomeie cada diagrama com clareza

4. `Instrucao de Salvamento`
- caminho sugerido em `docs/diagramas-de-sequencia/<nome-do-fluxo>.md`
- indique se o nome deve seguir `kebab-case`

## Tratamento de Ambiguidade

- Se um caller nao puder ser rastreado ate a entrada, documente-o como fluxo interno ou background.
- Se houver multiplos pontos de entrada, nao colapse tudo em um unico fluxo confuso.
- Se parte do comportamento for inferido, rotule isso explicitamente.
- Se o codigo nao permitir confirmar uma ligacao, diga que a relacao e provavel e explique a base.

## Guardrails

- Nao invente fluxos, atores, validacoes ou integracoes.
- Nao gere o diagrama antes de mapear callers e callees.
- Nao omita caminhos alternativos relevantes so para simplificar a resposta.
- Nao use nomes genericos como `Frontend` quando uma tela especifica puder ser identificada.
- Nao altere codigo do projeto, exceto se o usuario pedir explicitamente para salvar a documentacao gerada.
