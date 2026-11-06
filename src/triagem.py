def classificar(dias, documentos):
    # Regra fictícia do laboratório. Prazo em dias corridos.
    if not documentos:
        return "PENDENTE"
    if dias > 30:
        return "ATRASADA"
    return "NO_PRAZO"
