# main.py

from core.backgammongame import BackgammonGame
from pygame_ui.pygameui import PygameUI

def main():
    """
    Función principal para inicializar y correr el juego.
    """
    print("Iniciando el juego de Backgammon...")
    game = BackgammonGame()
    ui = PygameUI(game)
    ui.run()

if __name__ == "__main__":
    main()