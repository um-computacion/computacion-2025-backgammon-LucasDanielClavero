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