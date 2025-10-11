import unittest
from unittest.mock import Mock, patch, call
import sys
import os

# --- Configuración de la ruta para la importación ---
# Esto permite que el script de prueba encuentre los módulos 'core' y 'cli'
# al ejecutarse desde el directorio raíz del proyecto.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
# ----------------------------------------------------

from cli.cli import CLI
from core.player import Player # Necesitamos Player para crear un mock

class TestCLI(unittest.TestCase):

    def setUp(self):
        """Se ejecuta antes de cada prueba. Crea mocks para las dependencias."""
        # Creamos un mock del juego. Esto nos permite controlar su comportamiento
        # y verificar qué métodos son llamados por la CLI.
        self.mock_game = Mock()
        self.mock_game.get_current_player.return_value = Player("Test Player", "white")
        
        # Instanciamos la CLI con el juego mockeado.
        self.cli = CLI(self.mock_game)

    @patch('builtins.input', side_effect=['12', '5'])
    def test_handle_normal_turn_valid_move(self, mock_input):
        """
        Prueba que _handle_normal_turn_ llama a attempt_move con los datos correctos
        cuando el usuario ingresa un movimiento válido.
        """
        # Configuramos los movimientos disponibles en el mock del juego
        self.mock_game._moves_ = [5, 3]
        
        self.cli._handle_normal_turn_()
        
        # Verificamos que se llamó a attempt_move con los argumentos correctos
        self.mock_game.attempt_move.assert_called_once_with(12, 5)

    @patch('builtins.input', return_value='p')
    def test_handle_normal_turn_pass(self, mock_input):
        """
        Prueba que si el usuario ingresa 'p', se vacía la lista de movimientos
        y no se intenta mover ninguna ficha.
        """
        self.mock_game._moves_ = [5, 3]
        
        self.cli._handle_normal_turn_()
        
        # Verificamos que la lista de movimientos se vació para pasar el turno
        self.assertEqual(self.mock_game._moves_, [])
        # Verificamos que NO se intentó mover una ficha
        self.mock_game.attempt_move.assert_not_called()

    @patch('builtins.input', return_value='3')
    def test_handle_reentry_turn_valid(self, mock_input):
        """
        Prueba que se llama a attempt_reentry cuando un jugador en la barra
        ingresa un dado válido para reingresar.
        """
        self.mock_game._moves_ = [3, 4]
        player = self.mock_game.get_current_player()
        
        # Simulamos que el reingreso es posible con el dado 3
        self.mock_game._board_.is_reentry_possible.return_value = True

        self.cli._handle_reentry_turn_(player)
        
        # Verificamos que se intentó el reingreso con el dado correcto
        self.mock_game.attempt_reentry.assert_called_once_with(3)

    @patch('builtins.print') # Silenciamos el print para que no ensucie la salida del test
    def test_handle_reentry_turn_no_possible_moves(self, mock_print):
        """
        Prueba que si no hay movimientos de reingreso posibles, el turno se pierde
        (la lista de movimientos se vacía).
        """
        self.mock_game._moves_ = [3, 4]
        player = self.mock_game.get_current_player()

        # Simulamos que el reingreso NO es posible con ningún dado
        self.mock_game._board_.is_reentry_possible.return_value = False
        
        self.cli._handle_reentry_turn_(player)

        # Verificamos que NO se intentó reingresar
        self.mock_game.attempt_reentry.assert_not_called()
        # Verificamos que el turno del jugador se terminó
        self.assertEqual(self.mock_game._moves_, [])

    @patch('builtins.input', side_effect=['not_a_number', '7', '5'])
    @patch('builtins.print')
    def test_get_player_input_for_dice_validation(self, mock_print, mock_input):
        """
        Prueba que la entrada de dados se valida correctamente:
        1. Rechaza entradas no numéricas.
        2. Rechaza dados que no están en la lista de movimientos.
        3. Acepta un dado válido.
        """
        self.mock_game._moves_ = [5, 2]
        
        result = self.cli._get_player_input_for_dice_("Elige un dado: ")

        self.assertEqual(result, 5)
        # Verificamos que se llamó a input 3 veces
        self.assertEqual(mock_input.call_count, 3)
        # Verificamos los mensajes de error que se le mostraron al usuario
        mock_print.assert_any_call("Entrada inválida. Por favor, ingresa un número.")
        mock_print.assert_any_call("Ese no es un dado válido o disponible.")

    @patch('cli.cli.CLI._handle_normal_turn_')
    @patch('cli.cli.CLI._display_board_')
    def test_run_game_loop_normal_turn(self, mock_display, mock_handle_turn):
        """
        Prueba una iteración del bucle principal 'run' para un turno normal.
        Verifica la secuencia de llamadas a los métodos principales.
        """
        # Hacemos que is_game_over devuelva True después de la primera llamada
        # para que el bucle se ejecute solo una vez.
        self.mock_game.is_game_over.side_effect = [False, True]
        
        # Simulamos que no hay fichas en la barra
        self.mock_game._board_._bar_ = {'white': [], 'black': []}

        # Simulamos una tirada de dados
        # Usamos un `side_effect` para que `_moves_` se vacíe después de la llamada al handler
        def roll_side_effect():
            self.mock_game._moves_ = [4, 2]
        def handle_turn_side_effect():
            self.mock_game._moves_ = []
            
        self.mock_game.roll_dice.side_effect = roll_side_effect
        mock_handle_turn.side_effect = handle_turn_side_effect

        self.cli.run()

        # Verificamos la secuencia de llamadas
        mock_display.assert_called()
        self.mock_game.get_current_player.assert_called()
        self.mock_game.roll_dice.assert_called_once()
        mock_handle_turn.assert_called_once()
        self.mock_game.switch_turn.assert_called_once()


if __name__ == '__main__':
    unittest.main()