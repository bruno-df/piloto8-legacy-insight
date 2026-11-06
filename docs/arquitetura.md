# Contratos do serviço de lote
Entrada CSV: cabeçalho protocolo,dias,documentos nesta ordem, dias inteiro não negativo, documentos sim/nao.
Saída processar_csv: itens em ordem de entrada, códigos string, resumo com chaves fixas e total.
Saída relatorio_texto: protocolo:situacao, ordem preservada, sem quebra final.
Mensagens ValueError são parte do comportamento caracterizado neste exercício.
Inicial: src.servico mistura entrada, política e relatório, com regra duplicada.
Referência refatorada: leitura.ler_solicitacoes, triagem.classificar e relatorio.resumir/formatar.
O seam de entrada permite trocar CSV por adaptador futuro sem deslocar regra de domínio.
Não alterar sem revisão: normalização, ordem, mensagens, nomes públicos e tipo de retorno.
Dados fictícios: dados/solicitacoes.csv. Entrada malformada de colunas adicionais fica como risco conhecido fora dos testes atuais.
