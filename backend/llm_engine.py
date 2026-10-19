"""Motor de integración con Modelos de Lenguaje (Google GenAI / Gemini).

Utiliza la base de conocimiento estructurada como contexto aumentado (RAG ligero)
y soporta traducción neuro-simbólica de lenguaje natural a metas formales de Prolog.
Cumple estrictamente con estándares PEP 8 y PEP 257.
"""

import os
from pathlib import Path
from typing import Optional


class LLMEngine:
    """Motor de inferencia conversacional con LLMs (Google Gemini).

    Proporciona generación de respuestas fundamentadas en el dominio y traducción
    de consultas en lenguaje natural a metas ejecutables en Lógica de Primer Orden.
    """

    def __init__(self, context_path: Optional[str] = None) -> None:
        """Inicializa el motor de LLM cargando el contexto del dominio.

        Args:
            context_path: Ruta opcional al archivo de texto con el contexto del dominio.
                Por defecto utiliza 'knowledge/dominio_context.txt'.
        """
        default_context = (
            Path(__file__).resolve().parent.parent / "knowledge" / "dominio_context.txt"
        )
        self.context_path = Path(context_path) if context_path else default_context
        self.context_text = self._load_context()
        self.api_key = os.getenv("GEMINI_API_KEY")

    def _load_context(self) -> str:
        """Carga el texto de contexto del dominio desde disco.

        Returns:
            Contenido en texto plano del archivo de contexto, o cadena vacía si no existe.
        """
        if self.context_path.exists():
            return self.context_path.read_text(encoding="utf-8")
        return ""

    def responder(self, pregunta: str, api_key_override: Optional[str] = None) -> str:
        """Genera una respuesta fundamentada utilizando Gemini y el contexto del dominio.

        Args:
            pregunta: Pregunta del usuario en lenguaje natural.
            api_key_override: Clave API opcional ingresada manualmente en la interfaz.

        Returns:
            Texto de la respuesta generada por el LLM o mensaje amigable de error/configuración.
        """
        key = api_key_override or self.api_key or os.getenv("GEMINI_API_KEY")
        if not key or not key.strip():
            preview = self.context_text[:350].strip()
            return (
                "⚠️ **[Aviso LLM]: No se ha configurado una clave API (GEMINI_API_KEY).**\n\n"
                "Para activar las respuestas con Inteligencia Artificial generativa, ingresa tu API Key "
                "en la barra lateral de la interfaz o agrégala al archivo `.env`.\n\n"
                f"**Fragmento del contexto de dominio inyectado al modelo:**\n```text\n{preview}...\n```"
            )

        system_instruction = (
            "Eres un agente inteligente experto en el dominio de conocimiento definido a continuación. "
            "Debes responder las preguntas de forma precisa basándote estrictamente en el conocimiento provisto.\n\n"
            f"--- BASE DE CONOCIMIENTO DEL DOMINIO ---\n{self.context_text}\n----------------------------------------\n"
            "Instrucciones de formato:\n"
            "1. Responde de forma concisa, educada y fundamentada.\n"
            "2. Si la pregunta busca saber si algo es posible o verdadero, indica claramente Sí o No y explica la regla lógica.\n"
            "3. No inventes elementos que no existan en el contexto provisto."
        )

        # Intento 1: SDK moderno 'google.genai'
        try:
            from google import genai
            client = genai.Client(api_key=key.strip())
            prompt = f"{system_instruction}\n\nPregunta del usuario: {pregunta}"
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            if response and response.text:
                return response.text.strip()
        except Exception:
            # Fallback a SDK 'google.generativeai'
            try:
                import google.generativeai as legacy_genai
                legacy_genai.configure(api_key=key.strip())
                model = legacy_genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=system_instruction
                )
                res = model.generate_content(pregunta)
                if res and res.text:
                    return res.text.strip()
            except Exception as legacy_err:
                return (
                    f"❌ **Error al consultar el LLM:** {str(legacy_err)}\n\n"
                    "Verifica que la clave API sea válida y tenga cuota disponible en Google AI Studio."
                )

        return "El modelo no generó una respuesta estructurada."

    def traducir_a_meta_prolog(self, pregunta: str, api_key_override: Optional[str] = None) -> Optional[str]:
        """Traduce una pregunta en lenguaje natural a una meta formal de Prolog (Neuro-Simbólico).

        Args:
            pregunta: Pregunta del usuario en lenguaje natural.
            api_key_override: Clave API opcional ingresada manualmente.

        Returns:
            Cadena con la meta de Prolog sin punto final (ej. 'es_peligro_nocturno(vaca)') o None.
        """
        key = api_key_override or self.api_key or os.getenv("GEMINI_API_KEY")
        if not key or not key.strip():
            return None

        prompt = (
            "Convierte la siguiente pregunta sobre el dominio a una única meta lógica de Prolog.\n"
            "Usa únicamente los predicados del dominio: categoria(X, C), debil_contra(X, Y), "
            "requiere_directo(X, Y), requiere_material_base(X, Y), es_peligro_nocturno(X), "
            "es_no_muerto(X), propiedad(X, P), puntos_vida(X, HP), material_armadura_disponible(M).\n"
            "Devuelve ÚNICAMENTE la meta en sintaxis Prolog sin formato markdown, sin explicaciones y sin punto final.\n\n"
            f"Pregunta: {pregunta}"
        )

        try:
            from google import genai
            client = genai.Client(api_key=key.strip())
            resp = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            if resp and resp.text:
                clean_goal = resp.text.strip().rstrip(".").strip("`").strip()
                return clean_goal
        except Exception:
            pass

        return None
