# Modelado del Conocimiento en Lógica de Primer Orden (FOL)

**Proyecto N°2: Diseño de un Agente Inteligente que usa conocimiento**  
**Universidad Andrés Bello - Fundamentos de Inteligencia Artificial**

---

## 1. Definición y Alcance del Dominio
El dominio modelado corresponde a las **Mecánicas de Supervivencia, Fabricación y Ecosistema de Entidades (Minecraft)**.
Se excluyen deliberadamente componentes de circuitos y compuertas lógicas (Redstone compleja) para garantizar que el dominio no esté vinculado a la informática o arquitectura computacional.

---

## 2. Elementos del Lenguaje Formal

### 2.1 Constantes
- **Ítems / Objetos:** `espada_hierro`, `pico_hierro`, `armadura_diamante`, `pocion_curacion`, `lingote_hierro`, `palo`, `tabla_madera`, `tronco_madera`, `verruga_nether`, `sandia_reluciente`, `pepita_oro`, `rodaja_sandia`, `diamante`, `madera`, `hierro`.
- **Entidades / Mobs:** `zombie`, `esqueleto`, `creeper`, `vaca`, `aldeano`.
- **Categorías:** `arma`, `herramienta`, `proteccion`, `pocion`, `mob_hostil`, `mob_pasivo`.
- **Elementos / Amenazas:** `fuego`, `luz_solar`, `lobo`, `gato`, `ocelote`.

### 2.2 Predicados
- $\text{Categoria}(x, c)$: El elemento o entidad $x$ pertenece a la categoría $c$.
- $\text{RequiereDirecto}(x, y)$: Para fabricar el elemento $x$ se requiere directamente el ingrediente $y$.
- $\text{RequiereMaterialBase}(x, y)$: El elemento $x$ depende del material básico $y$ (relación transitiva).
- $\text{DebilContra}(m, e)$: El mob o entidad $m$ es vulnerable al elemento o criatura $e$.
- $\text{Propiedad}(x, p)$: El material $x$ posee la propiedad física o mecánica $p$.
- $\text{EsPeligroNocturno}(m)$: La entidad $m$ representa una amenaza activa durante la noche.
- $\text{EsNivelAvanzado}(x)$: El objeto $x$ pertenece a la jerarquía avanzada de equipamiento.

---

## 3. Hechos en Lógica de Primer Orden

### Categorización
$$\text{Categoria}(\text{espada\_hierro}, \text{arma})$$
$$\text{Categoria}(\text{pico\_hierro}, \text{herramienta})$$
$$\text{Categoria}(\text{armadura\_diamante}, \text{proteccion})$$
$$\text{Categoria}(\text{pocion\_curacion}, \text{pocion})$$
$$\text{Categoria}(\text{zombie}, \text{mob\_hostil})$$
$$\text{Categoria}(\text{esqueleto}, \text{mob\_hostil})$$
$$\text{Categoria}(\text{creeper}, \text{mob\_hostil})$$
$$\text{Categoria}(\text{vaca}, \text{mob\_pasivo})$$
$$\text{Categoria}(\text{aldeano}, \text{mob\_pasivo})$$

### Fabricación directa
$$\text{RequiereDirecto}(\text{espada\_hierro}, \text{lingote\_hierro})$$
$$\text{RequiereDirecto}(\text{espada\_hierro}, \text{palo})$$
$$\text{RequiereDirecto}(\text{pico\_hierro}, \text{lingote\_hierro})$$
$$\text{RequiereDirecto}(\text{pico\_hierro}, \text{palo})$$
$$\text{RequiereDirecto}(\text{palo}, \text{tabla\_madera})$$
$$\text{RequiereDirecto}(\text{tabla\_madera}, \text{tronco\_madera})$$
$$\text{RequiereDirecto}(\text{pocion\_curacion}, \text{verruga\_nether})$$
$$\text{RequiereDirecto}(\text{pocion\_curacion}, \text{sandia\_reluciente})$$

### Vulnerabilidades
$$\text{DebilContra}(\text{zombie}, \text{fuego}) \land \text{DebilContra}(\text{zombie}, \text{luz\_solar})$$
$$\text{DebilContra}(\text{esqueleto}, \text{lobo}) \land \text{DebilContra}(\text{esqueleto}, \text{luz\_solar})$$
$$\text{DebilContra}(\text{creeper}, \text{gato}) \land \text{DebilContra}(\text{creeper}, \text{ocelote})$$

---

## 4. Axiomas y Reglas Deductivas (Reglas de Inferencia)

### Axioma 1: Clausura Transitiva de Materiales
$$\forall x \forall y \ (\text{RequiereDirecto}(x, y) \rightarrow \text{RequiereMaterialBase}(x, y))$$
$$\forall x \forall y \forall z \ (\text{RequiereDirecto}(x, z) \land \text{RequiereMaterialBase}(z, y) \rightarrow \text{RequiereMaterialBase}(x, y))$$

### Axioma 2: Peligro Nocturno
$$\forall m \ (\text{Categoria}(m, \text{mob\_hostil}) \rightarrow \text{EsPeligroNocturno}(m))$$

### Axioma 3: Objeto de Nivel Avanzado
$$\forall x \ (\text{RequiereMaterialBase}(x, \text{diamante}) \lor \text{RequiereMaterialBase}(x, \text{pepita\_oro}) \rightarrow \text{EsNivelAvanzado}(x))$$

### Axioma 4: Estrategia de Defensa
$$\forall m \forall e \ (\text{DebilContra}(m, e) \rightarrow \text{EstrategiaDefensa}(m, e))$$
