import unittest
from src.servico import processar_csv, relatorio_texto
HEADER = "protocolo,dias,documentos\n"

class RegressaoServico(unittest.TestCase):
    def test_lote_contrato_estrutura_e_ordem(self):
        result = processar_csv(HEADER + "B,30,sim\nA,31,sim\nC,99,nao\n")
        self.assertEqual(result, {"itens": [
            {"protocolo":"B","dias":30,"documentos":True,"situacao":"NO_PRAZO"},
            {"protocolo":"A","dias":31,"documentos":True,"situacao":"ATRASADA"},
            {"protocolo":"C","dias":99,"documentos":False,"situacao":"PENDENTE"}],
            "resumo":{"PENDENTE":1,"NO_PRAZO":1,"ATRASADA":1},"total":3})
    def test_relatorio_sem_newline_final(self):
        self.assertEqual(relatorio_texto(HEADER+"B,30,sim\nA,31,sim\n"),"B:NO_PRAZO\nA:ATRASADA")
    def test_vazio_valido(self):
        self.assertEqual(processar_csv(HEADER)['total'],0)
        self.assertEqual(relatorio_texto(HEADER),"")
    def test_normalizacao_documentos(self):
        self.assertEqual(processar_csv(HEADER+" X ,1, SIM \n")['itens'][0]['protocolo'],'X')
    def test_cabecalho_publico(self):
        with self.assertRaisesRegex(ValueError,'^cabecalho invalido$'): processar_csv('dias,protocolo,documentos\n')
    def test_protocolo_duplicado(self):
        with self.assertRaisesRegex(ValueError,'^protocolo vazio ou duplicado$'): processar_csv(HEADER+'A,1,sim\n A ,2,nao\n')
    def test_dias_invalidos(self):
        for valor in ('abc','-1',''):
            with self.subTest(valor=valor):
                with self.assertRaisesRegex(ValueError,'^dias invalidos$'): processar_csv(HEADER+'A,'+valor+',sim\n')
    def test_documentos_invalidos(self):
        with self.assertRaisesRegex(ValueError,'^documentos invalidos$'): processar_csv(HEADER+'A,2,talvez\n')
