<PRIMERA CONSULTA EN AREA DE DESARROLLO>

Herramienta utilizada: Gemini PRO

Promp: Necesito la clase Python más simple para una ficha de Backgammon. Debe llamarse `Checker` y tener solo un atributo `_color_` (string) inicializado en el constructor, y un método `__repr__` para mostrar su estado.

Resultado extraido:
class Checker:

    def __init__(self, color: str):
        self._color_ = color

    def __repr__(self) -> str:
        return f"Checker(color='{self._color_}')"

-------------------------------------------------------------------------------------------

<SEGUNDA CONSULTA EN AREA DE DESARROLLO>

Herramienta utilizada: Gemini PRO

Promp: Ahora necesito la clase `Dice` para gestionar los dados. Debe usar el módulo `random`. Debe tener un método `roll()` que genere dos números aleatorios (1-6) y los guarde en una lista interna `_values_`. También necesito un método `get_moves()` que devuelva una lista de movimientos: si los dados son iguales (dobles), debe devolver una lista con 4 veces ese número; si son diferentes, debe devolver una lista con los dos números.

Resultado extraido:
import random
class Dice:
    def __init__(self):
        self._values_ = []

    def roll(self) -> list[int]:
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        self._values_ = [die1, die2]
        return self._values_
    
    def get_moves(self) -> list[int]:
        if not self._values_:
            return []
        die1, die2 = self._values_
        if die1 == die2:
            return [die1] * 4
        else:
            return [die1, die2]

-------------------------------------------------------------------------------------------

<TERCERA CONSULTA EN AREA DE DESARROLLO>

Herramienta utilizada: Gemini PRO

Promp: Necesito una clase `Player` simple. Debe tener un atributo `_name_` (string) y `_color_` (string), ambos inicializados en el constructor. También debe tener un método `__repr__`.

Resultado extraido:
class Player:
    def __init__(self, name: str, color: str):
        self._name_ = name
        self._color_ = color

    def __repr__(self) -> str:
        return f"Player(name='{self._name_}', color='{self._color_}')"

-------------------------------------------------------------------------------------------

<CUARTA CONSULTA EN AREA DE DESARROLLO>

Herramienta utilizada: Gemini PRO

Promp: Necesito la clase `Board` para el Backgammon, que importe la clase `Checker` (del mismo directorio).
Requisitos:
1.  `__init__`: Debe crear `_points_` (una lista de 24 listas vacías) y `_bar_` (un dict para 'white' y 'black', ambas listas vacías).
2.  Debe llamar a un método `_setup_board_()` que coloque las 15 fichas de cada color en la posición inicial estándar del Backgammon (2 blancas en el punto 0, 5 en el 11, etc., y las negras opuestas).
3.  `is_valid_move(start_point, end_point, player_color)`: Valida si el movimiento es legal (dirección correcta, punto de destino no bloqueado por 2+ oponentes, el jugador mueve su propio color).
4.  `move_checker(start_point, end_point)`: Mueve la ficha. Si el punto de destino tiene 1 ficha oponente (un 'blot'), debe mover esa ficha oponente al `_bar_` correspondiente.
5.  `is_reentry_possible(player_color, dice_roll)`: Verifica si una ficha del `_bar_` puede reingresar al tablero usando el `dice_roll`.
6.  `reenter_checker(player_color, dice_roll)`: Mueve la ficha del `_bar_` al tablero (calculando el índice de destino), capturando un 'blot' oponente si lo hubiera.

