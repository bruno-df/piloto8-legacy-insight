#!/usr/bin/env bash
# Teste de mutação: verifica se os testes detectam regras quebradas de propósito.
# Uso: bash mutacao.sh <raiz_do_projeto> <pasta_temporaria>
# Trabalha só em cópias dentro da pasta temporária; o projeto não é alterado.
P="$1"; T="$2"
prep() {  # monta uma cópia com o servico.py ORIGINAL (commit 6a19380) e os testes do commit 1f0dc79
  rm -rf "$T/m" && mkdir -p "$T/m/src" "$T/m/tests"
  for f in src/__init__.py src/servico.py src/triagem.py; do git -C "$P" show 6a19380:$f > "$T/m/$f"; done
  for f in tests/test_servico.py tests/test_triagem.py; do git -C "$P" show 1f0dc79:$f > "$T/m/$f"; done
}
com_original() {  # acrescenta os 8 testes do lote como estavam ANTES do teste novo
  git -C "$P" show 6a19380:tests/test_servico.py > "$T/m/tests/test_servico_original.py"
}
roda() { (cd "$T/m" && PYTHONDONTWRITEBYTECODE=1 python -m unittest "$@" 2>&1 | grep -E "^(FAIL|ERROR|Ran|OK|FAILED)"; echo "EXIT_CODE=${PIPESTATUS[0]}"); }

echo "== Controle: codigo original, sem mutacao, suite completa (13 testes)"
prep; roda discover -s tests

echo; echo "== Mutante 1: limite trocado de 'dias > 30' para 'dias >= 30' (viola RN-01)"
prep; sed -i 's/elif dias > 30:/elif dias >= 30:/' "$T/m/src/servico.py"; grep -n "dias >= 30" "$T/m/src/servico.py"
echo "-- suite completa:"; roda discover -s tests

echo; echo "== Mutante 2: PENDENTE so acima de 30 dias (viola RF-01 / precedencia documental)"
prep; com_original; sed -i 's/        if doc == "nao":/        if doc == "nao" and dias > 30:/' "$T/m/src/servico.py"; grep -n 'doc == "nao" and' "$T/m/src/servico.py"
echo "-- apenas os 8 testes ORIGINAIS do lote (antes do teste novo):"; roda tests/test_servico_original.py
echo "-- testes do lote COM o teste novo (9 testes):"; roda tests/test_servico.py
