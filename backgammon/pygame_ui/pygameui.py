# pygame_ui/pygame_ui.py

import pygame
from ..core.backgammongame import BackgammonGame

# --- Constantes de Configuración ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_COLOR = (205, 170, 125)  # Un tono madera
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TRIANGLE_COLOR_A = (139, 115, 85) # Marrón oscuro para los triángulos
TRIANGLE_COLOR_B = (245, 245, 220) # Beige para los triángulos
HIGHLIGHT_COLOR = (255, 255, 0, 128) # Amarillo semitransparente para resaltar

CHECKER_RADIUS = 20
POINT_WIDTH = 50
BAR_WIDTH = 60

class PygameUI:
    """
    Gestiona la interfaz gráfica del juego de Backgammon utilizando Pygame.
    
    Esta clase es responsable de dibujar el estado del juego (tablero, fichas, dados)
    y de manejar la interacción del usuario a través del ratón.
    """

    def __init__(self, game: BackgammonGame):
        self._game_ = game
        self._screen_ = None
        self._font_ = None
        self.selected_point = None # Almacena el punto de inicio seleccionado por el jugador
        self.running = True

        self._initialize_pygame()

    def _initialize_pygame(self):
        """Inicializa Pygame, la pantalla y las fuentes."""
        pygame.init()
        self._screen_ = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Backgammon")
        self._font_ = pygame.font.SysFont("arial", 24)
        self._small_font_ = pygame.font.SysFont("arial", 18)
        
    def _draw_board(self):
        """Dibuja el tablero de Backgammon con sus puntos triangulares."""
        self._screen_.fill(BOARD_COLOR)
        
        # Dibuja la barra central
        bar_x = (SCREEN_WIDTH - BAR_WIDTH) // 2
        pygame.draw.rect(self._screen_, TRIANGLE_COLOR_A, (bar_x, 0, BAR_WIDTH, SCREEN_HEIGHT))

        # Dibuja los 24 triángulos (puntos)
        for i in range(12):
            # Coordenadas base para los triángulos
            x_base = 20 + i * POINT_WIDTH + (BAR_WIDTH if i >= 6 else 0)
            
            # Triángulos superiores (puntos 13 a 24)
            top_points = [(x_base, 0), (x_base + POINT_WIDTH, 0), (x_base + POINT_WIDTH / 2, SCREEN_HEIGHT / 2 - 20)]
            # Triángulos inferiores (puntos 1 a 12)
            bottom_points = [(x_base, SCREEN_HEIGHT), (x_base + POINT_WIDTH, SCREEN_HEIGHT), (x_base + POINT_WIDTH / 2, SCREEN_HEIGHT / 2 + 20)]

            color = TRIANGLE_COLOR_B if i % 2 == 0 else TRIANGLE_COLOR_A
            pygame.draw.polygon(self._screen_, color, top_points)
            pygame.draw.polygon(self._screen_, color, bottom_points)

    def _get_coords_for_point(self, point_idx: int, checker_count: int) -> tuple[int, int]:
        """Calcula las coordenadas (x, y) para una ficha en un punto específico."""
        i = point_idx
        y_offset = CHECKER_RADIUS * 2 * (checker_count -1)

        # Puntos del cuadrante inferior derecho (1-6)
        if 0 <= i < 6:
            x = SCREEN_WIDTH - 45 - i * POINT_WIDTH
            y = SCREEN_HEIGHT - CHECKER_RADIUS - y_offset
        # Puntos del cuadrante inferior izquierdo (7-12)
        elif 6 <= i < 12:
            x = (SCREEN_WIDTH - BAR_WIDTH) // 2 - 45 - (i-6) * POINT_WIDTH
            y = SCREEN_HEIGHT - CHECKER_RADIUS - y_offset
        # Puntos del cuadrante superior izquierdo (13-18)
        elif 12 <= i < 18:
            x = 45 + (i - 12) * POINT_WIDTH
            y = CHECKER_RADIUS + y_offset
        # Puntos del cuadrante superior derecho (19-24)
        else: # 18 <= i < 24
            x = (SCREEN_WIDTH + BAR_WIDTH) // 2 + 45 + (i - 18) * POINT_WIDTH
            y = CHECKER_RADIUS + y_offset
            
        return int(x), int(y)

    def _draw_checkers(self):
        """Dibuja todas las fichas en sus posiciones actuales en el tablero."""
        # Dibuja fichas en los puntos
        for i, point in enumerate(self._game_._board_._points_):
            for j, checker in enumerate(point):
                color = WHITE if checker._color_ == "white" else BLACK
                x, y = self._get_coords_for_point(i, j + 1)
                pygame.draw.circle(self._screen_, color, (x, y), CHECKER_RADIUS)
                pygame.draw.circle(self._screen_, (128,128,128), (x, y), CHECKER_RADIUS, 2) # Borde

        # Dibuja fichas en la barra
        bar_x = SCREEN_WIDTH // 2
        for i, checker in enumerate(self._game_._board_._bar_["white"]):
            y = SCREEN_HEIGHT // 2 - 60 - i * (CHECKER_RADIUS * 2)
            pygame.draw.circle(self._screen_, WHITE, (bar_x, y), CHECKER_RADIUS)
        for i, checker in enumerate(self._game_._board_._bar_["black"]):
            y = SCREEN_HEIGHT // 2 + 60 + i * (CHECKER_RADIUS * 2)
            pygame.draw.circle(self._screen_, BLACK, (bar_x, y), CHECKER_RADIUS)

    def _draw_ui(self):
        """Dibuja elementos de la UI como texto, dados y botones."""
        player = self._game_.get_current_player()
        
        # Muestra el turno actual
        turn_text = self._font_.render(f"Turno de: {player._name_} ({player._color_})", True, BLACK)
        self._screen_.blit(turn_text, (10, SCREEN_HEIGHT // 2 - 50))

        # Muestra los movimientos disponibles (dados)
        moves_text = self._font_.render(f"Movimientos: {self._game_._moves_}", True, BLACK)
        self._screen_.blit(moves_text, (10, SCREEN_HEIGHT // 2))

        # Dibuja el botón para tirar los dados si no hay movimientos
        if not self._game_._moves_:
            self.roll_button_rect = pygame.Rect(10, SCREEN_HEIGHT // 2 + 40, 150, 40)
            pygame.draw.rect(self._screen_, TRIANGLE_COLOR_A, self.roll_button_rect)
            roll_text = self._font_.render("Tirar Dados", True, WHITE)
            self._screen_.blit(roll_text, (20, SCREEN_HEIGHT // 2 + 45))
        
        # Muestra un mensaje si una ficha está seleccionada
        if self.selected_point is not None:
             msg = self._small_font_.render(f"Ficha seleccionada en el punto {self.selected_point}", True, (200,0,0))
             self._screen_.blit(msg, (10, SCREEN_HEIGHT // 2 - 80))

    def _get_point_from_pos(self, pos: tuple[int, int]) -> int | None:
        """Convierte una coordenada del ratón en un índice de punto del tablero."""
        x, y = pos
        bar_x_start = (SCREEN_WIDTH - BAR_WIDTH) // 2
        bar_x_end = (SCREEN_WIDTH + BAR_WIDTH) // 2

        if bar_x_start < x < bar_x_end:
            return -1 # Identificador para la barra

        if y > SCREEN_HEIGHT / 2: # Mitad inferior (puntos 1-12)
            base_idx = 11
            offset_x = x - ((SCREEN_WIDTH + BAR_WIDTH) // 2) if x > bar_x_end else x
            point_offset = (offset_x - 20) // POINT_WIDTH
            if x < bar_x_start:
                 point_offset = (bar_x_start - x - 20)//POINT_WIDTH
                 return 6 + point_offset
            else:
                 point_offset = (SCREEN_WIDTH - x - 20)//POINT_WIDTH
                 return point_offset
        else: # Mitad superior (puntos 13-24)
            if x < bar_x_start:
                 point_offset = (x - 20)//POINT_WIDTH
                 return 12 + point_offset
            else:
                 point_offset = (x - bar_x_end - 20)//POINT_WIDTH
                 return 18 + point_offset
        return None

    def _handle_click(self, pos: tuple[int, int]):
        """Procesa el clic del usuario para realizar acciones en el juego."""
        player = self._game_.get_current_player()

        # 1. Si no hay movimientos, el único clic válido es en "Tirar Dados"
        if not self._game_._moves_:
            if self.roll_button_rect.collidepoint(pos):
                self._game_.roll_dice()
            return

        # 2. Si el jugador tiene fichas en la barra, debe reingresar
        if self._game_._board_._bar_[player._color_]:
            point_idx = self._get_point_from_pos(pos)
            if point_idx is None: return

            target_point = point_idx + 1
            dice_roll = 0
            
            if player._color_ == "white":
                dice_roll = 24 - point_idx
            else: # black
                dice_roll = point_idx + 1

            if dice_roll in self._game_._moves_:
                if self._game_.attempt_reentry(dice_roll):
                    print(f"Reingreso exitoso en el punto {target_point}")
                else:
                    print("Intento de reingreso fallido.")
            else:
                print(f"Movimiento de reingreso inválido con el dado: {dice_roll}")

        # 3. Lógica para movimientos normales
        else:
            clicked_point_idx = self._get_point_from_pos(pos)
            if clicked_point_idx is None: return

            # Si no hay ficha seleccionada, intenta seleccionar una
            if self.selected_point is None:
                start_point = clicked_point_idx + 1
                if self._game_._board_._points_[clicked_point_idx] and self._game_._board_._points_[clicked_point_idx][0]._color_ == player._color_:
                    self.selected_point = start_point
                    print(f"Ficha seleccionada en el punto: {self.selected_point}")
            
            # Si ya hay una ficha seleccionada, intenta moverla
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
                
                self.selected_point = None # Resetea la selección después del intento
        
        # 4. Cambiar de turno si no quedan movimientos
        if not self._game_._moves_:
            self._game_.switch_turn()
            print("No quedan movimientos. Cambiando de turno.")

    def run(self):
        """El bucle principal del juego que maneja eventos, actualizaciones y renderizado."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_click(pygame.mouse.get_pos())
            
            # Dibujar todo en cada frame
            self._draw_board()
            self._draw_checkers()
            self._draw_ui()
            
            pygame.display.flip()

        pygame.quit()