Resultado extraido:
from .checker import Checker
class Board:
    def __init__(self):
        self._points_ = [[] for _ in range(24)]
        self._bar_ = {"white": [], "black": []}
        self._setup_board_()

    def __repr__(self) -> str:
        return f"Board(points={len(self._points_)})"
    
    def _setup_board_(self):
        self._points_ = [[] for _ in range(24)]
        self._bar_ = {"white": [], "black": []}

        self._points_[0].extend([Checker("white")] * 2)
        self._points_[11].extend([Checker("white")] * 5)
        self._points_[16].extend([Checker("white")] * 3)
        self._points_[18].extend([Checker("white")] * 5)

        self._points_[23].extend([Checker("black")] * 2)
        self._points_[12].extend([Checker("black")] * 5)
        self._points_[7].extend([Checker("black")] * 3)
        self._points_[5].extend([Checker("black")] * 5)

    def move_checker(self, start_point: int, end_point: int):
        start_idx = start_point - 1
        end_idx = end_point - 1

        checker = self._points_[start_idx].pop()
        destination_checkers = self._points_[end_idx]

        if destination_checkers and destination_checkers[0]._color_ != checker._color_:
            hit_checker = self._points_[end_idx].pop()
            self._bar_[hit_checker._color_].append(hit_checker)
        
        self._points_[end_idx].append(checker)

    def is_valid_move(self, start_point: int, end_point: int, player_color: str) -> bool:

        start_idx = start_point - 1
        end_idx = end_point - 1

        if not (0 <= start_idx < 24 and 0 <= end_idx < 24):
            return False

        if not self._points_[start_idx] or self._points_[start_idx][0]._color_ != player_color:
            return False

        destination_checkers = self._points_[end_idx]

        if destination_checkers and destination_checkers[0]._color_ != player_color and len(destination_checkers) > 1:
            return False

        if player_color == "white" and start_idx < end_idx:
            return False
        if player_color == "black" and start_idx > end_idx:
            return False
        return True
        
    def move_checker(self, start_point: int, end_point: int):

        start_idx = start_point - 1
        end_idx = end_point - 1

        checker = self._points_[start_idx].pop()
        destination_checkers = self._points_[end_idx]

        if destination_checkers and destination_checkers[0]._color_ != checker._color_:
            hit_checker = self._points_[end_idx].pop()
            self._bar_[hit_checker._color_].append(hit_checker)
        
        self._points_[end_idx].append(checker)

    def is_reentry_possible(self, player_color: str, dice_roll: int) -> bool:

        if player_color == "white":
            target_idx = 24 - dice_roll
        else: 
            target_idx = dice_roll - 1

        destination_checkers = self._points_[target_idx]
        if destination_checkers and destination_checkers[0]._color_ != player_color and len(destination_checkers) > 1:
            return False  
        
        return True
    
    def reenter_checker(self, player_color: str, dice_roll: int):

        if player_color == "white":
            target_idx = 24 - dice_roll
        else:  
            target_idx = dice_roll - 1

        checker = self._bar_[player_color].pop()
        destination_checkers = self._points_[target_idx]

        if destination_checkers and destination_checkers[0]._color_ != checker._color_:
            hit_checker = self._points_[target_idx].pop()
            self._bar_[hit_checker._color_].append(hit_checker)

        self._points_[target_idx].append(checker)

-------------------------------------------------------------------------------------------

<QUINTA CONSULTA EN AREA DE DESARROLLO>

Herramienta utilizada: Gemini PRO

Promp: Finalmente, necesito la clase principal `BackgammonGame` que integre todo. Debe importar `Board`, `Player` y `Dice` (del mismo directorio).
1.  `__init__`: Debe crear una instancia de `Board`, dos instancias de `Player` (con nombres por defecto y colores 'white' y 'black'), y una instancia de `Dice`. Debe gestionar el turno actual (`_current_player_idx_`) y una lista de movimientos restantes (`_moves_`).
2.  `get_current_player()`: Devuelve el objeto Player actual.
3.  `roll_dice()`: Debe llamar a `dice.roll()` y luego obtener los movimientos de `dice.get_moves()`, guardándolos en `_moves_`.
4.  `switch_turn()`: Cambia el `_current_player_idx_` al siguiente jugador.
5.  `attempt_move(start_point, dice_roll)`: Intenta mover una ficha. Debe calcular el `end_point` (restando el dado para 'white', sumando para 'black'). Debe usar `board.is_valid_move()` y `board.move_checker()`. Si el movimiento es exitoso, debe eliminar el `dice_roll` de la lista `_moves_` y devolver True.
6.  `attempt_reentry(dice_roll)`: Intenta reingresar una ficha desde la barra. Debe usar `board.is_reentry_possible()` y `board.reenter_checker()`. Si es exitoso, elimina el dado de `_moves_` y devuelve True.
7.  `is_game_over()`: Por ahora, solo debe devolver `False`.

