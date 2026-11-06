# Exemplos didáticos para comparação offline
Estas saídas foram redigidas como exercícios e não são transcrições do Claude.
Básica: "Vamos simplificar o código e considerar atrasada a demanda com 30 dias ou mais."
Problemas: altera RN-01, não caracteriza a ausência de documentos, não separa RF-02.
Intermediária: "Extrair funções e testar 31 dias. A aplicação ficará pronta para aceite."
Problemas: não testa a fronteira 30 e infere aceite de execução técnica.
Estruturada: "Preservar classificar(30, True)=NO_PRAZO. Testar sem documentos em 0/30/31.
Separar refatoração de sinalizar. CA05 cobre 25 e 30, CA06 cobre 24 e 31. Validação funcional pendente."
Rubrica por saída: limite 30, precedência, CA observáveis, lacunas, nenhuma aprovação fabricada.
Pontue 0/1 por critério. Compare também tempo de leitura e esforço de revisão, sem criar ranking geral.
