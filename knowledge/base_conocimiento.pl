% ==============================================================================
% PROYECTO N°2 - FUNDAMENTOS DE INTELIGENCIA ARTIFICIAL (UNAB)
% BASE DE CONOCIMIENTO EN PROLOG (LÓGICA DE PRIMER ORDEN)
% Dominio: Mecánicas de Supervivencia, Fabricación y Ecosistema (Minecraft Java)
% ==============================================================================
% NOTA: Esta base de conocimiento se provee como PLANTILLA DE REFERENCIA
% y demostración funcional completa (alineada con mecánicas de Minecraft Java).
% Diseñada para ser modular, limpia y extensible en vivo durante la interrogación.
% ==============================================================================

:- discontiguous categoria/2.
:- discontiguous tipo_armadura/2.
:- discontiguous material_de/2.
:- discontiguous requiere_directo/2.
:- discontiguous debil_contra/2.
:- discontiguous propiedad/2.
:- discontiguous puntos_vida/2.
:- discontiguous alias/2.
:- discontiguous drop_habitual/2.
:- discontiguous habitad_principal/2.

% ==============================================================================
% 1. CATEGORÍAS Y ENTIDADES
% ==============================================================================

% Armas
categoria(espada_madera, arma).
categoria(espada_piedra, arma).
categoria(espada_cobre, arma).
categoria(espada_hierro, arma).
categoria(espada_oro, arma).
categoria(espada_diamante, arma).
categoria(espada_netherite, arma).
categoria(maza, arma).
categoria(arco, arma).
categoria(ballesta, arma).
categoria(tridente, arma).

% Herramientas
categoria(pico_madera, herramienta).
categoria(pico_piedra, herramienta).
categoria(pico_cobre, herramienta).
categoria(pico_hierro, herramienta).
categoria(pico_oro, herramienta).
categoria(pico_diamante, herramienta).
categoria(pico_netherite, herramienta).
categoria(hacha_hierro, herramienta).
categoria(pala_hierro, herramienta).
categoria(azada_hierro, herramienta).

% Armaduras (Piezas)
categoria(casco_cuero, armadura).
categoria(pechera_cuero, armadura).
categoria(pantalones_cuero, armadura).
categoria(botas_cuero, armadura).

categoria(casco_cobre, armadura).
categoria(pechera_cobre, armadura).
categoria(pantalones_cobre, armadura).
categoria(botas_cobre, armadura).

categoria(casco_hierro, armadura).
categoria(pechera_hierro, armadura).
categoria(pantalones_hierro, armadura).
categoria(botas_hierro, armadura).

categoria(casco_oro, armadura).
categoria(pechera_oro, armadura).
categoria(pantalones_oro, armadura).
categoria(botas_oro, armadura).

categoria(casco_diamante, armadura).
categoria(pechera_diamante, armadura).
categoria(pantalones_diamante, armadura).
categoria(botas_diamante, armadura).

categoria(casco_netherite, armadura).
categoria(pechera_netherite, armadura).
categoria(pantalones_netherite, armadura).
categoria(botas_netherite, armadura).

categoria(caparazon_tortuga, armadura).
categoria(armadura_lobo, proteccion_mob).

% Pociones
categoria(pocion_rara, pocion_base).
categoria(pocion_fuerza, pocion).
categoria(pocion_velocidad, pocion).
categoria(pocion_curacion, pocion).
categoria(pocion_dano, pocion).
categoria(pocion_vision_nocturna, pocion).
categoria(pocion_invisibilidad, pocion).
categoria(pocion_resistencia_fuego, pocion).
categoria(pocion_respiracion_acuatica, pocion).
categoria(pocion_caida_lenta, pocion).
categoria(pocion_regeneracion, pocion).
categoria(pocion_debilidad, pocion).
categoria(pocion_veneno, pocion).
categoria(pocion_tortuga, pocion).
categoria(pocion_ventisca, pocion).
categoria(pocion_tejedora, pocion).
categoria(pocion_densidad, pocion).

% Mobs Hostiles
categoria(zombie, mob_hostil).
categoria(esqueleto, mob_hostil).
categoria(creeper, mob_hostil).
categoria(arana, mob_hostil).
categoria(arana_cueva, mob_hostil).
categoria(enderman, mob_hostil).
categoria(blaze, mob_hostil).
categoria(ghast, mob_hostil).
categoria(witch, mob_hostil).
categoria(drowned, mob_hostil).
categoria(phantom, mob_hostil).
categoria(warden, mob_hostil).
categoria(breeze, mob_hostil).
categoria(bogged, mob_hostil).
categoria(piglin_brute, mob_hostil).

