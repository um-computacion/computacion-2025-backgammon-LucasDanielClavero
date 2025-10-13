# pygame_ui/pygameui.py

import pygame
from core.backgammongame import BackgammonGame

# --- Constantes de Configuración ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_COLOR = (205, 170, 125)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TRIANGLE_COLOR_A = (139, 115, 85)
TRIANGLE_COLOR_B = (245, 245, 220)
HIGHLIGHT_COLOR = (255, 255, 0, 128)

CHECKER_RADIUS = 20
POINT_WIDTH = 50
BAR_WIDTH = 60
BORDER_WIDTH = 20

class PygameUI:
    def __init__(self, game: BackgammonGame):
        self._game_ = game
        self._screen_ = None
        self._font_ = None
        self.selected_point = None
        self.running = True
        self._initialize_pygame()

    def _initialize_pygame(self):
        pygame.init()
        self._screen_ = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Backgammon")
        self._font_ = pygame.font.SysFont("arial", 22)
        self._small_font_ = pygame.font.SysFont("arial", 18)
        
    def _draw_board(self):
        self._screen_.fill(BOARD_COLOR)
        bar_x = (SCREEN_WIDTH - BAR_WIDTH) // 2
        pygame.draw.rect(self._screen_, TRIANGLE_COLOR_A, (bar_x, 0, BAR_WIDTH, SCREEN_HEIGHT))

        for i in range(6):
            x_top_left = BORDER_WIDTH + i * POINT_WIDTH
            x_top_right = (SCREEN_WIDTH + BAR_WIDTH) // 2 + BORDER_WIDTH + i * POINT_WIDTH
            x_bottom_left = BORDER_WIDTH + i * POINT_WIDTH
            x_bottom_right = (SCREEN_WIDTH + BAR_WIDTH) // 2 + BORDER_WIDTH + i * POINT_WIDTH
            
            top_apex_y = SCREEN_HEIGHT / 2 - BORDER_WIDTH
            bottom_apex_y = SCREEN_HEIGHT / 2 + BORDER_WIDTH

            tri_top_left = [(x_top_left, 0), (x_top_left + POINT_WIDTH, 0), (x_top_left + POINT_WIDTH / 2, top_apex_y)]
            tri_top_right = [(x_top_right, 0), (x_top_right + POINT_WIDTH, 0), (x_top_right + POINT_WIDTH / 2, top_apex_y)]
            tri_bottom_left = [(x_bottom_left, SCREEN_HEIGHT), (x_bottom_left + POINT_WIDTH, SCREEN_HEIGHT), (x_bottom_left + POINT_WIDTH / 2, bottom_apex_y)]
            tri_bottom_right = [(x_bottom_right, SCREEN_HEIGHT), (x_bottom_right + POINT_WIDTH, SCREEN_HEIGHT), (x_bottom_right + POINT_WIDTH / 2, bottom_apex_y)]

            color1 = TRIANGLE_COLOR_A if i % 2 == 0 else TRIANGLE_COLOR_B
            color2 = TRIANGLE_COLOR_B if i % 2 == 0 else TRIANGLE_COLOR_A
            
            pygame.draw.polygon(self._screen_, color1, tri_top_left)
            pygame.draw.polygon(self._screen_, color2, tri_top_right)
            pygame.draw.polygon(self._screen_, color2, tri_bottom_left)
            pygame.draw.polygon(self._screen_, color1, tri_bottom_right)

    def _get_coords_for_point(self, point_idx: int, checker_count: int) -> tuple[int, int]:
        y_offset = (checker_count - 1) * (CHECKER_RADIUS * 2)

        if point_idx >= 12: # Mitad superior del tablero (puntos 13-24)
            y = CHECKER_RADIUS + y_offset
            if 12 <= point_idx < 18: # Cuadrante superior izquierdo
                x = BORDER_WIDTH + (point_idx - 12) * POINT_WIDTH + POINT_WIDTH / 2
            else: # Cuadrante superior derecho
                x = (SCREEN_WIDTH + BAR_WIDTH) // 2 + BORDER_WIDTH + (point_idx - 18) * POINT_WIDTH + POINT_WIDTH / 2
        else: # Mitad inferior del tablero (puntos 1-12)
            y = SCREEN_HEIGHT - CHECKER_RADIUS - y_offset
            # --- CORRECCIÓN 1: Lógica ajustada para centrar fichas inferiores ---
            if 0 <= point_idx < 6: # Cuadrante inferior derecho (puntos 1-6)
                # La numeración va de derecha a izquierda (5, 4, ..., 0)
                # El dibujo va de izquierda a derecha (0, 1, ..., 5)
                # Relación: drawing_index = 5 - point_idx
                drawing_idx = 5 - point_idx
                x = (SCREEN_WIDTH + BAR_WIDTH) // 2 + BORDER_WIDTH + drawing_idx * POINT_WIDTH + POINT_WIDTH / 2
            else: # Cuadrante inferior izquierdo (puntos 7-12)
                # La numeración va de derecha a izquierda (11, 10, ..., 6)
                # El dibujo va de izquierda a derecha (0, 1, ..., 5)
                # Relación: drawing_index = 11 - point_idx
                drawing_idx = 11 - point_idx
                x = BORDER_WIDTH + drawing_idx * POINT_WIDTH + POINT_WIDTH / 2
                
        return int(x), int(y)

    def _draw_checkers(self):
        for i, point in enumerate(self._game_._board_._points_):
            for j, checker in enumerate(point):
                color = WHITE if checker._color_ == "white" else BLACK
                x, y = self._get_coords_for_point(i, j + 1)
                pygame.draw.circle(self._screen_, color, (x, y), CHECKER_RADIUS)
                pygame.draw.circle(self._screen_, (128,128,128), (x, y), CHECKER_RADIUS, 2)

        bar_x = SCREEN_WIDTH // 2
        for i, checker in enumerate(self._game_._board_._bar_["white"]):
            y = SCREEN_HEIGHT // 2 - 40 - i * (CHECKER_RADIUS * 2)
            pygame.draw.circle(self._screen_, WHITE, (bar_x, y), CHECKER_RADIUS)
        for i, checker in enumerate(self._game_._board_._bar_["black"]):
            y = SCREEN_HEIGHT // 2 + 40 + i * (CHECKER_RADIUS * 2)
            pygame.draw.circle(self._screen_, BLACK, (bar_x, y), CHECKER_RADIUS)

    # --- CORRECCIÓN 2: UI rediseñada para aparecer en la barra central ---
    def _draw_ui(self):
        player = self._game_.get_current_player()
        center_x = SCREEN_WIDTH // 2

        # Preparar los textos
        turn_text_surf = self._font_.render(f"Turno: {player._name_}", True, WHITE)
        moves_text_surf = self._font_.render(f"Movimientos: {self._game_._moves_}", True, WHITE)
        
        # Posicionar los textos en el centro de la barra
        turn_text_rect = turn_text_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 2 - 20))
        moves_text_rect = moves_text_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 2 + 20))
        
        self._screen_.blit(turn_text_surf, turn_text_rect)
        self._screen_.blit(moves_text_surf, moves_text_rect)

        if not self._game_._moves_:
            self.roll_button_rect = pygame.Rect(0, 0, 140, 40)
            self.roll_button_rect.center = (center_x, SCREEN_HEIGHT // 2 + 70)
            pygame.draw.rect(self._screen_, (200, 200, 200), self.roll_button_rect, border_radius=5)
            roll_text_surf = self._font_.render("Tirar Dados", True, BLACK)
            roll_text_rect = roll_text_surf.get_rect(center=self.roll_button_rect.center)
            self._screen_.blit(roll_text_surf, roll_text_rect)
        
        if self.selected_point is not None:
             msg_surf = self._small_font_.render(f"Ficha seleccionada: {self.selected_point}", True, (200,0,0))
             msg_rect = msg_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 2 - 60))
             self._screen_.blit(msg_surf, msg_rect)

    def _get_point_from_pos(self, pos: tuple[int, int]) -> int | None:
        x, y = pos
        bar_start_x = (SCREEN_WIDTH - BAR_WIDTH) // 2
        bar_end_x = (SCREEN_WIDTH + BAR_WIDTH) // 2

        if bar_start_x < x < bar_end_x: return -1

        if y < SCREEN_HEIGHT / 2:
            if BORDER_WIDTH < x < bar_start_x:
                return 12 + (x - BORDER_WIDTH) // POINT_WIDTH
            elif bar_end_x < x < SCREEN_WIDTH - BORDER_WIDTH:
                 return 18 + (x - bar_end_x - BORDER_WIDTH) // POINT_WIDTH
        else:
            if BORDER_WIDTH < x < bar_start_x:
                return 11 - ((x - BORDER_WIDTH) // POINT_WIDTH)
            elif bar_end_x < x < SCREEN_WIDTH - BORDER_WIDTH:
                return 5 - ((x - bar_end_x - BORDER_WIDTH) // POINT_WIDTH)
        return None

    def _handle_click(self, pos: tuple[int, int]):
        player = self._game_.get_current_player()

        if not self._game_._moves_:
            if hasattr(self, 'roll_button_rect') and self.roll_button_rect.collidepoint(pos):
                self._game_.roll_dice()
            return

        clicked_point_idx = self._get_point_from_pos(pos)
        if clicked_point_idx is None: return

        if self.selected_point is None:
            if clicked_point_idx >= 0 and self._game_._board_._points_[clicked_point_idx] and self._game_._board_._points_[clicked_point_idx][0]._color_ == player._color_:
                self.selected_point = clicked_point_idx + 1
                print(f"Ficha seleccionada en el punto: {self.selected_point}")
        else:
            end_point = clicked_point_idx + 1
            diff = abs(end_point - self.selected_point)
            
            if diff in self._game_._moves_:
                if self._game_.attempt_move(self.selected_point, diff):
                    print(f"Movimiento exitoso de {self.selected_point} a {end_point}")
                else:
                    print(f"Intento de movimiento de {self.selected_point} a {end_point} fallido.")
            else:
                print("El movimiento no corresponde a ningún dado.")
            
            self.selected_point = None

        if not self._game_._moves_ and self._game_._dice_._values_:
            self._game_.switch_turn()
            print("No quedan movimientos. Cambiando de turno.")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_click(pygame.mouse.get_pos())
            
            self._draw_board()
            self._draw_checkers()
            self._draw_ui()
            
            pygame.display.flip()

        pygame.quit()