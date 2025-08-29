class Player:
    def __init__(self, name: str, color: str):
        self._name_ = name
        self._color_ = color

    def __repr__(self) -> str:
        return f"Player(name='{self._name_}', color='{self._color_}')"