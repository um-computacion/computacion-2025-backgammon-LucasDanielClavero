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