Resultado extraido:
from .board import Board
from .player import Player
from .dice import Dice

class BackgammonGame:

    def __init__(self, player1_name: str = "Jugador 1", player2_name: str = "Jugador 2"):
        self._board_ = Board()
        self._players_ = [Player(player1_name, "white"), Player(player2_name, "black")]
        self._dice_ = Dice()
        self._current_player_idx_ = 0
        self._moves_ = []

    def get_current_player(self) -> Player:
        return self._players_[self._current_player_idx_]
    
    def roll_dice(self):
        self._dice_.roll()
        self._moves_ = self._dice_.get_moves()
        print(f"{self.get_current_player()._name_} sacó: {self._dice_._values_}")
        if len(self._moves_) == 4:
            print("¡Dobles! Tienes cuatro movimientos.")

    def switch_turn(self):
        self._current_player_idx_ = (self._current_player_idx_ + 1) % 2
        print("-" * 40)
        print(f"Es el turno de {self.get_current_player()._name_} ({self.get_current_player()._color_})")

    def attempt_move(self, start_point: int, dice_roll: int) -> bool:

        player = self.get_current_player()
        
        if player._color_ == "white":
            end_point = start_point - dice_roll
        else:  # Negro
            end_point = start_point + dice_roll

        if not (1 <= end_point <= 24):
            print("Movimiento inválido: Aún no se pueden sacar fichas del tablero.")
            return False

        if self._board_.is_valid_move(start_point, end_point, player._color_):
            self._board_.move_checker(start_point, end_point)
            self._moves_.remove(dice_roll)
            return True
        else:
            print("Movimiento inválido. Por favor, intenta de nuevo.")
            return False
        
    def attempt_reentry(self, dice_roll: int) -> bool:

        player = self.get_current_player()
        if self._board_.is_reentry_possible(player._color_, dice_roll):
            self._board_.reenter_checker(player._color_, dice_roll)
            self._moves_.remove(dice_roll)
            return True
        else:
            target_point = (25 - dice_roll) if player._color_ == 'white' else dice_roll
            print(f"No se puede reingresar en el punto {target_point}. Está bloqueado.")
            return False
        
    def is_game_over(self) -> bool:
        return False

-------------------------------------------------------------------------------------------

<SEXTA CONSULTA EN AREA DE DESARROLLO>

Herramienta utilizada: Gemini PRO

Promp: Necesito un script principal (p.ej., cli.py) para correr el BackgammonGame. Debe importar el juego y el tablero. Debe incluir:

1.  Una función print_board(board) para visualizar el estado del tablero en texto.

2.  Un bucle main() que maneje el turno de cada jugador.

3.  Lógica para pedir al jugador que 'lance' (roll) los dados.

4.  Lógica para manejar los movimientos: si hay fichas en la barra, debe forzar attempt_reentry; si no, debe permitir attempt_move.

5.  Debe pedir al usuario el punto de inicio y el dado a usar, validando que el dado esté disponible.

6.  Debe seguir pidiendo movimientos hasta que se acaben los _moves_ y luego cambiar de turno con switch_turn().

7.  El bucle debe terminar cuando game.is_game_over() sea verdadero.

Resultado extraido:
import sys
sys.path.append('..')

