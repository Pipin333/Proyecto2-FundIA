# Instrucciones y Guía para Agentes de IA (AGENTS.md)

Este repositorio contiene el **Proyecto N°2 de Fundamentos de Inteligencia Artificial (UNAB)**: *Diseño de un Agente Inteligente que usa conocimiento (Prolog + LLM)*.

Cualquier modelo o agente de IA que trabaje en esta base de código (Claude Code, Cursor, GitHub Copilot, Codex, Antigravity, etc.) **debe cumplir estrictamente las siguientes directrices**:

---

## 🎯 1. Propósito y Restricciones del Proyecto
1. **Dominio del Conocimiento:** Debe ser un tema del mundo real o sistema formal **no relacionado con la informática**. Actualmente modelado como *Mecánicas de Supervivencia, Fabricación y Ecosistema de Entidades (Minecraft)*.
   - **Regla Crítica:** NO modelar compuertas lógicas ni circuitos complejos de Redstone para evitar objeciones de que el dominio aborda "arquitectura de computadores o electrónica digital".
2. **Dualidad LPO + LLM:** El sistema compara dos enfoques:
   - Razonamiento formal deductivo en **Prolog** (Lógica de Primer Orden, determinista).
   - Razonamiento conversacional con **LLMs** (Python + Google Gemini / OpenAI).
3. **80% de la Evaluación es Interrogación en Taller:**
   - Durante la evaluación, el profesor solicitará a integrantes específicos **agregar o modificar reglas/hechos en vivo**.
   - Por tanto, todo código en Prolog (`knowledge/base_conocimiento.pl`) debe ser **extremadamente limpio, legible y modular**.

---

## 🏛️ 2. Arquitectura del Código
- **`knowledge/base_conocimiento.pl`**: Hechos (`categoria/2`, `requiere_directo/2`, `debil_contra/2`) y reglas deductivas (`requiere_material_base/2`, etc.).
- **`knowledge/dominio_context.txt`**: Documento de texto plano que sincroniza el conocimiento del dominio para inyectarlo como contexto al LLM.
- **`backend/prolog_engine.py`**: Interfaz Python para invocar SWI-Prolog vía subprocess. Maneja errores elegantemente si `swipl` no está en PATH.
- **`backend/llm_engine.py`**: Integración con el LLM (Gemini API), cargando el contexto desde `knowledge/dominio_context.txt`.
- **`app.py`**: Frontend web en Streamlit con modos de consulta: Prolog, LLM y Comparativa.
- **`docs/`**: Documentación formal requerida para las entregas académicas.

---

## 📜 3. Protocolos de Desarrollo para Agentes
1. **Sincronización Obligatoria:**
   - Si agregas o modificas un predicado o regla en `knowledge/base_conocimiento.pl`, **debes reflejarlo inmediatamente** en `knowledge/dominio_context.txt`, en `docs/modelado_fol.md` y en las preguntas de `docs/evaluacion_20_preguntas.md`.
2. **Buenas Prácticas (PEP-8 y Prolog):**
   - No usar bibliotecas pesadas innecesarias.
   - Mantener nombres de predicados en español y snake_case (`categoria/2`, `requiere_directo/2`).
   - Evitar duplicación de código y código espagueti.
3. **Manejo de Errores:**
   - Si SWI-Prolog no está disponible, el sistema debe informar amigablemente al usuario en lugar de colapsar con un traceback no capturado.

---

## 🛠️ 4. Comandos Frecuentes
- **Ejecutar la app web:** `streamlit run app.py`
- **Probar backend:** `python -c "import backend; print('OK')"`
- **Probar Prolog por consola:** `swipl -s knowledge/base_conocimiento.pl`
