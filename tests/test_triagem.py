import unittest
from src.triagem import classificar

class Caracterizacao(unittest.TestCase):
    def test_CA01_precedencia_documental(self):
        for d in (0, 29, 30, 31, 100):
            self.assertEqual(classificar(d, False), "PENDENTE")
    def test_CA02_limite_30(self):
        self.assertEqual(classificar(30, True), "NO_PRAZO")
    def test_CA03_apos_limite(self):
        self.assertEqual(classificar(31, True), "ATRASADA")
    def test_CA04_antes_limite(self):
        for d in (0, 1, 25, 29):
            self.assertEqual(classificar(d, True), "NO_PRAZO")
