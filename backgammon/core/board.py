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