from core.backgammongame import BackgammonGame
class CLI:
    def __init__(self, game: BackgammonGame):
        self._game_ = game

    def _display_board_(self):
        board = self._game_._board_
        points = board._points_

        top_line = "13 14 15 16 17 18 | BAR | 19 20 21 22 23 24\n"
        top_board = ""
        for i in range(5):
            row = ""
            for p in range(12, 18):
                row += f" {points[p][i]._color_[0].upper()} " if i < len(points[p]) else " . "
            
            if i == 2:
                row += f"| B:{len(board._bar_['black'])} |" 
            elif i == 3:
                row += f"| W:{len(board._bar_['white'])} |" 
            else:
                row += "|     |"

            for p in range(18, 24):
                row += f" {points[p][i]._color_[0].upper()} " if i < len(points[p]) else " . "
            top_board += row + "\n"

        bottom_line = "12 11 10  9  8  7 |     |  6  5  4  3  2  1\n"
        bottom_board = ""

        for i in range(4, -1, -1):
            row = ""
            for p in range(11, 5, -1):
                row += f" {points[p][i]._color_[0].upper()} " if i < len(points[p]) else " . "
            row += "|     |"
            for p in range(5, -1, -1):
                row += f" {points[p][i]._color_[0].upper()} " if i < len(points[p]) else " . "
            bottom_board += row + "\n"
        
        print("\n" + top_line + top_board)
        print("-" * 45)
        print(bottom_board + bottom_line)
    

    def _handle_reentry_turn_(self, player):
        """Gestiona el turno de un jugador que debe reingresar fichas."""
        board = self._game_._board_
        checkers_on_bar = len(board._bar_[player._color_])
        print(f"Tienes {checkers_on_bar} ficha(s) en la barra. Debes reingresar.")

        possible_moves = [r for r in self._game_._moves_ if board.is_reentry_possible(player._color_, r)]
        if not possible_moves:
            print("No hay movimientos posibles para reingresar. Pierdes el turno.")
            self._game_._moves_ = []
            return

        dice_roll = self._get_player_input_for_dice_("¿Qué dado quieres usar para reingresar? ")
        if dice_roll:
            self._game_.attempt_reentry(dice_roll)

    def _handle_normal_turn_(self):
        """Gestiona un turno normal de juego."""
        start_point_str = input("Ingresa el punto desde el que quieres mover (o 'p' para pasar): ")
        if start_point_str.lower() == 'p':
            print("Elegiste pasar tu turno.")
            self._game_._moves_ = []
            return

        start_point = int(start_point_str)
        dice_roll = self._get_player_input_for_dice_(f"¿Qué dado quieres usar para el punto {start_point}? ")
        if dice_roll:
            self._game_.attempt_move(start_point, dice_roll)

    def _get_player_input_for_dice_(self, message: str) -> int | None:
        """Pide al jugador que elija un dado y valida la entrada."""
        while True:
            try:
                dice_roll_str = input(message)
                dice_roll = int(dice_roll_str)
                if dice_roll not in self._game_._moves_:
                    print("Ese no es un dado válido o disponible.")
                    continue
                return dice_roll
            except ValueError:
                print("Entrada inválida. Por favor, ingresa un número.")
        return None
    
    def run(self):
        """Inicia y gestiona el bucle principal del juego para la CLI."""
        print("--- ¡Bienvenido a Backgammon! ---")
        while not self._game_.is_game_over():
            self._display_board_()
            player = self._game_.get_current_player()
            print(f"Turno: {player._name_} ({player._color_})")

            self._game_.roll_dice()
            
            while self._game_._moves_:
                print(f"Movimientos disponibles: {self._game_._moves_}")
                checkers_on_bar = len(self._game_._board_._bar_[player._color_])
                
                try:
                    if checkers_on_bar > 0:
                        self._handle_reentry_turn_(player)
                    else:
                        self._handle_normal_turn_()
                    
                    if self._game_._moves_:
                        self._display_board_()

                except ValueError:
                    print("Entrada inválida. Por favor, ingresa solo números.")
                except Exception as e:
                    print(f"Ocurrió un error: {e}")

            if self._game_.is_game_over(): 
                break

            self._game_.switch_turn()
            
if __name__ == "__main__":
    game = BackgammonGame()
    
    cli = CLI(game)
    
    cli.run()

-------------------------------------------------------------------------------------------

<SEPTIMA CONSULTA EN AREA DE DESARROLLO>

Herramienta utilizada: Gemini PRO

Promp: (ADJUNTO CODIGO DE CLI - CLASES - PDF del Trabajo) el cli funciona perfectamente, necesito que Generes la interfaz grafica utilizando la misma logica que en el cli y con los requerimientos que aparecen en el trabajo practico del PDF que te adjunto

Resultado extraido:
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