% Mobs Pasivos y Neutrales
categoria(vaca, mob_pasivo).
categoria(oveja, mob_pasivo).
categoria(cerdo, mob_pasivo).
categoria(pollo, mob_pasivo).
categoria(aldeano, mob_pasivo).
categoria(armadillo, mob_pasivo).
categoria(camello, mob_pasivo).
categoria(gato, mob_pasivo).
categoria(lobo, mob_neutral).
categoria(piglin, mob_neutral).
categoria(golem_hierro, mob_neutral).

% Jefes (Bosses)
categoria(ender_dragon, jefe).
categoria(wither, jefe).

% Puntos de Vida (Salud / HP)
puntos_vida(ender_dragon, 200).
puntos_vida(warden, 500).
puntos_vida(wither, 300).
puntos_vida(golem_hierro, 100).
puntos_vida(piglin_brute, 50).
puntos_vida(enderman, 40).
puntos_vida(breeze, 30).
puntos_vida(zombie, 20).
puntos_vida(esqueleto, 20).
puntos_vida(creeper, 20).
puntos_vida(aldeano, 20).
puntos_vida(arana, 16).
puntos_vida(armadillo, 12).
puntos_vida(vaca, 10).

% Alias y Sinónimos populares
alias(dragona, ender_dragon).
alias(dragon, ender_dragon).
alias(dragon_del_end, ender_dragon).
alias(jean, ender_dragon).
alias(golem, golem_hierro).

% ==============================================================================
% 2. CLASIFICACIÓN DE PIEZAS Y MATERIALES DE ARMADURA
% ==============================================================================

tipo_armadura(casco_cuero, casco).
tipo_armadura(pechera_cuero, pechera).
tipo_armadura(pantalones_cuero, pantalones).
tipo_armadura(botas_cuero, botas).

tipo_armadura(casco_cobre, casco).
tipo_armadura(pechera_cobre, pechera).
tipo_armadura(pantalones_cobre, pantalones).
tipo_armadura(botas_cobre, botas).

tipo_armadura(casco_hierro, casco).
tipo_armadura(pechera_hierro, pechera).
tipo_armadura(pantalones_hierro, pantalones).
tipo_armadura(botas_hierro, botas).

tipo_armadura(casco_oro, casco).
tipo_armadura(pechera_oro, pechera).
tipo_armadura(pantalones_oro, pantalones).
tipo_armadura(botas_oro, botas).

tipo_armadura(casco_diamante, casco).
tipo_armadura(pechera_diamante, pechera).
tipo_armadura(pantalones_diamante, pantalones).
tipo_armadura(botas_diamante, botas).

tipo_armadura(casco_netherite, casco).
tipo_armadura(pechera_netherite, pechera).
tipo_armadura(pantalones_netherite, pantalones).
tipo_armadura(botas_netherite, botas).

material_de(casco_cuero, cuero).
material_de(pechera_cuero, cuero).
material_de(pantalones_cuero, cuero).
material_de(botas_cuero, cuero).

material_de(casco_cobre, cobre).
material_de(pechera_cobre, cobre).
material_de(pantalones_cobre, cobre).
material_de(botas_cobre, cobre).

material_de(casco_hierro, hierro).
material_de(pechera_hierro, hierro).
material_de(pantalones_hierro, hierro).
material_de(botas_hierro, hierro).

material_de(casco_oro, oro).
material_de(pechera_oro, oro).
material_de(pantalones_oro, oro).
material_de(botas_oro, oro).

material_de(casco_diamante, diamante).
material_de(pechera_diamante, diamante).
material_de(pantalones_diamante, diamante).
material_de(botas_diamante, diamante).

material_de(casco_netherite, netherite).
material_de(pechera_netherite, netherite).
material_de(pantalones_netherite, netherite).
material_de(botas_netherite, netherite).

% ==============================================================================
% 3. RECETAS Y CADENA DE DEPENDENCIAS (CRAFTEO Y ALQUIMIA)
% ==============================================================================

% Armas y Herramientas
requiere_directo(espada_madera, tabla_madera).
requiere_directo(espada_madera, palo).

requiere_directo(espada_piedra, adoquines).
requiere_directo(espada_piedra, palo).

requiere_directo(espada_cobre, lingote_cobre).
requiere_directo(espada_cobre, palo).

