"""
Interfaz Web del Chatbot Inteligente (Streamlit)
Permite interactuar con la versión en Prolog, la versión con LLM,
o comparar ambas respuestas simultáneamente.
"""

import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

from backend.prolog_engine import PrologEngine
from backend.llm_engine import LLMEngine

st.set_page_config(
    page_title="Chatbot Basado en Conocimiento - IA UNAB",
    page_icon="🧠",
    layout="wide"
)

# Inicializar motores (sin caché persistente para recarga en caliente de la base de conocimiento)
prolog_engine = PrologEngine()
llm_engine = LLMEngine()

# Estado de la sesión para el historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================================================================
# BARRA LATERAL (Configuración y Base de Conocimiento)
# ==============================================================================
with st.sidebar:
    st.title("⚙️ Configuración")
    
    modo = st.radio(
        "Selecciona el Modo del Chatbot:",
        ["Comparativa (Prolog vs LLM)", "Solo Prolog (FOL)", "Solo LLM"],
        index=0
    )
    
    st.divider()
    st.subheader("🔍 Estado de los Motores")
    if prolog_engine.is_available():
        st.success(f"Prolog activo: `{Path(prolog_engine.swipl_binary).name}`")
    else:
        st.warning("⚠️ SWI-Prolog no detectado en PATH. Instálalo con `winget install SWI-Prolog.SWI-Prolog`")

    st.divider()
    st.subheader("🔑 Clave Gemini API")
    api_key_input = st.text_input(
        "API Key (opcional si está en .env):",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password"
    )

    st.divider()
    st.subheader("📖 Base de Conocimiento (.pl)")
    kb_path = Path("knowledge/base_conocimiento.pl")
    if kb_path.exists():
        with st.expander("Ver / Editar archivo Prolog en vivo"):
            content = st.text_area("Contenido Prolog", value=kb_path.read_text(encoding="utf-8"), height=300)
            if st.button("💾 Guardar Cambios en Vivo"):
                kb_path.write_text(content, encoding="utf-8")
                st.success("¡Base de conocimiento actualizada!")
                st.rerun()

# ==============================================================================
# PANEL PRINCIPAL
# ==============================================================================
st.title("🧠 Agente Inteligente Basado en Conocimiento")
st.caption("Proyecto N°2 - Fundamentos de Inteligencia Artificial | Lógica de Primer Orden vs Modelos de Lenguaje")

# Mostrar historial de conversación
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("tipo") == "comparativa":
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 🧩 Prolog (LPO)")
                st.markdown(msg["prolog"])
            with col2:
                st.markdown("### 🤖 LLM (Gemini)")
                st.markdown(msg["llm"])
        else:
            st.markdown(msg["content"])

# Entrada del usuario
pregunta = st.chat_input("Escribe tu pregunta sobre el dominio...")

if pregunta:
    # Registrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    # Procesar según el modo
    with st.chat_message("assistant"):
        if modo == "Comparativa (Prolog vs LLM)":
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🧩 Prolog (LPO)")
                with st.spinner("Consultando motor Prolog..."):
                    resp_prolog = prolog_engine.consultar_interpretado(pregunta)
                    st.markdown(resp_prolog)

            with col2:
                st.markdown("### 🤖 LLM (Gemini)")
                with st.spinner("Consultando LLM con contexto..."):
                    resp_llm = llm_engine.responder(pregunta, api_key_override=api_key_input)
                    st.markdown(resp_llm)

            st.session_state.messages.append({
                "role": "assistant",
                "tipo": "comparativa",
                "prolog": resp_prolog,
                "llm": resp_llm
            })

        elif modo == "Solo Prolog (FOL)":
            with st.spinner("Consultando motor Prolog..."):
                resp = prolog_engine.consultar_interpretado(pregunta)
                st.markdown(resp)
                st.session_state.messages.append({"role": "assistant", "content": resp})

        elif modo == "Solo LLM":
            with st.spinner("Consultando LLM..."):
                resp = llm_engine.responder(pregunta, api_key_override=api_key_input)
                st.markdown(resp)
                st.session_state.messages.append({"role": "assistant", "content": resp})
