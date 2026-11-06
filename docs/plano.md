# Plano de referência didático
1. Inventariar src/triagem.py e contrato em docs/demanda.md. Nenhuma escrita.
2. Rodar quatro testes iniciais. Registrar ambiente, logs e retorno.
3. Revisar caracterização: documentos, dia 30, dia 31 e valores antes do limite.
4. Refatorar representação interna sem alterar retorno string da função pública.
5. Rodar testes e diff. Em caso de falha, parar e localizar a menor mudança causal.
6. Separar RF-02 em outro incremento, acrescentando sinalizar e testes CA05..07.
7. Gerar matriz com hashes e resultados. Revisão, homologação e recebimento permanecem pendentes.
Rollback didático: abrir nova cópia de inicial. Não apagar pasta de trabalho existente.
Risco: confundir Enum com novo tipo de retorno; manter .value na interface pública.
Decisão: uso de Enum é uma alternativa didática, não imposição arquitetural.
