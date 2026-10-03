# Documento de Traspaso (HANDOFF.md)

**Proyecto:** Proyecto N°2 - Agente Inteligente Basado en Conocimiento (UNAB)  
**Fecha de corte:** Octubre 2026  
**Para:** Compañeros de equipo y agentes de IA (Cursor, Claude, Copilot, Antigravity, etc.)

---

## 📌 1. Estado Actual del Repositorio

El esqueleto técnico y funcional del proyecto ya está **100% implementado y probado**.

| Componente | Estado | Ubicación | Descripción |
|:---|:---:|:---|:---|
| **Base Prolog** | ✅ Listo (Plantilla) | `knowledge/base_conocimiento.pl` | Hechos de categorías, recetas, debilidades e inferencia transitiva. |
| **Contexto LLM** | ✅ Sincronizado | `knowledge/dominio_context.txt` | Contexto de soporte para inyectar en Gemini/OpenAI. |
| **Motor Prolog** | ✅ Operativo | `backend/prolog_engine.py` | Ejecuta metas de Prolog vía subprocess con captura de errores. |
| **Motor LLM** | ✅ Operativo | `backend/llm_engine.py` | Conexión con Gemini API basada en system prompting y contexto. |
| **Frontend Web** | ✅ Operativo | `app.py` | Streamlit con chat, comparativa lado a lado y editor en vivo de `.pl`. |
| **Modelado FOL** | ✅ Listo | `docs/modelado_fol.md` | Fórmulas lógicas formales (∀, ∃, →) para el informe de Entrega 1. |
| **20 Preguntas** | ✅ Diseñadas | `docs/evaluacion_20_preguntas.md` | Batería de 20 preguntas con análisis y propuestas de mejora. |

---

## 🧠 2. Decisiones de Diseño Clave
1. **Dominio Propuesto:** Mecánicas de Supervivencia y Fabricación en Minecraft.
   - **Atención:** Se omitieron circuitos lógicos de Redstone para asegurar que el profesor no catalogue el tema como "informática o arquitectura de computadores".
2. **Frontend con Streamlit:** Se eligió Streamlit porque permite tener un chat moderno, selector de modelos y editor de reglas en vivo en un solo archivo legible (`app.py`), ideal para la demo.
3. **Fácil Extensión en Vivo (Interrogación 80%):** En la barra lateral de la app se incluyó un editor de texto que permite guardar cambios en `base_conocimiento.pl` y recargar la base con un clic.

---

## 🚀 3. Tareas Pendientes / Próximos Pasos

### Inmediato (Para la Entrega 1 / Semana 10):
- [ ] **Validación en grupo:** Confirmar con el grupo si mantienen **Minecraft** o si prefieren cambiar el dominio (ej. Sommelier/Vinos o Plantas Medicinales).
  - *Si deciden cambiarlo:* Solo deben actualizar los hechos en `knowledge/base_conocimiento.pl`, el texto en `knowledge/dominio_context.txt` y los nombres en `docs/modelado_fol.md`. La arquitectura del backend y frontend se mantiene idéntica.
- [ ] **Instalar SWI-Prolog localmente:** En Windows, ejecutar:
  ```powershell
  winget install --id SWI-Prolog.SWI-Prolog -e
  ```
  O bajar el instalador de [swi-prolog.org](https://www.swi-prolog.org/) asegurando marcar "Add to PATH".
- [ ] **Entrenar la Interrogación en Vivo:** Asegurarse de que los 3 integrantes entiendan cómo agregar un hecho o regla en Prolog si el profesor lo pide en el taller (ver sección 4).

### Para la Entrega 2 (Noviembre):
- [ ] Ejecutar las 20 preguntas en la app comparativa y exportar los resultados finales al informe en PDF/Word.
- [ ] Afinar el prompt del LLM o agregar un evaluador de consistencia lógica.

---

## 💡 4. Chuleta para la Interrogación (Cómo modificar Prolog en vivo)

Si el profesor pide en la interrogación:
- **"Agreguen un nuevo mob hostil 'araña' que tema a los perros":**
  ```prolog
  categoria(arana, mob_hostil).
  debil_contra(arana, perro).
  ```
- **"Agreguen una nueva receta de flecha (requiere pedernal, palo y pluma)":**
  ```prolog
  requiere_directo(flecha, pedernal).
  requiere_directo(flecha, palo).
  requiere_directo(flecha, pluma).
  ```
*(Gracias a la regla transitiva `requiere_material_base/2`, el sistema automáticamente deducirá que la flecha también requiere tablas y troncos de madera).*
