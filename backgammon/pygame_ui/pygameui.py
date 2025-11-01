import pygame
from core.backgammongame import BackgammonGame

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
        self._small_font_ = None
        self.running = True

        self.selected_point = None
        self.selected_dice = None
        self.game_phase = "ROLL"
        self.winner = None
        
        self.roll_button_rect = None
        self.pass_button_rect = None
        self.dice_button_rects = []

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
        board = self._game_._board_
        player_color = self._game_.get_current_player()._color_

        for i, point in enumerate(board._points_):
            for j, checker in enumerate(point):
                color = WHITE if checker._color_ == "white" else BLACK
                x, y = self._get_coords_for_point(i, j + 1)
                
                if self.game_phase == "MOVE" and self.selected_point == (i + 1):
                    pygame.draw.circle(self._screen_, RED, (x, y), CHECKER_RADIUS + 3)

                pygame.draw.circle(self._screen_, color, (x, y), CHECKER_RADIUS)
                pygame.draw.circle(self._screen_, (128,128,128), (x, y), CHECKER_RADIUS, 2)

        bar_x = SCREEN_WIDTH // 2
        for i, checker in enumerate(board._bar_["white"]):
            y = SCREEN_HEIGHT // 2 - 40 - i * (CHECKER_RADIUS * 2)
            if self.game_phase == "REENTRY" and self.selected_point == -1 and player_color == "white":
                 pygame.draw.circle(self._screen_, RED, (bar_x, y), CHECKER_RADIUS + 3)
            pygame.draw.circle(self._screen_, WHITE, (bar_x, y), CHECKER_RADIUS)

        for i, checker in enumerate(board._bar_["black"]):
            y = SCREEN_HEIGHT // 2 + 40 + i * (CHECKER_RADIUS * 2)
            if self.game_phase == "REENTRY" and self.selected_point == -1 and player_color == "black":
                 pygame.draw.circle(self._screen_, RED, (bar_x, y), CHECKER_RADIUS + 3)
            pygame.draw.circle(self._screen_, BLACK, (bar_x, y), CHECKER_RADIUS)

    def _draw_ui(self):
        player = self._game_.get_current_player()
        center_x = SCREEN_WIDTH // 2
        
        if self.game_phase == "GAME_OVER":
            winner_name = "BLANCAS" if self.winner == "white" else "NEGRAS"
            text_surf = self._font_.render(f"¡JUEGO TERMINADO! ¡GANA {winner_name}!", True, WHITE, BLACK)
            text_rect = text_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 2))
            self._screen_.blit(text_surf, text_rect)
            return

        turn_text_surf = self._font_.render(f"Turno: {player._name_} ({player._color_})", True, WHITE)
        turn_text_rect = turn_text_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 2 - 60))
        self._screen_.blit(turn_text_surf, turn_text_rect)

        self.dice_button_rects = []
        
        if self.game_phase == "ROLL":
            self.roll_button_rect = pygame.Rect(0, 0, 140, 40)
            self.roll_button_rect.center = (center_x, SCREEN_HEIGHT // 2)
            pygame.draw.rect(self._screen_, GREY, self.roll_button_rect, border_radius=5)
            roll_text_surf = self._font_.render("Tirar Dados", True, BLACK)
            roll_text_rect = roll_text_surf.get_rect(center=self.roll_button_rect.center)
            self._screen_.blit(roll_text_surf, roll_text_rect)
        
        elif self.game_phase in ["MOVE", "REENTRY"]:
            moves = self._game_._moves_
            total_width = len(moves) * 40 + max(0, len(moves) - 1) * 10
            start_x = center_x - total_width // 2
            
            for i, move in enumerate(moves):
                die_rect = pygame.Rect(start_x + i * 50, SCREEN_HEIGHT // 2 - 20, 40, 40)
                self.dice_button_rects.append((die_rect, move))
                
                btn_color = GREEN if self.selected_dice == move else GREY
                pygame.draw.rect(self._screen_, btn_color, die_rect, border_radius=5)
                
                move_text_surf = self._font_.render(str(move), True, BLACK)
                move_text_rect = move_text_surf.get_rect(center=die_rect.center)
                self._screen_.blit(move_text_surf, move_text_rect)

            self.pass_button_rect = pygame.Rect(0, 0, 140, 30)
            self.pass_button_rect.center = (center_x, SCREEN_HEIGHT // 2 + 50)
            pygame.draw.rect(self._screen_, (255, 100, 100), self.pass_button_rect, border_radius=5)
            pass_text_surf = self._small_font_.render("Pasar Turno", True, BLACK)
            pass_text_rect = pass_text_surf.get_rect(center=self.pass_button_rect.center)
            self._screen_.blit(pass_text_surf, pass_text_rect)

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
        x, y = pos
        bar_start_x = (SCREEN_WIDTH - BAR_WIDTH) // 2
        bar_end_x = (SCREEN_WIDTH + BAR_WIDTH) // 2

        if bar_start_x < x < bar_end_x: return -1

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
        if self.game_phase == "GAME_OVER":
            return

        player = self._game_.get_current_player()

        if self.game_phase == "ROLL":
            if self.roll_button_rect and self.roll_button_rect.collidepoint(pos):
                self._game_.roll_dice()
                self._update_game_state_after_roll()
            return

        if self.game_phase in ["MOVE", "REENTRY"]:
            if self.pass_button_rect and self.pass_button_rect.collidepoint(pos):
                print("Jugador pasa el turno.")
                self._game_._moves_ = []
                self._end_turn()
                return

            clicked_dice = None
            for rect, move in self.dice_button_rects:
                if rect.collidepoint(pos):
                    clicked_dice = move
                    break
            
            if clicked_dice is not None:
                self.selected_dice = clicked_dice
                print(f"Dado seleccionado: {self.selected_dice}")
                self._try_execute_move()
                return

            clicked_point_idx = self._get_point_from_pos(pos)
            
            if clicked_point_idx is None:
                self.selected_point = None
                return

            if self.game_phase == "REENTRY":
                if clicked_point_idx == -1:
                    self.selected_point = -1
                    print("Barra seleccionada.")
                    self._try_execute_move()
                else:
                    print("Debes hacer clic en la barra para reingresar.")
                return

            if self.game_phase == "MOVE":
                if clicked_point_idx >= 0:
                    if self._game_._board_._points_[clicked_point_idx] and \
                       self._game_._board_._points_[clicked_point_idx][0]._color_ == player._color_:
                        self.selected_point = clicked_point_idx + 1
                        print(f"Ficha seleccionada: {self.selected_point}")
                        self._try_execute_move()
                    else:
                        print("Punto vacío o no es tu ficha.")
                return

    def _reset_selection(self):
        self.selected_point = None
        self.selected_dice = None

    def _end_turn(self):
        print("-" * 20)
        self._game_.switch_turn()
        self.game_phase = "ROLL"
        self._reset_selection()

    def _try_execute_move(self):
        if self.selected_dice is None or self.selected_point is None:
            return

        if self.game_phase == "REENTRY":
            if self.selected_point == -1:
                if self._game_.attempt_reentry(self.selected_dice):
                    print(f"Reingreso exitoso con dado {self.selected_dice}.")
                else:
                    print(f"Reingreso fallido con dado {self.selected_dice}.")
                self._update_game_state_after_action()
            return

        if self.game_phase == "MOVE":
            if self.selected_point > 0:
                if self._game_.attempt_move(self.selected_point, self.selected_dice):
                    print(f"Movimiento exitoso desde {self.selected_point} con dado {self.selected_dice}.")
                else:
                    print(f"Movimiento fallido desde {self.selected_point} con dado {self.selected_dice}.")
                self._update_game_state_after_action()
            return

    def _update_game_state_after_roll(self):
        player = self._game_.get_current_player()
        checkers_on_bar = len(self._game_._board_._bar_[player._color_])
        
        if checkers_on_bar > 0:
            self.game_phase = "REENTRY"
            possible_moves = [r for r in self._game_._moves_ if self._game_._board_.is_reentry_possible(player._color_, r)]
            if not possible_moves:
                print("No hay movimientos posibles para reingresar. Pierdes el turno.")
                self._game_._moves_ = []
                self._end_turn()
        else:
            self.game_phase = "MOVE"
            
    def _update_game_state_after_action(self):
        self._reset_selection()
        
        if self._game_.is_game_over():
            self.game_phase = "GAME_OVER"
            if self._game_._board_.get_borne_off_count("white") == 15:
                self.winner = "white"
            else:
                self.winner = "black"
            return

        if not self._game_._moves_:
            self._end_turn()
            return
            
        player = self._game_.get_current_player()
        checkers_on_bar = len(self._game_._board_._bar_[player._color_])
        
        if checkers_on_bar > 0:
            self.game_phase = "REENTRY"
            possible_moves = [r for r in self._game_._moves_ if self._game_._board_.is_reentry_possible(player._color_, r)]
            if not possible_moves:
                print("No hay más movimientos posibles para reingresar. Pierdes el turno.")
                self._game_._moves_ = []
                self._end_turn()
        else:
            self.game_phase = "MOVE"

    def run(self):
        while self.running:
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