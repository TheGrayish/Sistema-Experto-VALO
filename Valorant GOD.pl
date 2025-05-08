% -------------------------
% Mapas disponibles
% -------------------------

mapa(ascent).
mapa(bind).
mapa(haven).
mapa(split).
mapa(icebox).
mapa(fracture).
mapa(pearl).
mapa(lotus).
mapa(sunset).

% -------------------------
% Lista de composiciones por mapa (Actualizadas según meta 2025)
% -------------------------

composiciones(ascent, [
    [jett, omen, sova, kayo, killjoy],   % Meta profesional
    [jett, omen, sova, killjoy, sage],   % Variación ranked alto
    [jett, sova, breach, killjoy, omen], % Alternativa EMEA
    [jett, reyna, omen, killjoy, sova]   % Variación agresiva
]).

composiciones(fracture, [
    [raze, breach, brimstone, fade, chamber],  % Meta profesional
    [raze, breach, fade, killjoy, brimstone],  % Variación común
    [neon, breach, fade, killjoy, harbor],     % Alternativa NA
    [raze, skye, brimstone, chamber, fade]     % Variación ranked
]).

composiciones(haven, [
    [jett, sova, omen, breach, killjoy],   % Configuración profesional
    [jett, sova, omen, cypher, breach],    % Variación con Cypher
    [jett, skye, omen, killjoy, kayo],     % Alternativa NA
    [phoenix, sova, omen, killjoy, breach] % Variación LATAM
]).

composiciones(icebox, [
    [jett, sova, viper, sage, killjoy],    % Meta profesional
    [jett, sova, viper, sage, chamber],   % Variación con Chamber
    [reyna, sova, viper, sage, killjoy],  % Alternativa ranked
    [jett, fade, viper, sage, killjoy]     % Variación iniciador alternativo
]).

composiciones(lotus, [
    [raze, fade, omen, viper, killjoy],    % Meta profesional
    [raze, fade, harbor, viper, killjoy],  % Variación con Harbor
    [jett, fade, omen, viper, chamber],    % Alternativa Asia
    [raze, skye, omen, killjoy, viper]     % Versión simplificada ranked
]).

composiciones(pearl, [
    [jett, fade, astra, chamber, sage],    % Meta profesional
    [jett, fade, astra, killjoy, sage],    % Variación con Killjoy
    [raze, fade, harbor, killjoy, sage],   % Alternativa doble controlador
    [neon, fade, astra, chamber, sage]     % Variación agresiva ranked
]).

composiciones(split, [
    [raze, skye, omen, cypher, sage],      % Meta profesional
    [raze, skye, omen, killjoy, sage],     % Variación con Killjoy
    [jett, skye, omen, cypher, sage],      % Alternativa con Jett
    [raze, breach, omen, killjoy, sage]    % Versión EMEA
]).

composiciones(bind, [
    [raze, skye, brimstone, cypher, viper],  % Meta clásica
    [phoenix, kayo, harbor, sage, killjoy],  % Composición alternativa
    [jett, skye, omen, chamber, viper],      % Variación moderna
    [neon, fade, harbor, killjoy, sage]       % Estrategia agresiva
]).

composiciones(sunset, [
    [jett, sova, omen, killjoy, raze],     % Composición temporal (ejemplo)
    [iso, fade, astra, clove, chamber],    % Basado en meta emergente
    [raze, skye, harbor, cypher, sage]     % Estrategia de control
]).

% -------------------------
% Agentes y Roles (Actualizados)
% -------------------------

% Duelistas
duelista(jett).
duelista(reyna).
duelista(raze).
duelista(neon).
duelista(phoenix).
duelista(yoru).
duelista(iso).

% Iniciadores
iniciador(sova).
iniciador(breach).
iniciador(kayo).
iniciador(skye).
iniciador(fade).
iniciador(gekko).
iniciador(tejo).

% Controladores
controlador(brimstone).
controlador(omen).
controlador(viper).
controlador(astra).
controlador(harbor).
controlador(clove).

% Centinelas
centinela(cypher).
centinela(killjoy).
centinela(sage).
centinela(chamber).
centinela(deadlock).
centinela(vyse).

% -------------------------
% Sinergias destacadas (Ampliadas)
% -------------------------

