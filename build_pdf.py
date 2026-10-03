import os
from playwright.sync_api import sync_playwright

with open('teeko.py', 'r', encoding='utf-8') as f:
    teeko_code = f.read()

md_doc = f"""# Documento Proyecto Teeko - Fundamentos de Inteligencia Artificial

---

## 1. Código de Teeko Completo con Docstrings PEP-257 y Cumplimiento PEP-8

```python
{teeko_code}
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
**Respuesta:** Definimos una variable global `nodos_evaluados = 0`, la incrementamos al inicio de `minimax()` (`nodos_evaluados += 1`) y en `play_game()` imprimimos `print(f"Nodos explorados: {{nodos_evaluados}}")` justo después de recibir `best_move`, reiniciando el contador a 0.
"""

with open('Documento_Teeko_2.md', 'w', encoding='utf-8') as f:
    f.write(md_doc)

print('Documento_Teeko_2.md created successfully!')

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Documento Proyecto Teeko - Fundamentos de IA</title>
<style>
    @page {{
        size: A4;
        margin: 18mm 14mm 18mm 14mm;
        @bottom-right {{
            content: counter(page);
        }}
    }}
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #1f2328;
        line-height: 1.45;
        font-size: 10pt;
        background: #fff;
    }}
    h1 {{
        color: #0969da;
        border-bottom: 2px solid #0969da;
        padding-bottom: 6px;
        font-size: 18pt;
        margin-top: 0;
        margin-bottom: 6px;
    }}
    .subtitle {{
        font-size: 10.5pt;
        color: #57606a;
        margin-bottom: 16px;
    }}
    h2 {{
        color: #1f2328;
        border-bottom: 1px solid #d0d7de;
        padding-bottom: 4px;
        font-size: 13pt;
        margin-top: 20px;
        margin-bottom: 10px;
        page-break-after: avoid;
    }}
    h3 {{
        color: #0969da;
        font-size: 11pt;
        margin-top: 14px;
        margin-bottom: 8px;
        page-break-after: avoid;
    }}
    p, li {{
        font-size: 9.5pt;
        text-align: justify;
    }}
    ul {{
        padding-left: 18px;
        margin-top: 6px;
    }}
    li {{
        margin-bottom: 5px;
    }}
    pre {{
        background-color: #f6f8fa;
        border: 1px solid #d0d7de;
        border-radius: 6px;
        padding: 10px;
        font-family: "Consolas", "Courier New", monospace;
        font-size: 7.8pt;
        line-height: 1.3;
        overflow-x: auto;
        white-space: pre-wrap;
        word-break: break-all;
    }}
    code {{
        font-family: "Consolas", "Courier New", monospace;
        background-color: #eff1f3;
        padding: 2px 4px;
        border-radius: 4px;
        font-size: 8.5pt;
    }}
    pre code {{
        background: none;
        padding: 0;
    }}
    .question-box {{
        background-color: #f8fafc;
        border-left: 3.5px solid #0969da;
        padding: 8px 12px;
        margin-bottom: 10px;
        border-radius: 0 5px 5px 0;
        page-break-inside: avoid;
    }}
    .question-title {{
        font-weight: bold;
        color: #0969da;
        font-size: 9.8pt;
        margin-bottom: 3px;
    }}
    .page-break {{
        page-break-before: always;
    }}
</style>
</head>
<body>

<h1>Documento Proyecto Teeko - Fundamentos de IA</h1>
<div class="subtitle">
    <strong>Universidad Andrés Bello</strong> | Facultad de Ingeniería | Fundamentos de Inteligencia Artificial<br>
    <strong>Entrega 2:</strong> Implementación del Agente Inteligente (Minimax + Poda Alfa-Beta + Heurística PEP-257)
</div>

<h2>1. Código de Teeko Completo con Docstrings PEP-257</h2>
<pre><code>{teeko_code}</code></pre>

<div class="page-break"></div>

