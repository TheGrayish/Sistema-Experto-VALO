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

% Lista de composiciones por mapa
composiciones(ascent, [
    [jett, sova, omen, killjoy, sage],
    [jett, sova, omen, cypher, sage],
    [jett, sova, kayo, omen, killjoy],

    
    [jett, breach, viper, cypher, chamber],
    [iso, gekko, astra, killjoy, sage]
]).

composiciones(bind, [
    [raze, skye, brimstone, cypher, viper],
    [phoenix, kayo, harbor, sage, killjoy]
]).

composiciones(pearl, [
    [yoru, fade, harbor, cypher, sage],
    [iso, fade, omen, killjoy, chamber]
]).

composiciones(lotus, [
    [iso, fade, astra, clove, chamber],
    [raze, breach, viper, sage, cypher]
]).


% -------------------------
% Agentes y Roles
% -------------------------

duelista(jett).
duelista(reyna).
duelista(raze).
duelista(neon).
duelista(phoenix).
duelista(yoru).
duelista(waylay).
duelista(iso).

iniciador(sova).
iniciador(breach).
iniciador(kayo).
iniciador(skye).
iniciador(fade).
iniciador(gekko).
iniciador(tejo).

controlador(brimstone).
controlador(omen).
controlador(viper).
controlador(astra).
controlador(harbor).
controlador(clove).

centinela(cypher).
centinela(killjoy).
centinela(sage).
centinela(chamber).
centinela(deadlock).
centinela(vyse).


% -------------------------
% Sinergias destacadas
% -------------------------

sinergia(jett, sova, 'Sova revela y Jett entra agresivo.').
sinergia(killjoy, sage, 'El hecho de que los 2 sean centilas, sera mas facil defender ya que cada 1 puede defender un site').
sinergia(raze, skye, 'Skye flashea y Raze limpia el sitio.').
sinergia(iso, fade, 'Fade marca enemigos e ISO busca 1v1.').
sinergia(gekko, reyna, 'Gekko molesta con su utilidad y Reyna remata.').
sinergia(omen, reyna, 'Omen corta visión y Reyna ataca por sorpresa.').

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