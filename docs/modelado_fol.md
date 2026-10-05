# Modelado del Conocimiento en Lógica de Primer Orden (FOL)

**Proyecto N°2: Diseño de un Agente Inteligente que usa conocimiento**  
**Universidad Andrés Bello - Fundamentos de Inteligencia Artificial**

---

## 1. Definición y Alcance del Dominio
El dominio modelado corresponde a las **Mecánicas de Supervivencia, Fabricación y Ecosistema de Entidades (Minecraft Java)**.
Se excluyen deliberadamente componentes de circuitos y compuertas lógicas (Redstone compleja) para garantizar que el dominio no esté vinculado a la informática o arquitectura computacional.

---

## 2. Elementos del Lenguaje Formal

### 2.1 Constantes
- **Materiales:** `madera`, `piedra`, `cuero`, `cobre`, `hierro`, `oro`, `diamante`, `netherite`.
- **Armas y Herramientas:** `espada_madera`, `espada_piedra`, `espada_cobre`, `espada_hierro`, `espada_oro`, `espada_diamante`, `espada_netherite`, `maza`, `pico_cobre`, `pico_hierro`, `pico_diamante`, etc.
- **Armaduras:** `casco_cuero`, `pechera_cuero`, `casco_cobre`, `pechera_cobre`, `casco_hierro`, `pechera_hierro`, `casco_diamante`, `pechera_diamante`, `casco_netherite`, `pechera_netherite`, `caparazon_tortuga`.
- **Pociones:** `pocion_rara`, `pocion_fuerza`, `pocion_velocidad`, `pocion_curacion`, `pocion_vision_nocturna`, `pocion_invisibilidad`, `pocion_resistencia_fuego`, `pocion_dano`, `pocion_debilidad`, `pocion_ventisca`, `pocion_tejedora`.
- **Entidades / Mobs:** `zombie`, `esqueleto`, `creeper`, `enderman`, `blaze`, `warden`, `breeze`, `bogged`, `phantom`, `vaca`, `aldeano`, `armadillo`, `lobo`.
- **Elementos / Debilidades:** `luz_solar`, `fuego`, `agua`, `lobo`, `gato`, `bolas_nieve`, `distraccion_sonora`, `ataque_cuerpo_a_cuerpo`.

### 2.2 Predicados
- $\text{Categoria}(x, c)$: El elemento o entidad $x$ pertenece a la categoría $c$.
- $\text{TipoArmadura}(x, p)$: La pieza de armadura $x$ cubre la parte anatómica $p \in \{\text{casco}, \text{pechera}, \text{pantalones}, \text{botas}\}$.
- $\text{MaterialDe}(x, m)$: El objeto $x$ está confeccionado principalmente del material $m$.
- $\text{RequiereDirecto}(x, y)$: Para elaborar o fabricar $x$ se requiere directamente el ingrediente $y$.
- $\text{RequiereMaterialBase}(x, y)$: El elemento $x$ depende del insumo o recurso $y$ en su cadena de producción (relación transitiva).
- $\text{DebilContra}(m, e)$: La entidad $m$ es vulnerable al elemento o criatura $e$.
- $\text{Propiedad}(x, p)$: El material $x$ posee la característica física o mágica $p$.
- $\text{EsPeligroNocturno}(m)$: La entidad $m$ representa una amenaza hostil durante la noche.
- $\text{MaterialArmaduraDisponible}(m)$: El material $m$ permite confeccionar piezas de armadura protectora.
- $\text{PuntosVida}(x, hp)$: La entidad $x$ posee una cantidad máxima de $hp$ puntos de vida base.

---

## 3. Hechos en Lógica de Primer Orden (Extracto Formal)