<h2>2. Desglose por Funciones del Juego y Componentes del Sistema</h2>
<ul>
    <li><strong><code>Teeko.__init__</code></strong>: Configura el estado base del juego parametrizando el tamaño del tablero (n &ge; 5). Genera la matriz de n &times; n, inicializa el conteo de 4 fichas por jugador, fija el turno inicial en <code>'A'</code> e inicia la Fase 1 (Colocación).</li>
    <li><strong><code>Teeko.get_state_hash</code></strong>: Genera la firma única del estado para la detección de empates por repetición. Convierte el tablero en una sola cadena secuencial y le adjunta el identificador del jugador en turno.</li>
    <li><strong><code>Teeko.print_board</code></strong>: Renderiza el tablero en consola con numeración 1 a n, mostrando la fase actual y el jugador en turno.</li>
    <li><strong><code>Teeko.check_win</code></strong>: Árbitro de victoria. Escanea el tablero para confirmar si un jugador formó alguna de las 5 configuraciones ganadoras (4 fichas horizontales, verticales, diagonales o un bloque cerrado 2 &times; 2).</li>
    <li><strong><code>Teeko.get_legal_moves</code></strong>: Generador de acciones del agente. En Fase 1 retorna todas las casillas vacías (r, c). En Fase 2 calcula todos los desplazamientos válidos a casillas adyacentes vacías (r1, c1, r2, c2).</li>
    <li><strong><code>Teeko.make_move</code></strong>: Aplica la jugada al tablero, gestiona la transición a Fase 2 al colocar las 8 fichas, alterna el turno y registra el hash en el historial.</li>
    <li><strong><code>Teeko.undo_move</code></strong>: Revierte la jugada restaurando la casilla previa, el conteo de piezas, el turno y el historial, permitiendo que Minimax explore sin duplicar objetos en memoria.</li>
    <li><strong><code>Teeko.is_terminal</code></strong>: Evalúa si el estado actual es terminal revisando victoria de <code>'A'</code>, victoria de <code>'B'</code>, triple repetición (empate) o bloqueo de movimientos en Fase 2 (derrota del jugador sin jugadas).</li>
    <li><strong><code>evaluate</code></strong>: Función de evaluación heurística. Utiliza la distancia de Chebyshev entre las piezas para premiar agrupaciones compactas de la IA y penalizar formaciones enemigas cercanas.</li>
    <li><strong><code>minimax</code></strong>: Algoritmo de búsqueda adversarial. Construye el árbol de decisiones simulando las mejores respuestas del adversario e integra Poda Alfa-Beta para descartar ramas subóptimas.</li>
    <li><strong><code>play_game</code></strong>: Orquestador del juego. Maneja el menú de modos (Humano vs Humano / Humano vs IA), captura excepciones para validación robusta de entradas y controla el ciclo de partidas.</li>
</ul>

<h2>3. Preguntas Estratégicas para la Interrogación</h2>

<h3>🧠 Bloque 1: Heurística y Estrategia</h3>

<div class="question-box">
    <div class="question-title">P1: ¿Cuál es el propósito exacto de su Función de Evaluación Heurística y bajo qué criterios opera?</div>
    <p><strong>Respuesta:</strong> Como las condiciones de victoria de Teeko exigen agrupaciones de 4 fichas en línea o en un bloque cerrado 2&times;2, nuestra heurística premia los estados donde las fichas de la IA están a una distancia de Chebyshev adyacente (distancia 1 o 2). Al mismo tiempo, penaliza si las fichas del oponente están agrupadas. Esto guía al Minimax de forma orgánica hacia la formación de figuras ganadoras y al bloqueo defensivo sin requerir reglas manuales rígidas.</p>
</div>

<div class="question-box">
    <div class="question-title">P2: ¿Por qué eligieron la Distancia de Chebyshev en lugar de la distancia de Manhattan o Euclidiana?</div>
    <p><strong>Respuesta:</strong> Porque en Teeko las fichas se mueven y ganan tanto ortogonal como diagonalmente en 8 direcciones. La distancia de Chebyshev (max(|&Delta;x|, |&Delta;y|)) asigna costo 1 a un paso diagonal (igual que horizontal o vertical), modelando con exactitud la geometría del juego y la formación de bloques 2&times;2.</p>
</div>

<div class="question-box">
    <div class="question-title">P3: ¿Cómo distingue su IA entre una victoria inmediata, un empate y un estado intermedio?</div>
    <p><strong>Respuesta:</strong> Mediante una jerarquía clara de utilidades:
    <br>&bull; Victoria de la IA: +100.000 (utilidad máxima).
    <br>&bull; Victoria del adversario: -100.000 (utilidad mínima a evitar).
    <br>&bull; Empate (triple repetición): 0 (neutral).
    <br>&bull; Estados intermedios (no terminales): Puntuación heurística acotada entre -200 y +200 evaluada en las hojas del árbol.</p>
</div>

<h3>⚡ Bloque 2: Minimax, Poda Alfa-Beta y Complejidad</h3>

<div class="question-box">
    <div class="question-title">P4: ¿Dónde ocurre la Poda Alfa-Beta en el código y qué se gana computacionalmente?</div>
    <p><strong>Respuesta:</strong> Ocurre en las líneas <code>if beta &le; alpha: break</code>. En el maximizador se podan ramas cuando encontramos un valor superior o igual a &beta; (Poda Beta), y en el minimizador cuando encontramos un valor inferior o igual a &alpha; (Poda Alfa). Esto reduce el factor de ramificación efectivo de b^d hasta b^(d/2) en el mejor caso, ahorrando miles de evaluaciones de nodos por turno.</p>
</div>

<div class="question-box">
    <div class="question-title">P5: ¿Por qué la profundidad de búsqueda varía entre la Fase 1 (depth=3) y la Fase 2 (depth=4)?</div>
    <p><strong>Respuesta:</strong> En la Fase 1 (Colocación), el factor de ramificación es alto (b &approx; 20-25 casillas vacías), por lo que una profundidad mayor ralentizaría el turno. En la Fase 2 (Movimiento), cada jugador solo tiene 4 fichas con opciones de movimiento adyacentes limitadas (b &approx; 8-15), lo que permite descender a profundidad 4 con respuesta inmediata.</p>
