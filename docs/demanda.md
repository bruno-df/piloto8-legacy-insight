# DEM-001 Triagem de solicitações fictícias
Solicitante: unidade didática. Gestor do negócio: participante designado em sala.
Problema: módulo legado mistura classificação e apresentação. Preservar os resultados.
RF-01: sem documentos, a situação é PENDENTE independentemente da idade.
Com documentos, idade maior que 30 resulta ATRASADA, demais casos NO_PRAZO.
RN-01: o dia 30 continua no prazo. Dias corridos já calculados na entrada.
RF-02: adicionar aviso entre 25 e 30 dias, inclusive, somente com documentos.
HU-01: como analista de triagem, quero aviso antecipado para organizar a fila.
Escopo: função pura local, sem calendários, feriados, dados pessoais ou APIs reais.
Tipos esperados: dias inteiro não negativo e documentos booleano. Validação de entradas fora
desse domínio é questão aberta para um incremento futuro, não correção silenciosa.
Aceite: CA-01..04 caracterização, CA-05..07 aviso. Nomes de testes contêm esses IDs.
RNF-01: executar offline em Python 3.11+, sem dependências de terceiros no laboratório.
G3: simulação didática, sem aprovação institucional. Requisitos devem passar por validação funcional.
