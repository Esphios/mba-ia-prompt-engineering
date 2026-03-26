---
name: refatorar-classe-parcial-csharp
description: Especialista em refatoracao de classes C#. Use este skill quando o usuario precisar dividir um arquivo C# grande em `partial classes`, agrupando membros por dominio, funcao ou dependencia, sem alterar a logica existente.
---

# Refatorar Classe Parcial CSharp

Use este skill para dividir uma classe C# grande em arquivos `partial` mais coesos sem alterar a logica.
O foco e organizacao, legibilidade e manutencao. O comportamento deve continuar o mesmo.

## Quando Usar

- Quando uma classe C# cresceu demais e concentra responsabilidades demais.
- Quando a classe precisa ser organizada por dominio, tipo de operacao ou dependencia.
- Quando o objetivo e melhorar navegacao e manutencao sem redesenhar a arquitetura.

## Entradas

- Caminho do arquivo `.cs`.
- Nome da classe, quando o arquivo nao estiver claro.
- Conteudo bruto da classe, quando o usuario nao fornecer um caminho.
- Restricoes adicionais do usuario, como nome de arquivos, pasta de destino ou areas que nao podem ser tocadas.

Se nao houver caminho, nome de classe ou conteudo suficiente, peca a localizacao correta antes de prosseguir.

## Ordem de Agrupamento

Ao decidir como dividir a classe, siga esta prioridade:

1. Dominio de negocio.
Exemplos: `Usuario`, `Produto`, `Pedido`, `Autorizacao`, `Relatorios`.

2. Funcao tecnica.
Exemplos: `Queries`, `Commands`, `Downloads`, `Integracoes`, `Validacao`.

3. Afinidade de dependencia.
Agrupe membros que usam os mesmos servicos, repositories, gateways ou helpers.

## Workflow

1. Resolver a classe alvo.
Descubra o arquivo principal, o namespace, a declaracao da classe e possiveis arquivos relacionados.

2. Inventariar membros.
Mapeie metodos, propriedades, eventos, nested types, campos, construtor, comentarios, atributos e `#region`.

3. Mapear dependencias e afinidades.
Identifique quais campos, servicos, repositories, utilitarios e tipos compartilhados cada membro usa.

4. Criar o plano de divisao.
Agrupe os membros pela ordem de prioridade definida acima.
Revise o plano para evitar arquivos artificiais ou categorias sem sentido.

5. Definir o arquivo ancora.
Mantenha no arquivo principal, salvo instrucao contraria:
- declaracao principal da classe
- construtor
- campos privados e `private readonly`
- constantes e comportamento estrutural compartilhado

6. Criar os arquivos parciais.
Use nomes deterministas como `NomeDaClasse.<Categoria>.cs`.
Todos os arquivos devem manter o mesmo namespace e a mesma classe com a keyword `partial`.

7. Preservar a logica.
Nao altere a implementacao interna dos metodos, exceto ajustes mecanicos indispensaveis para a divisao.

8. Validar.
Se houver como compilar ou rodar testes focalizados, valide a refatoracao.
Se nao for possivel, declare o gap de verificacao.

## Regras Tecnicas

- Preserve modificadores de acesso, nomes, parametros e tipos de retorno.
- Preserve atributos, comentarios, XML docs e `#region` quando fizer sentido.
- Mantenha apenas os `using` necessarios em cada arquivo parcial.
- Nao mova codigo gerado automaticamente para dentro de arquivos manuais sem necessidade.
- Nao renomeie metodos, propriedades, campos ou arquivos existentes sem o usuario pedir.
- Nao crie novas abstracoes, interfaces ou classes fora do escopo da divisao em `partial`.

## Estrutura da Resposta

Quando a refatoracao for apresentada em resposta, use esta estrutura:

1. `Plano de Divisao`
- arquivo ou classe analisada
- criterio principal de agrupamento
- categorias criadas

2. `Arquivos Gerados ou Alterados`
- liste cada arquivo parcial
- explique em uma linha o que foi movido para ele

3. `Codigo`
- mostre apenas o necessario para o usuario entender a divisao
- se a execucao ocorreu no repositorio, priorize um resumo claro das mudancas

4. `Validacao`
- build, testes ou checagens executadas
- lacunas restantes

## Guardrails

- Nao altere a logica de negocio.
- Nao mude contratos publicos sem instrucao explicita.
- Nao espalhe campos compartilhados por varios arquivos sem um criterio claro.
- Nao gere arquivos parciais demais para categorias triviais.
- Nao descarte comentarios existentes.
