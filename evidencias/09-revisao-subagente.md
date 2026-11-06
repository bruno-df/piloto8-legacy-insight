# Revisão independente: subagente `revisor-regressao`

- **Origem:** subagente do projeto (`.claude/agents/revisor-regressao.md`), com ferramentas apenas de leitura (Read, Grep, Glob). Ele não executa comandos.
- **Data:** 2026-11-06, depois do commit `0861508`.
- **Natureza:** saída de modelo. **Não é revisão humana.** A revisão humana continua PENDENTE.
- **Pedido feito a ele:** verificar a equivalência de `processar_csv` e `relatorio_texto`, a precedência documental, o dia 30 e o dia 31, os riscos da importação relativa, os riscos residuais e se algo foi além do escopo autorizado. A versão original do `servico.py` foi entregue para comparação.

Abaixo está a transcrição do relatório devolvido. Os comentários do coordenador estão marcados com **[Nota]**.

---

**Status:** testes NÃO EXECUTADOS pelo subagente. Revisão humana PENDENTE. As regras de prazo são fictícias (docs/demanda.md), não do PDS.

**[Nota]** Os testes foram executados pelo coordenador; ver `01`, `02` e `10`.

## Comprovado pela leitura

1. **Equivalência** (src/servico.py:24-30 contra o original:22-33).
   - O trecho das linhas 9-26 é idêntico ao original: mensagens, `from None` e a ordem de validação (cabeçalho, protocolo, dias, documentos).
   - Depois da validação da linha 25, `doc` só pode ser "sim" ou "nao". Logo, `not (doc == "sim")` equivale a `doc == "nao"`.
   - `classificar` (src/triagem.py:3-7) segue a mesma precedência: documentos primeiro, depois `> 30`.
   - O campo `documentos` é o mesmo booleano de antes, e `classificar` não lança exceção para int e bool.
   - Resumo, total, ordem e `relatorio_texto` não mudaram. Sem achado.
2. **Garantias.** CA-01 a CA-03 estão em tests/test_triagem.py:5-11. No lote, ficam cobertas por tests/test_servico.py:30-37 (0, 30 e 31 dias, com "sim" e "nao") e :6-12. O teste novo também pegaria o erro de passar `doc` (texto, sempre verdadeiro) no lugar de `documentos`.
3. **Importação relativa** (src/servico.py:4).
   - Condição: `python src/servico.py`, `import servico` com `src/` no sys.path, ou carga via `spec_from_file_location`.
   - Esperado: importar como antes.
   - Observado, pela semântica do Python e sem execução: ImportError "attempted relative import with no known parent package".
   - Teste ausente: nenhum cobre isso, porque a suíte só importa `src.servico` a partir da raiz.
   - Para mocks, o alvo passa a ser `src.servico.classificar`.
4. **Riscos antigos, mantidos pela troca:**
   - **Coluna faltando.** Uma linha `A,1` gera `AttributeError` (`None.strip()`) em vez de `ValueError`, que é o esperado pela docs/arquitetura.md:5. Não há teste para isso. Já uma linha `A` gera `ValueError` "dias invalidos".
   - **Coluna extra.** `A,1,sim,x` é aceita e a coluna extra é ignorada sem aviso. É risco conhecido (docs/arquitetura.md:10) e não há teste.
   - **Tipos.** Em tests/test_servico.py:8, `assertEqual` não distingue `True` de `1` nem `30` de `30.0`.
   - **Nome do teste.** O teste novo não tem ID de CA no nome, embora o comentário cite CA-01..03 (docs/demanda.md:12).
5. **Escopo.** Não há mudança funcional nem dependência externa: a importação é interna, então o RNF-01 continua atendido. Nenhum teste foi removido. Teste e refatoração estão em commits separados. O commit inicial passou por amend, e o subagente não conseguiu verificar se a base corresponde à cópia limpa.

**[Nota]** Isso foi verificado pelo coordenador em `03-hashes-sha256.txt`: os 6/6 arquivos são idênticos, com diferença só no fim de linha CRLF→LF.

**[Nota]** Quanto aos tipos, a comparação diferencial (`06`) verifica que `situacao` é `str` e `documentos` é `bool` em todas as saídas.

## Hipóteses (não comprovadas)

- **RF-02 como novo código de retorno de `classificar`.**
  - src/servico.py lançaria KeyError, porque as chaves do resumo são fixas.
  - Testes existentes falhariam, e a regra `classificar(30, True) == "NO_PRAZO"` (CLAUDE.md) seria violada.
  - Com o acoplamento, qualquer mudança em `classificar` passa direto para o lote.
  - Recomendação: um sinal separado (`sinalizar`, docs/plano.md:6) e decisão do gestor sobre expor o aviso no serviço.
- **CA-05 a CA-07 ainda não existem.** Casos esperados:
  - 24 dias com documentos: sem aviso;
  - 25 dias: com aviso;
  - 30 dias: com aviso e NO_PRAZO;
  - 31 dias: sem aviso e ATRASADA;
  - 25 a 30 dias sem documentos: sem aviso e PENDENTE.

  O `dados/solicitacoes.csv` já tem esses dias, mas não é usado em teste.
- **Delegação sem teste estrutural.** Se alguém reintroduzir a regra duplicada no serviço, os testes continuam passando, desde que a cópia esteja correta.