requiere_directo(espada_hierro, lingote_hierro).
requiere_directo(espada_hierro, palo).

requiere_directo(espada_oro, lingote_oro).
requiere_directo(espada_oro, palo).

requiere_directo(espada_diamante, diamante).
requiere_directo(espada_diamante, palo).

requiere_directo(espada_netherite, espada_diamante).
requiere_directo(espada_netherite, lingote_netherite).
requiere_directo(espada_netherite, plantilla_herreria_netherite).

requiere_directo(maza, barra_brisa).
requiere_directo(maza, nucleo_pesado).

requiere_directo(pico_madera, tabla_madera).
requiere_directo(pico_madera, palo).
requiere_directo(pico_piedra, adoquines).
requiere_directo(pico_piedra, palo).
requiere_directo(pico_cobre, lingote_cobre).
requiere_directo(pico_cobre, palo).
requiere_directo(pico_hierro, lingote_hierro).
requiere_directo(pico_hierro, palo).
requiere_directo(pico_diamante, diamante).
requiere_directo(pico_diamante, palo).
requiere_directo(pico_netherite, pico_diamante).
requiere_directo(pico_netherite, lingote_netherite).

% Armaduras
requiere_directo(casco_cuero, cuero).
requiere_directo(pechera_cuero, cuero).
requiere_directo(pantalones_cuero, cuero).
requiere_directo(botas_cuero, cuero).

requiere_directo(casco_cobre, lingote_cobre).
requiere_directo(pechera_cobre, lingote_cobre).
requiere_directo(pantalones_cobre, lingote_cobre).
requiere_directo(botas_cobre, lingote_cobre).

requiere_directo(casco_hierro, lingote_hierro).
requiere_directo(pechera_hierro, lingote_hierro).
requiere_directo(pantalones_hierro, lingote_hierro).
requiere_directo(botas_hierro, lingote_hierro).

requiere_directo(casco_diamante, diamante).
requiere_directo(pechera_diamante, diamante).
requiere_directo(pantalones_diamante, diamante).
requiere_directo(botas_diamante, diamante).

requiere_directo(casco_netherite, casco_diamante).
requiere_directo(casco_netherite, lingote_netherite).
requiere_directo(pechera_netherite, pechera_diamante).
requiere_directo(pechera_netherite, lingote_netherite).
requiere_directo(pantalones_netherite, pantalones_diamante).
requiere_directo(pantalones_netherite, lingote_netherite).
requiere_directo(botas_netherite, botas_diamante).
requiere_directo(botas_netherite, lingote_netherite).

% Materiales Base y Procesados
requiere_directo(palo, tabla_madera).
requiere_directo(tabla_madera, tronco_madera).
requiere_directo(lingote_cobre, mena_cobre).
requiere_directo(lingote_cobre, carbon).
requiere_directo(lingote_hierro, mena_hierro).
requiere_directo(lingote_hierro, carbon).
requiere_directo(lingote_oro, mena_oro).
requiere_directo(lingote_netherite, fragmento_netherite).
requiere_directo(lingote_netherite, lingote_oro).
requiere_directo(fragmento_netherite, escombros_ancestrales).
requiere_directo(armadura_lobo, escamas_armadillo).

% Pociones (Alquimia)
requiere_directo(pocion_rara, verruga_nether).
requiere_directo(pocion_rara, frasco_con_agua).

requiere_directo(pocion_fuerza, polvo_blaze).
requiere_directo(pocion_fuerza, pocion_rara).

requiere_directo(pocion_velocidad, azucar).
requiere_directo(pocion_velocidad, pocion_rara).

requiere_directo(pocion_curacion, sandia_reluciente).
requiere_directo(pocion_curacion, pocion_rara).

requiere_directo(pocion_vision_nocturna, zanahoria_dorada).
requiere_directo(pocion_vision_nocturna, pocion_rara).

requiere_directo(pocion_invisibilidad, ojo_arana_fermentado).
requiere_directo(pocion_invisibilidad, pocion_vision_nocturna).

requiere_directo(pocion_resistencia_fuego, crema_magma).
requiere_directo(pocion_resistencia_fuego, pocion_rara).

requiere_directo(pocion_respiracion_acuatica, pez_globo).
requiere_directo(pocion_respiracion_acuatica, pocion_rara).

requiere_directo(pocion_caida_lenta, membrana_fantasma).
requiere_directo(pocion_caida_lenta, pocion_rara).

requiere_directo(pocion_regeneracion, lagrima_ghast).
requiere_directo(pocion_regeneracion, pocion_rara).

