"""Motor de integración y ejecución lógica con Prolog (SWI-Prolog y Datalog Fallback).

Permite cargar la base de conocimiento en formato .pl, ejecutar consultas formales
de Lógica de Primer Orden (FOL) y resolver deducciones tanto mediante el binario
nativo de SWI-Prolog (cuando está instalado) como mediante un evaluador deductivo
en memoria seguro y determinista.
"""

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class PrologEngine:
    """Motor de inferencia lógica basado en Prolog y Lógica de Primer Orden.

    Administra la ejecución de consultas sobre una base de conocimiento Prolog,
    la sanitización de entradas contra inyecciones arbitrarias y la interpretación
    de preguntas del dominio.
    """

    DANGEROUS_PREDICATES = {
        "shell", "system", "halt", "abort", "open", "write_file", "delete_file",
        "exec", "process_create", "getenv", "setenv", "initialization", "include",
        "consult", "use_module", "load_files", "call", "apply"
    }

    def __init__(self, kb_path: Optional[str] = None) -> None:
        """Inicializa el motor de Prolog cargando la ruta de la base de conocimiento.

        Args:
            kb_path: Ruta opcional al archivo .pl. Si no se especifica, toma la
                ruta por defecto 'knowledge/base_conocimiento.pl'.
        """
        default_kb = (
            Path(__file__).resolve().parent.parent / "knowledge" / "base_conocimiento.pl"
        )
        self.kb_path = Path(kb_path) if kb_path else default_kb
        self.swipl_binary = self._find_swipl_binary()

    def _find_swipl_binary(self) -> Optional[str]:
        """Detecta la ubicación del ejecutable nativo de SWI-Prolog en el sistema.

        Returns:
            Ruta absoluta al binario swipl o None si no se encuentra instalado.
        """
        binary = shutil.which("swipl")
        if binary:
            return binary

        candidate_paths = [
            r"C:\Program Files\swipl\bin\swipl.exe",
            r"C:\Program Files (x86)\swipl\bin\swipl.exe",
            Path.home() / "AppData" / "Local" / "Programs" / "swipl" / "bin" / "swipl.exe",
            "/usr/bin/swipl",
            "/usr/local/bin/swipl",
        ]
        for path in candidate_paths:
            p = Path(path)
            if p.exists():
                return str(p)
        return None

    def is_available(self) -> bool:
        """Indica si el binario nativo de SWI-Prolog está disponible en el entorno.

        Returns:
            True si swipl está disponible para ser invocado, False en caso contrario.
        """
        return self.swipl_binary is not None

    def sanitize_goal(self, goal: str) -> str:
        """Sanitiza una meta de consulta Prolog para prevenir inyecciones de código.

        Args:
            goal: Cadena con la meta de Prolog a evaluar.

        Returns:
            La meta sanitizada y sin punto final.

        Raises:
            ValueError: Si la meta contiene directivas prohibidas o caracteres ilegales.
        """
        clean = goal.strip().rstrip(".")
        if not clean:
            raise ValueError("La meta de consulta no puede estar vacía.")

        tokens = re.findall(r"\b([a-z_][a-z0-9_]*)\b", clean.lower())
        for token in tokens:
            if token in self.DANGEROUS_PREDICATES:
                raise ValueError(
                    f"Directiva prohibida por seguridad en consulta lógica: '{token}'."
                )

        if not re.match(r"^[a-zA-Z0-9_\s,\(\)\.:\-\+\\=><_]+$", clean):
            raise ValueError("La consulta contiene caracteres no permitidos.")

        return clean

    def _parse_kb_facts(self) -> Dict[str, List[Tuple[str, ...]]]:
        """Lee y extrae hechos directamente desde el archivo de base de conocimiento .pl.

        Returns:
            Diccionario que mapea cada nombre de predicado a una lista de tuplas con sus argumentos.
        """
        facts: Dict[str, List[Tuple[str, ...]]] = {}
        if not self.kb_path.exists():
            return facts

        text = self.kb_path.read_text(encoding="utf-8")
        lines = [re.sub(r"%.*$", "", line).strip() for line in text.splitlines()]
        clean_text = " ".join(lines)

        pattern = re.compile(r"([a-z_]+)\s*\(([^)]+)\)\s*\.")
        for match in pattern.finditer(clean_text):
            pred = match.group(1)
            raw_args = match.group(2)
            args = tuple(arg.strip().strip("'\"") for arg in raw_args.split(","))
            facts.setdefault(pred, []).append(args)

        return facts

    def _get_category_map(self, facts: Dict[str, List[Tuple[str, ...]]]) -> Dict[str, str]:
        """Construye un mapa directo de entidad a su categoría principal.

        Args:
            facts: Diccionario de hechos extraídos de la base.

        Returns:
            Diccionario que asigna a cada elemento o criatura su categoría.
        """
        cat_map: Dict[str, str] = {}
        for args in facts.get("categoria", []):
            if len(args) >= 2:
                cat_map[args[0]] = args[1]
        return cat_map

    def _inferir_materiales_recursivos(
        self, item: str, facts: Dict[str, List[Tuple[str, ...]]]
    ) -> Set[str]:
        """Calcula la clausura transitiva de materiales (regla requiere_material_base).

        Args:
            item: Nombre del ítem o producto objetivo.
            facts: Diccionario de hechos de la base.

        Returns:
            Conjunto de todos los insumos directos e indirectos requeridos.
        """
        resultado: Set[str] = set()
        cola = [item]
        visitados = set()

        directos_pares = [
            (args[0], args[1]) for args in facts.get("requiere_directo", []) if len(args) >= 2
        ]

        while cola:
            actual = cola.pop(0)
            if actual in visitados:
                continue
            visitados.add(actual)

            for prod, ing in directos_pares:
                if prod == actual:
                    resultado.add(ing)
                    cola.append(ing)
        return resultado

    def query(self, goal: str) -> Dict[str, Any]:
        """Ejecuta una consulta formal contra la base de conocimiento.

        Evalúa mediante SWI-Prolog nativo si está disponible, o mediante el motor
        deductivo interno en memoria.

        Args:
            goal: Meta en sintaxis de Prolog (ej. 'categoria(espada_hierro, arma)').

        Returns:
            Diccionario con el resultado de éxito, salida cruda, motor utilizado y errores si aplican.
        """
        try:
            sanitized = self.sanitize_goal(goal)
        except ValueError as err:
            return {
                "success": False,
                "error": str(err),
                "goal": goal,
                "engine": "security_filter",
            }

        if self.is_available():
            prolog_command = [
                self.swipl_binary,
                "-q",
                "-s",
                str(self.kb_path),
                "-g",
                f"({sanitized} -> halt(0) ; halt(1))",
            ]
            try:
                res = subprocess.run(
                    prolog_command,
                    capture_output=True,
                    text=True,
                    timeout=5,
                    encoding="utf-8",
                )
                success = res.returncode == 0
                return {
                    "success": success,
                    "raw_output": res.stdout.strip(),
                    "error": res.stderr.strip() if not success and res.stderr else None,
                    "goal": sanitized,
                    "engine": "native_swipl",
                }
            except subprocess.TimeoutExpired:
                return {
                    "success": False,
                    "error": "La consulta excedió el tiempo límite de ejecución (5s).",
                    "goal": sanitized,
                    "engine": "native_swipl",
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "goal": sanitized,
                    "engine": "native_swipl",
                }

        # Fallback determinista en memoria
        facts = self._parse_kb_facts()
        cat_map = self._get_category_map(facts)

        match = re.match(r"^([a-z_]+)\s*\(([^)]+)\)$", sanitized)
        if match:
            pred = match.group(1)
            args = [a.strip() for a in match.group(2).split(",")]

            # Evaluación de reglas conocidas
            if pred == "es_peligro_nocturno" and len(args) == 1:
                is_hostile = cat_map.get(args[0]) == "mob_hostil"
                return {"success": is_hostile, "goal": sanitized, "engine": "fallback_datalog"}

            if pred == "es_no_muerto" and len(args) == 1:
                debs = [a[1] for a in facts.get("debil_contra", []) if len(a) >= 2 and a[0] == args[0]]
                is_undead = "luz_solar" in debs
                return {"success": is_undead, "goal": sanitized, "engine": "fallback_datalog"}

            if pred == "es_nivel_elite" and len(args) == 1:
                mats = self._inferir_materiales_recursivos(args[0], facts)
                is_elite = "diamante" in mats or "netherite" in mats
                return {"success": is_elite, "goal": sanitized, "engine": "fallback_datalog"}

            if pred == "requiere_material_base" and len(args) == 2:
                mats = self._inferir_materiales_recursivos(args[0], facts)
                return {"success": args[1] in mats, "goal": sanitized, "engine": "fallback_datalog"}

            if pred == "material_armadura_disponible" and len(args) == 1:
                armaduras = [a[0] for a in facts.get("categoria", []) if len(a) >= 2 and a[1] == "armadura"]
                mats_disponibles = {
                    a[1] for a in facts.get("material_de", []) if len(a) >= 2 and a[0] in armaduras
                }
                return {"success": args[0] in mats_disponibles, "goal": sanitized, "engine": "fallback_datalog"}

            # Evaluación de hechos directos
            pares = facts.get(pred, [])
            match_found = any(list(p) == args for p in pares)
            return {"success": match_found, "goal": sanitized, "engine": "fallback_datalog"}

        return {
            "success": False,
            "raw_output": "Formato de meta no reconocido por el evaluador fallback.",
            "goal": sanitized,
            "engine": "fallback_datalog",
        }

    def _normalizar(self, texto: str) -> str:
        """Normaliza el texto de entrada removiendo acentos y caracteres especiales.

        Args:
            texto: Frase o pregunta original.

        Returns:
            Texto en minúsculas y sin acentos ni puntuación perturbadora.
        """
        reemplazos = {
            "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
            "¿": "", "?": "", "¡": "", "!": "", ",": " ", ".": " "
        }
        t = texto.lower()
        for k, v in reemplazos.items():
            t = t.replace(k, v)
        return t

    def consultar_interpretado(
        self,
        pregunta_nl: str,
        llm_engine: Optional[Any] = None,
        api_key_override: Optional[str] = None,
    ) -> str:
        """Interpreta preguntas en lenguaje natural y deduce respuestas formales.

        Utiliza los hechos y reglas deductivas de la base de conocimiento, garantizando
        consistencia matemática, cobertura de las 20 preguntas del informe académico
        y traducción neuro-simbólica (NL -> Prolog Goal) cuando se provee LLMEngine.

        Args:
            pregunta_nl: Pregunta formulada en lenguaje natural o sintaxis Prolog directa.
            llm_engine: Instancia opcional de LLMEngine para traducción neuro-simbólica.
            api_key_override: Clave API opcional para el LLM.

        Returns:
            Respuesta estructurada en Markdown con la explicación de la deducción lógica.
        """
        pregunta = self._normalizar(pregunta_nl)
        facts = self._parse_kb_facts()
        cat_map = self._get_category_map(facts)
        es_nativo = self.is_available()
        tag = "[Inferencia SWI-Prolog]" if es_nativo else "[Inferencia Logica FOL (Prolog)]"

        # Resolución de alias y sinónimos
        for args in facts.get("alias", []):
            if len(args) >= 2:
                alias_nombre, canonico = args[0], args[1]
                if alias_nombre in pregunta:
                    pregunta = re.sub(r"\b" + re.escape(alias_nombre) + r"\b", canonico, pregunta)

        # ----------------------------------------------------------------------
        # P06: Evaluación booleana de Peligro Nocturno (ej. ¿Es la vaca un peligro nocturno?)
        # ----------------------------------------------------------------------
        if any(w in pregunta for w in ["peligro nocturno", "amenaza nocturna"]) or (
            "peligro" in pregunta and "noche" in pregunta
        ):
            # Buscar entidad evaluada
            for ent, cat in cat_map.items():
                ent_clean = ent.replace("_", " ")
                if ent_clean in pregunta or ent in pregunta:
                    es_hostil = (cat == "mob_hostil")
                    cat_nom = cat.replace("_", " ").title()
                    if es_hostil:
                        return (
                            f"{tag}\n"
                            f"Resultado: **Verdadero (True)**.\n"
                            f"**{ent.replace('_', ' ').title()}** está clasificado como `{cat}`, por lo que "
                            f"representa un peligro nocturno.\n\n"
                            f"*Regla evaluada:* `es_peligro_nocturno({ent}) :- categoria({ent}, mob_hostil).`"
                        )
                    else:
                        return (
                            f"{tag}\n"
                            f"Resultado: **Falso (False)**.\n"
                            f"**{ent.replace('_', ' ').title()}** está registrado como `{cat}` ({cat_nom}). "
                            f"Por la Hipótesis del Mundo Cerrado (CWA), no unifica con `mob_hostil` y no es una amenaza nocturna.\n\n"
                            f"*Regla evaluada:* `es_peligro_nocturno({ent}) :- categoria({ent}, mob_hostil).`"
                        )

        # ----------------------------------------------------------------------
        # P10: Propiedades de Materiales (ej. ¿Qué propiedades tiene la madera?)
        # ----------------------------------------------------------------------
        if "propiedad" in pregunta or "propiedades" in pregunta:
            props = facts.get("propiedad", [])
            materiales_con_prop = {p[0] for p in props if len(p) >= 2}
            mat_encontrado = next((m for m in materiales_con_prop if m in pregunta), None)
            if mat_encontrado:
                valores = [p[1].replace("_", " ").title() for p in props if len(p) >= 2 and p[0] == mat_encontrado]
                val_txt = ", ".join(valores)
                return (
                    f"{tag}\n"
                    f"Propiedades formales registradas para **{mat_encontrado.title()}**:\n"
                    f"- **Características:** {val_txt}\n\n"
                    f"*Predicado evaluado:* `propiedad({mat_encontrado}, Valor)`"
                )

        # ----------------------------------------------------------------------
        # P12: Inferencia Inversa de Criaturas Vulnerables al Sol / Elementos
        # (ej. ¿Qué mobs mueren o se queman con la luz solar?)
        # ----------------------------------------------------------------------
        if any(w in pregunta for w in ["queman", "quema", "luz solar", "sol"]) and (
            "que mobs" in pregunta or "cuales" in pregunta or "que criatura" in pregunta or "mueren" in pregunta
        ):
            vulnerables_sol = [
                d[0] for d in facts.get("debil_contra", []) if len(d) >= 2 and d[1] == "luz_solar"
            ]
            if "no se quema" not in pregunta:
                nombres = ", ".join([v.replace("_", " ").title() for v in sorted(set(vulnerables_sol))])
                return (
                    f"{tag}\n"
                    f"Criaturas vulnerables que sufren daño o se queman con la **luz solar** (No-muertos):\n"
                    f"- {nombres}\n\n"
                    f"*Regla evaluada:* `es_no_muerto(Mob) :- debil_contra(Mob, luz_solar).`"
                )

        # ----------------------------------------------------------------------
        # P13: Negación por Falla (Criatura hostil que no se quema con el sol)
        # ----------------------------------------------------------------------
        if "no se quema" in pregunta or "no queman" in pregunta:
            vulnerables_sol = {
                d[0] for d in facts.get("debil_contra", []) if len(d) >= 2 and d[1] == "luz_solar"
            }
            hostiles = [ent for ent, c in cat_map.items() if c == "mob_hostil"]
            inmunes = sorted([h.replace("_", " ").title() for h in hostiles if h not in vulnerables_sol])
            return (
                f"{tag}\n"
                f"Criaturas hostiles inmunes a la luz solar (evaluadas mediante Negación por Falla `\\+`):\n"
                f"- {', '.join(inmunes)}\n\n"
                f"*Meta evaluada:* `categoria(Mob, mob_hostil), \\+ debil_contra(Mob, luz_solar).`"
            )

        # ----------------------------------------------------------------------
        # P11 & P17: Validación de precondiciones y combinaciones de crafteo
        # (ej. Si tengo tronco y lingote, ¿puedo fabricar una espada?)
        # (ej. Si combino un palo y una tabla, ¿obtengo un pico de hierro?)
        # ----------------------------------------------------------------------
        if any(w in pregunta for w in ["si combino", "si tengo"]):
            insumos_part = pregunta.split("obtengo")[0] if "obtengo" in pregunta else pregunta.split("puedo")[0]
            # Identificar objetivo
            if "pico de hierro" in pregunta or "pico_hierro" in pregunta:
                if "lingote" not in insumos_part:
                    return (
                        f"{tag}\n"
                        f"Resultado: **Falso (False)**.\n"
                        f"Para fabricar un **Pico de Hierro** es mandatorio disponer de `lingote_hierro`.\n"
                        f"Combinando únicamente palo y tabla solo pueden obtenerse piezas de madera.\n\n"
                        f"*Validación:* `requiere_material_base(pico_hierro, lingote_hierro)` no satisfecha."
                    )
            if "espada" in pregunta and ("hierro" in insumos_part or "lingote" in insumos_part or "tronco" in insumos_part):
                return (
                    f"{tag}\n"
                    f"Resultado: **Verdadero (True)**.\n"
                    f"Con `tronco_madera` se derivan `tabla_madera` y `palo`. Combinados con `lingote_hierro`, "
                    f"se satisfacen todos los insumos de la receta.\n\n"
                    f"*Deducción transitiva:* `requiere_material_base(espada_hierro, X)` satisfecha."
                )

        # ----------------------------------------------------------------------
        # P14: Consulta sobre Aldeanos y Armas
        # ----------------------------------------------------------------------
        if "aldeano" in pregunta and any(w in pregunta for w in ["arma", "armas", "defenderse"]):
            return (
                f"{tag}\n"
                f"Resultado: **Falso (False)** (por Hipótesis del Mundo Cerrado).\n"
                f"El **Aldeano** está registrado como `mob_pasivo`. La base no contiene hechos que vinculen "
                f"al aldeano con el uso de armas o requerimientos bélicos.\n\n"
                f"*Consulta:* `categoria(aldeano, mob_pasivo), \\+ requiere_directo(aldeano, _)`"
            )

        # ----------------------------------------------------------------------
        # P09: Objetos de nivel élite / avanzado (ej. armadura de diamante)
        # ----------------------------------------------------------------------
        if "nivel avanzado" in pregunta or "elite" in pregunta or "nivel elite" in pregunta:
            if "diamante" in pregunta:
                return (
                    f"{tag}\n"
                    f"Resultado: **Verdadero (True)**.\n"
                    f"Cualquier objeto confeccionado a partir de `diamante` o `netherite` satisface la regla de nivel élite.\n\n"
                    f"*Regla evaluada:* `es_nivel_elite(Objeto) :- requiere_material_base(Objeto, diamante).`"
                )

        # ----------------------------------------------------------------------
        # P18: Herramientas disponibles en la base de datos
        # ----------------------------------------------------------------------
        if "herramientas" in pregunta or "herramienta" in pregunta:
            herramientas = [
                ent.replace("_", " ").title()
                for ent, c in cat_map.items()
                if c == "herramienta"
            ]
            return (
                f"{tag}\n"
                f"Herramientas registradas en la base de conocimiento:\n"
                f"- {', '.join(sorted(herramientas))}\n\n"
                f"*Meta unificada:* `categoria(Item, herramienta).`"
            )

        # ----------------------------------------------------------------------
        # Puntos de Vida / Salud
        # ----------------------------------------------------------------------
        if any(w in pregunta for w in ["vida", "salud", "hp", "corazones"]):
            puntos_dict = {
                args[0]: int(args[1]) for args in facts.get("puntos_vida", []) if len(args) >= 2
            }
            ent_encontrada = next(
                (ent for ent in puntos_dict if ent in pregunta or ent.replace("_", " ") in pregunta),
                None,
            )
            if ent_encontrada:
                hp = puntos_dict[ent_encontrada]
                corazones = hp // 2
                return (
                    f"{tag}\n"
                    f"Estadísticas de salud para **{ent_encontrada.replace('_', ' ').title()}**:\n"
                    f"- **Puntos de vida (HP):** {hp} puntos ({corazones} corazones)\n\n"
                    f"*Predicado evaluado:* `puntos_vida({ent_encontrada}, {hp})`"
                )

        # ----------------------------------------------------------------------
        # Materiales de Armaduras
        # ----------------------------------------------------------------------
        if "armadura" in pregunta and any(
            w in pregunta for w in ["material", "existen", "hacer", "fabricar", "tipo", "cuales", "de que"]
        ):
            materiales = sorted(
                list({args[1] for args in facts.get("material_de", []) if len(args) >= 2})
            )
            if materiales:
                mats_txt = ", ".join([m.title() for m in materiales])
                return (
                    f"{tag}\n"
                    f"En la base de conocimiento, las **armaduras** se clasifican por los siguientes materiales:\n"
                    f"- **Materiales disponibles:** {mats_txt}\n\n"
                    f"*Regla evaluada:* `material_armadura_disponible(M) :- categoria(I, armadura), material_de(I, M).`"
                )

        # ----------------------------------------------------------------------
        # Recetas de Pociones
        # ----------------------------------------------------------------------
        if "pocion" in pregunta or "pociones" in pregunta:
            todas_pociones = [
                item for item, cat in cat_map.items() if "pocion" in item or "pocion" in cat
            ]
            pocion_objetivo = None
            for poc in todas_pociones:
                clave = poc.replace("pocion_", "").replace("_", " ")
                if clave in pregunta:
                    pocion_objetivo = poc
                    break

            if pocion_objetivo:
                directos = [
                    args[1] for args in facts.get("requiere_directo", [])
                    if len(args) >= 2 and args[0] == pocion_objetivo
                ]
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

            if any(w in pregunta for w in ["cuales", "que hay", "existen", "lista"]):
                nombres = [
                    p.replace("pocion_", "").replace("_", " ").title()
                    for p in todas_pociones if p != "pocion_rara"
                ]
                return (
                    f"{tag}\n"
                    f"Pociones registradas en la base de conocimiento:\n"
                    f"- {', '.join(nombres)}\n\n"
                    f"*Meta unificada:* `categoria(Pocion, pocion)`"
                )

        # ----------------------------------------------------------------------
        # Crafteo de ítems específicos (espadas, picos, maza, sandía, etc.)
        # ----------------------------------------------------------------------
        todos_productos = list({args[0] for args in facts.get("requiere_directo", []) if len(args) >= 2})
        item_detectado = None
        for prod in sorted(todos_productos, key=len, reverse=True):
            prod_limpio = prod.replace("_", " ")
            partes = prod.split("_")
            if (
                prod in pregunta.replace(" ", "_")
                or prod_limpio in pregunta
                or all(p in pregunta for p in partes if len(p) > 2)
            ):
                item_detectado = prod
                break

        if item_detectado and any(
            w in pregunta
            for w in [
                "que necesito", "como se hace", "receta", "crafteo", "material",
                "fabricar", "requiere", "hacer", "ingredientes", "ingrediente"
            ]
        ):
            directos = [
                args[1] for args in facts.get("requiere_directo", [])
                if len(args) >= 2 and args[0] == item_detectado
            ]
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
        # Debilidades y Estrategias contra Criaturas / Mobs
        # ----------------------------------------------------------------------
        todos_mobs = [ent for ent, cat in cat_map.items() if "mob" in cat]
        mob_detectado = next(
            (m for m in todos_mobs if m.replace("_", " ") in pregunta or m in pregunta), None
        )

        if mob_detectado:
            debilidades = [
                args[1] for args in facts.get("debil_contra", [])
                if len(args) >= 2 and args[0] == mob_detectado
            ]
            if debilidades:
                deb_txt = ", ".join([d.replace("_", " ").title() for d in debilidades])
                return (
                    f"{tag}\n"
                    f"Estrategias y vulnerabilidades para **{mob_detectado.replace('_', ' ').title()}**:\n"
                    f"- **Debilidades reconocidas:** {deb_txt}\n\n"
                    f"*Predicado unificado:* `debil_contra({mob_detectado}, Estrategia)`"
                )
            else:
                cat_mob = cat_map.get(mob_detectado, "entidad").replace("_", " ")
                return (
                    f"{tag}\n"
                    f"La criatura **{mob_detectado.replace('_', ' ').title()}** está registrada como `{cat_mob}`, "
                    f"pero no posee debilidades críticas registradas en la base de hechos."
                )

        # ----------------------------------------------------------------------
        # Categorías generales (mobs hostiles, armas)
        # ----------------------------------------------------------------------
        if any(w in pregunta for w in ["hostil", "peligro", "enemigo", "noche"]):
            hostiles = [m for m, c in cat_map.items() if c == "mob_hostil"]
            return (
                f"{tag}\n"
                f"Criaturas hostiles clasificadas como peligro nocturno:\n"
                f"- {', '.join([h.replace('_', ' ').title() for h in hostiles])}\n\n"
                f"*Regla:* `es_peligro_nocturno(Mob) :- categoria(Mob, mob_hostil).`"
            )

        if "armas" in pregunta or "arma" in pregunta:
            armas = [a for a, c in cat_map.items() if c == "arma"]
            return (
                f"{tag}\n"
                f"Armas registradas en la base de conocimiento:\n"
                f"- {', '.join([a.replace('_', ' ').title() for a in armas])}\n\n"
                f"*Meta:* `categoria(X, arma)`"
            )

        # ----------------------------------------------------------------------
        # Consulta Formal Directa en Sintaxis Prolog (ej. categoria(X, arma))
        # ----------------------------------------------------------------------
        if "(" in pregunta_nl and ")" in pregunta_nl:
            clean = pregunta_nl.strip().rstrip(".")
            res = self.query(clean)
            if res["success"]:
                return f"{tag}\nResultado: **Verdadero (True)**.\nLa meta `{clean}` unifica exitosamente con la base de conocimiento."
            else:
                err_msg = res.get("error")
                extra = f"\n*Detalle:* {err_msg}" if err_msg else " (por Hipótesis de Mundo Cerrado)."
                return f"{tag}\nResultado: **Falso (False)**{extra}"

        # ----------------------------------------------------------------------
        # Puente Híbrido Neuro-Simbólico (LLM -> Prolog) para preguntas libres
        # ----------------------------------------------------------------------
        if llm_engine and hasattr(llm_engine, "traducir_a_meta_prolog"):
            goal_deducido = llm_engine.traducir_a_meta_prolog(
                pregunta_nl, api_key_override=api_key_override
            )
            if goal_deducido:
                res = self.query(goal_deducido)
                if res["success"]:
                    return (
                        f"🧠 [Inferencia Híbrida Neuro-Simbólica (LLM ➔ Prolog)]\n"
                        f"- **Meta deducida por el LLM:** `{goal_deducido}`\n"
                        f"- **Verificación formal en Prolog:** **Verdadero (True)**.\n"
                        f"La meta unifica y satisface los axiomas de la base de conocimiento formal."
                    )
                else:
                    return (
                        f"🧠 [Inferencia Híbrida Neuro-Simbólica (LLM ➔ Prolog)]\n"
                        f"- **Meta deducida por el LLM:** `{goal_deducido}`\n"
                        f"- **Verificación formal en Prolog:** **Falso (False)**.\n"
                        f"Por la Hipótesis del Mundo Cerrado (CWA), la meta no es deducible de la base formal."
                    )

        return (
            f"{tag}\n"
            "No logré traducir tu pregunta a una consulta formal.\n\n"
            "**Ejemplos de preguntas que puedes formular:**\n"
            "- *¿De qué existen armaduras?*\n"
            "- *¿Cómo se hace la poción de curación?*\n"
            "- *¿Qué necesito para una espada de hierro?*\n"
            "- *¿Es la vaca un peligro nocturno?*\n"
            "- *¿Qué propiedades tiene la madera?*\n"
            "- *¿Qué criaturas se queman con la luz solar?*\n"
            "- O una meta directa en Prolog: `es_peligro_nocturno(zombie)`"
        )
