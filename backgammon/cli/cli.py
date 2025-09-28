import sys
sys.path.append('..')

from core.backgammongame import BackgammonGame
class CLI:
    """
    Interfaz de línea de comandos para el juego de Backgammon.
    """
    def __init__(self, game: BackgammonGame):
        self._game_ = game

    def _display_board_(self):
        """Muestra una representación textual del tablero, incluyendo la barra."""
        board = self._game_._board_
        points = board._points_

        top_line = "13 14 15 16 17 18 | BAR | 19 20 21 22 23 24\n"
        top_board = ""
        for i in range(5):
            row = ""
            for p in range(12, 18):
                row += f" {points[p][i]._color_[0].upper()} " if i < len(points[p]) else " . "
            
            if i == 2:
                row += f"| N:{len(board._bar_['black'])} |"
            elif i == 3:
                row += f"| B:{len(board._bar_['white'])} |"
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