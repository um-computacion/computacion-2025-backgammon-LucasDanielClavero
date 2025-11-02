import unittest
from unittest.mock import Mock, patch

# Importamos la clase que vamos a probar
from core.backgammongame import BackgammonGame
# Importamos Player solo para verificar el tipo de retorno
from core.player import Player

# -----------------------------------------------------------------
# Clase de Ayuda: MockChecker
# -----------------------------------------------------------------
# La lógica de BackgammonGame (línea 32) mira el color de la ficha.
# Necesitamos simular eso para que la prueba de 'color incorrecto' funcione.
class MockChecker:
    def __init__(self, color):
        self._color_ = color
# -----------------------------------------------------------------


class TestBackgammonGame(unittest.TestCase):

    def setUp(self):
        """
        Se ejecuta ANTES de CADA prueba.
        Inicia el 'patch' (simulación) de 'Board' manualmente.
        """
        # 1. Iniciar el patch
        # Le decimos a unittest que reemplace 'core.backgammongame.Board'
        # (la clase Board DENTRO del archivo backgammongame) por un Mock.
        patcher = patch('core.backgammongame.Board')
        self.MockBoard = patcher.start() # Inicia el patch y nos da la CLASE Mock
        
        # 2. Asegurarse de que el patch se detenga después de la prueba
        self.addCleanup(patcher.stop) 
        
        # 3. Guardamos la INSTANCIA del mock (lo que self._board_ = Board() retorna)
        self.mock_board = self.MockBoard.return_value 
        
        # 4. Configuramos los mocks por defecto para un tablero "normal"
        self.configure_default_mocks()
        
        # 5. Ahora creamos la instancia del juego.
        # Su 'self._board_ = Board()' usará el mock automáticamente.
        self.game = BackgammonGame("Alice", "Bob")

    def configure_default_mocks(self):
        """
        Helper para resetear los mocks a un estado "normal" y vacío
        en cada prueba.
        """
        # Simulamos un tablero vacío
        self.mock_board._points_ = [[] for _ in range(24)]
        
        # Comportamientos por defecto
        self.mock_board.is_valid_move.return_value = True
        self.mock_board.is_reentry_possible.return_value = True
        self.mock_board.all_checkers_in_home_board.return_value = False
        self.mock_board.get_borne_off_count.return_value = 0

    # --- Pruebas Básicas (Estado Inicial) ---

    def test_initialization(self):
        """Prueba la inicialización del juego."""
        # Verifica que el constructor de Board fue llamado 1 vez
        self.MockBoard.assert_called_once() 
        # Verifica que el board del juego es la instancia mockeada
        self.assertIsInstance(self.game._board_, Mock)
        self.assertEqual(self.game._board_, self.mock_board)
        
        # Pruebas de estado inicial
        self.assertEqual(len(self.game._players_), 2)
        self.assertEqual(self.game._players_[0]._name_, "Alice")
        self.assertEqual(self.game._players_[0]._color_, "white")
        self.assertEqual(self.game._players_[1]._name_, "Bob")
        self.assertEqual(self.game._players_[1]._color_, "black")
        self.assertEqual(self.game._current_player_idx_, 0)
        self.assertEqual(self.game._moves_, [])

    def test_get_current_player(self):
        """Prueba que se obtiene el jugador actual."""
        player = self.game.get_current_player()
        self.assertIsInstance(player, Player)
        self.assertEqual(player._name_, "Alice")
        self.assertEqual(player._color_, "white")

    def test_switch_turn(self):
        """Prueba el cambio de turno."""
        self.assertEqual(self.game.get_current_player()._name_, "Alice")
        with patch('builtins.print'): # Silenciar el print
            self.game.switch_turn()
        self.assertEqual(self.game.get_current_player()._name_, "Bob")
        
    @patch('core.backgammongame.Dice')
    def test_roll_dice(self, MockDice):
        """Prueba la tirada de dados (mockeando Dice)."""
        # 1. Configurar el mock de Dice
        mock_dice_instance = MockDice.return_value
        mock_dice_instance.get_moves.return_value = [3, 4]
        mock_dice_instance._values_ = (3, 4)
        
        # 2. Inyectar el mock en el juego
        self.game._dice_ = mock_dice_instance
        
        # 3. Ejecutar y Verificar
        with patch('builtins.print'): # Silenciar prints
            self.game.roll_dice()
        
        self.assertEqual(self.game._moves_, [3, 4])
        mock_dice_instance.roll.assert_called_once()

        # 4. Prueba de dobles
        mock_dice_instance.get_moves.return_value = [5, 5, 5, 5]
        mock_dice_instance._values_ = (5, 5)
        with patch('builtins.print'):
            self.game.roll_dice()
        self.assertEqual(self.game._moves_, [5, 5, 5, 5])

    # --- Pruebas de Cobertura (Las que faltaban) ---

    def test_cover_attempt_move_invalid_start_point(self):
        """Cubre línea 27: 'if' (start_point fuera de rango 1-24)."""
        self.game._moves_ = [2]
        with patch('builtins.print'):
            result = self.game.attempt_move(start_point=0, dice_roll=2)
            self.assertFalse(result)
            result = self.game.attempt_move(start_point=25, dice_roll=2)
            self.assertFalse(result)
        
        self.assertEqual(self.game._moves_, [2]) # No se consume el dado
        self.mock_board.is_valid_move.assert_not_called()

    def test_cover_attempt_move_wrong_color(self):
        """Cubre línea 32: 'else' (ficha de color incorrecto)."""
        # El jugador es 'white' (Alice)
        # Ponemos una ficha NEGRA en el punto 12 (índice 11)
        self.mock_board._points_[11] = [MockChecker("black")]
        self.game._moves_ = [2]
        
        with patch('builtins.print'):
            result = self.game.attempt_move(start_point=12, dice_roll=2)
            
        self.assertFalse(result)
        self.assertEqual(self.game._moves_, [2]) # No se consume
        self.mock_board.is_valid_move.assert_not_called()
    
    def test_cover_attempt_move_blocked(self):
        """Cubre línea 96: 'else' (movimiento normal bloqueado)."""
        # Ficha en punto 12 (índice 11)
        self.mock_board._points_[11] = [MockChecker("white")]
        self.game._moves_ = [2] # Mover a punto 10
        
        # Configuramos el mock para RECHAZAR este movimiento
        self.mock_board.is_valid_move.return_value = False
        
        with patch('builtins.print'):
            result = self.game.attempt_move(start_point=12, dice_roll=2)
        
        self.assertFalse(result)
        self.assertEqual(self.game._moves_, [2])
        self.mock_board.is_valid_move.assert_called_with(12, 10, "white")
        self.mock_board.move_checker.assert_not_called()

    def test_cover_attempt_reentry_invalid(self):
        """Cubre líneas 107-110: 'else' en attempt_reentry (reingreso bloqueado)."""
        self.mock_board.is_reentry_possible.return_value = False
        self.game._moves_ = [3]
        
        with patch('builtins.print'): # Silenciar el print de error
            result = self.game.attempt_reentry(dice_roll=3)
        
        self.assertFalse(result)
        self.assertEqual(self.game._moves_, [3]) # No se consume el dado
        self.mock_board.reenter_checker.assert_not_called()

    def test_cover_is_game_over_black_wins(self):
        """Cubre líneas 116-119: 'elif' para la victoria de negras."""
        # Hacemos que get_borne_off_count retorne 0 para blancas y 15 para negras
        self.mock_board.get_borne_off_count.side_effect = [0, 15]
        
        with patch('builtins.print'): # Silenciar prints de victoria
            result = self.game.is_game_over()
        
        self.assertTrue(result)
        # Verificamos que se llamó dos veces (primero white, luego black)
        self.assertEqual(self.mock_board.get_borne_off_count.call_count, 2)

    # --- Pruebas de Cobertura: Lógica de Bear Off (Líneas 42-91) ---

    def test_cover_bear_off_premature(self):
        """Cubre líneas 64 y 89: 'else' (intento prematuro de bear off)."""
        # 1. Caso Blanco
        self.mock_board.all_checkers_in_home_board.return_value = False # NO están todas
        self.mock_board._points_[2] = [MockChecker("white")] # Ficha en punto 3
        self.game._moves_ = [5] # Intenta sacar con un 5 (end_point < 1)
        
        with patch('builtins.print'):
            result = self.game.attempt_move(start_point=3, dice_roll=5)
        
        self.assertFalse(result) # Falla porque no están todas en casa
        self.assertEqual(self.game._moves_, [5]) # Dado no se usa

        # 2. Caso Negro
        with patch('builtins.print'): self.game.switch_turn() # Turno de Negro
        self.mock_board.all_checkers_in_home_board.return_value = False # NO están todas
        self.mock_board._points_[21] = [MockChecker("black")] # Ficha en punto 22
        self.game._moves_ = [5] # Intenta sacar con un 5 (end_point > 24)
        
        with patch('builtins.print'):
            result = self.game.attempt_move(start_point=22, dice_roll=5)
        
        self.assertFalse(result)
        self.assertEqual(self.game._moves_, [5])

    def test_cover_bear_off_white_exact(self):
        """Cubre línea 46: Bear off exacto para blancas."""
        self.mock_board.all_checkers_in_home_board.return_value = True # SÍ están todas
        self.mock_board._points_[2] = [MockChecker("white")] # Ficha en punto 3
        self.game._moves_ = [3] # Dado exacto
        
        with patch('builtins.print'):
            result = self.game.attempt_move(start_point=3, dice_roll=3) # end_point == 0
        
        self.assertTrue(result)
        self.mock_board.bear_off_checker.assert_called_with(3)
        self.assertEqual(self.game._moves_, [])

    def test_cover_bear_off_black_exact(self):
        """Cubre línea 71: Bear off exacto para negras."""
        with patch('builtins.print'): self.game.switch_turn()
        
        self.mock_board.all_checkers_in_home_board.return_value = True
        self.mock_board._points_[21] = [MockChecker("black")] # Ficha en punto 22
        self.game._moves_ = [3] # Dado exacto (22 + 3 = 25)
        
        with patch('builtins.print'):
            result = self.game.attempt_move(start_point=22, dice_roll=3) # end_point == 25
        
        self.assertTrue(result)
        self.mock_board.bear_off_checker.assert_called_with(22)
        self.assertEqual(self.game._moves_, [])

    def test_cover_bear_off_white_overshoot_valid(self):
        """Cubre líneas 50-57: Overshoot válido para blancas."""
        self.mock_board.all_checkers_in_home_board.return_value = True
        # Ficha en punto 2 (índice 1). No hay fichas en 3,4,5,6.
        self.mock_board._points_[1] = [MockChecker("white")] 
        self.game._moves_ = [5] # Dado 5 (end_point = 2 - 5 = -3)
        
        # El bucle 'for i in range(start_idx + 1, 6)' no encontrará fichas.
        
        with patch('builtins.print'):
            result = self.game.attempt_move(start_point=2, dice_roll=5)
        
        self.assertTrue(result)
        self.mock_board.bear_off_checker.assert_called_with(2)
        self.assertEqual(self.game._moves_, [])

    def test_cover_bear_off_white_overshoot_invalid(self):
        """Cubre líneas 60-61: Overshoot inválido para blancas."""
        self.mock_board.all_checkers_in_home_board.return_value = True
        # Ficha en punto 2 (índice 1) Y en punto 4 (índice 3)
        self.mock_board._points_[1] = [MockChecker("white")] 
        self.mock_board._points_[3] = [MockChecker("white")] # Esta ficha bloquea
        self.game._moves_ = [5] # Dado 5 (intenta sacar desde punto 2)
        
        # El bucle 'for' encontrará la ficha en el índice 3.
        
        with patch('builtins.print'):
            result = self.game.attempt_move(start_point=2, dice_roll=5)
        
        self.assertFalse(result)
        self.mock_board.bear_off_checker.assert_not_called()
        self.assertEqual(self.game._moves_, [5])

    def test_cover_bear_off_black_overshoot_valid(self):
        """Cubre líneas 75-82: Overshoot válido para negras."""
        with patch('builtins.print'): self.game.switch_turn()
            
        self.mock_board.all_checkers_in_home_board.return_value = True
        # Ficha en punto 23 (índice 22). No hay fichas en 19,20,21.
        self.mock_board._points_[22] = [MockChecker("black")] 
        self.game._moves_ = [5] # Dado 5 (end_postart_point = 23 + 5 = 28)
        
        # El bucle 'for i in range(18, start_idx)' no encontrará fichas.
        
        with patch('builtins.print'):
            result = self.game.attempt_move(start_point=23, dice_roll=5)
        
        self.assertTrue(result)
        self.mock_board.bear_off_checker.assert_called_with(23)
        self.assertEqual(self.game._moves_, [])

    def test_cover_bear_off_black_overshoot_invalid(self):
        """Cubre líneas 85-86: Overshoot inválido para negras."""
        with patch('builtins.print'): self.game.switch_turn()

        self.mock_board.all_checkers_in_home_board.return_value = True
        # Ficha en punto 23 (índice 22) Y en punto 20 (índice 19)
        self.mock_board._points_[22] = [MockChecker("black")] 
        self.mock_board._points_[19] = [MockChecker("black")] # Esta ficha bloquea
        self.game._moves_ = [5] # Dado 5 (intenta sacar desde punto 23)
        
        # El bucle 'for' encontrará la ficha en el índice 19.
        
        with patch('builtins.print'):
            result = self.game.attempt_move(start_point=23, dice_roll=5)
        
        self.assertFalse(result)
        self.mock_board.bear_off_checker.assert_not_called()
        self.assertEqual(self.game._moves_, [5])

    def test_attempt_move_valid(self):
        """Prueba un movimiento normal y válido."""
        # Esta prueba no estaba en tu archivo original pero es buena tenerla.
        # CUBRE LÍNEA 98: self._board_.move_checker(start_point, end_point)
        self.mock_board._points_[11] = [MockChecker("white")] # Ficha en punto 12
        self.game._moves_ = [2] # Mover a 10
        
        result = self.game.attempt_move(start_point=12, dice_roll=2)
        
        self.assertTrue(result)
        self.mock_board.is_valid_move.assert_called_with(12, 10, "white")
        self.mock_board.move_checker.assert_called_with(12, 10)
        self.assertEqual(self.game._moves_, []) # Se consume el dado

    def test_attempt_reentry_valid(self):
        """Prueba un reingreso normal y válido."""
        # CUBRE LÍNEA 105: self._board_.reenter_checker(player._color_, dice_roll)
        self.mock_board.is_reentry_possible.return_value = True
        self.game._moves_ = [3]
        
        result = self.game.attempt_reentry(dice_roll=3)
        
        self.assertTrue(result)
        self.mock_board.reenter_checker.assert_called_with("white", 3)
        self.assertEqual(self.game._moves_, [])


if __name__ == '__main__':
    unittest.main()