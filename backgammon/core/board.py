from .checker import Checker
class Board:
    def __init__(self):
        self._setup_board_()

    def __repr__(self) -> str:
        return f"Board(points={len(self._points_)})"
    
    def _setup_board_(self):
        self._points_ = [[] for _ in range(24)]
        self._bar_ = {"white": [], "black": []}
        self._borne_off_ = {"white": [], "black": []}

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

    def all_checkers_in_home_board(self, player_color: str) -> bool:
        if self._bar_[player_color]: 
            return False
        if player_color == "white":
            for i in range(6, 24):
                if self._points_[i] and self._points_[i][0]._color_ == "white":
                    return False
        else:
            for i in range(0, 18):
                if self._points_[i] and self._points_[i][0]._color_ == "black":
                    return False
        return True

    def bear_off_checker(self, start_point: int):
        start_idx = start_point - 1
        checker = self._points_[start_idx].pop()
        self._borne_off_[checker._color_].append(checker)
        print(f"¡Ficha sacada del punto {start_point}!")

    def get_borne_off_count(self, player_color: str) -> int:
        return len(self._borne_off_[player_color])