sinergia(jett, sova, 'Sova revela con dron/flechas y Jett entra con dash/updraft').
sinergia(raze, skye, 'Skye flashea con Guiding Light mientras Raze usa Boom Bot para limpiar el sitio').
sinergia(viper, sage, 'Viper divide el sitio con muro tóxico y Sage bloquea rotaciones con muro helado').
sinergia(fade, breach, 'Fade revela con Prowlers + Breach aturde con Fault Line para entrada coordinada').
sinergia(omen, chamber, 'Omen cubre con humos mientras Chamber controla ángulos largos con Tour de Force').
sinergia(astra, killjoy, 'Astra controla zonas con Cosmic Divide + Killjoy asegura área con Lockdown').
sinergia(neon, breach, 'Breach aturde con Flashpoint y Neon entra velozmente con Relay Bolt').
sinergia(cypher, sage, 'Cypher vigila flancos con trips + Sage cura y retrasa pushes con Slow Orbs').
sinergia(harbor, fade, 'Harbor inunda zonas con Cove + Fade revela con Haunt para ejecuciones').
sinergia(clove, gekko, 'Clove controla visión con smokes + Gekko molesta con Wingman y Dizzy').


% Detectar el rol del agente
rol(Agente, duelista) :- duelista(Agente).
rol(Agente, iniciador) :- iniciador(Agente).
rol(Agente, controlador) :- controlador(Agente).
rol(Agente, centinela) :- centinela(Agente).

% Buscar agentes alternativos por rol en las composiciones de un mapa
sugerir_agente(Mapa, RolDeseado, Alternativo) :-
    composiciones(Mapa, Lista),
    member(Compo, Lista),
    member(Alternativo, Compo),
    rol(Alternativo, RolDeseado),
    !. % Tomamos el primero que cumpla

solicitar_agente_valido(Mapa, Lista, AgenteValido) :-
    write('¿Con qué agente vas a jugar tú?'), nl,
    read(Agente),
    (agente_valido_en_mapa(Agente, Lista) ->
        AgenteValido = Agente
    ;
        (rol(Agente, Rol) ->
            sugerir_agente(Mapa, Rol, Alternativo),
            write('Ese agente no está en ninguna composición del mapa. Te sugiero usar otro del mismo rol como: '), write(Alternativo), nl,
            solicitar_agente_valido(Mapa, Lista, AgenteValido)
        ;
            write('Ese agente no existe o no tiene rol definido.'), nl,
            solicitar_agente_valido(Mapa, Lista, AgenteValido)
        )
    ).

agente_valido_en_mapa(Agente, Composiciones) :-
    member(Compo, Composiciones),
    member(Agente, Compo).



% -------------------------
% Flujo principal
% -------------------------

jugar :-
    write('¿Que mapa se va a jugar?'), nl,
    read(Mapa),
    (composiciones(Mapa, Lista) ->
        nl, write('Estas son las composiciones disponibles para '), write(Mapa), write(':'), nl,
        mostrar_mapa_completo(Mapa), nl,
        solicitar_agente_valido(Mapa, Lista, AgenteValido),
        filtrar_composiciones(Lista, AgenteValido, Filtradas),
        mostrar_lista(Filtradas, 1),
        elegir_compo(Filtradas, CompoElegida),
        write('Elegiste la composición: '), write(CompoElegida), nl,
        analizar_sinergias(CompoElegida)
    ;
        write('Ese mapa no tiene composiciones registradas.'), nl
    ).


% -------------------------
% Filtros y utilidades
% -------------------------

filtrar_composiciones([], _, []).
filtrar_composiciones([Compo|T], Agente, [Compo|Resto]) :-
    member(Agente, Compo),
    filtrar_composiciones(T, Agente, Resto).
filtrar_composiciones([_|T], Agente, Resto) :-
    filtrar_composiciones(T, Agente, Resto).

mostrar_lista([], _).
mostrar_lista([H|T], N) :-
    write('Opcion '), write(N), write(': '), write(H), nl,
    N2 is N + 1,
    mostrar_lista(T, N2).

elegir_compo(Lista, Compo) :-
    write('¿Que numero de composicion quieres usar?'), nl,
    read(Num),
    nth1(Num, Lista, Compo).

mostrar_mapa_completo(Mapa) :-
    composiciones(Mapa, Lista),
    write('Composiciones para el mapa '), write(Mapa), write(':'), nl,
    mostrar_lista(Lista, 1).


% -------------------------
% Análisis de sinergias
% -------------------------

analizar_sinergias([]).
analizar_sinergias([A|T]) :-
    comparar_con_otros(A, T),
    analizar_sinergias(T).

comparar_con_otros(_, []).
comparar_con_otros(A1, [A2|Resto]) :-
    (sinergia(A1, A2, Msg) ->
        write('Sinergia entre '), write(A1), write(' y '), write(A2), write(': '), write(Msg), nl
    ; sinergia(A2, A1, Msg2) ->
        write('Sinergia entre '), write(A2), write(' y '), write(A1), write(': '), write(Msg2), nl
    ; true),
    comparar_con_otros(A1, Resto).

