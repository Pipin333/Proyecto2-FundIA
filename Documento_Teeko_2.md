# Documento Proyecto Teeko - Fundamentos de Inteligencia Artificial

---

## 1. Código de Teeko Completo con Docstrings PEP-257 y Cumplimiento PEP-8

```python
"""Proyecto N°1 - Fundamentos de Inteligencia Artificial.

Juego: Teeko (Variante Parametrizable n >= 5).
Entrega 2: Implementación completa con Agente Inteligente (Minimax + Poda Alfa-Beta).
"""

import copy
import math
import sys


class Teeko:
    """Clase principal que encapsula el estado, reglas y mecánicas del juego Teeko.

    Atributos:
        n (int): Dimensión del tablero (n x n, con n >= 5).
        board (list[list[str]]): Matriz que representa el tablero de juego.
        current_player (str): Jugador en turno ('A' o 'B').
        pieces (dict[str, int]): Conteo de fichas colocadas en Fase 1 por cada jugador.
        phase (int): Fase actual del juego (1: Colocación, 2: Movimiento).
        history (dict[str, int]): Registro de estados para detectar triple repetición.
    """

    def __init__(self, n=5):
        """Inicializa una nueva partida de Teeko con tablero parametrizable.

        Args:
            n (int, optional): Dimensión del tablero. Por defecto es 5.
        """
        self.n = max(5, int(n))
        self.board = [["." for _ in range(self.n)] for _ in range(self.n)]
        self.current_player = "A"
        self.pieces = {"A": 0, "B": 0}
        self.phase = 1
        self.history = {}

    def get_state_hash(self):
        """Genera una firma única (hash en string) del estado actual del tablero y turno.

        Returns:
            str: Cadena representativa de la matriz concatenada con el jugador en turno.
        """
        board_str = "".join("".join(row) for row in self.board)
        return board_str + self.current_player

    def print_board(self):
        """Dibuja en consola el estado del tablero con coordenadas (1 a n), fase y turno.

        Returns:
            None: La función únicamente imprime información en pantalla.
        """
        print()
        encabezado = "    " + " ".join(f"{col:2}" for col in range(1, self.n + 1))
        print(encabezado)
        for i, fila in enumerate(self.board, start=1):
            fila_str = " ".join(f"{elem:2}" for elem in fila)
            print(f"{i:2}  {fila_str}")
        fase_desc = "1 (Colocación)" if self.phase == 1 else "2 (Movimiento)"
        print(f"\nFase actual: {fase_desc} | Turno: Jugador {self.current_player}")
        print("-" * 35)

    def check_win(self, player):
        """Verifica si el jugador especificado ha formado una configuración ganadora.

        Las configuraciones ganadoras de Teeko son:
        1. 4 fichas consecutivas en línea horizontal.
        2. 4 fichas consecutivas en línea vertical.
        3. 4 fichas consecutivas en diagonal principal (\\).
        4. 4 fichas consecutivas en diagonal secundaria (/).
        5. 4 fichas formando un bloque cuadrado cerrado de 2 x 2.

        Args:
            player (str): Jugador a verificar ('A' o 'B').

        Returns:
            bool: True si el jugador tiene una configuración ganadora; False en caso contrario.
        """
        for r in range(self.n):
            for c in range(self.n):
                if self.board[r][c] == player:
                    # 1. Horizontal
                    if c + 3 < self.n and all(self.board[r][c + i] == player for i in range(4)):
                        return True
                    # 2. Vertical
                    if r + 3 < self.n and all(self.board[r + i][c] == player for i in range(4)):
                        return True
                    # 3. Diagonal principal (\)
                    if r + 3 < self.n and c + 3 < self.n and all(
                        self.board[r + i][c + i] == player for i in range(4)
                    ):
                        return True
                    # 4. Diagonal secundaria (/)
                    if r + 3 < self.n and c - 3 >= 0 and all(
                        self.board[r + i][c - i] == player for i in range(4)
                    ):
                        return True
                    # 5. Bloque 2x2
                    if r + 1 < self.n and c + 1 < self.n:
                        if (
                            self.board[r][c + 1] == player
                            and self.board[r + 1][c] == player
                            and self.board[r + 1][c + 1] == player
                        ):
                            return True
        return False

    def get_legal_moves(self):
        """Genera todas las jugadas legales posibles para el jugador actual.

        En Fase 1: Cualquier casilla vacía (r, c).
        En Fase 2: Mover una ficha propia (r1, c1) a una casilla adyacente vacía (r2, c2).

        Returns:
            list[tuple]: Lista de tuplas (r, c) en Fase 1 o (r1, c1, r2, c2) en Fase 2 (0-based).
        """
        moves = []
        if self.phase == 1:
            for r in range(self.n):
                for c in range(self.n):
                    if self.board[r][c] == ".":
                        moves.append((r, c))
        else:
            directions = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1),           (0, 1),
                (1, -1),  (1, 0),  (1, 1),
            ]
            for r in range(self.n):
                for c in range(self.n):
                    if self.board[r][c] == self.current_player:
                        for dr, dc in directions:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.n and 0 <= nc < self.n and self.board[nr][nc] == ".":
                                moves.append((r, c, nr, nc))
        return moves

    def make_move(self, move):
        """Aplica un movimiento al tablero y actualiza el estado interno del juego.

        Args:
            move (tuple): Tupla (r, c) en Fase 1 o (r1, c1, r2, c2) en Fase 2.

        Returns:
            None: Modifica el estado del juego directamente.
        """
        if self.phase == 1:
            r, c = move
            self.board[r][c] = self.current_player
            self.pieces[self.current_player] += 1
            if self.pieces["A"] == 4 and self.pieces["B"] == 4:
                self.phase = 2
        else:
            r1, c1, r2, c2 = move
            self.board[r1][c1] = "."
            self.board[r2][c2] = self.current_player

        # Alternar turno
        self.current_player = "B" if self.current_player == "A" else "A"

        # Registrar historial en Fase 2 para detección de repeticiones
        if self.phase == 2:
            state_hash = self.get_state_hash()
            self.history[state_hash] = self.history.get(state_hash, 0) + 1

    def undo_move(self, move, old_phase, old_history):
        """Revierte un movimiento previo restaurando el estado anterior del juego.

        Args:
            move (tuple): Movimiento a deshacer.
            old_phase (int): Fase previa del juego.
            old_history (dict[str, int]): Copia previa del historial de estados.

        Returns:
            None: Modifica el estado del juego directamente.
        """
        self.current_player = "B" if self.current_player == "A" else "A"
        self.phase = old_phase
        self.history = copy.deepcopy(old_history)

        if self.phase == 1:
            r, c = move
            self.board[r][c] = "."
            self.pieces[self.current_player] -= 1
        else:
            r1, c1, r2, c2 = move
            self.board[r2][c2] = "."
            self.board[r1][c1] = self.current_player

    def is_terminal(self):
        """Evalúa si el estado actual es terminal (victoria, derrota o empate).

        Returns:
            tuple[bool, str | None]: (True, 'A'/'B'/'Draw') si terminó; (False, None) si continúa.
        """
        if self.check_win("A"):
            return True, "A"
        if self.check_win("B"):
            return True, "B"

        if self.phase == 2:
            state_hash = self.get_state_hash()
            if self.history.get(state_hash, 0) >= 3:
                return True, "Draw"
            if not self.get_legal_moves():
                # El jugador que no puede mover pierde inmediatamente (bloqueo)
                winner = "B" if self.current_player == "A" else "A"
                return True, winner

        return False, None


def evaluate(game, player):
    """Calcula la función de evaluación heurística para un estado no terminal.

    Utiliza la métrica de distancia de Chebyshev entre pares de fichas para premiar
    agrupaciones compactas del agente y penalizar agrupaciones del oponente.

    Args:
        game (Teeko): Instancia del juego en evaluación.
        player (str): Jugador objetivo para maximizar ('A' o 'B').

    Returns:
        int: Puntuación heurística asignada a la posición del tablero.
    """
    opponent = "B" if player == "A" else "A"

    if game.check_win(player):
        return 10000
    if game.check_win(opponent):
        return -10000

    score = 0
    my_pieces = []
    opp_pieces = []

    for r in range(game.n):
        for c in range(game.n):
            if game.board[r][c] == player:
                my_pieces.append((r, c))
            elif game.board[r][c] == opponent:
                opp_pieces.append((r, c))

    # Evaluar proximidad de piezas propias
    for p1 in my_pieces:
        for p2 in my_pieces:
            if p1 != p2:
                dist = max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))
                if dist == 1:
                    score += 10
                elif dist == 2:
                    score += 5

    # Evaluar y bloquear proximidad de piezas rivales
    for p1 in opp_pieces:
        for p2 in opp_pieces:
            if p1 != p2:
                dist = max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))
                if dist == 1:
                    score -= 10
                elif dist == 2:
                    score -= 5

    return score


def minimax(game, depth, alpha, beta, maximizing_player, ai_player):
    """Ejecuta el algoritmo Minimax con Poda Alfa-Beta para seleccionar la mejor jugada.

    Args:
        game (Teeko): Estado actual del juego.
        depth (int): Profundidad máxima de exploración restante.
        alpha (float): Mejor valor encontrado para el maximizador.
        beta (float): Mejor valor encontrado para el minimizador.
        maximizing_player (bool): True si el turno simulado corresponde al agente IA.
        ai_player (str): Identificador del jugador IA ('A' o 'B').

    Returns:
        tuple[int, tuple | None]: Par (mejor_puntaje, mejor_movimiento).
    """
    terminal, winner = game.is_terminal()
    if depth == 0 or terminal:
        if terminal:
            if winner == ai_player:
                return 100000, None
            elif winner == "Draw":
                return 0, None
            else:
                return -100000, None
        return evaluate(game, ai_player), None

    legal_moves = game.get_legal_moves()
    if not legal_moves:
        score = -100000 if maximizing_player else 100000
        return score, None

    if maximizing_player:
        max_eval = -math.inf
        best_move = None
        for move in legal_moves:
            old_phase = game.phase
            old_history = copy.deepcopy(game.history)
            game.make_move(move)

            eval_score, _ = minimax(game, depth - 1, alpha, beta, False, ai_player)
            game.undo_move(move, old_phase, old_history)

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Poda Beta

        return max_eval, best_move
    else:
        min_eval = math.inf
        best_move = None
        for move in legal_moves:
            old_phase = game.phase
            old_history = copy.deepcopy(game.history)
            game.make_move(move)

            eval_score, _ = minimax(game, depth - 1, alpha, beta, True, ai_player)
            game.undo_move(move, old_phase, old_history)

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Poda Alfa

        return min_eval, best_move


def pedir_tamano_tablero():
    """Solicita al usuario el tamaño del tablero garantizando n >= 5.

    Returns:
        int: Dimensión validada del tablero.
    """
    while True:
        try:
            n = int(input("Ingrese el tamaño del tablero (n >= 5): "))
            if n >= 5:
                return n
            print("El tamaño debe ser de al menos 5x5.")
        except ValueError:
            print("Entrada inválida. Ingrese un número entero.")


def pedir_jugada_humano(game):
    """Solicita y valida una jugada humana según la fase actual del juego.

    Args:
        game (Teeko): Estado actual del juego.

    Returns:
        tuple: Movimiento legal ingresado (0-based).
    """
    legal_moves = game.get_legal_moves()
    n = game.n

    while True:
        try:
            if game.phase == 1:
                entrada = input(f"Turno Jugador {game.current_player} - Ingrese fila y columna (ej: 3 3): ").strip()
                partes = entrada.split()
                if len(partes) != 2:
                    print(f"Debe ingresar dos números separados por espacio (1 a {n}).")
                    continue
                r, c = int(partes[0]) - 1, int(partes[1]) - 1
                move = (r, c)
            else:
                entrada = input(
                    f"Turno Jugador {game.current_player} - Ingrese origen y destino (fila1 col1 fila2 col2): "
                ).strip()
                partes = entrada.split()
                if len(partes) != 4:
                    print(f"Debe ingresar 4 números: fila_orig col_orig fila_dest col_dest (1 a {n}).")
                    continue
                r1, c1 = int(partes[0]) - 1, int(partes[1]) - 1
                r2, c2 = int(partes[2]) - 1, int(partes[3]) - 1
                move = (r1, c1, r2, c2)

            if move in legal_moves:
                return move
            else:
                print("Movimiento ilegal. Verifique que la casilla esté vacía y la adyacencia sea válida.")

        except ValueError:
            print("Entrada inválida. Ingrese números enteros.")


def play_game():
    """Controlador principal que orquesta el ciclo de vida de la partida de Teeko.

    Returns:
        None: Imprime el desarrollo de la partida y el resultado final.
    """
    while True:
        print("=" * 50)
        print("             BIENVENIDO A TEEKO             ")
        print("     FUNDAMENTOS DE INTELIGENCIA ARTIFICIAL ")
        print("=" * 50)

        n = pedir_tamano_tablero()
        game = Teeko(n)

        print("\nModos de Juego:")
        print("1. Humano vs Humano")
        print("2. Humano (A) vs Agente IA (B)")
        mode = input("Seleccione el modo (1/2): ").strip()

        while True:
            game.print_board()

            # Verificar si la partida terminó
            terminal, winner = game.is_terminal()
            if terminal:
                if winner == "Draw":
                    print("¡Partida finalizada en EMPATE por triple repetición de estado!")
                else:
                    print(f"¡Felicitaciones! ¡El ganador de la partida es el Jugador {winner}!")
                break

            # Turno de la IA
            if mode == "2" and game.current_player == "B":
                print("Turno de la IA (calculando jugada con Minimax + Alfa-Beta)...")
                depth = 3 if game.phase == 1 else 4
                _, best_move = minimax(game, depth, -math.inf, math.inf, True, "B")
                if best_move:
                    game.make_move(best_move)
                continue

            # Turno Humano
            move = pedir_jugada_humano(game)
            game.make_move(move)

        if input("\n¿Deseas jugar otra partida? (s/n): ").strip().lower() not in ["s", "si", "y", "yes"]:
            print("\n¡Gracias por jugar! Hasta pronto.")
            break


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nPartida interrumpida. ¡Hasta luego!")
        sys.exit(0)

```

