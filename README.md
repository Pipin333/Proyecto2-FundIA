# Proyecto N°2: Diseño de un Agente Inteligente que Usa Conocimiento

**Universidad Andrés Bello (UNAB)**  
**Facultad de Ingeniería — Ingeniería Civil Informática**  
**Curso:** Fundamentos de Inteligencia Artificial  

---

## 📋 Descripción del Proyecto
Este proyecto implementa un sistema inteligente de preguntas y respuestas (Chatbot) que opera bajo dos paradigmas fundamentales de la Inteligencia Artificial:
1. **Razonamiento Simbólico y Lógica de Primer Orden (FOL):** Implementado mediante una base de conocimiento y motor de inferencia deductiva en **Prolog** (`SWI-Prolog`).
2. **Modelos de Lenguaje Basados en Redes Neuronales (LLM):** Implementado en **Python** utilizando **Google Gemini** con inyección contextual de la base de conocimiento del dominio.
3. **Frontend Interactivo:** Interfaz gráfica web construida con **Streamlit** que permite consultar ambos agentes de forma independiente o en modo **comparativo lado a lado**.

### Dominio Actual (Plantilla de Referencia)
> ⚠️ **Nota Importante:** La base de conocimiento actual (*Mecánicas de Supervivencia, Fabricación y Ecosistema de Minecraft*) se encuentra implementada como una **plantilla de referencia y prototipo funcional**. El equipo puede modificarla, ampliarla o reemplazarla por cualquier otro dominio no informático acordado (ej. Maridaje/Coctelería, Botánica, etc.) sin romper la arquitectura del backend ni del frontend.

- **Crafteo e Inferencia de Materiales:** Deducción de cadenas de dependencias y recetas (ej. obtención recursiva de herramientas desde troncos crudos).
- **Alquimia y Pociones:** Elaboración y dependencias de ingredientes.
- **Biología y Ecosistema:** Clasificación de entidades (hostiles y pasivas), vulnerabilidades (luz solar, fuego, felinos) y estrategias de defensa.
- *Nota formal:* Se excluyen componentes de circuitos de Redstone compleja para mantener el dominio completamente ajeno a la arquitectura de computadores o la informática.

---

## 🏗️ Arquitectura y Estructura del Repositorio

```text
Proyecto2-FundIA/
├── knowledge/
│   ├── base_conocimiento.pl       # Hechos y reglas deductivas en Prolog (LPO)
│   └── dominio_context.txt        # Contexto del dominio para el motor LLM
├── backend/
│   ├── __init__.py
│   ├── prolog_engine.py           # Conector y ejecutor de consultas SWI-Prolog
│   └── llm_engine.py              # Integración con Google Gemini API
├── docs/
│   ├── modelado_fol.md            # Modelado formal en Lógica de Primer Orden
│   └── evaluacion_20_preguntas.md # Set de 20 preguntas, análisis y propuestas
├── app.py                         # Aplicación Web principal (Streamlit)
├── requirements.txt               # Dependencias de Python
├── AGENTS.md                      # Instrucciones para IAs colaboradoras
├── HANDOFF.md                     # Traspaso del proyecto
├── .env.example                   # Plantilla de variables de entorno
└── README.md                      # Documentación del proyecto
```

---

## ⚙️ Requisitos Previos

- **Python:** Versión 3.10 o superior (probado en Python 3.13).
- **SWI-Prolog:** Motor lógico para la ejecución de la base de conocimiento `.pl`.
  - En Windows se puede instalar mediante `winget`:
    ```powershell
    winget install --id SWI-Prolog.SWI-Prolog -e
    ```
  - O descargando el instalador oficial desde [swi-prolog.org](https://www.swi-prolog.org/download/stable).
  - *Asegúrate de marcar la casilla "Add to PATH" durante la instalación.*

---

## 🚀 Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Pipin333/Proyecto2-FundIA.git
   cd Proyecto2-FundIA
   ```

2. **Crear y activar un entorno virtual (recomendado):**
   ```bash
   python -m venv venv
   # En Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   - Copia el archivo `.env.example` y renómbralo a `.env`:
     ```bash
     copy .env.example .env
     ```
   - Abre `.env` y coloca tu API Key de Gemini:
     ```env
     GEMINI_API_KEY=tu_api_key_aqui
     ```
   *(También puedes ingresar la API Key directamente desde la barra lateral de la interfaz web).*

---

## 💻 Ejecución del Sistema

Para iniciar la aplicación web:

```powershell
streamlit run app.py
```

La aplicación se abrirá en tu navegador web predeterminado (usualmente en `http://localhost:8501`).

### Modos de Operación en la Web
- **Comparativa (Prolog vs LLM):** Despliega ambas respuestas en columnas paralelas para evaluar fortalezas, debilidades y posibles alucinaciones.
- **Solo Prolog (FOL):** Ejecuta estrictamente el motor de inferencia deductiva sobre la base `.pl`.
- **Solo LLM:** Consulta el modelo generativo condicionado al contexto del dominio.
- **Editor en Vivo (Sidebar):** Permite ver y modificar el archivo `base_conocimiento.pl` directamente desde la interfaz y recargar el estado, ideal para la interrogación de taller.

---

## 📝 Documentación Adicional
- [Guía para Agentes de IA](AGENTS.md): Normas, restricciones y convenciones para Cursor, Claude Code, Copilot, etc.
- [Documento de Traspaso (Handoff)](HANDOFF.md): Estado actual del proyecto, decisiones de diseño y chuleta para la interrogación oral.
- [Modelado Formal en Lógica de Primer Orden](docs/modelado_fol.md): Contiene constantes, predicados, hechos y axiomas con cuantificadores ($\forall, \exists$).
- [Evaluación de Desempeño y 20 Preguntas](docs/evaluacion_20_preguntas.md): Set de prueba completo, tablas de fortalezas/debilidades y propuestas de optimización.
