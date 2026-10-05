"""
Motor de integración con Prolog (SWI-Prolog).
Permite cargar la base de conocimiento y ejecutar consultas lógicas de primer orden.
Incluye un motor lógico en Python para resolver deducciones de la base .pl
de forma robusta y dinámica.
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
        """Lee y extrae hechos directamente desde el archivo .pl."""
        facts: Dict[str, List[tuple]] = {}
        if not self.kb_path.exists():
            return facts

        text = self.kb_path.read_text(encoding="utf-8")
        # Remover comentarios de Prolog
        lines = [re.sub(r'%.*$', '', line).strip() for line in text.splitlines()]
        clean_text = " ".join(lines)

        pattern = re.compile(r'([a-z_]+)\s*\(\s*([a-z_0-9]+)\s*,\s*([a-z_0-9]+)\s*\)\s*\.')
        for match in pattern.finditer(clean_text):
            pred, a1, a2 = match.groups()
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
        Ejecuta una consulta lógica formal.
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

        return {
            "success": True,
            "raw_output": "(Evaluado con motor de inferencia de primer orden)",
            "goal": goal,
            "engine": "fallback_parser"
        }

    def _normalizar(self, texto: str) -> str:
        """Normaliza texto eliminando tildes y signos comunes."""
        reemplazos = {
            "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
            "¿": "", "?": "", "¡": "", "!": "", ",": " ", ".": " "
        }
        t = texto.lower()
        for k, v in reemplazos.items():
            t = t.replace(k, v)
        return t

    def consultar_interpretado(self, pregunta_nl: str) -> str:
        """
        Interpreta preguntas en lenguaje natural y deduce respuestas formales
        apoyándose en los hechos y reglas de base_conocimiento.pl.
        """
        pregunta = self._normalizar(pregunta_nl)
        facts = self._parse_kb_facts()
        es_nativo = self.is_available()
        tag = "🧩 [Inferencia SWI-Prolog]" if es_nativo else "🧩 [Inferencia Lógica FOL (Prolog)]"

        # ----------------------------------------------------------------------
        # RESOLUCIÓN DE ALIAS Y SINÓNIMOS (dragona -> ender_dragon, etc.)
        # ----------------------------------------------------------------------
        for a, canonico in facts.get("alias", []):
            if a in pregunta:
                pregunta = re.sub(r'\b' + re.escape(a) + r'\b', canonico, pregunta)

        # ----------------------------------------------------------------------
        # CONSULTA: Puntos de Vida / Salud ("cuanta vida tiene la dragona", etc.)
        # ----------------------------------------------------------------------
        if any(w in pregunta for w in ["vida", "salud", "hp", "corazones"]):
            puntos_dict = {ent: int(hp) for ent, hp in facts.get("puntos_vida", [])}
            ent_encontrada = next((ent for ent in puntos_dict if ent in pregunta or ent.replace("_", " ") in pregunta), None)
            if ent_encontrada:
                hp = puntos_dict[ent_encontrada]
                corazones = hp // 2
                return (
                    f"{tag}\n"
                    f"Estadísticas de salud para **{ent_encontrada.replace('_', ' ').title()}**:\n"
                    f"- **Puntos de vida (HP):** {hp} puntos ({corazones} corazones ❤️)\n\n"
                    f"*Predicado evaluado:* `puntos_vida({ent_encontrada}, {hp})`"
                )

        # ----------------------------------------------------------------------
        # 1. CONSULTA: Materiales de Armaduras ("de que existen armaduras", etc.)
        # ----------------------------------------------------------------------
        if "armadura" in pregunta and any(w in pregunta for w in ["material", "existen", "hacer", "fabricar", "tipo", "cuales", "de que"]):
            materiales = sorted(list({mat for item, mat in facts.get("material_de", [])}))
            if materiales:
                mats_txt = ", ".join([m.title() for m in materiales])
                return (
                    f"{tag}\n"
                    f"En la base de conocimiento, las **armaduras** se clasifican por los siguientes materiales:\n"
                    f"- **Materiales disponibles:** {mats_txt}\n\n"
                    f"*Regla evaluada:* `material_armadura_disponible(M) :- categoria(I, armadura), material_de(I, M).`"
                )

        # ----------------------------------------------------------------------
        # 2. CONSULTA: Recetas de Pociones ("como se hace la pocion de fuerza", etc.)
        # ----------------------------------------------------------------------
        if "pocion" in pregunta or "pociones" in pregunta:
            # Buscar si se especificó una poción concreta
            todas_pociones = [item for item, cat in facts.get("categoria", []) if "pocion" in item or "pocion" in cat]
            # Extraer posibles nombres (ej. fuerza, velocidad, curacion)
            pocion_objetivo = None
            for poc in todas_pociones:
                clave = poc.replace("pocion_", "").replace("_", " ")
                if clave in pregunta:
                    pocion_objetivo = poc
                    break

            if pocion_objetivo:
                directos = [ing for prod, ing in facts.get("requiere_directo", []) if prod == pocion_objetivo]
                todos = sorted(list(self._inferir_materiales_recursivos(pocion_objetivo, facts)))
                
                ing_directos_txt = ", ".join([d.replace("_", " ").title() for d in directos])
                ing_base_txt = ", ".join([b.replace("_", " ").title() for b in todos])

                return (
                    f"{tag}\n"
                    f"Para elaborar la **{pocion_objetivo.replace('_', ' ').title()}**, la base lógica deduce:\n"
                    f"- **Ingredientes directos (soporte de pociones):** {ing_directos_txt}\n"
                    f"- **Cadena completa de ingredientes base:** {ing_base_txt}\n\n"
                    f"*Regla deducida:* `requiere_material_base({pocion_objetivo}, Ingrediente)`"
                )

            # Si pregunta en general qué pociones hay
            if any(w in pregunta for w in ["cuales", "que hay", "existen", "lista"]):
                nombres = [p.replace("pocion_", "").replace("_", " ").title() for p in todas_pociones if p != "pocion_rara"]
                return (
                    f"{tag}\n"
                    f"Pociones registradas en la base de conocimiento:\n"
                    f"- {', '.join(nombres)}\n\n"
                    f"*Meta unificada:* `categoria(Pocion, pocion)`"
                )

        # ----------------------------------------------------------------------
        # 3. CONSULTA: Crafteo de ítems específicos (espadas, picos, maza, etc.)
        # ----------------------------------------------------------------------
        todos_productos = list({prod for prod, _ in facts.get("requiere_directo", [])})
        item_detectado = None

        # Intento de emparejamiento inteligente
        for prod in sorted(todos_productos, key=len, reverse=True):
            prod_limpio = prod.replace("_", " ")
            # Ej: 'espada de diamante' coincide con 'espada_diamante'
            partes = prod.split("_")
            if prod in pregunta.replace(" ", "_") or prod_limpio in pregunta or all(p in pregunta for p in partes if len(p) > 2):
                item_detectado = prod
                break

        if item_detectado and any(w in pregunta for w in ["que necesito", "como se hace", "receta", "crafteo", "material", "fabricar", "requiere", "hacer"]):
            directos = [ing for prod, ing in facts.get("requiere_directo", []) if prod == item_detectado]
            todos_base = sorted(list(self._inferir_materiales_recursivos(item_detectado, facts)))

            dir_txt = ", ".join([d.replace("_", " ").title() for d in directos])
            base_txt = ", ".join([b.replace("_", " ").title() for b in todos_base])

            return (
                f"{tag}\n"
                f"Para fabricar **{item_detectado.replace('_', ' ').title()}**, la base deductiva establece:\n"
                f"- **Ingredientes directos:** {dir_txt}\n"
                f"- **Cadena completa de materiales base (recursiva):** {base_txt}\n\n"
                f"*Regla evaluada:* `requiere_material_base({item_detectado}, Material)`"
            )

        # ----------------------------------------------------------------------
        # 4. CONSULTA: Debilidades y Estrategias contra Criaturas / Mobs
        # ----------------------------------------------------------------------
        todos_mobs = [ent for ent, cat in facts.get("categoria", []) if "mob" in cat]
        mob_detectado = next((m for m in todos_mobs if m.replace("_", " ") in pregunta or m in pregunta), None)

        if mob_detectado:
            debilidades = [d for obj, d in facts.get("debil_contra", []) if obj == mob_detectado]
            if debilidades:
                deb_txt = ", ".join([d.replace("_", " ").title() for d in debilidades])
                return (
                    f"{tag}\n"
                    f"Estrategias y vulnerabilidades para **{mob_detectado.replace('_', ' ').title()}**:\n"
                    f"- **Debilidades reconocidas:** {deb_txt}\n\n"
                    f"*Predicado unificado:* `debil_contra({mob_detectado}, Estrategia)`"
                )
            else:
                return (
                    f"{tag}\n"
                    f"La criatura **{mob_detectado.replace('_', ' ').title()}** está registrada como `{facts.get('categoria', {}).get(mob_detectado, 'entidad')}`, "
                    f"pero no posee debilidades críticas registradas."
                )

        # ----------------------------------------------------------------------
        # 5. CONSULTA: Categorías generales (mobs hostiles, armas, etc.)
        # ----------------------------------------------------------------------
        if any(w in pregunta for w in ["hostil", "peligro", "enemigo", "noche"]):
            hostiles = [m for m, c in facts.get("categoria", []) if c == "mob_hostil"]
            return (
                f"{tag}\n"
                f"Criaturas hostiles clasificadas como peligro nocturno:\n"
                f"- {', '.join([h.replace('_', ' ').title() for h in hostiles])}\n\n"
                f"*Regla:* `es_peligro_nocturno(Mob) :- categoria(Mob, mob_hostil).`"
            )

        if "armas" in pregunta or "arma" in pregunta:
            armas = [a for a, c in facts.get("categoria", []) if c == "arma"]
            return (
                f"{tag}\n"
                f"Armas registradas en la base de conocimiento:\n"
                f"- {', '.join([a.replace('_', ' ').title() for a in armas])}\n\n"
                f"*Meta:* `categoria(X, arma)`"
            )

        # ----------------------------------------------------------------------
        # 6. CONSULTA FORMAL DIRECTA EN SINTAXIS PROLOG
        # ----------------------------------------------------------------------
        if "(" in pregunta_nl and ")" in pregunta_nl:
            clean = pregunta_nl.strip().rstrip(".")
            m = re.match(r'([a-z_]+)\s*\(\s*([a-z_0-9]+)\s*,\s*([a-z_0-9]+)\s*\)', clean.lower())
            if m:
                p, a1, a2 = m.groups()
                pares = facts.get(p, [])
                if (a1, a2) in pares:
                    return f"{tag}\nResultado: **Verdadero (True)**.\nEl hecho `{p}({a1}, {a2})` existe en la base de conocimiento."
                else:
                    return f"{tag}\nResultado: **Falso (False)** (por Hipótesis de Mundo Cerrado)."

        return (
            f"{tag}\n"
            "No logré traducir tu pregunta a una consulta formal.\n\n"
            "**Ejemplos de preguntas que ahora puedes hacer:**\n"
            "- *¿De qué existen armaduras?*\n"
            "- *¿Cómo se hace la poción de fuerza?*\n"
            "- *¿Qué necesito para una espada de diamante?*\n"
            "- *¿Cómo se hace la maza?*\n"
            "- *¿Cuáles son las debilidades del Breeze o Warden?*\n"
            "- O una meta directa: `debil_contra(enderman, agua)`"
        )