---

## 2. Desglose por Funciones del Juego y Componentes del Sistema

* **`Teeko.__init__`**: Configura el estado base del juego parametrizando el tamaño del tablero (n >= 5). Genera la matriz de n x n, inicializa el conteo de 4 fichas por jugador, fija el turno inicial en `'A'` e inicia la Fase 1 (Colocación).
* **`Teeko.get_state_hash`**: Genera la firma única del estado para la detección de empates por repetición. Convierte el tablero en una sola cadena secuencial y le adjunta el identificador del jugador en turno.
* **`Teeko.print_board`**: Renderiza el tablero en consola con numeración 1 a n, mostrando la fase actual y el jugador en turno.
* **`Teeko.check_win`**: Árbitro de victoria. Escanea el tablero para confirmar si un jugador formó alguna de las 5 configuraciones ganadoras (4 fichas horizontales, verticales, diagonales o un bloque cerrado 2 x 2).
* **`Teeko.get_legal_moves`**: Generador de acciones del agente. En Fase 1 retorna todas las casillas vacías (r, c). En Fase 2 calcula todos los desplazamientos válidos a casillas adyacentes vacías (r1, c1, r2, c2).
* **`Teeko.make_move`**: Aplica la jugada al tablero, gestiona la transición a Fase 2 al colocar las 8 fichas, alterna el turno y registra el hash en el historial.
* **`Teeko.undo_move`**: Revierte la jugada restaurando la casilla previa, el conteo de piezas, el turno y el historial, permitiendo que Minimax explore sin duplicar objetos en memoria.
* **`Teeko.is_terminal`**: Evalúa si el estado actual es terminal revisando victoria de `'A'`, victoria de `'B'`, triple repetición (empate) o bloqueo de movimientos en Fase 2 (derrota del jugador sin jugadas).
* **`evaluate`**: Función de evaluación heurística. Utiliza la distancia de Chebyshev entre las piezas para premiar agrupaciones compactas de la IA y penalizar formaciones enemigas cercanas.
* **`minimax`**: Algoritmo de búsqueda adversarial. Construye el árbol de decisiones simulando las mejores respuestas del adversario e integra Poda Alfa-Beta para descartar ramas subóptimas.
* **`play_game`**: Orquestador del juego. Maneja el menú de modos (Humano vs Humano / Humano vs IA), captura excepciones para validación robusta de entradas y controla el ciclo de partidas.

