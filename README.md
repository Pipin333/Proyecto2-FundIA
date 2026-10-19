# Proyecto N°2: Diseño de un Agente Inteligente que Usa Conocimiento

Carlos Castro 21.347.261-5  
Iván Gómez 21.484.010-3  
Matias Rodriguez 21.734.431-K  
Felipe Riquelme 21.219.955-9  

**Universidad Andrés Bello (UNAB)**  
**Facultad de Ingeniería — Ingeniería Civil Informática**  
**Curso:** Fundamentos de Inteligencia Artificial (2026)  

---

## 📋 Descripción del Proyecto
Este proyecto implementa un sistema inteligente de preguntas y respuestas (Chatbot) que opera bajo dos paradigmas fundamentales de la Inteligencia Artificial:
1. **Razonamiento Simbólico y Lógica de Primer Orden (FOL):** Implementado mediante una base de conocimiento y motor de inferencia deductiva en **Prolog** (`SWI-Prolog` y evaluador Datalog en memoria).
2. **Modelos de Lenguaje Basados en Redes Neuronales (LLM):** Implementado en **Python** utilizando **Google Gemini** con inyección contextual aumentada de la base de conocimiento del dominio y puente Neuro-Simbólico.
3. **Frontend Interactivo:** Interfaz gráfica web construida con **Streamlit** que permite consultar ambos agentes de forma independiente o en modo **comparativo lado a lado**, con acceso directo a la batería de 20 preguntas y editor de reglas en vivo.

### Dominio Actual (Plantilla de Referencia)
> ⚠️ **Nota Importante:** La base de conocimiento actual (*Mecánicas de Supervivencia, Fabricación y Ecosistema de Minecraft Java*) se encuentra implementada como una **plantilla de referencia y prototipo funcional**. El equipo puede modificarla, ampliarla o reemplazarla por cualquier otro dominio no informático acordado (ej. Maridaje/Coctelería, Botánica, etc.) sin alterar la arquitectura del backend ni del frontend.

- **Crafteo e Inferencia de Materiales:** Deducción de cadenas de dependencias y recetas (ej. obtención recursiva de herramientas desde troncos crudos mediante transitividad).
- **Alquimia y Pociones:** Elaboración y dependencias de ingredientes.
- **Biología y Ecosistema:** Clasificación de entidades (hostiles y pasivas), vulnerabilidades (luz solar, fuego, felinos) y estrategias de defensa.
- *Nota formal:* Se excluyen componentes de circuitos de Redstone compleja para mantener el dominio completamente ajeno a la arquitectura de computadores o la electrónica digital.

---

## 🏗️ Arquitectura y Estructura del Repositorio

```text
FundIA/
├── knowledge/
│   ├── base_conocimiento.pl       # Hechos y reglas deductivas en Prolog (LPO)
│   └── dominio_context.txt        # Contexto del dominio para el motor LLM
├── backend/
│   ├── __init__.py
│   ├── prolog_engine.py           # Conector SWI-Prolog, evaluador Datalog y filtro de seguridad
│   └── llm_engine.py              # Integración Gemini API (Google GenAI) y puente neuro-simbólico
├── tests/
│   └── test_prolog_engine.py      # Suite automatizada (20 preguntas, seguridad e inferencias)
├── docs/
│   ├── modelado_fol.md            # Modelado formal en Lógica de Primer Orden
│   └── evaluacion_20_preguntas.md # Set de 20 preguntas, análisis y propuestas
├── app.py                         # Aplicación Web principal (Streamlit)
├── Dockerfile                     # Imagen multi-stage con Python 3.12 y SWI-Prolog
├── docker-compose.yml             # Despliegue en 1 clic
├── .dockerignore                  # Exclusión de archivos pesados y secretos
├── requirements.txt               # Dependencias de Python
├── AGENTS.md                      # Instrucciones para IAs colaboradoras
├── HANDOFF.md                     # Traspaso del proyecto y chuleta de interrogación oral
├── .env.example                   # Plantilla de variables de entorno
└── README.md                      # Documentación del proyecto
```

---

## 🐳 Ejecución Inmediata con Docker (Recomendado)

El proyecto está 100% containerizado para garantizar portabilidad universal (Linux, macOS y Windows con WSL2 o Docker Desktop). Incluye tanto el entorno Python como el motor SWI-Prolog preconfigurado.

```bash
# 1. Ingresar a la carpeta de Proyecto 2
cd Proyecto2

# 2. Configurar variables de entorno
cp .env.example .env

# 3. Construir y levantar el contenedor (1-Click Run)
docker compose up --build
```

Una vez levantado, ingresa desde cualquier navegador a:
👉 **`http://localhost:8501`**

---

## ⚙️ Ejecución Local (Sin Docker)

### Requisitos Previos
- **Python:** Versión 3.10 o superior (probado en Python 3.13).
- **SWI-Prolog (Opcional):** Motor nativo para ejecución directa en el SO.
  - En Windows se puede instalar mediante `winget`:
    ```powershell
    winget install --id SWI-Prolog.SWI-Prolog -e
    ```
  - *Si no está instalado, el sistema activa automáticamente su evaluador deductivo seguro en memoria.*

### Instalación
1. **Crear y activar un entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # En Linux / macOS:
   source venv/bin/activate
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar API Key:**
   - Copia `.env.example` como `.env` y agrega tu clave de Google Gemini:
     ```env
     GEMINI_API_KEY=tu_api_key_aqui
     ```
   *(También puedes ingresar la API Key directamente desde la barra lateral de la app web).*

4. **Ejecutar la suite de pruebas automatizada:**
   ```bash
   python -m pytest -v tests/
   ```

5. **Iniciar la aplicación web:**
   ```bash
   streamlit run app.py
   ```

---

## 💻 Modos de Operación en la Web
- **Comparativa (Prolog vs LLM):** Despliega ambas respuestas en columnas paralelas para evaluar fortalezas, debilidades, determinismo matemático y posibles alucinaciones.
- **Solo Prolog (FOL):** Ejecuta estrictamente el motor de inferencia deductiva sobre la base `.pl`.
- **Solo LLM:** Consulta el modelo generativo condicionado al contexto del dominio.
- **Selector Rápido de 20 Preguntas:** Menú desplegable para disparar instantáneamente cualquiera de las 20 consultas del informe de evaluación.
- **Editor en Vivo (Sidebar):** Permite visualizar y modificar `base_conocimiento.pl` directamente desde la interfaz y recargar el estado en caliente (con respaldo automático `.bak`), ideal para la interrogación de taller (80% de la nota).

---

## 📝 Documentación del Proyecto
- [Guía para Agentes de IA](AGENTS.md): Normas, restricciones y convenciones para Cursor, Claude Code, Copilot, Antigravity.
- [Documento de Traspaso (Handoff)](HANDOFF.md): Estado actual, decisiones técnicas y chuleta paso a paso para la interrogación oral.
- [Modelado Formal en Lógica de Primer Orden](docs/modelado_fol.md): Constantes, predicados, hechos y axiomas con cuantificadores ($\forall, \exists$).
- [Evaluación de Desempeño y 20 Preguntas](docs/evaluacion_20_preguntas.md): Set de prueba completo, tablas de fortalezas/debilidades y propuestas de optimización.
