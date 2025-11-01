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
        start_idx = start_point - 1
        if not (0 <= start_idx < 24) or \
           not self._board_._points_[start_idx] or \
           self._board_._points_[start_idx][0]._color_ != player._color_:
            print(f"Movimiento inválido: No tienes fichas en el punto {start_point}.")
            return False
        
        if player._color_ == "white":
            end_point = start_point - dice_roll
        else: 
            end_point = start_point + dice_roll
            
        if not (1 <= end_point <= 24):
            if not self._board_.all_checkers_in_home_board(player._color_):
                print("Movimiento inválido: Todas tus fichas deben estar en el cuadrante final para sacarlas.")
                return False

            if (player._color_ == "white" and end_point == 0) or \
               (player._color_ == "black" and end_point == 25):
                self._board_.bear_off_checker(start_point)
                self._moves_.remove(dice_roll)
                return True

            if (player._color_ == "white" and end_point < 0) or \
               (player._color_ == "black" and end_point > 25):
                is_highest_checker = True
                if player._color_ == "white":
                    for p_idx in range(5, start_idx, -1):
                        if self._board_._points_[p_idx] and self._board_._points_[p_idx][0]._color_ == "white":
                            is_highest_checker = False
                            break
                else: 
                    for p_idx in range(18, start_idx):
                        if self._board_._points_[p_idx] and self._board_._points_[p_idx][0]._color_ == "black":
                            is_highest_checker = False
                            break
                
                if is_highest_checker:
                    self._board_.bear_off_checker(start_point)
                    self._moves_.remove(dice_roll)
                    return True
                else:
                    print(f"Movimiento inválido: No puedes usar un dado de {dice_roll} desde {start_point} porque tienes fichas en puntos más altos.")
                    return False

            print("Movimiento inválido para sacar la ficha.")
            return False
        
        if self._board_.is_valid_move(start_point, end_point, player._color_):
            self._board_.move_checker(start_point, end_point)
            self._moves_.remove(dice_roll)
            return True
        else:
            print(f"Movimiento inválido. El punto {end_point} está bloqueado.")
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
        if self._board_.get_borne_off_count("white") == 15:
            print("\n" + "=" * 40)
            print("¡JUEGO TERMINADO! ¡El jugador 1 (White) GANA!")
            print("=" * 40)
            return True
        if self._board_.get_borne_off_count("black") == 15:
            print("\n" + "=" * 40)
            print("¡JUEGO TERMINADO! ¡El jugador 2 (Black) GANA!")
            print("=" * 40)
            return True
        return False