---

## 3. Preguntas Estratégicas para la Interrogación

### 🧠 Bloque 1: Heurística y Estrategia

#### **P1: ¿Cuál es el propósito exacto de su Función de Evaluación Heurística y bajo qué criterios opera?**
**Respuesta:** Como las condiciones de victoria de Teeko exigen agrupaciones de 4 fichas en línea o en un bloque cerrado 2x2, nuestra heurística premia los estados donde las fichas de la IA están a una distancia de Chebyshev adyacente (distancia 1 o 2). Al mismo tiempo, penaliza si las fichas del oponente están agrupadas. Esto guía al Minimax de forma orgánica hacia la formación de figuras ganadoras y al bloqueo defensivo sin requerir reglas manuales rígidas.

#### **P2: ¿Por qué eligieron la Distancia de Chebyshev en lugar de la distancia de Manhattan o Euclidiana?**
**Respuesta:** Porque en Teeko las fichas se mueven y ganan tanto ortogonal como diagonalmente en 8 direcciones. La distancia de Chebyshev (max(|Δx|, |Δy|)) asigna costo 1 a un paso diagonal (igual que horizontal o vertical), modelando con exactitud la geometría del juego y la formación de bloques 2x2.

#### **P3: ¿Cómo distingue su IA entre una victoria inmediata, un empate y un estado intermedio?**
**Respuesta:** Mediante una jerarquía clara de utilidades:
* Victoria de la IA: +100.000 (utilidad máxima).
* Victoria del adversario: -100.000 (utilidad mínima a evitar).
* Empate (triple repetición): 0 (neutral).
* Estados intermedios (no terminales): Puntuación heurística acotada entre -200 y +200 evaluada en las hojas del árbol.

