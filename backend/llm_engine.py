"""
Motor de integración con Modelos de Lenguaje (LLM).
Utiliza la base de conocimiento estructurada como contexto y soporte para responder preguntas.
"""

import os
from pathlib import Path
from typing import Optional


class LLMEngine:
    def __init__(self, context_path: Optional[str] = None):
        default_context = Path(__file__).resolve().parent.parent / "knowledge" / "dominio_context.txt"
        self.context_path = Path(context_path) if context_path else default_context
        self.context_text = self._load_context()
        self.api_key = os.getenv("GEMINI_API_KEY")

    def _load_context(self) -> str:
        if self.context_path.exists():
            return self.context_path.read_text(encoding="utf-8")
        return ""

    def responder(self, pregunta: str, api_key_override: Optional[str] = None) -> str:
        """
        Envía la pregunta junto con el contexto del dominio al LLM.
        """
        key = api_key_override or self.api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            return (
                "⚠️ [Aviso LLM]: No se ha configurado una clave API (GEMINI_API_KEY).\n"
                "Puedes ingresarla en la barra lateral de la interfaz o definirla en el archivo `.env`.\n\n"
                f"**Contexto disponible que usaría el LLM:**\n{self.context_text[:300]}..."
            )

        try:
            # Uso de google-generativeai / google-genai
            import google.generativeai as genai
            genai.configure(api_key=key)

            system_instruction = (
                "Eres un agente inteligente experto en el dominio de conocimiento definido a continuación. "
                "Debes responder las preguntas de forma precisa basándote principalmente en el conocimiento provisto.\n\n"
                f"--- BASE DE CONOCIMIENTO DEL DOMINIO ---\n{self.context_text}\n----------------------------------------\n"
                "Responde de forma concisa, educada y fundamentada."
            )

            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_instruction
            )

            response = model.generate_content(pregunta)
            return response.text if response.text else "El modelo no generó una respuesta."

        except Exception as e:
            return f"❌ Error al consultar el LLM: {str(e)}"
