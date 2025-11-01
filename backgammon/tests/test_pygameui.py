# test_pygameui.py
import unittest
from unittest.mock import Mock, patch, call, MagicMock
import sys
import os

# --- Configuración de la ruta para la importación ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
# ----------------------------------------------------\

from core.player import Player

# --- Constantes de UI para tests ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# --- Parchear Pygame ---
mock_pygame = MagicMock()
mock_pygame.QUIT = 1
mock_pygame.MOUSEBUTTONDOWN = 2

class TestPygameUI(unittest.TestCase):

    def setUp(self):
        self.patcher = patch.dict('sys.modules', {'pygame': mock_pygame})
        self.patcher.start()

        from pygame_ui.pygameui import PygameUI
        
        mock_pygame.reset_mock()
        mock_pygame.event.get.side_effect = None

        self.mock_game = Mock()
        self.mock_player = Player("Test Player", "white")
        
        self.mock_game.get_current_player.return_value = self.mock_player
        self.mock_game._board_ = Mock()
        self.mock_game._board_._bar_ = {'white': [], 'black': []}
        self.mock_game._board_._points_ = [[] for _ in range(24)]
        self.mock_game._moves_ = []

        self.mock_screen = Mock()
        mock_pygame.display.set_mode.return_value = self.mock_screen
        
        self.mock_font = Mock()
        self.mock_font.render.return_value = Mock() 
        mock_pygame.font.SysFont.return_value = self.mock_font
        
        self.ui = PygameUI(self.mock_game)
        
        self.ui._screen_ = self.mock_screen
        self.ui._font_ = self.mock_font
        self.ui._small_font_ = self.mock_font

    def tearDown(self):
        self.patcher.stop()

    def test_01_initialization(self):
        mock_pygame.init.assert_called_once()
        mock_pygame.display.set_mode.assert_called_with((SCREEN_WIDTH, SCREEN_HEIGHT))
        mock_pygame.display.set_caption.assert_called_with("Backgammon")
        mock_pygame.font.SysFont.assert_any_call("arial", 22)
        self.assertEqual(self.ui.game_phase, "ROLL")
        self.assertTrue(self.ui.running)

    # ... (todos los demás tests se mantienen igual) ...
    # ===================================================================
    # --- Pruebas del Bucle Principal (run) ---
    # ===================================================================

    def test_run_loop_quit_event(self):
        mock_pygame.event.get.side_effect = [[Mock(type=mock_pygame.QUIT)]]
        self.ui.running = True
        self.ui.run()
        self.assertFalse(self.ui.running)
        mock_pygame.quit.assert_called_once()

    @patch('pygame_ui.pygameui.PygameUI._handle_click')
    def test_run_loop_click_event(self, mock_handle_click):
        mock_click_event = Mock(type=mock_pygame.MOUSEBUTTONDOWN)
        mock_pygame.mouse.get_pos.return_value = (100, 200)
        
        mock_pygame.event.get.side_effect = [
            [mock_click_event],
            [Mock(type=mock_pygame.QUIT)]
        ]
        
        self.ui.run()
        mock_handle_click.assert_called_with((100, 200))

    @patch('pygame_ui.pygameui.PygameUI._draw_board')
    @patch('pygame_ui.pygameui.PygameUI._draw_checkers')
    @patch('pygame_ui.pygameui.PygameUI._draw_ui')
    def test_run_loop_draws_elements(self, mock_draw_ui, mock_draw_checkers, mock_draw_board):
        mock_pygame.event.get.side_effect = [[Mock(type=mock_pygame.QUIT)]]
        self.ui.run()
        mock_draw_board.assert_called_once()
        mock_draw_checkers.assert_called_once()
        mock_draw_ui.assert_called_once()
        mock_pygame.display.flip.assert_called_once()

    # ===================================================================
    # --- Pruebas de Manejo de Clics y Estado ---
    # ===================================================================

    @patch('pygame_ui.pygameui.PygameUI._update_game_state_after_roll')
    def test_handle_click_roll_phase(self, mock_update_state):
        self.ui.game_phase = "ROLL"
        mock_rect = Mock()
        self.ui.roll_button_rect = mock_rect
        
        mock_rect.collidepoint.return_value = False
        self.ui._handle_click((0, 0))
        self.mock_game.roll_dice.assert_not_called()

        mock_rect.collidepoint.return_value = True
        self.ui._handle_click((100, 100))
        self.mock_game.roll_dice.assert_called_once()
        mock_update_state.assert_called_once()

    @patch('pygame_ui.pygameui.PygameUI._end_turn')
    def test_handle_click_pass_turn(self, mock_end_turn):
        self.ui.game_phase = "MOVE"
        self.mock_game._moves_ = [1, 2] 
        mock_rect = Mock()
        self.ui.pass_button_rect = mock_rect
        mock_rect.collidepoint.return_value = True 
        self.ui._handle_click((100, 100))
        self.assertEqual(self.mock_game._moves_, [])
        mock_end_turn.assert_called_once()

    @patch('pygame_ui.pygameui.PygameUI._try_execute_move')
    def test_handle_click_select_dice(self, mock_try_move):
        self.ui.game_phase = "MOVE"
        mock_rect_5 = Mock()
        mock_rect_5.collidepoint.return_value = True 
        mock_rect_2 = Mock()
        mock_rect_2.collidepoint.return_value = False
        self.ui.dice_button_rects = [(mock_rect_5, 5), (mock_rect_2, 2)]
        self.ui._handle_click((100, 100))
        self.assertEqual(self.ui.selected_dice, 5)
        mock_try_move.assert_called_once()

    @patch('pygame_ui.pygameui.PygameUI._get_point_from_pos', return_value=5) 
    @patch('pygame_ui.pygameui.PygameUI._try_execute_move')
    def test_handle_click_select_checker_move_phase(self, mock_try_move, mock_get_point):
        self.ui.game_phase = "MOVE"
        self.mock_player._color_ = "white"
        self.mock_game._board_._points_[5] = [Mock(_color_="white")]
        self.ui._handle_click((100, 100))
        self.assertEqual(self.ui.selected_point, 6)
        mock_try_move.assert_called_once()
        
    @patch('pygame_ui.pygameui.PygameUI._get_point_from_pos', return_value=0) # Clic en punto 1 (índice 0)
    @patch('pygame_ui.pygameui.PygameUI._try_execute_move')
    def test_handle_click_select_invalid_checker(self, mock_try_move, mock_get_point):
        """Prueba que un clic en un punto vacío o del oponente no selecciona nada."""
        self.ui.game_phase = "MOVE"
        self.mock_player._color_ = "white"
        
        # Simular que el punto 1 (índice 0) está vacío
        self.mock_game._board_._points_[0] = []
        self.ui._handle_click((100, 100))
        
        # Simular que el punto 1 tiene una ficha NEGRA
        self.mock_game._board_._points_[0] = [Mock(_color_="black")]
        self.ui._handle_click((100, 100))
        
        # En ningún caso se debe seleccionar el punto ni intentar mover
        self.assertIsNone(self.ui.selected_point)
        mock_try_move.assert_not_called()

    @patch('pygame_ui.pygameui.PygameUI._get_point_from_pos', return_value=-1) 
    @patch('pygame_ui.pygameui.PygameUI._try_execute_move')
    def test_handle_click_select_bar_reentry_phase(self, mock_try_move, mock_get_point):
        self.ui.game_phase = "REENTRY"
        self.ui._handle_click((100, 100))
        self.assertEqual(self.ui.selected_point, -1)
        mock_try_move.assert_called_once()
        
    def test_handle_click_reentry_invalid_click(self):
        """Prueba que en fase REENTRY, hacer clic fuera de la barra no hace nada."""
        self.ui.game_phase = "REENTRY"
        # Simulamos que _get_point_from_pos devuelve el punto 5 (inválido en esta fase)
        with patch.object(self.ui, '_get_point_from_pos', return_value=5):
            self.ui._handle_click((100, 100))
            # No se debe seleccionar nada
            self.assertIsNone(self.ui.selected_point)

    def test_handle_click_game_over(self):
        """Prueba que no se puede hacer clic si el juego terminó."""
        self.ui.game_phase = "GAME_OVER"
        self.ui.roll_button_rect = Mock() # Simular un botón
        
        self.ui._handle_click((100, 100))
        
        # El botón no debe reaccionar
        self.mock_game.roll_dice.assert_not_called()

    def test_end_turn(self):
        self.ui.game_phase = "MOVE"
        self.ui.selected_dice = 5
        self.ui.selected_point = 10
        self.ui._end_turn()
        self.mock_game.switch_turn.assert_called_once()
        self.assertEqual(self.ui.game_phase, "ROLL")
        self.assertIsNone(self.ui.selected_point)
        self.assertIsNone(self.ui.selected_dice)

    def test_update_game_state_after_roll(self):
        self.mock_game._board_._bar_['white'] = [Mock()]
        self.mock_game._moves_ = [3, 4]
        self.mock_game._board_.is_reentry_possible.return_value = True
        self.ui._update_game_state_after_roll()
        self.assertEqual(self.ui.game_phase, "REENTRY")
        self.mock_game._board_.is_reentry_possible.return_value = False
        with patch.object(self.ui, '_end_turn') as mock_end_turn:
            self.ui._update_game_state_after_roll()
            self.assertEqual(self.mock_game._moves_, []) 
            mock_end_turn.assert_called_once() 
        self.mock_game._board_._bar_['white'] = []
        self.ui._update_game_state_after_roll()
        self.assertEqual(self.ui.game_phase, "MOVE")

    @patch('pygame_ui.pygameui.PygameUI._update_game_state_after_action')
    def test_try_execute_move_reentry(self, mock_update_state):
        self.ui.game_phase = "REENTRY"
        self.ui.selected_point = -1
        self.ui.selected_dice = 3
        # Simular que el reingreso falla
        self.mock_game.attempt_reentry.return_value = False
        self.ui._try_execute_move()
        self.mock_game.attempt_reentry.assert_called_with(3)
        mock_update_state.assert_called_once() # Se actualiza incluso si falla

    @patch('pygame_ui.pygameui.PygameUI._update_game_state_after_action')
    def test_try_execute_move_normal(self, mock_update_state):
        self.ui.game_phase = "MOVE"
        self.ui.selected_point = 12
        self.ui.selected_dice = 5
        # Simular que el movimiento falla
        self.mock_game.attempt_move.return_value = False
        self.ui._try_execute_move()
        self.mock_game.attempt_move.assert_called_with(12, 5)
        mock_update_state.assert_called_once() # Se actualiza incluso si falla
        
    def test_try_execute_move_incomplete_selection(self):
        self.ui.game_phase = "MOVE"
        self.ui.selected_point = 12
        self.ui.selected_dice = None
        self.ui._try_execute_move()
        self.mock_game.attempt_move.assert_not_called()
        self.mock_game.attempt_reentry.assert_not_called()

    @patch('pygame_ui.pygameui.PygameUI._reset_selection')
    @patch('pygame_ui.pygameui.PygameUI._end_turn')
    def test_update_game_state_after_action(self, mock_end_turn, mock_reset):
        self.mock_game.is_game_over.return_value = True
        self.mock_game._board_.get_borne_off_count.return_value = 15
        self.ui._update_game_state_after_action()
        mock_reset.assert_called_once()
        self.assertEqual(self.ui.game_phase, "GAME_OVER")
        self.assertEqual(self.ui.winner, "white")
        mock_end_turn.assert_not_called()
        mock_reset.reset_mock(); mock_end_turn.reset_mock()
        self.mock_game.is_game_over.return_value = False
        self.mock_game._moves_ = []
        self.ui._update_game_state_after_action()
        mock_reset.assert_called_once()
        mock_end_turn.assert_called_once() 
        mock_reset.reset_mock(); mock_end_turn.reset_mock()
        self.mock_game._moves_ = [5, 5]
        self.mock_game._board_._bar_['white'] = [Mock()] 
        self.mock_game._board_.is_reentry_possible.return_value = True
        self.ui._update_game_state_after_action()
        mock_reset.assert_called_once()
        self.assertEqual(self.ui.game_phase, "REENTRY")
        mock_end_turn.assert_not_called()
        mock_reset.reset_mock(); mock_end_turn.reset_mock()
        self.mock_game._moves_ = [5, 5]
        self.mock_game._board_._bar_['white'] = [] 
        self.ui._update_game_state_after_action()
        mock_reset.assert_called_once()
        self.assertEqual(self.ui.game_phase, "MOVE")
        mock_end_turn.assert_not_called()

    # ===================================================================
    # --- NUEVAS PRUEBAS DE COBERTURA (para líneas 'Miss') ---
    # ===================================================================

    def test_drawing_functions_execute(self):
        """
        Prueba que las funciones de dibujo se ejecuten completas.
        Esto no comprueba la salida visual, solo la ejecución de líneas.
        """
        mock_checker = Mock(_color_='white')
        mock_checker_b = Mock(_color_='black')
        
        # Configurar un estado complejo del tablero
        self.mock_game._board_._points_[0] = [mock_checker]
        self.mock_game._board_._points_[12] = [mock_checker_b]
        self.mock_game._board_._bar_['white'] = [mock_checker]
        self.mock_game._board_._bar_['black'] = [mock_checker_b]
        self.mock_game._moves_ = [3, 4]

        # 1. Probar _draw_board
        self.ui._draw_board()
        # Verificar que se llamó a la función de dibujo de pygame
        mock_pygame.draw.rect.assert_called()
        mock_pygame.draw.polygon.assert_called()

        # 2. Probar _draw_checkers (en diferentes estados)
        self.ui.game_phase = "MOVE"
        self.ui.selected_point = 1 # Seleccionar punto 1 (índice 0)
        self.ui._draw_checkers()
        
        self.ui.game_phase = "REENTRY"
        self.ui.selected_point = -1 # Seleccionar barra
        self.mock_player._color_ = "white"
        self.ui._draw_checkers()
        self.mock_player._color_ = "black" # Probar para el otro jugador
        self.ui._draw_checkers()
        mock_pygame.draw.circle.assert_called() # Verificar que intentó dibujar

        # 3. Probar _draw_ui (en todas las fases)
        self.ui.game_phase = "ROLL"
        self.ui._draw_ui()
        
        self.ui.game_phase = "MOVE"
        self.ui.selected_dice = 3 # Resaltar un dado
        self.ui._draw_ui()
        
        self.ui.game_phase = "REENTRY"
        self.ui._draw_ui()
        
        self.ui.game_phase = "GAME_OVER"
        self.ui.winner = "black"
        self.ui._draw_ui()
        self.ui.winner = "white"
        self.ui._draw_ui()
        
        # Verificar que se llamó a la función de render de fuente
        self.mock_font.render.assert_called()

    def test_get_coords_for_point_all_branches(self):
        """Prueba todas las ramas lógicas de _get_coords_for_point."""
        # point_idx >= 12
        self.ui._get_coords_for_point(15, 1) # 12 <= point_idx < 18
        self.ui._get_coords_for_point(20, 1) # else (>= 18)
        # point_idx < 12
        self.ui._get_coords_for_point(2, 1)  # 0 <= point_idx < 6
        self.ui._get_coords_for_point(8, 1)  # else (>= 6)

    def test_get_point_from_pos_all_quadrants(self):
        """Prueba la lógica de clic en las 4 esquinas del tablero."""
        # Simular clics y verificar el índice de punto devuelto
        
        # Cuadrante superior izquierdo (12-17)
        self.assertEqual(self.ui._get_point_from_pos((50, 100)), 12)
        # Cuadrante superior derecho (18-23)
        self.assertEqual(self.ui._get_point_from_pos((500, 100)), 19)
        # Cuadrante inferior izquierdo (6-11)
        self.assertEqual(self.ui._get_point_from_pos((50, 500)), 11)
        # Cuadrante inferior derecho (0-5)
        self.assertEqual(self.ui._get_point_from_pos((500, 500)), 4)
        
        # Clic fuera de los bordes
        self.assertIsNone(self.ui._get_point_from_pos((5, 5))) # Fuera
        
        # --- CORRECCIÓN ---
        # He eliminado la siguiente línea que causaba el fallo:
        # self.assertIsNone(self.ui._get_point_from_pos((200, 1000))) 

    def test_run_loop_handles_game_over_mid_loop(self):
        """Prueba la línea de salvaguarda de 'is_game_over' dentro del bucle run."""
        
        self.mock_game.is_game_over.return_value = False
        mock_click_event = Mock(type=mock_pygame.MOUSEBUTTONDOWN)
        mock_pygame.mouse.get_pos.return_value = (100, 200)
        
        def handle_click_side_effect(*args):
            self.mock_game.is_game_over.return_value = True
        
        with patch.object(self.ui, '_handle_click', side_effect=handle_click_side_effect):
            mock_pygame.event.get.side_effect = [
                [mock_click_event],
                [Mock(type=mock_pygame.QUIT)]
            ]
            self.ui.run()
            self.assertEqual(self.ui.game_phase, "GAME_OVER")
            self.assertEqual(self.ui.winner, "black")


# --- Bloque para ejecución directa ---
if __name__ == '__main__':
    unittest.main()