### Categorización
$$\text{Categoria}(\text{espada\_diamante}, \text{arma}) \land \text{Categoria}(\text{maza}, \text{arma})$$
$$\text{Categoria}(\text{pechera\_diamante}, \text{armadura}) \land \text{Categoria}(\text{pechera\_netherite}, \text{armadura})$$
$$\text{Categoria}(\text{pocion\_fuerza}, \text{pocion}) \land \text{Categoria}(\text{pocion\_curacion}, \text{pocion})$$
$$\text{Categoria}(\text{zombie}, \text{mob\_hostil}) \land \text{Categoria}(\text{breeze}, \text{mob\_hostil}) \land \text{Categoria}(\text{warden}, \text{mob\_hostil})$$

### Materiales y Piezas de Armadura
$$\text{MaterialDe}(\text{pechera\_cuero}, \text{cuero}) \land \text{MaterialDe}(\text{pechera\_hierro}, \text{hierro})$$
$$\text{MaterialDe}(\text{pechera\_diamante}, \text{diamante}) \land \text{MaterialDe}(\text{pechera\_netherite}, \text{netherite})$$
$$\text{TipoArmadura}(\text{casco\_diamante}, \text{casco}) \land \text{TipoArmadura}(\text{pechera\_diamante}, \text{pechera})$$

### Fabricación y Alquimia Directa
$$\text{RequiereDirecto}(\text{espada\_diamante}, \text{diamante}) \land \text{RequiereDirecto}(\text{espada\_diamante}, \text{palo})$$
$$\text{RequiereDirecto}(\text{maza}, \text{barra\_brisa}) \land \text{RequiereDirecto}(\text{maza}, \text{nucleo\_pesado})$$
$$\text{RequiereDirecto}(\text{pocion\_fuerza}, \text{polvo\_blaze}) \land \text{RequiereDirecto}(\text{pocion\_fuerza}, \text{pocion\_rara})$$
$$\text{RequiereDirecto}(\text{pocion\_rara}, \text{verruga\_nether}) \land \text{RequiereDirecto}(\text{pocion\_rara}, \text{frasco\_con\_agua})$$
$$\text{RequiereDirecto}(\text{palo}, \text{tabla\_madera}) \land \text{RequiereDirecto}(\text{tabla\_madera}, \text{tronco\_madera})$$

### Vulnerabilidades
$$\text{DebilContra}(\text{enderman}, \text{agua}) \land \text{DebilContra}(\text{creeper}, \text{gato})$$
$$\text{DebilContra}(\text{blaze}, \text{bolas\_nieve}) \land \text{DebilContra}(\text{warden}, \text{distraccion\_sonora})$$
$$\text{DebilContra}(\text{zombie}, \text{luz\_solar}) \land \text{DebilContra}(\text{breeze}, \text{ataque\_cuerpo\_a\_cuerpo})$$

---

## 4. Axiomas y Reglas Deductivas (Reglas de Inferencia)

### Axioma 1: Clausura Transitiva de Fabricación
$$\forall x \forall y \ (\text{RequiereDirecto}(x, y) \rightarrow \text{RequiereMaterialBase}(x, y))$$
$$\forall x \forall y \forall z \ (\text{RequiereDirecto}(x, z) \land \text{RequiereMaterialBase}(z, y) \rightarrow \text{RequiereMaterialBase}(x, y))$$

### Axioma 2: Deducción de Materiales de Armadura
$$\forall m \ (\exists x (\text{Categoria}(x, \text{armadura}) \land \text{MaterialDe}(x, m)) \rightarrow \text{MaterialArmaduraDisponible}(m))$$

### Axioma 3: Peligro Nocturno
$$\forall m \ (\text{Categoria}(m, \text{mob\_hostil}) \rightarrow \text{EsPeligroNocturno}(m))$$

### Axioma 4: Naturaleza No-Muerta (Undead)
$$\forall m \ (\text{DebilContra}(m, \text{luz\_solar}) \rightarrow \text{EsNoMuerto}(m))$$

### Axioma 5: Recomendación de Defensa
$$\forall m \forall e \ (\text{DebilContra}(m, e) \rightarrow \text{EstrategiaDefensa}(m, e))$$
