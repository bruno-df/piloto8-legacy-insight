# Relatório: Piloto IA 08, Legacy Insight

**Atividade:** modernização de sistema legado com refatoração segura (Unidade VIII).
**Projeto:** `legacy_pds`, o GovFlow Legacy Lab. É um caso inteiramente fictício, sem dados reais.
**Participante:** _(preencher nome e turma)_
**Data:** 2026-11-06
**Ferramenta:** Claude Code, no Claude Desktop (aba Code, modo Local), modelo Claude Opus 5.5.
**Repositório:** <https://github.com/bruno-df/piloto8-legacy-insight>

| Commit | Conteúdo |
|---|---|
| `6a19380` | Estado inicial: cópia limpa recebida, sem nenhuma alteração |
| `1f0dc79` | `test:`, um teste de caracterização do lote, adicionado **antes** da refatoração |
| `0861508` | `refactor:`, a única refatoração estrutural |
| (último) | `docs:`, este relatório e a pasta `evidencias/` |

---

## 1. Compreensão do sistema

**Componentes**

- `src/triagem.py`: `classificar(dias, documentos)`, função pura com a regra de negócio. Sem documentos, retorna `PENDENTE`. Com documentos, retorna `ATRASADA` acima de 30 dias e `NO_PRAZO` nos demais casos (RF-01 e RN-01 de `docs/demanda.md`).
- `src/servico.py`: `processar_csv(texto)` lê e valida o CSV, classifica cada linha e monta o resumo. `relatorio_texto(texto)` formata as linhas como `protocolo:situacao`.
- `tests/test_triagem.py`: caracterização da regra (CA-01 a CA-04).
- `tests/test_servico.py`: contrato do lote, ou seja, estrutura, ordem, mensagens de erro e normalização.
- `dados/solicitacoes.csv` traz os dados fictícios. Os contratos estão em `docs/arquitetura.md` e `docs/demanda.md`.

**Fluxo de uma demanda**

1. O texto CSV é lido; o cabeçalho tem de ser exatamente `protocolo,dias,documentos`.
2. Para cada linha, nesta ordem:
   - o protocolo é limpo de espaços e não pode ser vazio nem repetido;
   - `dias` tem de ser inteiro e ≥ 0;
   - `documentos` tem de ser `sim` ou `nao` (sem diferenciar maiúsculas e ignorando espaços).
3. A linha é classificada e vira um item.
4. Ao final, a função conta cada situação (com chaves fixas) e devolve `{itens, resumo, total}`.

## 2. Problemas identificados

| # | Problema | Onde | Consequência |
|---|---|---|---|
| 1 | **Regra de negócio duplicada.** O serviço reescrevia com `if/elif` a mesma regra de `classificar`, inclusive o limite 30. | `src/servico.py` (linhas 25-31 originais) e `src/triagem.py:3-7` | Uma mudança futura, como o RF-02, poderia ser feita num lugar e esquecida no outro, e o sistema daria respostas diferentes para a mesma demanda. |
| 2 | **Responsabilidades misturadas.** Uma só função lê, valida, classifica e resume. | `src/servico.py:4-37` (original) | É difícil testar cada parte isoladamente e trocar a entrada CSV por outra (`docs/arquitetura.md:8`). |
| 3 | **Robustez da entrada** (confirmada por execução). Uma linha com coluna faltando (`A,1`) gera `AttributeError` em vez de `ValueError`, e uma coluna extra é ignorada sem aviso. | `src/servico.py:22` (original) | Erro inesperado para quem chama a função. Corrigir isso **muda o comportamento**, então ficou registrado como lacuna. |

**Escolha: problema 1.** É a menor mudança que melhora a estrutura sem alterar o comportamento, e é exatamente o que a demanda descreve como problema (`docs/demanda.md:3`). O problema 2 exigiria criar vários módulos, uma mudança maior do que a atividade pede. O problema 3 é uma mudança funcional.

## 3. Planejamento e refatoração

A refatoração seguiu `CLAUDE.md`: primeiro o plano, depois a edição. O plano foi apresentado e **autorizado explicitamente** antes de qualquer edição. Os passos foram:

1. **Git:** `git init`, commit de base com a cópia recebida e branch de trabalho `refatoracao/regra-unica`.
2. **Teste antes de refatorar (commit `1f0dc79`):** novo `test_classificacao_lote_fronteiras` (0, 30 e 31 dias, com `sim` e `nao`). Ele passou no código **original**. Nenhum teste existente foi alterado ou removido.
3. **Refatoração (commit `0861508`, só em `src/servico.py`):**

```diff
+from .triagem import classificar
 ...
-        # Regra duplicada de src.triagem.classificar.
-        if doc == "nao":
-            situacao = "PENDENTE"
-        elif dias > 30:
-            situacao = "ATRASADA"
-        else:
-            situacao = "NO_PRAZO"
+        documentos = doc == "sim"
+        situacao = classificar(dias, documentos)
         itens.append({"protocolo": protocolo, "dias": dias,
-                      "documentos": doc == "sim", "situacao": situacao})
+                      "documentos": documentos, "situacao": situacao})
```

