---
name: dotnet-bug-fixer
description: Skill de depuracao .NET especializado em isolamento com git worktree, leitura obrigatoria das instrucoes do repositorio, rastreamento de callers e callees, e aplicacao de correcoes cirurgicas e seguras em projetos .NET legados ou modernos.
---

# Dotnet Bug Fixer

Use este skill quando o usuario pedir investigacao e correcao de um bug em um repositorio .NET.
O objetivo e diagnosticar a causa provavel com base em evidencias do codigo, aplicar a menor correcao segura possivel em um worktree isolado e explicar riscos e validacao.

## Quando Usar

- Bugs funcionais em .NET Framework, ASP.NET MVC ou Web API, Web Forms, WCF ou .NET moderno.
- Falhas que exigem rastreamento de callers, callees e raio de impacto.
- Correcao segura sem tocar na branch atual do usuario.

## Pre-condicoes

- O repositorio precisa estar em Git.
- Uma branch base precisa ser informada pelo usuario ou inferida com seguranca.
- Deve ser possivel criar um `git worktree`.

Se a branch nao existir ou a criacao do worktree falhar, pare e reporte o erro sem prosseguir.

## Entradas

- Branch base.
- Relato do bug.
- Stack trace, logs, endpoint, tela, job, metodo, arquivo ou classe envolvidos, quando houver.
- Passos de reproducao e comportamento esperado, quando disponiveis.

## Workflow

1. Sanitizar o relato do bug.
Resuma o sintoma, impacto, comportamento esperado, area suspeita e passos de reproducao.

2. Validar a branch base.
Confirme se a branch existe localmente ou no remoto antes de criar o worktree.

3. Criar worktree isolado.
Sempre trabalhe fora da branch atual do usuario. Use um diretorio temporario e reporte o caminho criado.

4. Ler o contexto do repositorio.
No worktree, leia o arquivo principal de instrucoes na raiz, como `AGENTS.md`, `GEMINI.md`, `README.md` ou equivalente.

5. Localizar o ponto de falha.
Busque as classes, metodos, endpoints, handlers ou jobs citados no relato.

6. Mapear o raio de impacto.
Identifique callers, callees, dependencias, side effects, configuracoes e componentes externos relacionados.

7. Formular e testar a hipotese principal.
Priorize hipoteses compativeis com as evidencias do codigo e descarte explicacoes fracas.

8. Aplicar a menor correcao segura.
Mantenha o estilo do projeto, altere apenas o necessario e preserve comentarios existentes.

9. Validar.
Execute a menor validacao segura possivel, como build, testes focalizados ou verificacao estatica.
Se nao for possivel validar, explique exatamente o bloqueio.

10. Responder.
Entregue apenas o Markdown final com as secoes definidas abaixo.

## Pontos de Atencao para .NET

Inspecione ativamente padroes e falhas comuns como:

- uso inadequado de `HttpContext.Current`
- problemas de ciclo de vida em `Global.asax` e `App_Start`
- deadlocks com `Task.Result`, `Wait()` ou sincronizacao incorreta
- falhas de DI customizada
- configuracao divergente entre `web.config`, transforms e runtime
- erros em classes parciais, code-behind, WCF, jobs ou handlers assincronos
- concorrencia, idempotencia e acesso compartilhado a cache, sessao ou recursos estaticos

## Estrutura da Resposta

Entregue apenas estas secoes, nesta ordem:

1. `Diagnostico do Problema`
- arquivos analisados
- causa provavel
- evidencia principal
- impacto

2. `Proposta de Correcao`
- mudanca aplicada no worktree
- arquivos alterados
- resumo do patch
- trecho de codigo somente quando ele ajudar a explicar a correcao

3. `Efeitos Colaterais e Validacao`
- riscos residuais
- limitacoes da abordagem
- validacoes executadas
- validacoes recomendadas quando nao foi possivel executar

## Guardrails

- Nunca altere a branch atual do usuario.
- Sempre use `git worktree` quando for editar codigo.
- Nao adicione pacotes NuGet externos sem justificativa forte e alinhada com a arquitetura existente.
- Nao apague comentarios existentes.
- Nao faca refatoracoes amplas quando uma correcao local resolver o bug.
- Nao afirme comportamento de runtime sem base em codigo, configuracao, logs ou testes.
