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