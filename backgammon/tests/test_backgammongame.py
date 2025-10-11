import unittest
from unittest.mock import Mock, patch

# Asegúrate de que la ruta de importación sea la correcta
from core.backgammongame import BackgammonGame
from core.player import Player

class TestBackgammonGame(unittest.TestCase):

    def setUp(self):
        """Este método se ejecuta antes de cada prueba para crear una instancia fresca del juego."""
        self.game = BackgammonGame("Alice", "Bob")

    def test_initialization(self):
        """Verifica que el juego se inicialice con los valores correctos."""
        self.assertIsInstance(self.game._board_, Mock) # Board será mockeado en otras pruebas
        self.assertEqual(len(self.game._players_), 2)
        self.assertEqual(self.game._players_[0]._name_, "Alice")
        self.assertEqual(self.game._players_[0]._color_, "white")
        self.assertEqual(self.game._players_[1]._name_, "Bob")
        self.assertEqual(self.game._players_[1]._color_, "black")
        self.assertEqual(self.game._current_player_idx_, 0)
        self.assertEqual(self.game._moves_, [])

    def test_get_current_player(self):
        """Verifica que se obtiene el jugador actual correctamente."""
        current_player = self.game.get_current_player()
        self.assertEqual(current_player._name_, "Alice")
        self.assertEqual(current_player._color_, "white")

    def test_switch_turn(self):
        """Prueba que el turno cambie correctamente entre jugadores."""
        # Turno inicial: Jugador 1 (Alice)
        self.assertEqual(self.game.get_current_player()._name_, "Alice")
        
        # Cambiar a Jugador 2 (Bob)
        self.game.switch_turn()
        self.assertEqual(self.game.get_current_player()._name_, "Bob")
        
        # Cambiar de vuelta a Jugador 1 (Alice)
        self.game.switch_turn()
        self.assertEqual(self.game.get_current_player()._name_, "Alice")

    @patch('core.backgammongame.Dice')
    def test_roll_dice(self, MockDice):
        """
        Prueba la tirada de dados, asegurándose de que los movimientos se actualicen.
        Usamos un mock para controlar el resultado de los dados.
        """
        # Configurar el mock para un tiro normal
        mock_dice_instance = MockDice.return_value
        mock_dice_instance.get_moves.return_value = [3, 4]
        mock_dice_instance._values_ = (3, 4)
        
        game = BackgammonGame()
        game._dice_ = mock_dice_instance # Reemplazamos la instancia real por el mock
        game.roll_dice()
        
        self.assertEqual(game._moves_, [3, 4])
        mock_dice_instance.roll.assert_called_once() # Verificar que el método roll() fue llamado

        # Configurar el mock para un tiro de dobles
        mock_dice_instance.get_moves.return_value = [5, 5, 5, 5]
        mock_dice_instance._values_ = (5, 5)
        game.roll_dice()
        self.assertEqual(game._moves_, [5, 5, 5, 5])

    @patch('core.backgammongame.Board')
    def test_attempt_move_valid(self, MockBoard):
        """Prueba un intento de movimiento válido."""
        mock_board_instance = MockBoard.return_value
        mock_board_instance.is_valid_move.return_value = True # Simular que el movimiento es válido
        
        self.game._board_ = mock_board_instance
        self.game._moves_ = [5, 2]
        
        # Jugador blanco (Alice) mueve del punto 6 con un dado de 5 (al punto 1)
        result = self.game.attempt_move(start_point=6, dice_roll=5)
        
        self.assertTrue(result)
        mock_board_instance.is_valid_move.assert_called_with(6, 1, "white")
        mock_board_instance.move_checker.assert_called_with(6, 1)
        self.assertEqual(self.game._moves_, [2]) # El 5 debe ser removido de los movimientos

    @patch('core.backgammongame.Board')
    def test_attempt_move_invalid(self, MockBoard):
        """Prueba un intento de movimiento inválido (punto bloqueado)."""
        mock_board_instance = MockBoard.return_value
        mock_board_instance.is_valid_move.return_value = False # Simular que el movimiento es inválido
        
        self.game._board_ = mock_board_instance
        self.game._moves_ = [3]
        
        result = self.game.attempt_move(start_point=12, dice_roll=3)
        
        self.assertFalse(result)
        mock_board_instance.move_checker.assert_not_called() # move_checker no debe ser llamado
        self.assertEqual(self.game._moves_, [3]) # El movimiento no debe ser removido

    def test_attempt_move_off_board(self):
        """Prueba un intento de mover una ficha fuera del tablero prematuramente."""
        self.game._moves_ = [4]
        # El jugador blanco intenta mover desde el punto 3 con un 4, lo que daría -1
        result = self.game.attempt_move(start_point=3, dice_roll=4)
        self.assertFalse(result)
        self.assertEqual(self.game._moves_, [4]) # El movimiento no debe ser consumido

    @patch('core.backgammongame.Board')
    def test_attempt_reentry_valid(self, MockBoard):
        """Prueba un reingreso válido desde la barra."""
        mock_board_instance = MockBoard.return_value
        mock_board_instance.is_reentry_possible.return_value = True

        self.game._board_ = mock_board_instance
        self.game._moves_ = [3]
        
        result = self.game.attempt_reentry(dice_roll=3)

        self.assertTrue(result)
        mock_board_instance.reenter_checker.assert_called_with("white", 3)
        self.assertEqual(self.game._moves_, [])

    @patch('core.backgammongame.Board')
    def test_attempt_reentry_invalid(self, MockBoard):
        """Prueba un reingreso inválido (punto de entrada bloqueado)."""
        mock_board_instance = MockBoard.return_value
        mock_board_instance.is_reentry_possible.return_value = False

        self.game._board_ = mock_board_instance
        self.game._moves_ = [3]
        
        result = self.game.attempt_reentry(dice_roll=3)
        
        self.assertFalse(result)
        mock_board_instance.reenter_checker.assert_not_called()
        self.assertEqual(self.game._moves_, [3])

    def test_is_game_over(self):
        """Prueba la condición de fin de juego (que por ahora siempre es False)."""
        self.assertFalse(self.game.is_game_over())

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)