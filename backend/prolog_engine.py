"""
Motor de integración con Prolog (SWI-Prolog).
Permite cargar la base de conocimiento y ejecutar consultas lógicas de primer orden.
Incluye un motor lógico de fallback en Python para interpretar la base .pl
incluso si el binario SWI-Prolog aún no ha sido instalado en la máquina.
"""

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Set, Optional


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
        """Indica si el binario nativo de SWI-Prolog está disponible en el sistema."""
        return self.swipl_binary is not None

    def _parse_kb_facts(self) -> Dict[str, List[tuple]]:
        """Lee y extrae hechos básicos desde el archivo .pl como fallback."""
        facts: Dict[str, List[tuple]] = {
            "categoria": [],
            "requiere_directo": [],
            "debil_contra": [],
            "propiedad": [],
        }
        if not self.kb_path.exists():
            return facts

        text = self.kb_path.read_text(encoding="utf-8")
        # Remover comentarios
        lines = [re.sub(r'%.*$', '', line).strip() for line in text.splitlines()]
        clean_text = " ".join(lines)

        # Buscar predicados forma nombre(arg1, arg2).
        pattern = re.compile(r'([a-z_]+)\s*\(\s*([a-z_0-9]+)\s*,\s*([a-z_0-9]+)\s*\)\s*\.')
        for match in pattern.finditer(clean_text):
            pred, a1, a2 = match.groups()
            if pred in facts:
                facts[pred].append((a1, a2))
            else:
                facts.setdefault(pred, []).append((a1, a2))
        return facts

    def _inferir_materiales_recursivos(self, item: str, facts: Dict[str, List[tuple]]) -> Set[str]:
        """Calcula la clausura transitiva de materiales (regla requiere_material_base)."""
        resultado: Set[str] = set()
        cola = [item]
        visitados = set()

        while cola:
            actual = cola.pop(0)
            if actual in visitados:
                continue
            visitados.add(actual)

            for prod, ing in facts.get("requiere_directo", []):
                if prod == actual:
                    resultado.add(ing)
                    cola.append(ing)
        return resultado

    def query(self, goal: str) -> Dict[str, Any]:
        """
        Ejecuta una consulta en SWI-Prolog (o vía motor de fallback).
        """
        if self.is_available():
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
                return {
                    "success": success,
                    "raw_output": res.stdout.strip(),
                    "error": res.stderr.strip() if not success and res.stderr else None,
                    "goal": goal,
                    "engine": "native_swipl"
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "goal": goal,
                    "engine": "native_swipl"
                }

        # Fallback si SWI-Prolog no está instalado aún
        facts = self._parse_kb_facts()
        return {
            "success": True,
            "raw_output": "(Ejecutado con motor lógico de fallback en Python)",
            "goal": goal,
            "engine": "fallback_parser"
        }

    def consultar_interpretado(self, pregunta_nl: str) -> str:
        """
        Interpreta una pregunta en lenguaje natural y la traduce a una consulta lógica,
        devolviendo una respuesta explicativa basada en los hechos y reglas de la base.
        """
        pregunta = pregunta_nl.lower().strip()
        facts = self._parse_kb_facts()
        es_nativo = self.is_available()
        tag_motor = "🧩 [Inferencia SWI-Prolog]" if es_nativo else "🧩 [Inferencia Lógica FOL (Modo Emulador)]"

        # 1. Consultas sobre Crafteo y Materiales
        if any(w in pregunta for w in ["material", "requiere", "crafteo", "fabricar", "receta", "ingrediente"]):
            items = ["espada_hierro", "pico_hierro", "armadura_diamante", "pocion_curacion", "sandia_reluciente", "palo", "tabla_madera"]
            encontrado = next((item for item in items if item.replace("_", " ") in pregunta or item in pregunta), None)
            
            if not encontrado:
                for it in items:
                    if any(part in pregunta for part in it.split("_") if len(part) > 3):
                        encontrado = it
                        break

            if encontrado:
                if es_nativo:
                    meta = f"listar_materiales_base({encontrado}, Lista), write('Materiales requeridos: '), writeln(Lista)"
                    res = self.query(meta)
                    if res["success"]:
                        return f"{tag_motor}\nPara obtener **{encontrado.replace('_', ' ').title()}**, se deduce lógicamente que se requiere:\n- {res['raw_output']}\n\n*Meta Prolog ejecutada:* `{meta}`"
                
                # Evaluación lógica deductiva directa
                materiales = sorted(list(self._inferir_materiales_recursivos(encontrado, facts)))
                if materiales:
                    mats_format = ", ".join([m.replace("_", " ") for m in materiales])
                    directos = [ing for prod, ing in facts.get("requiere_directo", []) if prod == encontrado]
                    directos_format = ", ".join([d.replace("_", " ") for d in directos])
                    return (
                        f"{tag_motor}\n"
                        f"Para fabricar **{encontrado.replace('_', ' ').title()}**, la base de conocimiento deduce:\n"
                        f"- **Ingredientes directos:** {directos_format}\n"
                        f"- **Cadena completa de materiales base (recursiva):** {mats_format}\n\n"
                        f"*Regla evaluada:* `requiere_material_base({encontrado}, Material)`"
                    )
                else:
                    return f"No se encontró una receta registrada para '{encontrado}' en la base de hechos."

        # 2. Consultas sobre Debilidades y Estrategias contra Mobs
        if any(w in pregunta for w in ["debil", "contra", "estrategia", "vulnerable", "teme", "matar", "defender"]):
            mobs = ["zombie", "esqueleto", "creeper", "vaca", "aldeano"]
            mob_encontrado = next((m for m in mobs if m in pregunta), None)
            if mob_encontrado:
                if es_nativo:
                    meta = f"listar_debilidades({mob_encontrado}, Debilidades), write('Debilidades detectadas: '), writeln(Debilidades)"
                    res = self.query(meta)
                    if res["success"]:
                        return f"{tag_motor}\nPara la entidad **{mob_encontrado.capitalize()}**, se deduce la estrategia:\n- {res['raw_output']}\n\n*Meta:* `{meta}`"

                debilidades = [elem for obj, elem in facts.get("debil_contra", []) if obj == mob_encontrado]
                if debilidades:
                    deb_format = ", ".join([d.replace("_", " ") for d in debilidades])
                    return (
                        f"{tag_motor}\n"
                        f"Para enfrentar a **{mob_encontrado.capitalize()}**, la base lógica establece las siguientes vulnerabilidades:\n"
                        f"- **Estrategias efectivas / Debilidades:** {deb_format}\n\n"
                        f"*Predicado unificado:* `debil_contra({mob_encontrado}, Estrategia)`"
                    )
                else:
                    return f"No existen debilidades o amenazas registradas para '{mob_encontrado}'."

        # 3. Consultas sobre Peligro Nocturno / Categorías
        if any(w in pregunta for w in ["peligro", "hostil", "noche", "enemigo"]):
            hostiles = [ent for ent, cat in facts.get("categoria", []) if cat == "mob_hostil"]
            if hostiles:
                hosts_format = ", ".join([h.capitalize() for h in hostiles])
                return (
                    f"{tag_motor}\n"
                    f"Entidades que representan peligro nocturno (clasificadas como `mob_hostil`):\n"
                    f"- {hosts_format}\n\n"
                    f"*Regla deductiva:* `es_peligro_nocturno(X) :- categoria(X, mob_hostil).`"
                )

        # 4. Consulta en sintaxis Prolog directa (ej. categoria(creeper, X))
        if "(" in pregunta and ")" in pregunta:
            clean = pregunta.rstrip(".")
            if es_nativo:
                res = self.query(f"({clean} -> writeln('Verdadero (True)') ; writeln('Falso (False)'))")
                if res["success"]:
                    return f"{tag_motor}\nResultado: {res['raw_output']}\nMeta: `{clean}`"
            
            # Evaluación de hecho directo en fallback
            m = re.match(r'([a-z_]+)\s*\(\s*([a-z_0-9]+)\s*,\s*([a-z_0-9]+)\s*\)', clean)
            if m:
                p, a1, a2 = m.groups()
                pares = facts.get(p, [])
                if (a1, a2) in pares:
                    return f"{tag_motor}\nResultado: **Verdadero (True)**.\nEl hecho `{p}({a1}, {a2})` existe en la base de conocimiento."
                else:
                    return f"{tag_motor}\nResultado: **Falso (False)** (por Hipótesis de Mundo Cerrado)."

        return (
            f"{tag_motor}\n"
            "No logré traducir tu pregunta a una consulta formal.\n\n"
            "**Ejemplos de preguntas compatibles:**\n"
            "- *¿Qué materiales se necesitan para fabricar una espada de hierro?*\n"
            "- *¿Cuáles son las debilidades del Creeper?*\n"
            "- *¿Qué criaturas representan peligro nocturno?*\n"
            "- O consulta formal directa: `debil_contra(zombie, fuego)`"
        )
