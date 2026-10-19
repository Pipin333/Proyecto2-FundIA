"""Suite de pruebas unitarias y de regresión para PrologEngine.

Verifica la consistencia lógica de las 20 preguntas del informe académico,
la seguridad del filtro contra inyección de comandos y la clausura transitiva.
"""

import pytest
from backend.prolog_engine import PrologEngine


@pytest.fixture
def engine() -> PrologEngine:
    """Fixture que retorna una instancia fresca de PrologEngine."""
    return PrologEngine()


class TestPrologEngineSecurity:
    """Pruebas de seguridad e inmunidad contra inyección de código en Prolog."""

    @pytest.mark.parametrize("dangerous_goal", [
        "shell('calc.exe')",
        "system(ls)",
        "halt",
        "open('/etc/passwd', read, S)",
        "delete_file('knowledge/base_conocimiento.pl')",
        "process_create(path, [], [])",
        "initialization(halt)",
    ])
    def test_blocks_dangerous_predicates(self, engine: PrologEngine, dangerous_goal: str) -> None:
        """Verifica que el motor rechace y neutralice directivas maliciosas."""
        res = engine.query(dangerous_goal)
        assert res["success"] is False
        assert res["engine"] == "security_filter"
        assert "Directiva prohibida" in res.get("error", "")

    def test_rejects_empty_query(self, engine: PrologEngine) -> None:
        """Verifica que consultas vacías arrojen error controlado."""
        res = engine.query("   ")
        assert res["success"] is False
        assert "vacía" in res.get("error", "").lower()


class TestPrologEngineEvaluationQuestions:
    """Pruebas exhaustivas para la batería de 20 preguntas del informe académico."""

    PREGUNTAS = [
        ("¿Qué ingredientes requiere directamente una espada de hierro?", ["lingote", "palo"]),
        ("¿Qué materiales base necesito para fabricar un pico de hierro desde cero?", ["lingote", "hierro"]),
        ("¿Cuáles son las debilidades del Zombie?", ["luz solar", "fuego"]),
        ("¿A qué le teme el Creeper?", ["gato", "ocelote"]),
        ("¿Qué criaturas son hostiles en el juego?", ["zombie", "creeper"]),
        ("¿Es la vaca un peligro nocturno?", ["Falso"]),
        ("¿Por qué el esqueleto es vulnerable a los lobos?", ["lobo"]),
        ("¿Qué se necesita para elaborar una poción de curación?", ["sandia reluciente", "pocion rara"]),
        ("¿La armadura de diamante es considerada un objeto de nivel avanzado?", ["Verdadero"]),
        ("¿Qué propiedades tiene la madera?", ["inflamable"]),
        ("Si tengo tronco de madera y lingotes de hierro, ¿puedo fabricar una espada?", ["Verdadero"]),
        ("¿Qué mobs mueren o se queman con la luz solar?", ["zombie", "esqueleto"]),
        ("¿Qué criatura hostil no se quema con el sol de día?", ["creeper", "enderman"]),
        ("¿El aldeano requiere armas para defenderse?", ["Falso"]),
        ("¿Cómo influye el fuego contra un zombie?", ["fuego"]),
        ("¿Qué necesito para fabricar una sandía reluciente?", ["pepita oro", "rodaja sandia"]),
        ("Si combino un palo y una tabla, ¿obtengo un pico de hierro?", ["Falso"]),
        ("¿Cuáles son las herramientas disponibles en la base de datos?", ["pico", "hacha", "pala"]),
        ("¿Cuál es la estrategia recomendada para defenderse de un Creeper?", ["gato", "ocelote"]),
        ("¿Qué ocurre si agrego un mob nuevo araña que sea hostil?", ["hostil", "peligro"])
    ]

    @pytest.mark.parametrize("pregunta, expected_keywords", PREGUNTAS)
    def test_20_preguntas_evaluacion(
        self, engine: PrologEngine, pregunta: str, expected_keywords: list
    ) -> None:
        """Valida que cada una de las 20 preguntas se interprete correctamente."""
        resp = engine.consultar_interpretado(pregunta)
        assert "No logré traducir" not in resp, f"Fallo al traducir: {pregunta}"
        resp_lower = resp.lower()
        for kw in expected_keywords:
            assert kw.lower() in resp_lower, (
                f"Palabra clave '{kw}' no encontrada en respuesta para: {pregunta}\nRespuesta: {resp}"
            )


class TestPrologEngineDeductions:
    """Pruebas de deducción formal y clausura transitiva."""

    def test_transitive_materials_espada_diamante(self, engine: PrologEngine) -> None:
        """Verifica que la espada de diamante deduzca recursivamente tronco de madera."""
        facts = engine._parse_kb_facts()
        mats = engine._inferir_materiales_recursivos("espada_diamante", facts)
        assert "diamante" in mats
        assert "palo" in mats
        assert "tabla_madera" in mats
        assert "tronco_madera" in mats

    def test_direct_query_boolean(self, engine: PrologEngine) -> None:
        """Verifica evaluación de metas booleanas directas."""
        res_true = engine.query("categoria(espada_hierro, arma)")
        assert res_true["success"] is True

        res_false = engine.query("categoria(espada_hierro, armadura)")
        assert res_false["success"] is False
