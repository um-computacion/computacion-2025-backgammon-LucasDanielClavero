import unittest
from unittest.mock import patch
from core.dice import Dice  # Asegúrate de que la ruta de importación sea correcta

class TestDice(unittest.TestCase):
    """
    Pruebas unitarias para la clase Dice.
    Estas pruebas verifican la inicialización, el lanzamiento de dados
    y la obtención de movimientos tanto para tiradas normales como para dobles.
    """

    def setUp(self):
        """
        Este método se ejecuta antes de cada prueba.
        Crea una nueva instancia de la clase Dice.
        """
        self.dice = Dice()

    def test_initial_state(self):
        """
        Verifica que los dados se inicializan en un estado correcto.
        - Los valores deben estar vacíos al principio.
        - No debería haber movimientos disponibles antes del primer lanzamiento.
        """
        self.assertEqual(self.dice._values_, [])
        self.assertEqual(self.dice.get_moves(), [])

    @patch('random.randint')
    def test_roll_dice(self, mock_randint):
        """
        Prueba que el método roll() genera y devuelve dos valores aleatorios.
        Se utiliza un mock para simular la generación de números y asegurar
        que los valores internos de la clase se actualizan correctamente.
        """
        # Configuramos el mock para que devuelva 3 y 5 en llamadas sucesivas
        mock_randint.side_effect = [3, 5]

        # Realizamos el lanzamiento
        result = self.dice.roll()

        # Verificamos que el resultado y el estado interno son los esperados
        self.assertEqual(result, [3, 5])
        self.assertEqual(self.dice._values_, [3, 5])