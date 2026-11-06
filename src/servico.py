import csv
from io import StringIO

from .triagem import classificar

def processar_csv(texto):
    # Legado: parsing, validação e resumo no mesmo módulo; a classificação é de src.triagem.
    reader = csv.DictReader(StringIO(texto))
    if reader.fieldnames != ["protocolo", "dias", "documentos"]:
        raise ValueError("cabecalho invalido")
    itens = []
    vistos = set()
    for linha in reader:
        protocolo = linha["protocolo"].strip()
        if not protocolo or protocolo in vistos:
            raise ValueError("protocolo vazio ou duplicado")
        vistos.add(protocolo)
        try:
            dias = int(linha["dias"])
        except (ValueError, TypeError):
            raise ValueError("dias invalidos") from None
        if dias < 0:
            raise ValueError("dias invalidos")
        doc = linha["documentos"].strip().lower()
        if doc not in ("sim", "nao"):
            raise ValueError("documentos invalidos")
        documentos = doc == "sim"
        situacao = classificar(dias, documentos)
        itens.append({"protocolo": protocolo, "dias": dias,
                      "documentos": documentos, "situacao": situacao})
    contagem = {"PENDENTE": 0, "NO_PRAZO": 0, "ATRASADA": 0}
    for item in itens:
        contagem[item["situacao"]] += 1
    return {"itens": itens, "resumo": contagem, "total": len(itens)}

def relatorio_texto(texto):
    dados = processar_csv(texto)
    return "\n".join(item["protocolo"] + ":" + item["situacao"] for item in dados["itens"])
