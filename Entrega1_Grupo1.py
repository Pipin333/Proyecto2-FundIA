"""Proyecto N°1 - Fundamentos de Inteligencia Artificial.

Juego: Gomoku (Variante Libre / Freestyle).
Entrega 1: Implementación para 2 jugadores humanos con tablero parametrizable.
"""

import sys


def crea_tablero(n):
    """Crea un tablero de Gomoku de tamaño n x n con casillas vacías.

    Args:
        n (int): Dimensión del tablero (n >= 5).

    Returns:
        list[list[str]]: Matriz de n x n inicializada con '.' en cada casilla.
    """
    return [["." for _ in range(n)] for _ in range(n)]


def imprime_tablero(tablero):
    """Imprime en pantalla el estado actual del tablero con coordenadas (1 a n).

    Args:
        tablero (list[list[str]]): Matriz con el estado actual del juego.

    Returns:
        None: La función únicamente imprime información en pantalla.
    """
    n = len(tablero)

    print()
    encabezado = "    " + " ".join(f"{col:2}" for col in range(1, n + 1))
    print(encabezado)

    for i, fila in enumerate(tablero, start=1):
        fila_str = " ".join(f"{elem:2}" for elem in fila)
        print(f"{i:2}  {fila_str}")

    print()


def tablero_lleno(tablero):
    """Determina si todas las casillas del tablero están ocupadas.

    Args:
        tablero (list[list[str]]): Matriz con el estado actual del juego.

    Returns:
        bool: True si no quedan casillas vacías ('.'); False en caso contrario.
    """
    for fila in tablero:
        if "." in fila:
            return False
    return True


def es_movimiento_valido(tablero, fila, col):
    """Valida si una jugada en coordenadas (1-based) está dentro del tablero y la casilla está libre.

    Args:
        tablero (list[list[str]]): Matriz con el estado actual del juego.
        fila (int): Índice de fila ingresado por el usuario (1 a n).
        col (int): Índice de columna ingresado por el usuario (1 a n).

    Returns:
        bool: True si la posición es legal; False si está fuera de rango u ocupada.
    """
    n = len(tablero)

    if not (1 <= fila <= n and 1 <= col <= n):
        return False

    return tablero[fila - 1][col - 1] == "."


def verificar_victoria(tablero, fila, col, jugador):
    """Verifica si la última jugada genera una línea de 5 o más fichas consecutivas.

    Revisa en las 4 direcciones posibles a partir de la casilla recién colocada:
    horizontal, vertical, diagonal principal y diagonal secundaria.

    Args:
        tablero (list[list[str]]): Matriz con el estado actual del juego.
        fila (int): Fila de la última jugada (1 a n).
        col (int): Columna de la última jugada (1 a n).
        jugador (str): Ficha del jugador que realizó la jugada ('A' o 'B').

    Returns:
        bool: True si se formó una línea de 5 o más fichas consecutivas; False en caso contrario.
    """
    n = len(tablero)

    # Convertimos de coordenadas 1-based a índices 0-based.
    r = fila - 1
    c = col - 1

    direcciones = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal principal (\)
        (1, -1),  # Diagonal secundaria (/)
    ]

    for dr, dc in direcciones:
        consecutivas = 1

        # Buscar hacia adelante.
        nr = r + dr
        nc = c + dc

        while 0 <= nr < n and 0 <= nc < n and tablero[nr][nc] == jugador:
            consecutivas += 1
            nr += dr
            nc += dc

        # Buscar hacia atrás.
        nr = r - dr
        nc = c - dc

        while 0 <= nr < n and 0 <= nc < n and tablero[nr][nc] == jugador:
            consecutivas += 1
            nr -= dr
            nc -= dc

        # Freestyle Gomoku: 5 o MÁS fichas consecutivas otorgan la victoria.
        if consecutivas >= 5:
            return True

    return False


def pedir_tamano_tablero():
    """Solicita al usuario el tamaño del tablero garantizando n >= 5.

    Returns:
        int: Tamaño del tablero n x n seleccionado.
    """
    while True:
        try:
            n = int(input("Ingrese el tamaño del tablero (n >= 5): "))

            if n >= 5:
                return n

            print("El tamaño debe ser mayor o igual a 5.")

        except ValueError:
            print("Entrada inválida. Ingrese un número entero.")


def pedir_jugada(tablero, jugador):
    """Solicita al jugador en turno las coordenadas de su jugada hasta recibir una válida.

    Args:
        tablero (list[list[str]]): Matriz con el estado actual del juego.
        jugador (str): Identificador del jugador ('A' o 'B').

    Returns:
        tuple[int, int]: Coordenadas (fila, columna) válidas ingresadas (1 a n).
    """
    n = len(tablero)

    while True:
        try:
            entrada = input(
                f"Turno Jugador {jugador} - Ingrese fila y columna (ej: 3 4): "
            ).strip()

            partes = entrada.split()

            if len(partes) != 2:
                print(
                    f"Debe ingresar exactamente dos números "
                    f"separados por espacio (1 a {n})."
                )
                continue

            fila = int(partes[0])
            col = int(partes[1])

            if not (1 <= fila <= n and 1 <= col <= n):
                print(
                    f"Coordenadas fuera del tablero. "
                    f"Deben estar entre 1 y {n}."
                )
                continue

            if not es_movimiento_valido(tablero, fila, col):
                print("Esa casilla ya está ocupada. Elija otra.")
                continue

            return fila, col

        except ValueError:
            print("Entrada inválida. Ingrese dos números enteros.")


def juego_gomoku():
    """Ejecuta una partida de Gomoku para dos jugadores humanos.

    Returns:
        None: Imprime el desarrollo de la partida y el resultado final.
    """
    print("=" * 50)
    print("         GOMOKU - 2 JUGADORES HUMANOS")
    print("              VARIANTE FREESTYLE")
    print("=" * 50)

    n = pedir_tamano_tablero()
    tablero = crea_tablero(n)

    # Jugador A comienza siempre según las especificaciones del proyecto.
    turno = "A"

    while True:
        imprime_tablero(tablero)

        # Solicitar jugada.
        fila, col = pedir_jugada(tablero, turno)

        # Realizar jugada.
        tablero[fila - 1][col - 1] = turno

        # Verificar victoria.
        if verificar_victoria(tablero, fila, col, turno):
            imprime_tablero(tablero)
            print(
                f"¡Felicitaciones! El Jugador {turno} "
                f"ha ganado con 5 o más fichas en línea."
            )
            break

        # Verificar empate.
        if tablero_lleno(tablero):
            imprime_tablero(tablero)
            print("¡La partida ha terminado en empate!")
            print("No quedan casillas libres.")
            break

        # Cambiar jugador.
        if turno == "A":
            turno = "B"
        else:
            turno = "A"


if __name__ == "__main__":
    try:
        juego_gomoku()

    except KeyboardInterrupt:
        print("\n\nPartida interrumpida. ¡Hasta luego!")
        sys.exit(0)