requiere_directo(pocion_dano, ojo_arana_fermentado).
requiere_directo(pocion_dano, pocion_curacion).

requiere_directo(pocion_debilidad, ojo_arana_fermentado).
requiere_directo(pocion_debilidad, frasco_con_agua).

requiere_directo(pocion_veneno, ojo_arana).
requiere_directo(pocion_veneno, pocion_rara).

requiere_directo(pocion_ventisca, barra_brisa).
requiere_directo(pocion_ventisca, pocion_rara).

requiere_directo(pocion_tejedora, telarana).
requiere_directo(pocion_tejedora, pocion_rara).

requiere_directo(sandia_reluciente, pepita_oro).
requiere_directo(sandia_reluciente, rodaja_sandia).
requiere_directo(zanahoria_dorada, pepita_oro).
requiere_directo(zanahoria_dorada, zanahoria).
requiere_directo(polvo_blaze, vara_blaze).
requiere_directo(azucar, cana_azucar).

% ==============================================================================
% 4. DEBILIDADES, AMENAZAS Y PROPIEDADES
% ==============================================================================

debil_contra(zombie, luz_solar).
debil_contra(zombie, fuego).
debil_contra(zombie, pocion_curacion). % Los undead reciben daño de curación

debil_contra(esqueleto, luz_solar).
debil_contra(esqueleto, lobo).
debil_contra(esqueleto, pocion_curacion).

debil_contra(creeper, gato).
debil_contra(creeper, ocelote).

debil_contra(enderman, agua).
debil_contra(enderman, lluvia).

debil_contra(blaze, bolas_nieve).
debil_contra(blaze, agua).

debil_contra(breeze, ataque_cuerpo_a_cuerpo).
debil_contra(breeze, proyectil_reflejado).

debil_contra(bogged, luz_solar).
debil_contra(bogged, lobo).

debil_contra(warden, distraccion_sonora).

debil_contra(phantom, luz_solar).
debil_contra(phantom, gato).

debil_contra(drowned, luz_solar).

debil_contra(ender_dragon, destruir_cristales_end).
debil_contra(ender_dragon, explosiones_camas).

debil_contra(wither, pocion_curacion).
debil_contra(wither, combate_cuerpo_a_cuerpo_fase2).

% Propiedades
propiedad(madera, inflamable).
propiedad(cuero, tinte_personalizable).
propiedad(cobre, oxidable).
propiedad(cobre, conductor).
propiedad(hierro, versatil).
propiedad(oro, afinidad_piglin).
propiedad(diamante, alta_durabilidad).
propiedad(netherite, resistente_a_lava).
propiedad(netherite, incombustible).

% ==============================================================================
% 5. REGLAS DEDUCTIVAS (LÓGICA DE PRIMER ORDEN)
% ==============================================================================

% Inferencia transitiva recursiva de materiales requeridos
requiere_material_base(X, Y) :-
    requiere_directo(X, Y).
requiere_material_base(X, Y) :-
    requiere_directo(X, Z),
    requiere_material_base(Z, Y).

% Materiales existentes para fabricar armaduras
material_armadura_disponible(Material) :-
    categoria(Item, armadura),
    material_de(Item, Material).

% Un mob es peligroso en la superficie durante la noche si es hostil
es_peligro_nocturno(Mob) :-
    categoria(Mob, mob_hostil).

% Un objeto es de nivel élite o superior
es_nivel_elite(Objeto) :-
    requiere_material_base(Objeto, diamante).
es_nivel_elite(Objeto) :-
    requiere_material_base(Objeto, netherite).

% Una criatura es de tipo no-muerto (undead) si se quema al sol o daña con curación
es_no_muerto(Mob) :-
    debil_contra(Mob, luz_solar).

% Estrategia de defensa efectiva
estrategia_defensa(Mob, Estrategia) :-
    debil_contra(Mob, Estrategia).

% ==============================================================================
% 6. PREDICADOS DE CONSULTA RÁPIDA
% ==============================================================================

listar_materiales_base(Item, Materiales) :-
    setof(M, requiere_material_base(Item, M), Materiales), !.
listar_materiales_base(_, []).

listar_materiales_armadura(Materiales) :-
    setof(M, material_armadura_disponible(M), Materiales), !.
listar_materiales_armadura([]).

listar_debilidades(Mob, Debilidades) :-
    setof(D, debil_contra(Mob, D), Debilidades), !.
listar_debilidades(_, []).
