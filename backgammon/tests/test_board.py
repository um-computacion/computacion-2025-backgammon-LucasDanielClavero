import unittest
# Asegúrate de que la ruta de importación sea la correcta según la estructura de tu proyecto.
# Si tu archivo de test está en una carpeta 'tests' al mismo nivel que 'core',
# necesitarás ajustar el path o la forma en que ejecutas los tests.
# Por simplicidad, este ejemplo asume que Board es directamente importable.
from core.board import Board
from core.checker import Checker

class TestBoard(unittest.TestCase):

    def setUp(self):
        """Este método se ejecuta antes de cada prueba."""
        self.board = Board()

    def test_initial_setup(self):
        """
        Verifica que el tablero se inicialice correctamente con la disposición
        estándar de las fichas de Backgammon.
        """
        # Verificar el número total de puntos y la barra vacía
        self.assertEqual(len(self.board._points_), 24)
        self.assertEqual(len(self.board._bar_["white"]), 0)
        self.assertEqual(len(self.board._bar_["black"]), 0)

        # Verificar posiciones y colores de las fichas blancas
        self.assertEqual(len(self.board._points_[0]), 2)
        self.assertEqual(self.board._points_[0][0]._color_, "white")
        self.assertEqual(len(self.board._points_[11]), 5)
        self.assertEqual(self.board._points_[11][0]._color_, "white")
        self.assertEqual(len(self.board._points_[16]), 3)
        self.assertEqual(self.board._points_[16][0]._color_, "white")
        self.assertEqual(len(self.board._points_[18]), 5)
        self.assertEqual(self.board._points_[18][0]._color_, "white")
        
        # Verificar posiciones y colores de las fichas negras
        self.assertEqual(len(self.board._points_[23]), 2)
        self.assertEqual(self.board._points_[23][0]._color_, "black")
        self.assertEqual(len(self.board._points_[12]), 5)
        self.assertEqual(self.board._points_[12][0]._color_, "black")
        self.assertEqual(len(self.board._points_[7]), 3)
        self.assertEqual(self.board._points_[7][0]._color_, "black")
        self.assertEqual(len(self.board._points_[5]), 5)
        self.assertEqual(self.board._points_[5][0]._color_, "black")

        # Verificar que la suma total de fichas es correcta
        total_checkers = sum(len(p) for p in self.board._points_)
        self.assertEqual(total_checkers, 30)

    def test_move_checker_simple(self):
        """Prueba un movimiento simple a un punto vacío."""
        # Mover una ficha blanca del punto 1 al 2 (índices 0 al 1)
        self.board._points_[1] = [] # Asegurarse que el destino está vacío
        self.board.move_checker(1, 2)
        self.assertEqual(len(self.board._points_[0]), 1)
        self.assertEqual(len(self.board._points_[1]), 1)
        self.assertEqual(self.board._points_[1][0]._color_, "white")

    def test_move_checker_and_hit_blot(self):
        """Prueba mover una ficha a un punto con una única ficha rival (blot)."""
        # Colocar una ficha negra en el punto 3 (índice 2) para ser capturada
        self.board._points_[2] = [Checker("black")]
        
        # Mover una ficha blanca del punto 1 al 3
        self.board.move_checker(1, 3)
        
        # Verificar que la ficha blanca se movió
        self.assertEqual(len(self.board._points_[0]), 1)
        self.assertEqual(len(self.board._points_[2]), 1)
        self.assertEqual(self.board._points_[2][0]._color_, "white")

        # Verificar que la ficha negra fue capturada y está en la barra
        self.assertEqual(len(self.board._bar_["black"]), 1)
        self.assertEqual(self.board._bar_["black"][0]._color_, "black")

    def test_is_valid_move(self):
        """Prueba varios escenarios para la validación de movimientos."""
        # Movimiento válido para las blancas
        self.assertTrue(self.board.is_valid_move(12, 10, "white"))
        
        # Movimiento válido para las negras
        self.assertTrue(self.board.is_valid_move(13, 15, "black"))
        
        # Inválido: Mover a un punto bloqueado por el oponente
        # Las negras tienen 2 fichas en el punto 24 (índice 23)
        self.assertFalse(self.board.is_valid_move(19, 24, "white"))
        
        # Inválido: Mover en la dirección incorrecta para las blancas
        self.assertFalse(self.board.is_valid_move(1, 3, "white"))

        # Inválido: Mover en la dirección incorrecta para las negras
        self.assertFalse(self.board.is_valid_move(24, 22, "black"))
        
        # Inválido: Mover desde un punto vacío
        self.assertFalse(self.board.is_valid_move(2, 4, "white"))
        
        # Inválido: Mover la ficha del oponente
        self.assertFalse(self.board.is_valid_move(1, 3, "black"))
        
        # Inválido: Mover fuera del tablero
        self.assertFalse(self.board.is_valid_move(24, 25, "black"))
        self.assertFalse(self.board.is_valid_move(0, 5, "white"))

    def test_reentry_possible(self):
        """Prueba si el reingreso desde la barra es posible."""
        # Es posible para las blancas reingresar en el punto 22 (tirando un 3)
        # porque el punto de destino (índice 21) está vacío.
        self.assertTrue(self.board.is_reentry_possible("white", 3))

        # Es posible para las negras reingresar en el punto 3 (tirando un 3)
        # porque el punto de destino (índice 2) está vacío.
        self.assertTrue(self.board.is_reentry_possible("black", 3))
        
        # No es posible para las blancas reingresar en el punto 24 (tirando un 1)
        # porque está bloqueado por dos fichas negras.
        self.assertFalse(self.board.is_reentry_possible("white", 1))

        # Es posible reingresar si hay un blot del oponente
        self.board._points_[2] = [Checker("white")] # punto 3
        self.assertTrue(self.board.is_reentry_possible("black", 3))
        
    def test_reenter_checker_simple(self):
        """Prueba el reingreso de una ficha a un punto vacío."""
        # Añadir una ficha negra a la barra
        self.board._bar_["black"].append(Checker("black"))
        
        # Reingresar con un dado de valor 4 (al punto 4, índice 3)
        self.board.reenter_checker("black", 4)
        
        # Verificar que la barra negra está vacía
        self.assertEqual(len(self.board._bar_["black"]), 0)
        # Verificar que la ficha está en el punto correcto
        self.assertEqual(len(self.board._points_[3]), 1)
        self.assertEqual(self.board._points_[3][0]._color_, "black")

    def test_reenter_and_hit_blot(self):
        """Prueba el reingreso de una ficha que captura un blot rival."""
        # Añadir una ficha blanca a la barra
        self.board._bar_["white"].append(Checker("white"))
        # Colocar una ficha negra (blot) en el punto de reingreso de las blancas
        # con un dado de 5 (punto 20, índice 19)
        self.board._points_[19] = [Checker("black")]
        
        self.board.reenter_checker("white", 5)
        
        # Verificar que la barra blanca está vacía
        self.assertEqual(len(self.board._bar_["white"]), 0)
        # Verificar que la ficha blanca está en el punto correcto
        self.assertEqual(len(self.board._points_[19]), 1)
        self.assertEqual(self.board._points_[19][0]._color_, "white")
        # Verificar que la ficha negra capturada está en la barra
        self.assertEqual(len(self.board._bar_["black"]), 1)
        self.assertEqual(self.board._bar_["black"][0]._color_, "black")
    def test_all_checkers_in_home_board(self):
        """
        Prueba la lógica de 'all_checkers_in_home_board' (líneas 88-99).
        """
        # 1. Caso Falso: Ficha en la barra
        self.board._bar_["white"].append(Checker("white"))
        self.assertFalse(self.board.all_checkers_in_home_board("white"))
        self.board._bar_["white"] = [] # Limpiar

        # 2. Caso Falso: Ficha blanca fuera del home (puntos 1-6 / índices 0-5)
        # (El setup inicial ya tiene fichas afuera, por ej. en punto 12 / índice 11)
        self.assertFalse(self.board.all_checkers_in_home_board("white"))

        # 3. Caso Falso: Ficha negra fuera del home (puntos 19-24 / índices 18-23)
        self.assertFalse(self.board.all_checkers_in_home_board("black"))

        # 4. Caso Verdadero: Mover todas las fichas al home
        # Limpiamos el tablero y ponemos fichas solo en el home
        self.board._points_ = [[] for _ in range(24)]
        self.board._points_[0].append(Checker("white")) # Punto 1
        self.board._points_[5].append(Checker("white")) # Punto 6
        self.assertTrue(self.board.all_checkers_in_home_board("white"))

        # 5. Caso Verdadero: Negro
        self.board._points_ = [[] for _ in range(24)]
        self.board._points_[18].append(Checker("black")) # Punto 19
        self.board._points_[23].append(Checker("black")) # Punto 24
        self.assertTrue(self.board.all_checkers_in_home_board("black"))

        # 6. Caso Falso: Ficha negra en el home blanco
        self.board._points_[0].append(Checker("black")) # Punto 1
        self.assertFalse(self.board.all_checkers_in_home_board("black"))


    def test_bear_off_checker(self):
        """
        Prueba la lógica de 'bear_off_checker' (líneas 103-106).
        """
        # El punto 1 (índice 0) tiene 2 fichas blancas
        self.assertEqual(len(self.board._points_[0]), 2)
        self.assertEqual(len(self.board._borne_off_["white"]), 0)

        # Sacamos una ficha del punto 1
        self.board.bear_off_checker(1)
        
        # Verificamos que se movió a 'borne_off'
        self.assertEqual(len(self.board._points_[0]), 1)
        self.assertEqual(len(self.board._borne_off_["white"]), 1)
        self.assertEqual(self.board._borne_off_["white"][0]._color_, "white")

    def test_get_borne_off_count(self):
        """
        Prueba la lógica de 'get_borne_off_count' (líneas 108-110).
        """
        self.assertEqual(self.board.get_borne_off_count("white"), 0)
        self.assertEqual(self.board.get_borne_off_count("black"), 0)

        # Añadimos una ficha manualmente para probar el conteo
        self.board._borne_off_["white"].append(Checker("white"))
        
        self.assertEqual(self.board.get_borne_off_count("white"), 1)
        self.assertEqual(self.board.get_borne_off_count("black"), 0)


if __name__ == '__main__':
    unittest.main()