O comentário da linha 7 também foi atualizado para refletir a nova divisão: a classificação agora pertence a `src.triagem`.

**Por que o comportamento se mantém:** a validação anterior garante que `doc` só pode ser `sim` ou `nao`. Então `doc == "nao"` é o mesmo que `not documentos`, e `classificar` aplica a mesma precedência (documentos primeiro, depois `> 30`).

**O que ficou igual:**
- nomes públicos, tipos de retorno, ordem dos itens, chaves do resumo e formato do relatório;
- mensagens e tipos de exceção, e a ordem das validações;
- `classificar(30, True) == "NO_PRAZO"`.

Nada foi alterado em `src/triagem.py`, `tests/test_triagem.py` ou nos dados, e nenhuma dependência foi adicionada.

## 4. Testes e comparação antes/depois

| Verificação | Antes | Depois | Evidência |
|---|---|---|---|
| `python -m unittest discover -s tests -v` | 12 testes, **OK**, código de saída 0 | 13 testes, **OK**, código de saída 0 | `evidencias/01`, `02`, `10` |
| Versão do Python | 3.14.0 | 3.14.0 | idem |
| Hashes SHA-256 | — | só `servico.py` e `test_servico.py` mudaram | `evidencias/03` |
| Comparação diferencial, versão original contra a nova | — | 301 entradas, 602 chamadas, **0 divergências** | `evidencias/06` |
| Teste de mutação | — | o teste novo detecta 2 regras quebradas | `evidencias/07` |

- **Comparação diferencial.** O script roda a versão original e a refatorada com as mesmas entradas e compara valor, tipo e exceção. As entradas incluem:
  - o CSV de dados e todas as combinações de 0 a 40 dias, 99, 100 e 1000 dias;
  - grafias como `" SIM "` e `"Nao"`, um lote grande e 17 entradas inválidas (coluna faltando, coluna extra, decimal, CRLF, entre outras).
- **Teste de mutação.** Em cópias temporárias, quebrei a regra de propósito:
  - Mutante 1, trocando `> 30` por `>= 30`: detectado pela suíte, com 3 falhas.
  - Mutante 2, "sem documentos só é PENDENTE acima de 30 dias": **os 8 testes originais do lote passam**, e só o teste novo falha, nos casos 0 e 30 dias.

  Isso mostra que havia uma lacuna real de cobertura e que o teste novo a fecha.
- **Commit de base.** É idêntico à cópia recebida nos 6/6 arquivos de código e dados. A única diferença é o fim de linha: o Git (`core.autocrlf=true`) guarda LF, e o disco usa CRLF (`evidencias/03`).

## 5. Revisão crítica: o que foi comprovado e o que não foi

**Comprovado (com evidência executada ou lida)**
- Os testes passam antes e depois da refatoração.
- O diff está limitado a `src/servico.py`, e o teste novo está num commit separado.
- O resultado é igual ao da versão original em 301 entradas, incluindo os erros.
- A revisão independente do subagente, feita só por leitura, não encontrou regressão nem mudança fora do escopo (`evidencias/09`).

**Não comprovado / riscos residuais**
1. **Equivalência total não está provada.** Os testes e a comparação cobrem muitos casos, mas não todos os possíveis.
2. **Importação relativa** (`from .triagem import classificar`): o módulo deixa de carregar fora do pacote `src` (`python src/servico.py`, `import servico` com `src/` no caminho de busca). Nenhum teste cobre isso, porque a suíte importa `src.servico` a partir da raiz.
3. **Acoplamento intencional:** qualquer mudança em `classificar` agora afeta o lote. Se o RF-02 for feito como um novo código de retorno, o resumo de chaves fixas quebra (KeyError). O caminho previsto é uma função `sinalizar` separada (`docs/plano.md:6`).
4. **Lacunas antigas, mantidas de propósito:** uma linha sem uma coluna gera `AttributeError`, e uma coluna extra é ignorada. Os testes usam `assertEqual`, que não distingue `True` de `1`; a comparação diferencial verificou os tipos.
5. **Nome do teste novo:** não tem o ID de CA no nome (`docs/demanda.md:12`); ele só aparece no comentário.
6. **Não há teste estrutural da delegação.** Se a regra duplicada for reintroduzida corretamente, os testes não percebem.

## 6. Recursos do Claude utilizados

