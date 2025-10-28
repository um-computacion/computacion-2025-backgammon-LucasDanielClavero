<PRIMERA CONSULTA GENERAL>

Herramienta utilizada: Gemini PRO

Promp: (ADJUNTO PDF DEL PRACTICO) (ADJUNTO CAPTURA DE PANTALLA DE MI CARPETA DEL PROYECYO) estoy haciendo este practico (el del pdf) y ya funciona el codigo y tengo los tests cargados, ahora quiero hacer el coverage, puedes hacer un codigo que se adapte a mi estructura y me haga el coverage de mis codigos?

Resultado extraido: 

import subprocess
import os
import sys

# --- Configuración ---
SOURCE_DIRS = "core,cli"
TEST_DIR = "tests"
OUTPUT_FILENAME = "coverage_report.txt"

def main():
    """
    Función principal para ejecutar coverage y generar el reporte,
    incluso si las pruebas fallan.
    """
    print("--- Iniciando la generación del reporte de cobertura ---")
    
    python_executable = sys.executable

    # 1. Ejecutar las pruebas con coverage para recolectar datos.
    # Se ignora si las pruebas fallan para poder generar un reporte parcial.
    run_command = [
        python_executable, "-m", "coverage", "run",
        f"--source={SOURCE_DIRS}",
        "-m", "unittest", "discover",
        "-s", TEST_DIR
    ]
    
    print(f"Ejecutando comando: {' '.join(run_command)}")
    # Ejecutamos el comando sin 'check=True' para que no se detenga si hay errores.
    result = subprocess.run(
        run_command,
        capture_output=True,
        text=True,
        encoding='latin-1'
    )

    if result.returncode != 0:
        print("\n⚠️ ADVERTENCIA: Una o más pruebas fallaron. El reporte de cobertura generado será parcial e impreciso.")
        print("   Se recomienda corregir los errores en las pruebas para obtener un resultado válido.")
        print("\n--- Errores de Pruebas ---")
        print(result.stderr)
        print("--------------------------\n")
    else:
        print("Pruebas ejecutadas y datos de cobertura recolectados. ✅")

    # 2. Generar el reporte de texto sin importar el resultado de las pruebas.
    report_command = [python_executable, "-m", "coverage", "report", "-m"]
    
    try:
        print("Generando reporte...")
        report_content = subprocess.run(
            report_command,
            capture_output=True,
            text=True,
            check=True, # Aquí sí se necesita que el comando funcione
            encoding='latin-1'
        ).stdout
        
        # 3. Guardar el reporte en un archivo de texto.
        with open(OUTPUT_FILENAME, "w", encoding='latin-1') as f:
            f.write(report_content)
            
        print(f"Reporte guardado exitosamente en: '{os.path.abspath(OUTPUT_FILENAME)}' 📋")
        print("\n--- Proceso finalizado ---")
        print("\nContenido del Reporte:")
        print("--------------------------------------------------")
        print(report_content)
        print("--------------------------------------------------")

    except subprocess.CalledProcessError as e:
        print("Error crítico al intentar generar el reporte de coverage.")
        print("Esto puede suceder si no se recolectó ningún dato de cobertura,")
        print("posiblemente debido a un error de configuración o a que no se encontró ninguna prueba.")
        print(e.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

if __name__ == '__main__':
    unittest.main()

-------------------------------------------------------------------------------------------

<SEGUNDA CONSULTA GENERAL>

Herramienta utilizada: Gemini PRO

Promp: (ADJUNTO PDF DEL PRACTICO)(ADJUNTO TODOS LOS CODIGOS DE LAS CLASES) estoy realizando el practico del pdf que te estoy compartiendo, te paso tambien el codigo de las clases creadas, el juego ya esta andando, necesito que me desarrolles el pygame_ui

Resultado extraido:
# pygame_ui/pygame_ui.py

import pygame
from ..core.backgammongame import BackgammonGame

# --- Constantes de Configuración ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_COLOR = (205, 170, 125)  # Un tono madera
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TRIANGLE_COLOR_A = (139, 115, 85) # Marrón oscuro para los triángulos
TRIANGLE_COLOR_B = (245, 245, 220) # Beige para los triángulos
HIGHLIGHT_COLOR = (255, 255, 0, 128) # Amarillo semitransparente para resaltar

CHECKER_RADIUS = 20
POINT_WIDTH = 50
BAR_WIDTH = 60

class PygameUI:
    """
    Gestiona la interfaz gráfica del juego de Backgammon utilizando Pygame.
    
    Esta clase es responsable de dibujar el estado del juego (tablero, fichas, dados)
    y de manejar la interacción del usuario a través del ratón.
    """

    def __init__(self, game: BackgammonGame):
        self._game_ = game
        self._screen_ = None
        self._font_ = None
        self.selected_point = None # Almacena el punto de inicio seleccionado por el jugador
        self.running = True

        self._initialize_pygame()

    def _initialize_pygame(self):
        """Inicializa Pygame, la pantalla y las fuentes."""
        pygame.init()
        self._screen_ = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Backgammon")
        self._font_ = pygame.font.SysFont("arial", 24)
        self._small_font_ = pygame.font.SysFont("arial", 18)
        
    def _draw_board(self):
        """Dibuja el tablero de Backgammon con sus puntos triangulares."""
        self._screen_.fill(BOARD_COLOR)
        
        # Dibuja la barra central
        bar_x = (SCREEN_WIDTH - BAR_WIDTH) // 2
        pygame.draw.rect(self._screen_, TRIANGLE_COLOR_A, (bar_x, 0, BAR_WIDTH, SCREEN_HEIGHT))

        # Dibuja los 24 triángulos (puntos)
        for i in range(12):
            # Coordenadas base para los triángulos
            x_base = 20 + i * POINT_WIDTH + (BAR_WIDTH if i >= 6 else 0)
            
            # Triángulos superiores (puntos 13 a 24)
            top_points = [(x_base, 0), (x_base + POINT_WIDTH, 0), (x_base + POINT_WIDTH / 2, SCREEN_HEIGHT / 2 - 20)]
            # Triángulos inferiores (puntos 1 a 12)
            bottom_points = [(x_base, SCREEN_HEIGHT), (x_base + POINT_WIDTH, SCREEN_HEIGHT), (x_base + POINT_WIDTH / 2, SCREEN_HEIGHT / 2 + 20)]

            color = TRIANGLE_COLOR_B if i % 2 == 0 else TRIANGLE_COLOR_A
            pygame.draw.polygon(self._screen_, color, top_points)
            pygame.draw.polygon(self._screen_, color, bottom_points)

    def _get_coords_for_point(self, point_idx: int, checker_count: int) -> tuple[int, int]:
        """Calcula las coordenadas (x, y) para una ficha en un punto específico."""
        i = point_idx
        y_offset = CHECKER_RADIUS * 2 * (checker_count -1)

        # Puntos del cuadrante inferior derecho (1-6)
        if 0 <= i < 6:
            x = SCREEN_WIDTH - 45 - i * POINT_WIDTH
            y = SCREEN_HEIGHT - CHECKER_RADIUS - y_offset
        # Puntos del cuadrante inferior izquierdo (7-12)
        elif 6 <= i < 12:
            x = (SCREEN_WIDTH - BAR_WIDTH) // 2 - 45 - (i-6) * POINT_WIDTH
            y = SCREEN_HEIGHT - CHECKER_RADIUS - y_offset
        # Puntos del cuadrante superior izquierdo (13-18)
        elif 12 <= i < 18:
            x = 45 + (i - 12) * POINT_WIDTH
            y = CHECKER_RADIUS + y_offset
        # Puntos del cuadrante superior derecho (19-24)
        else: # 18 <= i < 24
            x = (SCREEN_WIDTH + BAR_WIDTH) // 2 + 45 + (i - 18) * POINT_WIDTH
            y = CHECKER_RADIUS + y_offset
            
        return int(x), int(y)

    def _draw_checkers(self):
        """Dibuja todas las fichas en sus posiciones actuales en el tablero."""
        # Dibuja fichas en los puntos
        for i, point in enumerate(self._game_._board_._points_):
            for j, checker in enumerate(point):
                color = WHITE if checker._color_ == "white" else BLACK
                x, y = self._get_coords_for_point(i, j + 1)
                pygame.draw.circle(self._screen_, color, (x, y), CHECKER_RADIUS)
                pygame.draw.circle(self._screen_, (128,128,128), (x, y), CHECKER_RADIUS, 2) # Borde

        # Dibuja fichas en la barra
        bar_x = SCREEN_WIDTH // 2
        for i, checker in enumerate(self._game_._board_._bar_["white"]):
            y = SCREEN_HEIGHT // 2 - 60 - i * (CHECKER_RADIUS * 2)
            pygame.draw.circle(self._screen_, WHITE, (bar_x, y), CHECKER_RADIUS)
        for i, checker in enumerate(self._game_._board_._bar_["black"]):
            y = SCREEN_HEIGHT // 2 + 60 + i * (CHECKER_RADIUS * 2)
            pygame.draw.circle(self._screen_, BLACK, (bar_x, y), CHECKER_RADIUS)

    def _draw_ui(self):
        """Dibuja elementos de la UI como texto, dados y botones."""
        player = self._game_.get_current_player()
        
        # Muestra el turno actual
        turn_text = self._font_.render(f"Turno de: {player._name_} ({player._color_})", True, BLACK)
        self._screen_.blit(turn_text, (10, SCREEN_HEIGHT // 2 - 50))

        # Muestra los movimientos disponibles (dados)
        moves_text = self._font_.render(f"Movimientos: {self._game_._moves_}", True, BLACK)
        self._screen_.blit(moves_text, (10, SCREEN_HEIGHT // 2))

        # Dibuja el botón para tirar los dados si no hay movimientos
        if not self._game_._moves_:
            self.roll_button_rect = pygame.Rect(10, SCREEN_HEIGHT // 2 + 40, 150, 40)
            pygame.draw.rect(self._screen_, TRIANGLE_COLOR_A, self.roll_button_rect)
            roll_text = self._font_.render("Tirar Dados", True, WHITE)
            self._screen_.blit(roll_text, (20, SCREEN_HEIGHT // 2 + 45))
        
        # Muestra un mensaje si una ficha está seleccionada
        if self.selected_point is not None:
             msg = self._small_font_.render(f"Ficha seleccionada en el punto {self.selected_point}", True, (200,0,0))
             self._screen_.blit(msg, (10, SCREEN_HEIGHT // 2 - 80))

    def _get_point_from_pos(self, pos: tuple[int, int]) -> int | None:
        """Convierte una coordenada del ratón en un índice de punto del tablero."""
        x, y = pos
        bar_x_start = (SCREEN_WIDTH - BAR_WIDTH) // 2
        bar_x_end = (SCREEN_WIDTH + BAR_WIDTH) // 2

        if bar_x_start < x < bar_x_end:
            return -1 # Identificador para la barra

        if y > SCREEN_HEIGHT / 2: # Mitad inferior (puntos 1-12)
            base_idx = 11
            offset_x = x - ((SCREEN_WIDTH + BAR_WIDTH) // 2) if x > bar_x_end else x
            point_offset = (offset_x - 20) // POINT_WIDTH
            if x < bar_x_start:
                 point_offset = (bar_x_start - x - 20)//POINT_WIDTH
                 return 6 + point_offset
            else:
                 point_offset = (SCREEN_WIDTH - x - 20)//POINT_WIDTH
                 return point_offset
        else: # Mitad superior (puntos 13-24)
            if x < bar_x_start:
                 point_offset = (x - 20)//POINT_WIDTH
                 return 12 + point_offset
            else:
                 point_offset = (x - bar_x_end - 20)//POINT_WIDTH
                 return 18 + point_offset
        return None

    def _handle_click(self, pos: tuple[int, int]):
        """Procesa el clic del usuario para realizar acciones en el juego."""
        player = self._game_.get_current_player()

        # 1. Si no hay movimientos, el único clic válido es en "Tirar Dados"
        if not self._game_._moves_:
            if self.roll_button_rect.collidepoint(pos):
                self._game_.roll_dice()
            return

        # 2. Si el jugador tiene fichas en la barra, debe reingresar
        if self._game_._board_._bar_[player._color_]:
            point_idx = self._get_point_from_pos(pos)
            if point_idx is None: return

            target_point = point_idx + 1
            dice_roll = 0
            
            if player._color_ == "white":
                dice_roll = 24 - point_idx
            else: # black
                dice_roll = point_idx + 1

            if dice_roll in self._game_._moves_:
                if self._game_.attempt_reentry(dice_roll):
                    print(f"Reingreso exitoso en el punto {target_point}")
                else:
                    print("Intento de reingreso fallido.")
            else:
                print(f"Movimiento de reingreso inválido con el dado: {dice_roll}")

        # 3. Lógica para movimientos normales
        else:
            clicked_point_idx = self._get_point_from_pos(pos)
            if clicked_point_idx is None: return

            # Si no hay ficha seleccionada, intenta seleccionar una
            if self.selected_point is None:
                start_point = clicked_point_idx + 1
                if self._game_._board_._points_[clicked_point_idx] and self._game_._board_._points_[clicked_point_idx][0]._color_ == player._color_:
                    self.selected_point = start_point
                    print(f"Ficha seleccionada en el punto: {self.selected_point}")
            
            # Si ya hay una ficha seleccionada, intenta moverla
            else:
                end_point = clicked_point_idx + 1
                diff = abs(end_point - self.selected_point)
                
                if diff in self._game_._moves_:
                    if self._game_.attempt_move(self.selected_point, diff):
                        print(f"Movimiento exitoso de {self.selected_point} a {end_point}")
                    else:
                        print(f"Intento de movimiento de {self.selected_point} a {end_point} fallido.")
                else:
                    print("El movimiento no corresponde a ningún dado.")
                
                self.selected_point = None # Resetea la selección después del intento
        
        # 4. Cambiar de turno si no quedan movimientos
        if not self._game_._moves_:
            self._game_.switch_turn()
            print("No quedan movimientos. Cambiando de turno.")

    def run(self):
        """El bucle principal del juego que maneja eventos, actualizaciones y renderizado."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_click(pygame.mouse.get_pos())
            
            # Dibujar todo en cada frame
            self._draw_board()
            self._draw_checkers()
            self._draw_ui()
            
            pygame.display.flip()

        pygame.quit()

-------------------------------------------------------------------------------------------

<TERCERA CONSULTA GENERAL>

Herramienta utilizada: Gemini PRO

Promp: (Adjunto foto de como se ve la interfaz en ejecucion) (Adjunto foto de una interfaz expectativa) se ejecuta pero hay cosas a corregir del codigo, te envio una captura de pantalla de como se ve la interfaz, ademas al tocarme 4 en los dados no pude mover las fichas, tambien te adjunto una foto expectativa del tablero, principalmente las correcciones son al como estan distribuidos los elementos, notaras que en la captura estan muy desviados y descentrados algunos elementos a diferencia de la foto expectativa

Resultado extraido:

# pygame_ui/pygameui.py

import pygame
from core.backgammongame import BackgammonGame

# --- Constantes de Configuración ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_COLOR = (205, 170, 125)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TRIANGLE_COLOR_A = (139, 115, 85)
TRIANGLE_COLOR_B = (245, 245, 220)
HIGHLIGHT_COLOR = (255, 255, 0, 128)

CHECKER_RADIUS = 20
POINT_WIDTH = 50
BAR_WIDTH = 60
BORDER_WIDTH = 20

class PygameUI:
    def __init__(self, game: BackgammonGame):
        self._game_ = game
        self._screen_ = None
        self._font_ = None
        self.selected_point = None
        self.running = True
        self._initialize_pygame()

    def _initialize_pygame(self):
        pygame.init()
        self._screen_ = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Backgammon")
        self._font_ = pygame.font.SysFont("arial", 22)
        self._small_font_ = pygame.font.SysFont("arial", 18)
        
    def _draw_board(self):
        self._screen_.fill(BOARD_COLOR)
        bar_x = (SCREEN_WIDTH - BAR_WIDTH) // 2
        pygame.draw.rect(self._screen_, TRIANGLE_COLOR_A, (bar_x, 0, BAR_WIDTH, SCREEN_HEIGHT))

        for i in range(6):
            x_top_left = BORDER_WIDTH + i * POINT_WIDTH
            x_top_right = (SCREEN_WIDTH + BAR_WIDTH) // 2 + BORDER_WIDTH + i * POINT_WIDTH
            x_bottom_left = BORDER_WIDTH + i * POINT_WIDTH
            x_bottom_right = (SCREEN_WIDTH + BAR_WIDTH) // 2 + BORDER_WIDTH + i * POINT_WIDTH
            
            top_apex_y = SCREEN_HEIGHT / 2 - BORDER_WIDTH
            bottom_apex_y = SCREEN_HEIGHT / 2 + BORDER_WIDTH

            tri_top_left = [(x_top_left, 0), (x_top_left + POINT_WIDTH, 0), (x_top_left + POINT_WIDTH / 2, top_apex_y)]
            tri_top_right = [(x_top_right, 0), (x_top_right + POINT_WIDTH, 0), (x_top_right + POINT_WIDTH / 2, top_apex_y)]
            tri_bottom_left = [(x_bottom_left, SCREEN_HEIGHT), (x_bottom_left + POINT_WIDTH, SCREEN_HEIGHT), (x_bottom_left + POINT_WIDTH / 2, bottom_apex_y)]
            tri_bottom_right = [(x_bottom_right, SCREEN_HEIGHT), (x_bottom_right + POINT_WIDTH, SCREEN_HEIGHT), (x_bottom_right + POINT_WIDTH / 2, bottom_apex_y)]

            color1 = TRIANGLE_COLOR_A if i % 2 == 0 else TRIANGLE_COLOR_B
            color2 = TRIANGLE_COLOR_B if i % 2 == 0 else TRIANGLE_COLOR_A
            
            pygame.draw.polygon(self._screen_, color1, tri_top_left)
            pygame.draw.polygon(self._screen_, color2, tri_top_right)
            pygame.draw.polygon(self._screen_, color2, tri_bottom_left)
            pygame.draw.polygon(self._screen_, color1, tri_bottom_right)

    def _get_coords_for_point(self, point_idx: int, checker_count: int) -> tuple[int, int]:
        y_offset = (checker_count - 1) * (CHECKER_RADIUS * 2)

        if point_idx >= 12: # Mitad superior del tablero (puntos 13-24)
            y = CHECKER_RADIUS + y_offset
            if 12 <= point_idx < 18: # Cuadrante superior izquierdo
                x = BORDER_WIDTH + (point_idx - 12) * POINT_WIDTH + POINT_WIDTH / 2
            else: # Cuadrante superior derecho
                x = (SCREEN_WIDTH + BAR_WIDTH) // 2 + BORDER_WIDTH + (point_idx - 18) * POINT_WIDTH + POINT_WIDTH / 2
        else: # Mitad inferior del tablero (puntos 1-12)
            y = SCREEN_HEIGHT - CHECKER_RADIUS - y_offset
            # --- CORRECCIÓN 1: Lógica ajustada para centrar fichas inferiores ---
            if 0 <= point_idx < 6: # Cuadrante inferior derecho (puntos 1-6)
                # La numeración va de derecha a izquierda (5, 4, ..., 0)
                # El dibujo va de izquierda a derecha (0, 1, ..., 5)
                # Relación: drawing_index = 5 - point_idx
                drawing_idx = 5 - point_idx
                x = (SCREEN_WIDTH + BAR_WIDTH) // 2 + BORDER_WIDTH + drawing_idx * POINT_WIDTH + POINT_WIDTH / 2
            else: # Cuadrante inferior izquierdo (puntos 7-12)
                # La numeración va de derecha a izquierda (11, 10, ..., 6)
                # El dibujo va de izquierda a derecha (0, 1, ..., 5)
                # Relación: drawing_index = 11 - point_idx
                drawing_idx = 11 - point_idx
                x = BORDER_WIDTH + drawing_idx * POINT_WIDTH + POINT_WIDTH / 2
                
        return int(x), int(y)

    def _draw_checkers(self):
        for i, point in enumerate(self._game_._board_._points_):
            for j, checker in enumerate(point):
                color = WHITE if checker._color_ == "white" else BLACK
                x, y = self._get_coords_for_point(i, j + 1)
                pygame.draw.circle(self._screen_, color, (x, y), CHECKER_RADIUS)
                pygame.draw.circle(self._screen_, (128,128,128), (x, y), CHECKER_RADIUS, 2)

        bar_x = SCREEN_WIDTH // 2
        for i, checker in enumerate(self._game_._board_._bar_["white"]):
            y = SCREEN_HEIGHT // 2 - 40 - i * (CHECKER_RADIUS * 2)
            pygame.draw.circle(self._screen_, WHITE, (bar_x, y), CHECKER_RADIUS)
        for i, checker in enumerate(self._game_._board_._bar_["black"]):
            y = SCREEN_HEIGHT // 2 + 40 + i * (CHECKER_RADIUS * 2)
            pygame.draw.circle(self._screen_, BLACK, (bar_x, y), CHECKER_RADIUS)

    # --- CORRECCIÓN 2: UI rediseñada para aparecer en la barra central ---
    def _draw_ui(self):
        player = self._game_.get_current_player()
        center_x = SCREEN_WIDTH // 2

        # Preparar los textos
        turn_text_surf = self._font_.render(f"Turno: {player._name_}", True, WHITE)
        moves_text_surf = self._font_.render(f"Movimientos: {self._game_._moves_}", True, WHITE)
        
        # Posicionar los textos en el centro de la barra
        turn_text_rect = turn_text_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 2 - 20))
        moves_text_rect = moves_text_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 2 + 20))
        
        self._screen_.blit(turn_text_surf, turn_text_rect)
        self._screen_.blit(moves_text_surf, moves_text_rect)

        if not self._game_._moves_:
            self.roll_button_rect = pygame.Rect(0, 0, 140, 40)
            self.roll_button_rect.center = (center_x, SCREEN_HEIGHT // 2 + 70)
            pygame.draw.rect(self._screen_, (200, 200, 200), self.roll_button_rect, border_radius=5)
            roll_text_surf = self._font_.render("Tirar Dados", True, BLACK)
            roll_text_rect = roll_text_surf.get_rect(center=self.roll_button_rect.center)
            self._screen_.blit(roll_text_surf, roll_text_rect)
        
        if self.selected_point is not None:
             msg_surf = self._small_font_.render(f"Ficha seleccionada: {self.selected_point}", True, (200,0,0))
             msg_rect = msg_surf.get_rect(center=(center_x, SCREEN_HEIGHT // 2 - 60))
             self._screen_.blit(msg_surf, msg_rect)

    def _get_point_from_pos(self, pos: tuple[int, int]) -> int | None:
        x, y = pos
        bar_start_x = (SCREEN_WIDTH - BAR_WIDTH) // 2
        bar_end_x = (SCREEN_WIDTH + BAR_WIDTH) // 2

        if bar_start_x < x < bar_end_x: return -1

        if y < SCREEN_HEIGHT / 2:
            if BORDER_WIDTH < x < bar_start_x:
                return 12 + (x - BORDER_WIDTH) // POINT_WIDTH
            elif bar_end_x < x < SCREEN_WIDTH - BORDER_WIDTH:
                 return 18 + (x - bar_end_x - BORDER_WIDTH) // POINT_WIDTH
        else:
            if BORDER_WIDTH < x < bar_start_x:
                return 11 - ((x - BORDER_WIDTH) // POINT_WIDTH)
            elif bar_end_x < x < SCREEN_WIDTH - BORDER_WIDTH:
                return 5 - ((x - bar_end_x - BORDER_WIDTH) // POINT_WIDTH)
        return None

    def _handle_click(self, pos: tuple[int, int]):
        player = self._game_.get_current_player()

        if not self._game_._moves_:
            if hasattr(self, 'roll_button_rect') and self.roll_button_rect.collidepoint(pos):
                self._game_.roll_dice()
            return

        clicked_point_idx = self._get_point_from_pos(pos)
        if clicked_point_idx is None: return

        if self.selected_point is None:
            if clicked_point_idx >= 0 and self._game_._board_._points_[clicked_point_idx] and self._game_._board_._points_[clicked_point_idx][0]._color_ == player._color_:
                self.selected_point = clicked_point_idx + 1
                print(f"Ficha seleccionada en el punto: {self.selected_point}")
        else:
            end_point = clicked_point_idx + 1
            diff = abs(end_point - self.selected_point)
            
            if diff in self._game_._moves_:
                if self._game_.attempt_move(self.selected_point, diff):
                    print(f"Movimiento exitoso de {self.selected_point} a {end_point}")
                else:
                    print(f"Intento de movimiento de {self.selected_point} a {end_point} fallido.")
            else:
                print("El movimiento no corresponde a ningún dado.")
            
            self.selected_point = None

        if not self._game_._moves_ and self._game_._dice_._values_:
            self._game_.switch_turn()
            print("No quedan movimientos. Cambiando de turno.")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_click(pygame.mouse.get_pos())
            
            self._draw_board()
            self._draw_checkers()
            self._draw_ui()
            
            pygame.display.flip()

        pygame.quit()