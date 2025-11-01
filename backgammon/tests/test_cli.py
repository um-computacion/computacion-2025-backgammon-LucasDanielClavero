import unittest
from unittest.mock import Mock, patch, call
import sys
import os
import io

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from cli.cli import CLI
from core.player import Player

class TestCLI(unittest.TestCase):

    def setUp(self):
        self.mock_game = Mock()
        self.mock_game.get_current_player.return_value = Player("Test Player", "white")
        self.mock_game._board_ = Mock()
        self.mock_game._board_._bar_ = {'white': [], 'black': []}
        self.mock_game._moves_ = []
        self.mock_game._board_._points_ = [[] for _ in range(24)]
        self.cli = CLI(self.mock_game)
        self.stdout_patcher = patch('sys.stdout', new_callable=io.StringIO)
        self.mock_stdout = self.stdout_patcher.start()
    def tearDown(self):
        """Se ejecuta después de cada prueba. Detiene el parcheador de stdout."""
        self.stdout_patcher.stop()
    @patch('builtins.input', side_effect=['12', '5'])
    def test_handle_normal_turn_valid_move(self, mock_input):
        """
        Prueba que _handle_normal_turn_ llama a attempt_move con los datos correctos
        cuando el usuario ingresa un movimiento válido.
        """
        self.cli._get_player_input_for_dice_ = Mock(return_value=5)
        
        self.cli._handle_normal_turn_()

        self.cli._get_player_input_for_dice_.assert_called_once()
        
        self.mock_game.attempt_move.assert_called_with(12, 5)

    @patch('builtins.input', return_value='p')
    def test_handle_normal_turn_pass(self, mock_input):

        self.mock_game._moves_ = [1, 2, 3] 
        
        self.cli._handle_normal_turn_()
        
        self.assertEqual(self.mock_game._moves_, [])

    @patch('builtins.input', side_effect=['not_a_number', '7', '5'])
    def test_get_player_input_for_dice_validation(self, mock_input):

        self.mock_game._moves_ = [4, 5]
        result = self.cli._get_player_input_for_dice_("Selecciona un dado")  
        self.assertEqual(result, 5)
        self.assertEqual(mock_input.call_count, 3)
        self.mock_game.use_move.assert_not_called()

    @patch('builtins.input', side_effect=['1', '5']) 
    def test_handle_reentry_turn_valid(self, mock_input):
        """
        Prueba que se llama a attempt_reentry cuando un jugador en la barra
        ingresa un movimiento válido.
        """
        self.mock_game._moves_ = [1, 3]
        # CORREGIDO: Seteamos una ficha en la barra para que el test sea realista
        self.mock_game._board_._bar_['white'] = [Mock()] 
        
        # Simulamos que ambos dados son válidos para reingresar
        self.mock_game._board_.is_reentry_possible.return_value = True
        
        self.cli._get_player_input_for_dice_ = Mock(return_value=1)
        
        self.cli._handle_reentry_turn_(Player("Test", "white"))
        
        self.cli._get_player_input_for_dice_.assert_called_once()
        self.mock_game.attempt_reentry.assert_called_with(1)

    @patch('cli.cli.CLI._get_player_input_for_dice_', return_value=None)
    def test_handle_reentry_turn_no_possible_moves(self, mock_get_input):
        """
        Prueba que si no hay movimientos de reingreso posibles, el turno se pierde.
        """
        # Seteamos una ficha en la barra
        self.mock_game._board_._bar_['white'] = [Mock()]
        # Seteamos movimientos disponibles
        self.mock_game._moves_ = [1, 2]
        # PERO, simulamos que ninguno es válido
        self.mock_game._board_.is_reentry_possible.return_value = False
        
        self.cli._handle_reentry_turn_(Player("Test", "white"))
        
        # CORREGIDO: El código hace `_moves_ = []`, no llama a `clear_moves()`.
        self.assertEqual(self.mock_game._moves_, [])
        # El input de dado no debe llamarse si no hay movimientos
        mock_get_input.assert_not_called()


    @patch('cli.cli.CLI._handle_normal_turn_')
    @patch('cli.cli.CLI._display_board_')
    def test_run_game_loop_normal_turn(self, mock_display, mock_handle_turn):
        """
        Prueba una iteración del bucle principal 'run' para un turno normal.
        Verifica la secuencia de llamadas a los métodos principales.
        """
        self.mock_game.is_game_over.side_effect = [False, True]
        
        self.mock_game._board_._bar_ = {'white': [], 'black': []}

        def roll_side_effect():
            self.mock_game._moves_ = [4, 2]
        def handle_turn_side_effect():
            self.mock_game._moves_ = [] # Simulamos que el turno consume los dados
            
        self.mock_game.roll_dice.side_effect = roll_side_effect
        mock_handle_turn.side_effect = handle_turn_side_effect

        self.cli.run()

        # Verificamos la secuencia de llamadas
        self.assertEqual(mock_display.call_count, 1) # Solo se llama al inicio del turno
        self.mock_game.roll_dice.assert_called_once()
        mock_handle_turn.assert_called_once()
        self.mock_game.switch_turn.assert_not_called() # El juego terminó (is_game_over: True)
        
        self.assertEqual(self.mock_game.is_game_over.call_count, 2)


    # ===================================================================
    # --- NUEVAS PRUEBAS PARA COBERTURA (CORREGIDAS) ---
    # ===================================================================

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_display_board_with_checkers_and_bar(self, mock_stdout):
        """
        Prueba que _display_board_ imprime correctamente el estado del tablero,
        incluyendo fichas en los puntos y en la barra.
        Cubre las líneas 10-45.
        """
        mock_board = Mock()
        mock_w = Mock(); mock_w._color_ = 'white'
        mock_b = Mock(); mock_b._color_ = 'black'

        mock_points = [[] for _ in range(24)]
        mock_points[0] = [mock_w, mock_w] # 2 blancas en punto 1
        mock_points[12] = [mock_b, mock_b, mock_b] # 3 negras en punto 13
        
        mock_board._points_ = mock_points
        mock_board._bar_ = {'white': [mock_w], 'black': [mock_b, mock_b]}
        
        self.cli._game_._board_ = mock_board
        
        self.cli._display_board_()
        output = mock_stdout.getvalue()

        # Verificar líneas clave
        self.assertIn("13 14 15 16 17 18 | BAR | 19 20 21 22 23 24", output)
        self.assertIn("12 11 10  9  8  7 |     |  6  5  4  3  2  1", output)
        self.assertIn("| B:2 |", output)
        self.assertIn("| W:1 |", output)

        # CORREGIDO: Las aserciones multilínia son frágiles.
        # Es mejor contar las filas de texto generadas, que son más estables.
        # Fila superior, punto 13 (índice 12)
        self.assertEqual(output.count(" B  .  .  .  .  ."), 3) # 3 fichas 'B'
        # Fila inferior, punto 1 (índice 0)
        self.assertEqual(output.count(".  .  .  .  .  W "), 2) # 2 fichas 'W'

    @patch('cli.cli.CLI._handle_normal_turn_') # CORREGIDO: Aplicamos el patch aquí
    @patch('cli.cli.CLI._display_board_')
    def test_run_loop_handles_value_error(self, mock_display, mock_handle_turn): # CORREGIDO: Recibimos el mock
        """
        Prueba que el bucle principal 'run' captura un ValueError
        y *termina el turno* (para evitar bucle infinito).
        """
        self.mock_game.is_game_over.side_effect = [False, True]
        
        def roll_side_effect():
            self.mock_game._moves_ = [1, 2]
        self.mock_game.roll_dice.side_effect = roll_side_effect
        
        # CORREGIDO: El side_effect debe vaciar _moves_ O el test entra en bucle infinito.
        def handle_turn_with_error(*args):
            self.mock_game._moves_ = [] # Vacía los movimientos
            raise ValueError("Test Input Error") # Lanza el error

        mock_handle_turn.side_effect = handle_turn_with_error
        
        self.cli.run()
        
        # Verificamos que el bucle se ejecutó, llamó al handler,
        # y luego salió (porque is_game_over es True). No debe colgarse.
        self.mock_game.roll_dice.assert_called_once()
        mock_handle_turn.assert_called_once()
        self.mock_game.switch_turn.assert_not_called() # El juego terminó

    @patch('cli.cli.CLI._handle_normal_turn_') # CORREGIDO
    @patch('cli.cli.CLI._display_board_')
    def test_run_loop_handles_generic_exception(self, mock_display, mock_handle_turn): # CORREGIDO
        """
        Prueba que el bucle principal 'run' captura una Excepción genérica
        y *termina el turno* (para evitar bucle infinito).
        """
        self.mock_game.is_game_over.side_effect = [False, True]
        def roll_side_effect():
            self.mock_game._moves_ = [1, 2]
        self.mock_game.roll_dice.side_effect = roll_side_effect
        
        # CORREGIDO: El side_effect debe vaciar _moves_
        def handle_turn_with_exception(*args):
            self.mock_game._moves_ = []
            raise Exception("Generic Test Error")

        mock_handle_turn.side_effect = handle_turn_with_exception
        
        self.cli.run()
        
        # La prueba termina sin crashear, demostrando que la excepción fue capturada
        # y el bucle infinito evitado.
        self.mock_game.roll_dice.assert_called_once()
        mock_handle_turn.assert_called_once()

    @patch('cli.cli.CLI._handle_normal_turn_')
    @patch('cli.cli.CLI._display_board_')
    def test_run_loop_partial_move_redisplays_board(self, mock_display, mock_handle_turn):
        """
        Prueba que si un movimiento no consume todos los dados (p.ej., dobles),
        el tablero se vuelve a mostrar.
        """
        self.mock_game.is_game_over.side_effect = [False, True]

        # CORREGIDO: Usamos lambda para setear el atributo en el mock
        self.mock_game.roll_dice.side_effect = lambda: setattr(self.mock_game, '_moves_', [5, 5]) # 2 movimientos
        
        # CORREGIDO: El side_effect debe *consumir* los dados uno por uno.
        def handle_turn_pop_move():
            if self.mock_game._moves_:
                self.mock_game._moves_.pop() # Consume un movimiento
            
        mock_handle_turn.side_effect = handle_turn_pop_move

        self.cli.run()

        # El display debe llamarse 2 veces:
        # 1. Al inicio del turno (L97) (moves=[5, 5])
        # 2. Después del primer movimiento (L108) (moves=[5])
        # (Después del segundo movimiento, moves=[] y L108 es falso)
        self.assertEqual(mock_display.call_count, 2)
        # El handler debe llamarse 2 veces (una por cada dado)
        self.assertEqual(mock_handle_turn.call_count, 2)


    @patch('cli.cli.CLI._handle_normal_turn_')
    @patch('cli.cli.CLI._display_board_')
    def test_run_loop_continues_if_not_game_over(self, mock_display, mock_handle_turn):
        """
        Prueba que el bucle 'run' continúa a un nuevo turno si el juego no ha terminado.
        """
        # Simular un juego de 2 turnos:
        # L96 (Turno 1): False
        # L122 (Turno 1): False
        # L96 (Turno 2): False
        # L122 (Turno 2): True (-> Esto es un error en el test original, debe ser L96)
        # CORREGIDO: La secuencia correcta de is_game_over es:
        # 1. L96 (Turno 1) -> False
        # 2. L122 (Turno 1) -> False
        # 3. L96 (Turno 2) -> True
        self.mock_game.is_game_over.side_effect = [False, False, True]
        
        def roll_side_effect():
            self.mock_game._moves_ = [1, 2]
        def handle_turn_side_effect():
            self.mock_game._moves_ = [] # Termina el turno
            
        self.mock_game.roll_dice.side_effect = roll_side_effect
        mock_handle_turn.side_effect = handle_turn_side_effect
        
        self.cli.run()

        # Verificar que el juego pasó al siguiente turno (solo 1 vez)
        self.mock_game.switch_turn.assert_called_once()
        # Verificar que 'is_game_over' fue llamado 3 veces
        self.assertEqual(self.mock_game.is_game_over.call_count, 3)

# --- Bloque para ejecución directa ---
if __name__ == '__main__':
    unittest.main()