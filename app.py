"""Interfaz Web del Chatbot Inteligente Basado en Conocimiento (Streamlit).

Permite interactuar con la versión en Prolog (Lógica de Primer Orden), la versión
con Modelos de Lenguaje (Google Gemini con contexto aumentado) o comparar ambas
respuestas simultáneamente con soporte para el set de 20 preguntas de evaluación.
"""

import os
import re
import shutil
from pathlib import Path
from typing import List

import streamlit as st
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

from backend.llm_engine import LLMEngine
from backend.prolog_engine import PrologEngine

# Configuración de página con título e icono
st.set_page_config(
    page_title="Chatbot Basado en Conocimiento - IA UNAB",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar motores
prolog_engine = PrologEngine()
llm_engine = LLMEngine()

# Inicializar estado de la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# Batería de 20 preguntas del informe académico
PREGUNTAS_EVALUACION: List[str] = [
    "¿Qué ingredientes requiere directamente una espada de hierro?",
    "¿Qué materiales base necesito para fabricar un pico de hierro desde cero?",
    "¿Cuáles son las debilidades del Zombie?",
    "¿A qué le teme el Creeper?",
    "¿Qué criaturas son hostiles en el juego?",
    "¿Es la vaca un peligro nocturno?",
    "¿Por qué el esqueleto es vulnerable a los lobos?",
    "¿Qué se necesita para elaborar una poción de curación?",
    "¿La armadura de diamante es considerada un objeto de nivel avanzado?",
    "¿Qué propiedades tiene la madera?",
    "Si tengo tronco de madera y lingotes de hierro, ¿puedo fabricar una espada?",
    "¿Qué mobs mueren o se queman con la luz solar?",
    "¿Qué criatura hostil no se quema con el sol de día?",
    "¿El aldeano requiere armas para defenderse?",
    "¿Cómo influye el fuego contra un zombie?",
    "¿Qué necesito para fabricar una sandía reluciente?",
    "Si combino un palo y una tabla, ¿obtengo un pico de hierro?",
    "¿Cuáles son las herramientas disponibles en la base de datos?",
    "¿Cuál es la estrategia recomendada para defenderse de un Creeper?",
    "¿Qué ocurre si agrego un mob nuevo araña que sea hostil?"
]

# ==============================================================================
# BARRA LATERAL (Configuración, Diagnóstico y Base de Conocimiento)
# ==============================================================================
with st.sidebar:
    st.title("⚙️ Configuración")

    modo = st.radio(
        "Selecciona el Modo del Chatbot:",
        ["Comparativa (Prolog vs LLM)", "Solo Prolog (FOL)", "Solo LLM"],
        index=0,
        help="Elige el modo de razonamiento: formal determinista (Prolog), generativo (LLM) o comparativo."
    )

    st.divider()
    st.subheader("🔍 Estado de los Motores")
    if prolog_engine.is_available():
        st.success(f"✅ SWI-Prolog Nativo: `{Path(prolog_engine.swipl_binary).name}`")
    else:
        st.info("ℹ️ Motor Prolog: Evaluador Deductivo en Memoria (Datalog Fallback)")

    st.divider()
    st.subheader("🔑 Clave Gemini API")
    api_key_input = st.text_input(
        "API Key (o configurar en .env):",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        help="Obtén tu clave gratuita en Google AI Studio (aistudio.google.com)."
    )

    st.divider()
    st.subheader("📖 Base de Conocimiento (.pl)")
    kb_path = Path(__file__).resolve().parent / "knowledge" / "base_conocimiento.pl"

    if kb_path.exists():
        with st.expander("📝 Editor en Vivo de Reglas Prolog"):
            st.caption("Modifica o agrega hechos/reglas para la interrogación del taller.")
            kb_content = kb_path.read_text(encoding="utf-8")
            edited_content = st.text_area(
                "Código Prolog:",
                value=kb_content,
                height=260,
                key="editor_prolog_sidebar"
            )
            if st.button("💾 Guardar y Recargar en Vivo", type="primary"):
                # Validación de seguridad antes de escribir
                dangerous_tokens = ["shell(", "system(", "delete_file(", "process_create("]
                if any(dt in edited_content.lower() for dt in dangerous_tokens):
                    st.error("❌ El contenido contiene directivas prohibidas por seguridad.")
                else:
                    # Crear copia de respaldo (.bak)
                    backup_path = kb_path.with_suffix(".pl.bak")
                    shutil.copyfile(kb_path, backup_path)
                    kb_path.write_text(edited_content, encoding="utf-8")
                    st.success("¡Base de conocimiento actualizada y recargada con éxito!")
                    st.rerun()

    st.divider()
    if st.button("🗑️ Limpiar Historial de Chat"):
        st.session_state.messages = []
        st.rerun()

# ==============================================================================
# PANEL PRINCIPAL
# ==============================================================================
st.title("🧠 Agente Inteligente Basado en Conocimiento")
st.caption(
    "Proyecto N°2 — Fundamentos de Inteligencia Artificial (UNAB) | "
    "Lógica de Primer Orden (Prolog) vs. Modelos de Lenguaje (Gemini)"
)

# Selector rápido de preguntas de evaluación (20 preguntas)
with st.expander("🎯 Batería de Pruebas: 20 Preguntas de Evaluación", expanded=False):
    st.markdown(
        "Selecciona cualquiera de las **20 preguntas del informe académico** para probar "
        "ambos motores de razonamiento de forma instantánea:"
    )
    col_sel, col_btn = st.columns([4, 1])
    with col_sel:
        pregunta_seleccionada = st.selectbox(
            "Seleccionar pregunta:",
            options=PREGUNTAS_EVALUACION,
            index=0,
            label_visibility="collapsed"
        )
    with col_btn:
        ejecutar_preset = st.button("🚀 Consultar", use_container_width=True)

# Mostrar historial de conversación
if not st.session_state.messages:
    st.info(
        "👋 **Bienvenido al Agente Inteligente Basado en Conocimiento.**\n\n"
        "- Escribe una pregunta en el chat inferior o selecciona una de las **20 preguntas predefinidas** arriba.\n"
        "- En modo **Comparativa**, podrás contrastar la deducción matemática determinista (Prolog) "
        "con la respuesta generativa contextualizada (LLM)."
    )

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("tipo") == "comparativa":
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 🧩 Prolog (LPO)")
                st.markdown(msg["prolog"])
            with col2:
                st.markdown("#### 🤖 LLM (Gemini)")
                st.markdown(msg["llm"])
        else:
            st.markdown(msg["content"])

# Captura de entrada (chat o preset)
pregunta_usuario = None
if ejecutar_preset and pregunta_seleccionada:
    pregunta_usuario = pregunta_seleccionada
else:
    chat_input_val = st.chat_input("Escribe tu pregunta sobre el dominio o una meta Prolog...")
    if chat_input_val:
        pregunta_usuario = chat_input_val

if pregunta_usuario:
    # Registrar mensaje del usuario en el historial
    st.session_state.messages.append({"role": "user", "content": pregunta_usuario})
    with st.chat_message("user"):
        st.markdown(pregunta_usuario)

    # Procesar respuesta según el modo activo
    with st.chat_message("assistant"):
        if modo == "Comparativa (Prolog vs LLM)":
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 🧩 Prolog (LPO)")
                with st.spinner("Deduciendo con motor Prolog..."):
                    resp_prolog = prolog_engine.consultar_interpretado(
                        pregunta_usuario,
                        llm_engine=llm_engine,
                        api_key_override=api_key_input
                    )
                    st.markdown(resp_prolog)

            with col2:
                st.markdown("#### 🤖 LLM (Gemini)")
                with st.spinner("Consultando LLM con contexto..."):
                    resp_llm = llm_engine.responder(
                        pregunta_usuario,
                        api_key_override=api_key_input
                    )
                    st.markdown(resp_llm)

            st.session_state.messages.append({
                "role": "assistant",
                "tipo": "comparativa",
                "prolog": resp_prolog,
                "llm": resp_llm
            })

        elif modo == "Solo Prolog (FOL)":
            with st.spinner("Deduciendo con motor Prolog..."):
                resp = prolog_engine.consultar_interpretado(
                    pregunta_usuario,
                    llm_engine=llm_engine,
                    api_key_override=api_key_input
                )
                st.markdown(resp)
                st.session_state.messages.append({"role": "assistant", "content": resp})

        elif modo == "Solo LLM":
            with st.spinner("Consultando LLM con contexto..."):
                resp = llm_engine.responder(
                    pregunta_usuario,
                    api_key_override=api_key_input
                )
                st.markdown(resp)
                st.session_state.messages.append({"role": "assistant", "content": resp})
