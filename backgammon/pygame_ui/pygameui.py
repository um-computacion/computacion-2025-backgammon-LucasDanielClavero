# pygame_ui/pygameui.py

import pygame
from core.backgammongame import BackgammonGame

# --- Constantes de Configuración ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_COLOR = (205, 170, 125)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
GREY = (200, 200, 200)
TRIANGLE_COLOR_A = (139, 115, 85)
TRIANGLE_COLOR_B = (245, 245, 220)
HIGHLIGHT_COLOR = (255, 255, 0, 128) # No se usa actualmente, pero se mantiene

CHECKER_RADIUS = 20
POINT_WIDTH = 50
BAR_WIDTH = 60
BORDER_WIDTH = 20

class PygameUI:
    def __init__(self, game: BackgammonGame):
        self._game_ = game
        self._screen_ = None
        self._font_ = None
        self._small_font_ = None
        self.running = True

        # --- NUEVOS ATRIBUTOS DE ESTADO ---
        self.selected_point = None  # Puede ser un int (1-24) o -1 para la barra
        self.selected_dice = None   # El valor del dado (int) seleccionado
        self.game_phase = "ROLL"    # Fases: "ROLL", "REENTRY", "MOVE", "GAME_OVER"
        self.winner = None          # "white" o "black"
        
        # Rectángulos para botones (se definirán en _draw_ui)
        self.roll_button_rect = None
        self.pass_button_rect = None
        self.dice_button_rects = [] # Lista de (rect, dice_value)
        # --- FIN DE NUEVOS ATRIBUTOS ---

        self._initialize_pygame()

    def _initialize_pygame(self):
        pygame.init()
        self._screen_ = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Backgammon")
        self._font_ = pygame.font.SysFont("arial", 22)
        self._small_font_ = pygame.font.SysFont("arial", 18)
        
    def _draw_board(self):
        # Esta función se mantiene sin cambios
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
        # Esta función se mantiene sin cambios (con la corrección 1 ya aplicada)
        y_offset = (checker_count - 1) * (CHECKER_RADIUS * 2)

        if point_idx >= 12: 
            y = CHECKER_RADIUS + y_offset
            if 12 <= point_idx < 18: 
                x = BORDER_WIDTH + (point_idx - 12) * POINT_WIDTH + POINT_WIDTH / 2
            else: 
                x = (SCREEN_WIDTH + BAR_WIDTH) // 2 + BORDER_WIDTH + (point_idx - 18) * POINT_WIDTH + POINT_WIDTH / 2
        else: 
            y = SCREEN_HEIGHT - CHECKER_RADIUS - y_offset
            if 0 <= point_idx < 6: 
                drawing_idx = 5 - point_idx
                x = (SCREEN_WIDTH + BAR_WIDTH) // 2 + BORDER_WIDTH + drawing_idx * POINT_WIDTH + POINT_WIDTH / 2
            else: 
                drawing_idx = 11 - point_idx
                x = BORDER_WIDTH + drawing_idx * POINT_WIDTH + POINT_WIDTH / 2
                
        return int(x), int(y)

    def _draw_checkers(self):
        # Esta función se mantiene casi sin cambios
        # Añadida una pequeña sombra para la ficha seleccionada
        board = self._game_._board_
        player_color = self._game_.get_current_player()._color_

        for i, point in enumerate(board._points_):
            for j, checker in enumerate(point):
                color = WHITE if checker._color_ == "white" else BLACK
                x, y = self._get_coords_for_point(i, j + 1)
                
                # Resaltar si es la ficha seleccionada
                if self.game_phase == "MOVE" and self.selected_point == (i + 1):
                    pygame.draw.circle(self._screen_, RED, (x, y), CHECKER_RADIUS + 3)

                pygame.draw.circle(self._screen_, color, (x, y), CHECKER_RADIUS)
                pygame.draw.circle(self._screen_, (128,128,128), (x, y), CHECKER_RADIUS, 2)

        bar_x = SCREEN_WIDTH // 2
        for i, checker in enumerate(board._bar_["white"]):
            y = SCREEN_HEIGHT // 2 - 40 - i * (CHECKER_RADIUS * 2)
            # Resaltar si la barra está seleccionada
            if self.game_phase == "REENTRY" and self.selected_point == -1 and player_color == "white":
                 pygame.draw.circle(self._screen_, RED, (bar_x, y), CHECKER_RADIUS + 3)
            pygame.draw.circle(self._screen_, WHITE, (bar_x, y), CHECKER_RADIUS)

        for i, checker in enumerate(board._bar_["black"]):
            y = SCREEN_HEIGHT // 2 + 40 + i * (CHECKER_RADIUS * 2)
            # Resaltar si la barra está seleccionada
            if self.game_phase == "REENTRY" and self.selected_point == -1 and player_color == "black":
                 pygame.draw.circle(self._screen_, RED, (bar_x, y), CHECKER_RADIUS + 3)
            pygame.draw.circle(self._screen_, BLACK, (bar_x, y), CHECKER_RADIUS)

    def _draw_ui(self):
        # --- FUNCIÓN COMPLETAMENTE REESCRITA ---
        # para manejar los nuevos estados (ROLL, MOVE, GAME_OVER) y botones
        
        player = self._game_.get_current_player()
        center_x = SCREEN_WIDTH // 2
        
        # --- 1. Si el juego terminó ---
        if self.game_phase == "GAME_OVER":
            winner_name = "BLANCAS" if self.winner == "white" else "NEGRAS"
            text_surf = self._font_.render(f"¡JUEGO TERMINADO! ¡GANA {winner_name}!", True, WHITE, BLACK)
            text_rect = text_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 2))
            self._screen_.blit(text_surf, text_rect)
            return

        # --- 2. Información del jugador ---
        turn_text_surf = self._font_.render(f"Turno: {player._name_} ({player._color_})", True, WHITE)
        turn_text_rect = turn_text_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 2 - 60))
        self._screen_.blit(turn_text_surf, turn_text_rect)

        # --- 3. Mostrar estado y botones según la fase ---
        self.dice_button_rects = [] # Limpiar rects de dados
        
        if self.game_phase == "ROLL":
            # --- Fase: Tirar Dados ---
            self.roll_button_rect = pygame.Rect(0, 0, 140, 40)
            self.roll_button_rect.center = (center_x, SCREEN_HEIGHT // 2)
            pygame.draw.rect(self._screen_, GREY, self.roll_button_rect, border_radius=5)
            roll_text_surf = self._font_.render("Tirar Dados", True, BLACK)
            roll_text_rect = roll_text_surf.get_rect(center=self.roll_button_rect.center)
            self._screen_.blit(roll_text_surf, roll_text_rect)
        
        elif self.game_phase in ["MOVE", "REENTRY"]:
            # --- Fase: Mover o Reingresar ---
            moves = self._game_._moves_
            
            # Dibujar los dados como botones
            total_width = len(moves) * 40 + max(0, len(moves) - 1) * 10
            start_x = center_x - total_width // 2
            
            for i, move in enumerate(moves):
                die_rect = pygame.Rect(start_x + i * 50, SCREEN_HEIGHT // 2 - 20, 40, 40)
                self.dice_button_rects.append((die_rect, move))
                
                # Resaltar dado seleccionado
                btn_color = GREEN if self.selected_dice == move else GREY
                pygame.draw.rect(self._screen_, btn_color, die_rect, border_radius=5)
                
                move_text_surf = self._font_.render(str(move), True, BLACK)
                move_text_rect = move_text_surf.get_rect(center=die_rect.center)
                self._screen_.blit(move_text_surf, move_text_rect)

            # Dibujar botón de Pasar
            self.pass_button_rect = pygame.Rect(0, 0, 140, 30)
            self.pass_button_rect.center = (center_x, SCREEN_HEIGHT // 2 + 50)
            pygame.draw.rect(self._screen_, (255, 100, 100), self.pass_button_rect, border_radius=5)
            pass_text_surf = self._small_font_.render("Pasar Turno", True, BLACK)
            pass_text_rect = pass_text_surf.get_rect(center=self.pass_button_rect.center)
            self._screen_.blit(pass_text_surf, pass_text_rect)

            # Mostrar mensaje de estado (qué seleccionar)
            msg = "..."
            if self.game_phase == "REENTRY":
                msg = "Haz clic en la BARRA y luego un DADO"
            elif self.selected_point is None:
                msg = "Selecciona una FICHA"
            elif self.selected_dice is None:
                msg = "Selecciona un DADO"
            
            msg_surf = self._small_font_.render(msg, True, WHITE)
            msg_rect = msg_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 2 + 90))
            self._screen_.blit(msg_surf, msg_rect)

    def _get_point_from_pos(self, pos: tuple[int, int]) -> int | None:
        # Esta función se mantiene casi sin cambios
        # Solo se asegura que devuelva None si está fuera de los bordes
        x, y = pos
        bar_start_x = (SCREEN_WIDTH - BAR_WIDTH) // 2
        bar_end_x = (SCREEN_WIDTH + BAR_WIDTH) // 2

        if bar_start_x < x < bar_end_x: return -1 # -1 para la barra

        if y < SCREEN_HEIGHT / 2:
            if BORDER_WIDTH < x < bar_start_x:
                idx = 12 + (x - BORDER_WIDTH) // POINT_WIDTH
                return idx if idx < 18 else None
            elif bar_end_x < x < SCREEN_WIDTH - BORDER_WIDTH:
                 idx = 18 + (x - bar_end_x - BORDER_WIDTH) // POINT_WIDTH
                 return idx if idx < 24 else None
        else:
            if BORDER_WIDTH < x < bar_start_x:
                idx = 11 - ((x - BORDER_WIDTH) // POINT_WIDTH)
                return idx if idx >= 6 else None
            elif bar_end_x < x < SCREEN_WIDTH - BORDER_WIDTH:
                idx = 5 - ((x - bar_end_x - BORDER_WIDTH) // POINT_WIDTH)
                return idx if idx >= 0 else None
        return None

    def _handle_click(self, pos: tuple[int, int]):
        # --- FUNCIÓN COMPLETAMENTE REESCRITA ---
        # Para manejar el nuevo flujo de estado (state machine)

        if self.game_phase == "GAME_OVER":
            return # No hacer nada si el juego terminó

        player = self._game_.get_current_player()

        # 1. Fase: ROLL
        if self.game_phase == "ROLL":
            if self.roll_button_rect and self.roll_button_rect.collidepoint(pos):
                self._game_.roll_dice()
                self._update_game_state_after_roll() # Comprobar estado después de tirar
            return

        # 2. Fases: MOVE / REENTRY
        if self.game_phase in ["MOVE", "REENTRY"]:
            
            # 2a. Comprobar clic en "Pasar Turno"
            if self.pass_button_rect and self.pass_button_rect.collidepoint(pos):
                print("Jugador pasa el turno.")
                self._game_._moves_ = [] # Forzar fin de movimientos
                self._end_turn()
                return

            # 2b. Comprobar clic en un dado
            clicked_dice = None
            for rect, move in self.dice_button_rects:
                if rect.collidepoint(pos):
                    clicked_dice = move
                    break
            
            if clicked_dice is not None:
                self.selected_dice = clicked_dice
                print(f"Dado seleccionado: {self.selected_dice}")
                self._try_execute_move() # Intentar mover si ya tenemos ficha
                return

            # 2c. Comprobar clic en el tablero
            clicked_point_idx = self._get_point_from_pos(pos)
            
            if clicked_point_idx is None:
                self.selected_point = None # Deseleccionar al hacer clic fuera
                return

            if self.game_phase == "REENTRY":
                if clicked_point_idx == -1: # Clic en la barra
                    self.selected_point = -1
                    print("Barra seleccionada.")
                    self._try_execute_move() # Intentar mover si ya tenemos dado
                else:
                    print("Debes hacer clic en la barra para reingresar.")
                return

            if self.game_phase == "MOVE":
                if clicked_point_idx >= 0: # Clic en un punto normal
                    if self._game_._board_._points_[clicked_point_idx] and \
                       self._game_._board_._points_[clicked_point_idx][0]._color_ == player._color_:
                        self.selected_point = clicked_point_idx + 1
                        print(f"Ficha seleccionada: {self.selected_point}")
                        self._try_execute_move() # Intentar mover si ya tenemos dado
                    else:
                        print("Punto vacío o no es tu ficha.")
                return

    # --- INICIO DE NUEVOS MÉTODOS DE AYUDA ---

    def _reset_selection(self):
        """Limpia las selecciones de ficha y dado."""
        self.selected_point = None
        self.selected_dice = None

    def _end_turn(self):
        """Termina el turno actual y pasa al siguiente jugador."""
        print("-" * 20)
        self._game_.switch_turn()
        self.game_phase = "ROLL"
        self._reset_selection()

    def _try_execute_move(self):
        """
        Intenta ejecutar un movimiento si tanto la ficha/barra como el dado
        han sido seleccionados.
        """
        if self.selected_dice is None or self.selected_point is None:
            return # Faltan datos para mover

        # Lógica de Reingreso
        if self.game_phase == "REENTRY":
            if self.selected_point == -1: # Barra seleccionada
                if self._game_.attempt_reentry(self.selected_dice):
                    print(f"Reingreso exitoso con dado {self.selected_dice}.")
                else:
                    print(f"Reingreso fallido con dado {self.selected_dice}.")
                # Actualizar estado (incluso si falla, para resetear selección)
                self._update_game_state_after_action()
            return

        # Lógica de Movimiento Normal
        if self.game_phase == "MOVE":
            if self.selected_point > 0: # Ficha seleccionada
                if self._game_.attempt_move(self.selected_point, self.selected_dice):
                    print(f"Movimiento exitoso desde {self.selected_point} con dado {self.selected_dice}.")
                else:
                    print(f"Movimiento fallido desde {self.selected_point} con dado {self.selected_dice}.")
                # Actualizar estado (incluso si falla, para resetear selección)
                self._update_game_state_after_action()
            return

    def _update_game_state_after_roll(self):
        """
        Llamado después de 'roll_dice'. 
        Comprueba si hay movimientos posibles y actualiza la fase.
        """
        player = self._game_.get_current_player()
        checkers_on_bar = len(self._game_._board_._bar_[player._color_])
        
        if checkers_on_bar > 0:
            self.game_phase = "REENTRY"
            # Comprobar si el reingreso es posible (lógica del cli)
            possible_moves = [r for r in self._game_._moves_ if self._game_._board_.is_reentry_possible(player._color_, r)]
            if not possible_moves:
                print("No hay movimientos posibles para reingresar. Pierdes el turno.")
                self._game_._moves_ = [] # Limpiar movimientos
                self._end_turn()
        else:
            self.game_phase = "MOVE"
            # (Opcional) Se podría añadir una comprobación de 'has_any_valid_move'
            # pero por simplicidad, dejamos que el jugador use "Pasar"
            
    def _update_game_state_after_action(self):
        """
        Llamado después de 'attempt_move' o 'attempt_reentry'.
        Comprueba si el juego terminó, si quedan movimientos, o si el turno termina.
        """
        self._reset_selection() # Siempre limpiar selección después de un intento
        
        # 1. Comprobar victoria
        if self._game_.is_game_over():
            self.game_phase = "GAME_OVER"
            # El mensaje de victoria en is_game_over() se imprime en consola
            # Asignamos el ganador para la UI
            if self._game_._board_.get_borne_off_count("white") == 15:
                self.winner = "white"
            else:
                self.winner = "black"
            return

        # 2. Comprobar si quedan movimientos
        if not self._game_._moves_:
            self._end_turn()
            return
            
        # 3. Si quedan movimientos, comprobar si la fase debe cambiar
        # (p.ej. de REENTRY a MOVE)
        player = self._game_.get_current_player()
        checkers_on_bar = len(self._game_._board_._bar_[player._color_])
        
        if checkers_on_bar > 0:
            self.game_phase = "REENTRY"
            # Comprobar si el reingreso sigue siendo posible
            possible_moves = [r for r in self._game_._moves_ if self._game_._board_.is_reentry_possible(player._color_, r)]
            if not possible_moves:
                print("No hay más movimientos posibles para reingresar. Pierdes el turno.")
                self._game_._moves_ = []
                self._end_turn()
        else:
            self.game_phase = "MOVE" # Continuar moviendo

    # --- FIN DE NUEVOS MÉTODOS DE AYUDA ---

    def run(self):
        # --- BUCLE PRINCIPAL LIGERAMENTE MODIFICADO ---
        while self.running:
            # Comprobar victoria al inicio de cada frame
            # (esto es redundante si _update_game_state_after_action funciona,
            # pero es una buena salvaguarda)
            if self.game_phase != "GAME_OVER" and self._game_.is_game_over():
                self.game_phase = "GAME_OVER"
                self.winner = "white" if self._game_._board_.get_borne_off_count("white") == 15 else "black"

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