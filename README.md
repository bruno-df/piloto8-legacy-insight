# Piloto IA 08: Legacy Insight

Atividade de refatoração segura sobre o projeto didático `legacy_pds` (GovFlow Legacy Lab). É um caso **inteiramente fictício**, sem dados reais nem credenciais.

**Melhoria realizada:** `src/servico.py` tinha uma cópia da regra de classificação. Agora ele usa `src/triagem.py:classificar`, e a regra fica num lugar só. Regras de negócio, contratos, mensagens e saídas foram preservados.

- **Relatório completo:** [RELATORIO.md](RELATORIO.md)
- **Evidências:** pasta [evidencias/](evidencias/)

## Como verificar

```bash
python -m unittest discover -s tests -v
```

Resultado esperado: 13 testes, `OK` (Python 3.11 ou superior, sem dependências externas).

## Histórico

| Commit | Conteúdo |
|---|---|
| `6a19380` | Cópia original recebida (linha de base) |
| `1f0dc79` | Teste de caracterização do lote, adicionado antes da refatoração |
| `0861508` | Refatoração: o serviço delega a classificação a `triagem.classificar` |
| último | Relatório e evidências |

Para ver só a refatoração:

```bash
git show 0861508
```

## Evidências

| Arquivo | Conteúdo |
|---|---|
| `01-testes-antes.txt` | Testes na cópia original: 12 OK, código de saída 0 |
| `02-testes-depois-refatoracao.txt` | Testes depois da refatoração: 13 OK, código de saída 0 |
| `03-hashes-sha256.txt` | Hashes antes e depois, e conferência do commit de base |
| `04-diff-teste-caracterizacao.txt` | Diff do teste novo |
| `05-diff-refatoracao.txt` | Diff da refatoração |
| `06-comparacao-antes-depois.txt` | Versão original contra a nova: 301 entradas, 0 divergências |
| `07-teste-mutacao.txt` | Regras quebradas de propósito são detectadas pelo teste novo |
| `08-git-log.txt` | Histórico, status e remoto |
| `09-revisao-subagente.md` | Revisão independente (saída de modelo, não humana) |
| `10-testes-final.txt` | Testes na versão entregue |
| `scripts/` | Scripts usados na comparação e na mutação |

A revisão humana e o aceite funcional estão **PENDENTES**.
