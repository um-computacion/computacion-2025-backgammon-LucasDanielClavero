<Justificación del Diseño del Software>

Para armar el juego, pensé que lo mejor era separar todo por responsabilidades, como pedía el práctico. La idea principal era que cada "pieza" del código tuviera un solo trabajo y lo hiciera bien. Así, todo el programa queda mucho más ordenado y es más fácil de probar después.

Arranqué por las clases más simples, que son básicamente para guardar datos. Checker es la ficha, y lo único que sabe es su _color_. No tiene idea de dónde está en el tablero. Player es parecido, solo guarda el _name_ del jugador y el _color_ de las fichas que usa. Luego hice Dice, que se encarga de todo lo que tenga que ver con los dados: tiene el método roll() para tirarlos, y get_moves() que es clave, porque se fija si salieron dobles y te devuelve cuatro movimientos en vez de dos.

La clase Board es la más importante y la que tiene la lógica más pesada. Es como si fuera el árbitro y el tablero al mismo tiempo. Para guardar dónde está cada ficha usé el atributo _points_, que es una lista que contiene 24 listas más (una por cada triángulo del tablero). También tiene el _bar_ para las fichas que van comiendo. Los métodos de esta clase, como is_valid_move o reenter_checker, tienen todas las reglas del juego: validan si te podés mover ahí, si la dirección es correcta, si el punto está bloqueado por el oponente, o si podés sacar una ficha de la barra.

Por último, la clase BackgammonGame es la que "dirige la orquesta". Esta clase no sabe cómo funcionan las reglas (de eso se encarga el Board), pero sabe cuándo pasa cada cosa. Se encarga de crear el tablero y los jugadores, maneja de quién es el turno (switch_turn), y le pide a Dice que tire los dados. Cuando un jugador quiere moverse, BackgammonGame guarda los dados disponibles en _moves_ y le pregunta al Board si el movimiento es válido. Si el Board (el árbitro) le da el OK, recién ahí BackgammonGame le ordena que mueva la ficha y tacha ese dado de la lista _moves_. Esta separación me pareció la mejor forma de que todo quede prolijo.

<Justificación de las Clases Elegidas>

Checker, Player, Dice: Clases simples para guardar datos (color, nombre) y manejar lógica aislada (tirar dados, chequear dobles).

Board: Es el árbitro y tablero. Sabe dónde están las fichas y cuáles son las reglas (is_valid_move, reenter_checker). Es la clase con la lógica más pesada.

BackgammonGame: Es el director. No sabe las reglas, pero maneja el flujo del juego: gestiona los turnos (switch_turn), pide los dados (roll_dice) y le pregunta al Board si un movimiento es válido antes de ordenarle que mueva una ficha.

<Justificación de Atributos>

La elección fue minimalista, solo los datos necesarios para que cada clase cumpla su función.

Clase Checker

_color_: Guarda el color de la ficha ("white" o "black").

Clase Player

_name_: Guarda el nombre del jugador.

_color_: Guarda el color ("white" o "black") de las fichas que usa el jugador.

Clase Dice

_values_: Almacena la última tirada de dados como una lista de dos enteros (ej: [3, 5]).

Clase Board

_points_: Lista de 24 listas que representa los triángulos y las fichas que contienen.

_bar_: Diccionario que almacena las fichas capturadas, separado por color.

_borne_off_: Diccionario que almacena las fichas que ya salieron del juego, separado por color.

Clase BackgammonGame

_board_: Instancia de la clase Board que se usará para la partida.

_players_: Lista con las dos instancias de Player que participan.

_dice_: Instancia de la clase Dice para gestionar las tiradas.

_current_player_idx_: Índice (0 o 1) que apunta al jugador actual en la lista _players_.

_moves_: Lista de enteros (dados) que el jugador tiene disponibles para su turno.

<Decisiones de Diseño Relevantes>

Separación Lógica-UI: La lógica (core/) está 100% separada de la presentación. Las clases del juego no tienen input(). Esto permite que se conecte a una consola (cli/) o a Pygame (pygame_ui/) sin cambiar el core.

Validación en dos pasos: BackgammonGame (director) recibe la intención del jugador (ej: mover de 5 a 10). Le pregunta al Board (árbitro) si es válido. Solo si el Board da el OK, BackgammonGame le ordena al Board que mueva la ficha.

Manejo de dados: La lista _moves_ en BackgammonGame es la "fuente de verdad" del turno. Cada movimiento válido elimina un dado de esa lista.

<Excepciones y Manejo de Errores>

No usé excepciones personalizadas (como raise MovimientoInvalidoError).

Métodos devuelven booleanos: Las acciones (attempt_move) devuelven True (éxito) o False (fallo).

Mensajes de error por print: Si una acción devuelve False, el mismo método imprime la razón (ej: "Punto bloqueado.").

Justificación: Es un sistema más simple para un bucle de juego en consola (si es False, vuelve a preguntar).

<Referencias a Requisitos SOLID>

<S> - Responsabilidad Única (SRP): Cada clase tiene un solo trabajo.

Ejemplo: Dice solo sabe de dados (roll()). Board solo sabe de reglas (is_valid_move()). BackgammonGame solo sabe de turnos (switch_turn()).

<O> - Abierto/Cerrado (OCP): El código está abierto a extenderse, pero cerrado a modificarse.

Ejemplo: Si quisiéramos un dado de apuestas, creamos una clase DoublingCube y la agregamos a BackgammonGame, sin tener que modificar Board o Dice.

<L> - Sustitución de Liskov (LSP): Las clases hijas deben poder sustituir a sus clases padre sin romper nada.

Ejemplo: Si creáramos una clase AIPlayer que herede de Player, BackgammonGame debería poder usarla (.get_current_player()) exactamente igual que a un Player humano.

<I> - Segregación de Interfaces (ISP): Los clientes no deben depender de métodos que no usan.

Ejemplo: BackgammonGame ofrece una única interfaz de lógica (attempt_move, roll_dice). Esta interfaz es limpia y no contiene métodos de UI, permitiendo que Cli y PygameUI la usen sin depender de métodos que no necesitan (ej: Cli no tiene que ignorar un método .draw_window()).

<D> - Inversión de Dependencias (DIP): Los módulos de alto nivel no dependen de los de bajo nivel.

Ejemplo: BackgammonGame (lógica, alto nivel) no sabe que existen Cli o PygameUI. Son las UIs (bajo nivel) las que importan e instancian BackgammonGame.
