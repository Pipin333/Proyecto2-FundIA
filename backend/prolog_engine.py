"""
Motor de integración con Prolog (SWI-Prolog).
Permite cargar la base de conocimiento y ejecutar consultas lógicas de primer orden.
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional


class PrologEngine:
    def __init__(self, kb_path: Optional[str] = None):
        default_kb = Path(__file__).resolve().parent.parent / "knowledge" / "base_conocimiento.pl"
        self.kb_path = Path(kb_path) if kb_path else default_kb
        self.swipl_binary = self._find_swipl_binary()

    def _find_swipl_binary(self) -> Optional[str]:
        """Detecta la ubicación del ejecutable de SWI-Prolog en el sistema."""
        binary = shutil.which("swipl")
        if binary:
            return binary

        # Rutas comunes en Windows
        candidate_paths = [
            r"C:\Program Files\swipl\bin\swipl.exe",
            r"C:\Program Files (x86)\swipl\bin\swipl.exe",
            Path.home() / "AppData" / "Local" / "Programs" / "swipl" / "bin" / "swipl.exe",
        ]
        for path in candidate_paths:
            p = Path(path)
            if p.exists():
                return str(p)
        return None

    def is_available(self) -> bool:
        """Indica si el binario de SWI-Prolog está disponible en el sistema."""
        return self.swipl_binary is not None

    def query(self, goal: str) -> Dict[str, Any]:
        """
        Ejecuta una consulta en SWI-Prolog y retorna el resultado.
        """
        if not self.is_available():
            return {
                "success": False,
                "error": "SWI-Prolog no encontrado en PATH ni en rutas estándar.",
                "goal": goal,
                "raw_output": "",
            }

        if not self.kb_path.exists():
            return {
                "success": False,
                "error": f"Base de conocimiento no encontrada en {self.kb_path}",
                "goal": goal,
                "raw_output": "",
            }

        # Envuelve la consulta para imprimir resultados en formato legible
        prolog_command = [
            self.swipl_binary,
            "-q",
            "-s", str(self.kb_path),
            "-g", f"({goal} -> halt(0) ; halt(1))"
        ]

        try:
            res = subprocess.run(
                prolog_command,
                capture_output=True,
                text=True,
                timeout=10,
                encoding="utf-8"
            )
            success = (res.returncode == 0)
            output = res.stdout.strip()
            err_output = res.stderr.strip()

            return {
                "success": success,
                "raw_output": output,
                "error": err_output if not success and err_output else None,
                "goal": goal,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Tiempo de ejecución de la consulta excedido (Timeout).",
                "goal": goal,
                "raw_output": "",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "goal": goal,
                "raw_output": "",
            }

    def consultar_interpretado(self, pregunta_nl: str) -> str:
        """
        Interpreta una pregunta en lenguaje natural y la traduce a una consulta Prolog,
        devolviendo una respuesta explicativa y lógica.
        """
        pregunta = pregunta_nl.lower().strip()

        # Mapeos de consultas frecuentes del dominio
        if "material" in pregunta or "requiere" in pregunta or "crafteo" in pregunta or "fabricar" in pregunta:
            items = ["espada_hierro", "pico_hierro", "pocion_curacion", "sandia_reluciente", "palo", "tabla_madera"]
            encontrado = next((item for item in items if item.replace("_", " ") in pregunta or item in pregunta), None)
            
            if not encontrado:
                # Intento de extraer palabra clave
                for it in items:
                    if any(part in pregunta for part in it.split("_")):
                        encontrado = it
                        break

            if encontrado:
                meta = f"listar_materiales_base({encontrado}, Lista), write('Materiales requeridos: '), writeln(Lista)"
                res = self.query(meta)
                if res["success"]:
                    return f"🧩 [Inferencia Prolog]\nPara obtener '{encontrado.replace('_', ' ').capitalize()}', la base de conocimiento deduce que se requiere:\n- {res['raw_output']}\n\nMeta ejecutada: `{meta}`"
                else:
                    return f"No se pudo inferir la cadena de materiales para '{encontrado}'. Error: {res.get('error')}"

        if "debil" in pregunta or "contra" in pregunta or "estrategia" in pregunta or "vulnerable" in pregunta:
            mobs = ["zombie", "esqueleto", "creeper"]
            mob_encontrado = next((m for m in mobs if m in pregunta), None)
            if mob_encontrado:
                meta = f"listar_debilidades({mob_encontrado}, Debilidades), write('Debilidades detectadas: '), writeln(Debilidades)"
                res = self.query(meta)
                if res["success"]:
                    return f"⚔️ [Inferencia Prolog]\nPara el mob hostil '{mob_encontrado.capitalize()}', se deduce la siguiente estrategia de defensa:\n- {res['raw_output']}\n\nMeta ejecutada: `{meta}`"
                else:
                    return f"No se encontraron debilidades registradas para '{mob_encontrado}'."

        if "peligro" in pregunta or "hostil" in pregunta or "noche" in pregunta:
            meta = "categoria(Mob, mob_hostil), write('Mob hostil identificado: '), writeln(Mob)"
            res = self.query(meta)
            if res["success"]:
                return f"🌙 [Inferencia Prolog]\nEntidades que representan peligro nocturno:\n{res['raw_output']}\n\nMeta ejecutada: `{meta}`"

        # Consulta directa en sintaxis Prolog si el usuario escribe código o meta
        if "(" in pregunta and ")" in pregunta:
            goal_clean = pregunta.rstrip(".")
            res = self.query(f"({goal_clean} -> writeln('Verdadero (True)') ; writeln('Falso (False)'))")
            if res["success"]:
                return f"🔍 [Resultado Prolog]:\n{res['raw_output']}\nMeta: `{goal_clean}`"
            else:
                return f"❌ [Fallo en consulta Prolog]: {res.get('error', 'Falso / No unifica')}"

        return (
            "🤖 [Modo Prolog]: No logré traducir la pregunta a una meta unificable.\n"
            "Prueba preguntando por:\n"
            "- ¿Qué materiales requiere la espada de hierro?\n"
            "- ¿Cuáles son las debilidades del creeper o esqueleto?\n"
            "- O escribe directamente una meta en Prolog: `categoria(creeper, mob_hostil)`"
        )
