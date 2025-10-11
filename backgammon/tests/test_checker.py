import unittest
from core.checker import Checker # Asegúrate de que la ruta de importación sea correcta

class TestChecker(unittest.TestCase):

    def test_checker_creation_and_color_attribute(self):
        """
        Verifica que el color de la ficha se asigna correctamente durante la creación.
        """
        checker = Checker(color='white')
        self.assertEqual(checker._color_, 'white')

    def test_checker_representation(self):
        """
        Verifica que la representación en string del objeto Checker sea la correcta.
        """
        checker = Checker(color='black')
        expected_repr = "Checker(color='black')"
        self.assertEqual(repr(checker), expected_repr)

if __name__ == '__main__':
    unittest.main()
