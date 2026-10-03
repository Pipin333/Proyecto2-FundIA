% ==============================================================================
% PROYECTO N°2 - FUNDAMENTOS DE INTELIGENCIA ARTIFICIAL (UNAB)
% BASE DE CONOCIMIENTO EN PROLOG (LÓGICA DE PRIMER ORDEN)
% ==============================================================================
% Este archivo almacena hechos y reglas deductivas del dominio.
% Se encuentra diseñado para ser extensible en vivo durante la interrogación.
% ==============================================================================

:- discontiguous categoria/2.
:- discontiguous requiere/2.
:- discontiguous propiedad/2.
:- discontiguous debil_contra/2.

% ------------------------------------------------------------------------------
% 1. HECHOS: Categorías y Entidades del Dominio
% ------------------------------------------------------------------------------
% categoria(Elemento, Categoria)
categoria(espada_hierro, arma).
categoria(pico_hierro, herramienta).
categoria(armadura_diamante, proteccion).
categoria(pocion_curacion, pocion).
categoria(zombie, mob_hostil).
categoria(esqueleto, mob_hostil).
categoria(creeper, mob_hostil).
categoria(vaca, mob_pasivo).
categoria(aldeano, mob_pasivo).

% ------------------------------------------------------------------------------
% 2. HECHOS: Relaciones y Dependencias directas (Crafteo / Fabricación)
% ------------------------------------------------------------------------------
% requiere_directo(Producto, Ingrediente)
requiere_directo(espada_hierro, lingote_hierro).
requiere_directo(espada_hierro, palo).
requiere_directo(pico_hierro, lingote_hierro).
requiere_directo(pico_hierro, palo).
requiere_directo(palo, tabla_madera).
requiere_directo(tabla_madera, tronco_madera).
requiere_directo(pocion_curacion, verruga_nether).
requiere_directo(pocion_curacion, sandia_reluciente).
requiere_directo(sandia_reluciente, pepita_oro).
requiere_directo(sandia_reluciente, rodaja_sandia).

% ------------------------------------------------------------------------------
% 3. HECHOS: Propiedades, Fortalezas y Debilidades
% ------------------------------------------------------------------------------
% debil_contra(Objetivo, Elemento)
debil_contra(zombie, fuego).
debil_contra(zombie, luz_solar).
debil_contra(esqueleto, lobo).
debil_contra(esqueleto, luz_solar).
debil_contra(creeper, gato).
debil_contra(creeper, ocelote).

% propiedad(Elemento, Caracteristica)
propiedad(madera, inflamable).
propiedad(hierro, resistente).
propiedad(diamante, alta_durabilidad).

% ------------------------------------------------------------------------------
% 4. REGLAS DEDUCTIVAS (Lógica de Primer Orden)
% ------------------------------------------------------------------------------

% Inferencia Transitiva de Materiales:
% X requiere Y recursivamente si lo requiere directo, o si requiere un intermediario Z que requiere Y.
requiere_material_base(X, Y) :-
    requiere_directo(X, Y).
requiere_material_base(X, Y) :-
    requiere_directo(X, Z),
    requiere_material_base(Z, Y).

% Regla: Un mob es peligroso de noche si es hostil y la luz solar no lo elimina inmediatamente (o acecha de noche)
es_peligro_nocturno(Mob) :-
    categoria(Mob, mob_hostil).

% Regla: Un objeto es de nivel avanzado si requiere directa o indirectamente oro o diamante
es_nivel_avanzado(Objeto) :-
    requiere_material_base(Objeto, diamante).
es_nivel_avanzado(Objeto) :-
    requiere_material_base(Objeto, pepita_oro).

% Regla de recomendación de defensa contra un mob hostil
estrategia_defensa(Mob, Estrategia) :-
    debil_contra(Mob, Estrategia).

% ------------------------------------------------------------------------------
% 5. PREDICADOS DE CONSULTA RÁPIDA (Para interacción con el Chatbot)
% ------------------------------------------------------------------------------

% listar_materiales_base(Item, ListaMateriales)
listar_materiales_base(Item, Materiales) :-
    setof(M, requiere_material_base(Item, M), Materiales), !.
listar_materiales_base(_, []).

% listar_debilidades(Mob, ListaDebilidades)
listar_debilidades(Mob, Debilidades) :-
    setof(D, debil_contra(Mob, D), Debilidades), !.
listar_debilidades(_, []).
