import unittest
from core.player import Player # Asegúrate de que la ruta de importación sea correcta

class TestPlayer(unittest.TestCase):
    """
    Pruebas unitarias para la clase Player.
    Estas pruebas verifican la correcta inicialización de los atributos
    de un jugador y su representación en formato de cadena de texto.
    """

    def setUp(self):
        """
        Este método se ejecuta antes de cada prueba.
        Crea instancias de Player que se usarán en los tests.
        """
        self.player1 = Player(name="Alice", color="White")
        self.player2 = Player(name="Bob", color="Black")

    def test_player_initialization(self):
        """
        Verifica que los atributos 'name' y 'color' se asignan
        correctamente al crear una instancia de Player.
        """
        self.assertEqual(self.player1._name_, "Alice")
        self.assertEqual(self.player1._color_, "White")

        self.assertEqual(self.player2._name_, "Bob")
        self.assertEqual(self.player2._color_, "Black")

    def test_player_representation(self):
        """
        Verifica que el método __repr__ devuelve una cadena con el formato
        esperado, lo cual es útil para la depuración y registros.
        """
        expected_repr_p1 = "Player(name='Alice', color='White')"
        expected_repr_p2 = "Player(name='Bob', color='Black')"

        self.assertEqual(repr(self.player1), expected_repr_p1)
        self.assertEqual(repr(self.player2), expected_repr_p2)


if __name__ == '__main__':
    unittest.main()