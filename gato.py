from math import inf


def imprime_tablero(tablero):
    """Imprime en pantalla el estado actual del tablero de juego.

    Args:
        tablero (list[list[str]]): Matriz de 3 x 3 con el estado actual
            de las casillas.

    Returns:
        None: La función únicamente imprime información en pantalla.
    """
    print()
    for fila in tablero:
        for elem in fila:
            print(elem, end=" ")
        print()
    print()


def tablero_lleno(tablero):
    """Determina si todas las casillas del tablero están ocupadas.

    Args:
        tablero (list[list[str]]): Matriz de 3 x 3 con el estado actual
            de las casillas.

    Returns:
        bool: True si el tablero está lleno; False en caso contrario.
    """
    for fila in tablero:
        if "." in fila:
            return False
    return True


def busca_ganador(tablero):
    """Busca un ganador revisando filas, columnas y diagonales.

    Args:
        tablero (list[list[str]]): Matriz de 3 x 3 con el estado actual
            de las casillas.

    Returns:
        str | None: "X" u "O" si existe un ganador; None si no lo hay.
    """
    # Revisa filas.
    for fila in tablero:
        if fila[0] == fila[1] == fila[2] and fila[0] != ".":
            return fila[0]

    # Revisa columnas.
    for col in range(3):
        if (
            tablero[0][col]
            == tablero[1][col]
            == tablero[2][col]
            and tablero[0][col] != "."
        ):
            return tablero[0][col]

    # Revisa diagonal principal.
    if (
        tablero[0][0]
        == tablero[1][1]
        == tablero[2][2]
        and tablero[0][0] != "."
    ):
        return tablero[0][0]

    # Revisa diagonal secundaria.
    if (
        tablero[0][2]
        == tablero[1][1]
        == tablero[2][0]
        and tablero[0][2] != "."
    ):
        return tablero[0][2]

    return None


def minimax(tablero, le_toca_al_compu):
    """Evalúa recursivamente una posición mediante el algoritmo Minimax.

    Args:
        tablero (list[list[str]]): Matriz de 3 x 3 con el estado actual
            de las casillas.
        le_toca_al_compu (bool): Indica si corresponde evaluar el turno
            del PC.

    Returns:
        int: 1 si gana el PC, -1 si gana el humano o 0 si hay empate.
    """
    global cont

    cont += 1

    # Casos base.
    ganador = busca_ganador(tablero)
    if ganador == "X":  # PC gana -> 1.
        return 1
    if ganador == "O":  # Humano gana -> -1.
        return -1
    if tablero_lleno(tablero):  # Empate -> 0.
        return 0

    # Casos recursivos.
    if le_toca_al_compu:
        mejor_puntaje = -inf
        for i in range(3):
            for j in range(3):
                if tablero[i][j] == ".":
                    tablero[i][j] = "X"  # Prueba la jugada i, j.
                    puntaje = minimax(tablero, False)
                    tablero[i][j] = "."  # Borra la jugada i, j.
                    mejor_puntaje = max(puntaje, mejor_puntaje)
    else:
        mejor_puntaje = inf
        for i in range(3):
            for j in range(3):
                if tablero[i][j] == ".":
                    tablero[i][j] = "O"  # Prueba la jugada i, j.
                    puntaje = minimax(tablero, True)
                    tablero[i][j] = "."  # Borra la jugada i, j.
                    mejor_puntaje = min(puntaje, mejor_puntaje)

    return mejor_puntaje


def mejor_movimiento(tablero):
    """Selecciona la jugada del PC con mayor puntaje según Minimax.

    Args:
        tablero (list[list[str]]): Matriz de 3 x 3 con el estado actual
            de las casillas.

    Returns:
        tuple[int, int] | None: Coordenadas de la mejor jugada o None
            si no existe una jugada disponible.
    """
    mejor_puntaje = -inf
    movimiento = None

    for i in range(3):
        for j in range(3):
            if tablero[i][j] == ".":
                tablero[i][j] = "X"
                puntaje = minimax(tablero, False)
                tablero[i][j] = "."

                if puntaje > mejor_puntaje:
                    mejor_puntaje = puntaje
                    movimiento = (i, j)

    return movimiento


def juego_gato():
    """Ejecuta el juego hasta que haya un ganador o el tablero se llene.

    La función solicita al usuario la fila y la columna mediante teclado.

    Returns:
        None: Imprime el desarrollo y el resultado del juego.
    """
    global cont

    tablero = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]
    turno = "X"  # Inicia jugando el PC.

    while busca_ganador(tablero) is None and not tablero_lleno(tablero):
        imprime_tablero(tablero)

        if turno == "X":
            i, j = mejor_movimiento(tablero)  # PC decide con Minimax.
            print(f"Número de tableros revisados: {cont}")
            cont = 0
            tablero[i][j] = "X"
            print("Juego del PC:")
            turno = "O"
        else:
            fila = int(input("Fila (1,2,3): "))
            columna = int(input("Columna (1,2,3): "))

            if tablero[fila - 1][columna - 1] == ".":
                tablero[fila - 1][columna - 1] = "O"
                turno = "X"

    ganador = busca_ganador(tablero)
    imprime_tablero(tablero)

    if ganador == "X":
        print("Ganó el PC!")
    elif ganador == "O":
        print("Ganaste!")
    else:
        print("Empate")


# Bloque principal.
cont = 0
juego_gato()
