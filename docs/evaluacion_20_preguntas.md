# Evaluación de Desempeño: Chatbot Prolog vs Chatbot LLM

**Proyecto N°2: Agente Inteligente Basado en Conocimiento**  
**Universidad Andrés Bello - Fundamentos de Inteligencia Artificial**

---

## 1. Set de 20 Preguntas de Prueba del Dominio

A continuación se presenta la batería de pruebas diseñada para comparar la precisión lógica, completitud, flexibilidad y robustez de ambas implementaciones:

| N° | Pregunta | Tipo de Consulta |
|:---|:---|:---|
| 1 | ¿Qué ingredientes requiere directamente una espada de hierro? | Hecho directo |
| 2 | ¿Qué materiales base necesito para fabricar un pico de hierro desde cero? | Inferencia transitiva |
| 3 | ¿Cuáles son las debilidades del Zombie? | Hecho relacional |
| 4 | ¿A qué le teme el Creeper? | Hecho relacional |
| 5 | ¿Qué criaturas son hostiles en el juego? | Búsqueda por categoría |
| 6 | ¿Es la vaca un peligro nocturno? | Evaluación booleana |
| 7 | ¿Por qué el esqueleto es vulnerable a los lobos? | Explicación causal |
| 8 | ¿Qué se necesita para elaborar una poción de curación? | Inferencia compuesta |
| 9 | ¿La armadura de diamante es considerada un objeto de nivel avanzado? | Regla deductiva |
| 10 | ¿Qué propiedades tiene la madera? | Propiedad material |
| 11 | Si tengo tronco de madera y lingotes de hierro, ¿puedo fabricar una espada? | Deducción de precondiciones |
| 12 | ¿Qué mobs mueren o se queman con la luz solar? | Inferencia inversa |
| 13 | ¿Qué criatura hostil no se quema con el sol de día? | Negación por falla |
| 14 | ¿El aldeano requiere armas para defenderse? | Fuera de la base de hechos cerrada |
| 15 | ¿Cómo influye el fuego contra un zombie? | Mecánica de daño |
| 16 | ¿Qué necesito para fabricar una sandía reluciente? | Hecho directo |
| 17 | Si combino un palo y una tabla, ¿obtengo un pico de hierro? | Validación negativa |
| 18 | ¿Cuáles son las herramientas disponibles en la base de datos? | Listado de conjunto |
| 19 | ¿Cuál es la estrategia recomendada para defenderse de un Creeper? | Regla de recomendación |
| 20 | ¿Qué ocurre si agrego un mob nuevo 'araña' que sea hostil? | Extensibilidad en vivo |

---

## 2. Comparativa de Respuestas y Análisis de Desempeño

| Criterio | Chatbot Prolog (LPO) | Chatbot LLM (Gemini) |
|:---|:---|:---|
| **Precisión Lógica** | **Exacta (100% determinista):** No alucina; si el hecho o regla existe y unifica, la respuesta es matemáticamente correcta. | **Alta con contexto:** Muy precisa cuando el prompt está bien restringido, pero susceptible a alucinaciones leves si se extrapola fuera del contexto. |
| **Flexibilidad Lingüística**| **Rígida:** Requiere patrones de consulta o sintaxis formal (`meta/aridad`). | **Muy alta:** Comprende lenguaje natural informal, errores ortográficos y preguntas ambiguas con soltura. |
| **Explicabilidad** | **Total:** Cada conclusión puede trazarse paso a paso mediante el árbol de derivación/resolución SLD de Prolog. | **Baja/Opaca:** Basada en pesos neuronales probabilísticos ("caja negra"). |
| **Manejo de Información Faltante** | Asume la **Hipótesis del Mundo Cerrado (CWA)**: si no está en la base, es falso. | Puede inventar información plausible basada en su pre-entrenamiento global si no se delimita estrictamente. |

---

## 3. Fortalezas y Debilidades

### Versión Prolog (Lógica de Primer Orden)
- **Fortalezas:**
  - Cero ambigüedad: las deducciones son formalmente demostrables.
  - Trazabilidad y consistencia formal completa.
  - Extremadamente ligero en consumo de cómputo y sin latencia de red.
  - Fácil de modificar y verificar en vivo durante interrogaciones.
- **Debilidades:**
  - Pobre tolerancia a la variabilidad del lenguaje natural sin una capa pesada de Procesamiento de Lenguaje Natural (PLN/DCG).
  - No maneja incertidumbre ni respuestas probabilísticas por defecto.

### Versión LLM (Python + Gemini)
- **Fortalezas:**
  - Interacción humana fluida y amigable.
  - Capacidad para sintetizar y formatear respuestas complejas de forma intuitiva.
  - Manejo robusto de sinónimos, contexto conversacional y aclaraciones.
- **Debilidades:**
  - Dependencia de conectividad y costo/límites de tokens de la API.
  - Riesgo de alucinación si la base de conocimiento se contradice o el prompt es ambiguo.

---

## 4. Propuestas para Mejorar el Desempeño

1. **Arquitectura Neuro-Simbólica Híbrida:**
   - Usar el LLM únicamente como traductor de lenguaje natural a predicados Prolog estructurados (`NL -> Prolog Goal`), y luego usar el resultado devuelto por Prolog como verdad base para que el LLM redacte la respuesta final. Esto une lo mejor de ambos mundos: la flexibilidad del LLM con el determinismo matemático de Prolog.
2. **Gramáticas de Cláusulas Definidas (DCG) en Prolog:**
   - Incorporar un parser sintáctico en Prolog usando DCGs para interpretar frases en español directamente dentro del motor lógico sin depender de scripts externos.
3. **Mecanismo de Verificación de Alucinaciones en el LLM:**
   - Implementar un validador en Python que verifique que cada entidad mencionada por el LLM exista en el conjunto de hechos formales antes de mostrar la respuesta al usuario.