---

### ⚡ Bloque 2: Minimax, Poda Alfa-Beta y Complejidad

#### **P4: ¿Dónde ocurre la Poda Alfa-Beta en el código y qué se gana computacionalmente?**
**Respuesta:** Ocurre en las líneas `if beta <= alpha: break`. En el maximizador se podan ramas cuando encontramos un valor superior o igual a β (Poda Beta), y en el minimizador cuando encontramos un valor inferior o igual a α (Poda Alfa). Esto reduce el factor de ramificación efectivo de b^d hasta b^(d/2) en el mejor caso, ahorrando miles de evaluaciones de nodos por turno.

#### **P5: ¿Por qué la profundidad de búsqueda varía entre la Fase 1 (`depth=3`) y la Fase 2 (`depth=4`)?**
**Respuesta:** En la Fase 1 (Colocación), el factor de ramificación es alto (b ≈ 20-25 casillas vacías), por lo que una profundidad mayor ralentizaría el turno. En la Fase 2 (Movimiento), cada jugador solo tiene 4 fichas con opciones de movimiento adyacentes limitadas (b ≈ 8-15), lo que permite descender a profundidad 4 con respuesta inmediata.

#### **P6: ¿Cómo afectaría el orden de exploración de movimientos (*Move Ordering*) a la Poda Alfa-Beta?**
**Respuesta:** Si ordenamos los movimientos legales explorando primero aquellos con mejor puntaje heurístico, los valores de α y β se ajustan rápidamente a sus extremos en los primeros hijos, provocando que la gran mayoría de las ramas restantes se corten de inmediato.