</div>

<div class="question-box">
    <div class="question-title">P6: ¿Cómo afectaría el orden de exploración de movimientos (Move Ordering) a la Poda Alfa-Beta?</div>
    <p><strong>Respuesta:</strong> Si ordenamos los movimientos legales explorando primero aquellos con mejor puntaje heurístico, los valores de &alpha; y &beta; se ajustan rápidamente a sus extremos en los primeros hijos, provocando que la gran mayoría de las ramas restantes se corten de inmediato.</p>
</div>

<div class="question-box">
    <div class="question-title">P7: ¿Por qué implementaron make_move y undo_move en lugar de clonar el objeto Teeko en cada paso?</div>
    <p><strong>Respuesta:</strong> Para optimizar memoria y tiempo de CPU. Clonar objetos complejos con <code>copy.deepcopy(game)</code> miles de veces por llamada satura el garbage collector. Modificar el estado en el lugar y deshacer la jugada al regresar de la recursión mantiene el árbol en tiempo de ejecución instantáneo (O(1) por nodo).</p>
</div>

<div class="page-break"></div>

<h3>🛡️ Bloque 3: Detección de Estados y Robustez</h3>

<div class="question-box">
    <div class="question-title">P8: ¿Qué problema tuvieron previamente con la detección del Empate por Repetición y cómo lo resolvieron?</div>
    <p><strong>Respuesta:</strong> Inicialmente almacenábamos la firma del tablero <em>antes</em> de alternar el turno, asociando la foto al jugador incorrecto. Lo solucionamos invirtiendo el orden: en <code>make_move</code> primero alternamos <code>current_player</code> y luego calculamos el hash <code>board_str + current_player</code>. Así la repetición evalúa fielmente el tablero y a quién le toca mover.</p>
</div>

<div class="question-box">
    <div class="question-title">P9: ¿Qué comportamiento tiene la aplicación frente a entradas inválidas (texto, fuera de rango o casillas ocupadas)?</div>
    <p><strong>Respuesta:</strong> Cuenta con validación robusta con bloques <code>try-except ValueError</code>. Si el usuario ingresa texto, un número fuera de rango (&lt;1 o &gt;n) o una casilla ocupada, el programa atrapa la excepción o valida la condición, despliega un mensaje amigable y solicita nuevamente el dato con <code>continue</code>, sin que el programa se caiga.</p>
</div>

<h3>🛠️ Bloque 4: Modificaciones de Código en Vivo (Live Coding)</h3>

<div class="question-box">
    <div class="question-title">P10: Si les pido que la IA juegue con el turno 'A' (primer jugador) y el humano con 'B', ¿qué modifican?</div>
    <p><strong>Respuesta:</strong> En el bucle de <code>play_game()</code>, cambiamos la condición a <code>if mode == '2' and game.current_player == 'A':</code> y en la llamada a Minimax pasamos <code>'A'</code> como <code>ai_player</code>:<br>
    <code>_, best_move = minimax(game, depth, -math.inf, math.inf, True, "A")</code></p>
</div>

<div class="question-box">
    <div class="question-title">P11: Si les pido desactivar la condición de victoria por bloque 2x2 (solo permitir 4 en línea), ¿qué línea tocan?</div>
    <p><strong>Respuesta:</strong> En el método <code>check_win(self, player)</code>, comentamos la verificación del bloque 2x2:<br>
    <code># if r + 1 &lt; self.n and c + 1 &lt; self.n:</code><br>
    <code>#     if (self.board[r][c+1] == player and self.board[r+1][c] == player ...): return True</code></p>
</div>

<div class="question-box">
    <div class="question-title">P12: Si les pido mostrar en consola cuántos nodos o tableros exploró Minimax en cada turno, ¿dónde lo implementan?</div>
    <p><strong>Respuesta:</strong> Definimos una variable global <code>nodos_evaluados = 0</code>, la incrementamos al inicio de <code>minimax()</code> (<code>nodos_evaluados += 1</code>) y en <code>play_game()</code> imprimimos <code>print(f"Nodos explorados: {{nodos_evaluados}}")</code> justo después de recibir <code>best_move</code>, reiniciando el contador a 0.</p>
</div>

</body>
</html>"""

with open('Documento_Teeko_2.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Documento_Teeko_2.html created successfully!')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('file:///' + os.path.abspath('Documento_Teeko_2.html').replace('\\', '/'))
    page.pdf(path='Documento_Teeko_2.pdf', format='A4', print_background=True, margin={'top': '15mm', 'bottom': '15mm', 'left': '14mm', 'right': '14mm'})
    browser.close()

print('Documento_Teeko_2.pdf rendered and saved successfully!')
