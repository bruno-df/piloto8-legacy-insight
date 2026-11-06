"""Comparação diferencial: servico.py original x refatorado.

Uso: python comparar_antes_depois.py <raiz_do_projeto> <servico_original.py>
Não altera nenhum arquivo. Imprime o total de casos e as divergências.
"""
import importlib.util
import sys

raiz, caminho_original = sys.argv[1], sys.argv[2]
sys.path.insert(0, raiz)

spec = importlib.util.spec_from_file_location("servico_original", caminho_original)
original = importlib.util.module_from_spec(spec)
spec.loader.exec_module(original)
import src.servico as novo  # noqa: E402

H = "protocolo,dias,documentos\n"
casos = {}

# 1. Arquivo de dados fictícios do laboratório.
with open(raiz + "/dados/solicitacoes.csv", encoding="utf-8", newline="") as f:
    casos["dados/solicitacoes.csv"] = f.read()

# 2. Matriz de linhas únicas: dias x grafias de documentos.
dias_lista = [str(d) for d in range(0, 41)] + ["99", "100", "1000", " 7", "+3", "007"]
docs_lista = ["sim", "nao", " SIM ", "Nao", "NAO ", "sIm"]
for d in dias_lista:
    for doc in docs_lista:
        casos[f"linha dias={d!r} doc={doc!r}"] = H + f"A,{d},{doc}\n"

# 3. Lote grande com todas as combinações (testa ordem e resumo).
linhas = [f"P{i},{d},{doc}" for i, (d, doc) in
          enumerate((d, doc) for d in dias_lista for doc in docs_lista)]
casos["lote combinado"] = H + "\n".join(linhas) + "\n"

# 4. Entradas inválidas e de borda (devem falhar igual).
invalidos = {
    "vazio": H,
    "sem cabecalho": "",
    "cabecalho invertido": "dias,protocolo,documentos\n",
    "cabecalho com espaco": "protocolo, dias,documentos\n",
    "duplicado": H + "A,1,sim\n A ,2,nao\n",
    "protocolo vazio": H + ",1,sim\n",
    "dias abc": H + "A,abc,sim\n",
    "dias negativo": H + "A,-1,sim\n",
    "dias vazio": H + "A,,sim\n",
    "dias decimal": H + "A,1.5,sim\n",
    "documentos talvez": H + "A,2,talvez\n",
    "documentos vazio": H + "A,2,\n",
    "coluna faltando": H + "A,1\n",
    "so protocolo": H + "A\n",
    "coluna extra": H + "A,1,sim,extra\n",
    "erro na segunda linha": H + "A,1,sim\nB,x,sim\n",
    "CRLF": "protocolo,dias,documentos\r\nA,30,sim\r\nB,31,nao\r\n",
}
casos.update(invalidos)


def executar(func, texto):
    try:
        r = func(texto)
        return ("ok", r, type(r).__name__)
    except Exception as e:  # compara tipo e mensagem da exceção
        return ("erro", type(e).__name__, str(e))


divergencias = []
for nome, texto in casos.items():
    for funcao in ("processar_csv", "relatorio_texto"):
        a = executar(getattr(original, funcao), texto)
        b = executar(getattr(novo, funcao), texto)
        if a != b:
            divergencias.append((nome, funcao, a, b))
    r = executar(novo.processar_csv, texto)
    if r[0] == "ok":
        for item in r[1]["itens"]:
            if type(item["situacao"]) is not str or type(item["documentos"]) is not bool:
                divergencias.append((nome, "tipos", item, None))

print(f"Python {sys.version.split()[0]}")
print(f"Casos de entrada: {len(casos)}  |  comparações: {len(casos) * 2}")
print(f"Divergências: {len(divergencias)}")
for d in divergencias:
    print("  DIVERGE:", d)
print("Amostra de erros iguais nas duas versões:")
for nome in ("coluna faltando", "coluna extra", "dias decimal", "CRLF"):
    print(f"  {nome}: {executar(novo.processar_csv, casos[nome])}")
sys.exit(1 if divergencias else 0)
