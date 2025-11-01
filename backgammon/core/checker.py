class Checker:
    def __init__(self, color: str):
        self._color_ = color

    def __repr__(self) -> str:
        return f"Checker(color='{self._color_}')"