| Recurso | Uso | Situação |
|---|---|---|
| `CLAUDE.md` e `.claude/rules/evidencias.md` | Lidos no início e seguidos: plano antes de editar, RF-02 separado, `classificar(30, True)` preservado, registro de lacunas e de teste que falha, e evidências com stdout, stderr, código de saída, versão do Python e hashes | **Usado** |
| Docs do projeto | `context-pack.md`, `demanda.md`, `arquitetura.md`, `plano.md`, `conflito.md` e `comparacao-offline.md` lidos antes da proposta | **Usado** |
| Subagente `revisor-regressao` | Revisão independente, só de leitura, de contratos, fronteiras e riscos | **Usado** (`evidencias/09`) |
| Skill `revisar-pds` | Está configurada com `disable-model-invocation: true`, então o modelo não pode chamá-la; só o participante pode, digitando `/revisar-pds` | **Não executada (PENDENTE)** |
| MCP `demandas` | O servidor falhou ao conectar: o `.mcp.json` aponta para caminhos de outra máquina (`C:\Users\IFMT\...`) | **Indisponível**, nenhuma evidência inventada |
| Referência `../../08-referencias/mapa-pds.md` | O arquivo não existe nesta máquina, então nenhuma seção do PDS foi consultada ou citada | **Indisponível** |
| Learning (aprendizagem orientada) | Não experimentado nesta sessão | **Não utilizado** |
| Git | Linha de base, branch de trabalho, commits separados por natureza, `diff`, `log` e `status` | **Usado** (`evidencias/04`, `05`, `08`) |

## 7. Conclusão

**Antes:** o sistema funcionava, mas a regra de classificação existia em dois lugares, com risco de divergência.
**Depois:** o mesmo sistema funciona, e a regra existe num lugar só (`src/triagem.py`), usado pelo serviço do lote. Os testes passam, a cobertura do lote ficou melhor (o teste novo pega um erro que os anteriores deixavam passar) e as alterações estão documentadas e versionadas.

**Situação formal.** Seguindo `.claude/rules/evidencias.md`, que distingue conclusão técnica, aceite funcional e recebimento contratual:
- **Conclusão técnica:** refatoração implementada e verificada por testes, comparação e revisão automatizada.
- **Revisão humana:** **PENDENTE** até a seção 8.1 ser preenchida.
- **Aceite funcional:** **PENDENTE** até a seção 8.2 ser preenchida.
- **Recebimento contratual:** não se aplica a este exercício. Nada foi aprovado ou homologado.

**Ocorrências registradas:**
- O primeiro commit de base incluiu `.claude/settings.local.json`, uma configuração local do app sem segredos. O arquivo foi retirado com `--amend` antes de qualquer publicação e ficou listado em `.git/info/exclude`.
- A primeira execução do script de mutação usou um padrão de busca errado (21 testes em vez de 13). O script foi corrigido e executado de novo. A saída válida está em `evidencias/07`.

## 8. Registro de revisão humana e aceite funcional

> **Esta seção é preenchida somente por uma pessoa.** O assistente (Claude) criou os campos, mas não preencheu nem marcou nenhum item. Enquanto os campos estiverem em branco, a revisão humana e o aceite funcional continuam **PENDENTES**.
>
> Como preencher: no GitHub, abra este arquivo e clique no lápis (Edit). Ou edite localmente e faça commit. Para marcar um item, troque `[ ]` por `[x]`. Marque só o que você de fato verificou.

### 8.1 Revisão humana (técnica)

| Campo | Preenchimento |
|---|---|
| Revisor(a) |  |
| Papel (participante, dupla, monitor ou professor) |  |
| Data |  |
| Commit revisado |  |

**Itens conferidos**
- [X] Li o diff da refatoração (`git show 0861508`) e entendi o que mudou.
- [X] Executei `python -m unittest discover -s tests -v` e obtive 13 testes OK.
- [X] Conferi que `classificar(30, True)` continua retornando `"NO_PRAZO"`.
- [X] Conferi que nenhum teste foi removido ou enfraquecido (`git show 1f0dc79`).
- [X] Li os riscos residuais (seção 5) e concordo que estão registrados corretamente.

**Resultado**
- [X] Aprovado
- [ ] Aprovado com ressalvas
- [ ] Reprovado

**Ressalvas / observações:**

&nbsp;

### 8.2 Aceite funcional

Responsável: o **gestor do negócio**, que neste exercício é o participante designado em sala (`docs/demanda.md:2`).

| Campo | Preenchimento |
|---|---|
| Nome |  |
| Data |  |

**Critérios conferidos**
- [ ] RF-01 preservado: sem documentos, o resultado é PENDENTE em qualquer idade.
- [ ] RN-01 preservado: com documentos, 30 dias é NO_PRAZO e 31 dias é ATRASADA.
- [ ] As saídas de `processar_csv` e `relatorio_texto` para `dados/solicitacoes.csv` estão iguais às de antes da mudança.
- [ ] Ciente de que o RF-02 (aviso entre 25 e 30 dias) **não** faz parte desta entrega.

**Decisão**
- [ ] Aceito
- [ ] Aceito com ressalvas
- [ ] Não aceito

**Observações:**

&nbsp;

> **Recebimento contratual:** não se aplica a este exercício didático.