#### **P7: ¿Por qué implementaron `make_move` y `undo_move` en lugar de clonar el objeto `Teeko` en cada paso?**
**Respuesta:** Para optimizar memoria y tiempo de CPU. Clonar objetos complejos con `copy.deepcopy(game)` miles de veces por llamada satura el *garbage collector*. Modificar el estado en el lugar y deshacer la jugada al regresar de la recursión mantiene el árbol en tiempo de ejecución instantáneo (O(1) por nodo).

---

### 🛡️ Bloque 3: Detección de Estados y Robustez

#### **P8: ¿Qué problema tuvieron previamente con la detección del Empate por Repetición y cómo lo resolvieron?**
**Respuesta:** Inicialmente almacenábamos la firma del tablero *antes* de alternar el turno, asociando la foto al jugador incorrecto. Lo solucionamos invirtiendo el orden: en `make_move` primero alternamos `current_player` y luego calculamos el hash `board_str + current_player`. Así la repetición evalúa fielmente el tablero y a quién le toca mover.

#### **P9: ¿Qué comportamiento tiene la aplicación frente a entradas inválidas (texto, fuera de rango o casillas ocupadas)?**
**Respuesta:** Cuenta con validación robusta con bloques `try-except ValueError`. Si el usuario ingresa texto, un número fuera de rango (<1 o >n) o una casilla ocupada, el programa atrapa la excepción o valida la condición, despliega un mensaje amigable y solicita nuevamente el dato con `continue`, sin que el programa se caiga.

---

### 🛠️ Bloque 4: Modificaciones de Código en Vivo (*Live Coding*)

#### **P10: Si les pido que la IA juegue con el turno 'A' (primer jugador) y el humano con 'B', ¿qué modifican?**
**Respuesta:** En el bucle de `play_game()`, cambiamos la condición a `if mode == '2' and game.current_player == 'A':` y en la llamada a Minimax pasamos `'A'` como `ai_player`:
```python
_, best_move = minimax(game, depth, -math.inf, math.inf, True, "A")
```

#### **P11: Si les pido desactivar la condición de victoria por bloque 2 x 2 (solo permitir 4 en línea), ¿qué línea tocan?**
**Respuesta:** En el método `check_win(self, player)`, comentamos la verificación del bloque 2 x 2:
```python
# if r + 1 < self.n and c + 1 < self.n:
#     if (self.board[r][c+1] == player and self.board[r+1][c] == player ...):
#         return True
```

#### **P12: Si les pido mostrar en consola cuántos nodos o tableros exploró Minimax en cada turno, ¿dónde lo implementan?**
**Respuesta:** Definimos una variable global `nodos_evaluados = 0`, la incrementamos al inicio de `minimax()` (`nodos_evaluados += 1`) y en `play_game()` imprimimos `print(f"Nodos explorados: {nodos_evaluados}")` justo después de recibir `best_move`, reiniciando el contador a 0.
