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
    [tejo, fade, astra, clove, chamber], % Meta profesional
    [jett, sova, omen, killjoy, raze],   % Composición temporal
    [raze, skye, harbor, cypher, sage],  % Estrategia de control
    [vyse, fade, omen, killjoy, jett]    % Variación S-tier
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
sinergia(sova, jett, 'Jett aprovecha la info de Sova para entradas agresivas').
sinergia(clove, gekko, 'Clove controla visión con smokes + Gekko molesta con Wingman y Dizzy').
sinergia(gekko, clove, 'Smokes de Clove permiten a Gekko ejecutar habilidades de control').


% -------------------------
% Regla para sugerir una composición basada en un agente
% -------------------------
sugerir_composicion(Mapa, Agente, Composicion) :-
    composiciones(Mapa, Composiciones),
    member(Compo, Composiciones),
    member(Agente, Compo),
    Composicion = Compo.

% -------------------------
% Regla para sugerir un agente alternativo basado en su rol
% -------------------------
sugerir_agente(Mapa, RolDeseado, Alternativo) :-
    composiciones(Mapa, Lista),
    member(Compo, Lista),
    member(Alternativo, Compo),
    rol(Alternativo, RolDeseado),
    !.

% -------------------------
% Roles de los agentes
% -------------------------
rol(jett, duelista).
rol(reyna, duelista).
rol(raze, duelista).
rol(neon, duelista).
rol(phoenix, duelista).
rol(yoru, duelista).
rol(iso, duelista).

rol(sova, iniciador).
rol(breach, iniciador).
rol(kayo, iniciador).
rol(skye, iniciador).
rol(fade, iniciador).
rol(gekko, iniciador).
rol(tejo, iniciador).

rol(brimstone, controlador).
rol(omen, controlador).
rol(viper, controlador).
rol(astra, controlador).
rol(harbor, controlador).
rol(clove, controlador).

rol(cypher, centinela).
rol(killjoy, centinela).
rol(sage, centinela).
rol(chamber, centinela).
rol(deadlock, centinela).
rol(vyse, centinela).

% Tier list de agentes
tier(s_tier, [tejo, clove, raze, vyse]).
tier(a_tier, [yoru, deadlock, cypher, jett, iso, neon, sova, gekko, killjoy, omen, brimstone, phoenix, sage]).
tier(b_tier, [chamber, viper, breach, skye, fade, astra, reyna]).
tier(c_tier, [kayo, harbor]).
