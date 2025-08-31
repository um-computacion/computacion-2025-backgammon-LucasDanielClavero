from .checker import Checker
class Board:
    def __init__(self):
        self._points_ = [[] for _ in range(24)]
        self._bar_ = {"white": [], "black": []}
        self._setup_board_()

    def __repr__(self) -> str:
        return f"Board(points={len(self._points_)})"