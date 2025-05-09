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
% Lista de composiciones por mapa (Actualizadas seg�n meta 2025)
% -------------------------

composiciones(ascent, [
    [jett, omen, sova, kayo, killjoy],   % Meta profesional
    [jett, omen, sova, killjoy, sage],   % Variaci�n ranked alto
    [jett, sova, breach, killjoy, omen], % Alternativa EMEA
    [jett, reyna, omen, killjoy, sova]   % Variaci�n agresiva
]).

composiciones(fracture, [
    [raze, breach, brimstone, fade, chamber],  % Meta profesional
    [raze, breach, fade, killjoy, brimstone],  % Variaci�n com�n
    [neon, breach, fade, killjoy, harbor],     % Alternativa NA
    [raze, skye, brimstone, chamber, fade]     % Variaci�n ranked
]).

composiciones(haven, [
    [jett, sova, omen, breach, killjoy],   % Configuraci�n profesional
    [jett, sova, omen, cypher, breach],    % Variaci�n con Cypher
    [jett, skye, omen, killjoy, kayo],     % Alternativa NA
    [phoenix, sova, omen, killjoy, breach] % Variaci�n LATAM
]).

composiciones(icebox, [
    [jett, sova, viper, sage, killjoy],    % Meta profesional
    [jett, sova, viper, sage, chamber],   % Variaci�n con Chamber
    [reyna, sova, viper, sage, killjoy],  % Alternativa ranked
    [jett, fade, viper, sage, killjoy]     % Variaci�n iniciador alternativo
]).

composiciones(lotus, [
    [raze, fade, omen, viper, killjoy],    % Meta profesional
    [raze, fade, harbor, viper, killjoy],  % Variaci�n con Harbor
    [jett, fade, omen, viper, chamber],    % Alternativa Asia
    [raze, skye, omen, killjoy, viper]     % Versi�n simplificada ranked
]).

composiciones(pearl, [
    [jett, fade, astra, chamber, sage],    % Meta profesional
    [jett, fade, astra, killjoy, sage],    % Variaci�n con Killjoy
    [raze, fade, harbor, killjoy, sage],   % Alternativa doble controlador
    [neon, fade, astra, chamber, sage]     % Variaci�n agresiva ranked
]).

composiciones(split, [
    [raze, skye, omen, cypher, sage],      % Meta profesional
    [raze, skye, omen, killjoy, sage],     % Variaci�n con Killjoy
    [jett, skye, omen, cypher, sage],      % Alternativa con Jett
    [raze, breach, omen, killjoy, sage]    % Versi�n EMEA
]).

composiciones(bind, [
    [raze, skye, brimstone, cypher, viper],  % Meta cl�sica
    [phoenix, kayo, harbor, sage, killjoy],  % Composici�n alternativa
    [jett, skye, omen, chamber, viper],      % Variaci�n moderna
    [neon, fade, harbor, killjoy, sage]       % Estrategia agresiva
]).

composiciones(sunset, [
    [tejo, fade, astra, clove, chamber], % Meta profesional
    [jett, sova, omen, killjoy, raze],   % Composici�n temporal
    [raze, skye, harbor, cypher, sage],  % Estrategia de control
    [vyse, fade, omen, killjoy, jett]    % Variaci�n S-tier
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
% Tier list de agentes
% -------------------------
tier(s_tier, [tejo, clove, raze, vyse]).
tier(a_tier, [yoru, deadlock, cypher, jett, iso, neon, sova, gekko, killjoy, omen, brimstone, phoenix, sage]).
tier(b_tier, [chamber, viper, breach, skye, fade, astra, reyna]).
tier(c_tier, [kayo, harbor]).

% -------------------------
% Descripciones de mapas
% -------------------------
descripcion_mapa(ascent, 'Equilibra poder de entrada, control de mapa e informaci�n. Jett aporta entrada r�pida y uso del Operator, Omen controla �ngulos con sus humos, los iniciadores brindan reconocimiento, y Killjoy asegura la defensa de sitios.').
descripcion_mapa(fracture, 'Composici�n con alto poder de iniciadores y utilidades de control. Raze aprovecha los �ngulos cerrados, Breach y Fade proporcionan un combo de aturdimiento y revelado, Brimstone coloca humos r�pidos, mientras el centinela controla flancos.').
descripcion_mapa(haven, 'Al tener tres sitios, exige una composici�n vers�til. Jett es imprescindible para aprovechar las largas l�neas de visi�n, Omen cubre m�ltiples �ngulos, la combinaci�n de Sova y Breach provee informaci�n constante, mientras el centinela ofrece control de flancos.').
descripcion_mapa(icebox, 'Viper es imprescindible, dividiendo sitios con su Pantalla T�xica. Sage proporciona muro para plantar (especialmente en B) y orbes lentos. Sova despejar espacios largos. Jett puede tomar �ngulos elevados. Killjoy vigila flancos en este mapa de amplias rotaciones.').
descripcion_mapa(lotus, 'La dupla de controladores Omen + Viper es clave. Raze limpia esquinas estrechas y zonas de las puertas. Fade explora los amplios espacios y conectores del mapa. Killjoy vigila rotaciones a trav�s de las puertas y su definitiva cubre �reas extensas.').
descripcion_mapa(pearl, 'Astra con sus humos globales puede tapar �ngulos largos. Fade revela enemigos en rincones. Chamber vigila flancos y su definitiva es letal en largas distancias. Jett infiltra y toma duelos de larga distancia. Sage controla Mid Connector o bloquea A Main.').
descripcion_mapa(split, 'Raze aprovecha sus Blast Packs y granadas en entradas cortas. Skye usa destellos y trailblazer para limpiar esquinas. Omen bloquea visibilidad en puntos clave. Cypher coloca trampas en flancos. Sage levanta muros que bloquean rutas cruciales y ralentiza pushes.').
descripcion_mapa(bind, 'Mapa con espacios estrechos donde Raze destaca. Brimstone y Viper controlan sitios con humos y toxinas. Skye proporciona informaci�n con sus habilidades. El centinela vigila los teleportadores para evitar flancos.').
descripcion_mapa(sunset, 'Mapa con m�ltiples niveles donde Jett puede aprovechar su movilidad. Omen coloca humos estrat�gicos. Fade revela posiciones enemigas. Killjoy y Sage controlan �reas clave y aseguran el post-planta.').

% -------------------------
% Consejos para agentes
% -------------------------
consejo_agente(jett, 'Usa Tailwind para entrar r�pido y Cloudburst para cubrir �ngulos. Ideal para operar con AWP.').
consejo_agente(raze, 'Utiliza Blast Pack para moverte r�pido y Paint Shells para limpiar esquinas. Showstopper es excelente para romper defensas.').
consejo_agente(phoenix, 'Aprovecha Curveball para cegar y Hot Hands para curar. Run It Back te permite hacer entradas seguras.').
consejo_agente(reyna, 'Dismiss despu�s de cada eliminaci�n para reposicionarte. Leer es clave para cegar a m�ltiples enemigos.').
consejo_agente(neon, 'Usa Sprint para rotaciones r�pidas y Slide para entrar a sitios. Fast Lane divide el mapa eficazmente.').
consejo_agente(yoru, 'Utiliza Fakeout para enga�ar y Gatecrash para flanquear. Dimensional Drift permite reconocimiento seguro.').
consejo_agente(iso, 'Aprovecha Double Tap para duelos y Kill Contract para aislar objetivos. Contingency es excelente para post-planta.').
consejo_agente(sova, 'Aprende lineups de Recon Bolt y Shock Dart. Hunters Fury es ideal para limpiar �reas estrechas.').
consejo_agente(breach, 'Coordina Flashpoint con tu equipo. Aftershock limpia esquinas y Rolling Thunder rompe defensas.').
consejo_agente(skye, 'Gu�a Trailblazer para informaci�n y Guiding Light para cegar. Seekers revela posiciones enemigas.').
consejo_agente(kayo, 'FLASH/drive para entradas y ZERO/point para suprimir habilidades. NULL/cmd neutraliza defensas.').
consejo_agente(fade, 'Usa Haunt para revelar y Prowler para buscar enemigos. Nightfall es excelente para post-planta.').
consejo_agente(gekko, 'Wingman planta/defusa la spike. Dizzy ciega m�ltiples �ngulos. Thrash limpia posiciones.').
consejo_agente(tejo, 'Aprovecha Relampago para revelar y Cascada para empujar. Torrente controla �reas amplias.').
consejo_agente(brimstone, 'Coloca Sky Smoke en puntos clave. Stim Beacon acelera pushes y Orbital Strike asegura post-planta.').
consejo_agente(viper, 'Toxic Screen divide sitios. Poison Cloud bloquea �ngulos clave. Pit controla post-planta.').
consejo_agente(omen, 'Dark Cover para humos precisos. Shrouded Step para reposicionamiento. From the Shadows para flanqueos.').
consejo_agente(astra, 'Gravity Well atrae y vulnera. Nova Pulse aturde grupos. Cosmic Divide divide el mapa.').
consejo_agente(harbor, 'Cascade bloquea l�neas de visi�n. High Tide crea paredes de agua. Reckoning controla �reas.').
consejo_agente(clove, 'Pick-Me-Up revive r�pidamente. Meddle desinforma. Not Dead Yet permite jugar agresivo.').
consejo_agente(killjoy, 'Turret vigila flancos. Alarmbot + Nanoswarm es letal. Lockdown controla sitios enteros.').
consejo_agente(cypher, 'Trapwire en flancos. Spycam para informaci�n. Neural Theft revela posiciones enemigas.').
consejo_agente(sage, 'Barrier Wall bloquea entradas. Slow Orb retrasa pushes. Resurrection cambia rondas.').
consejo_agente(chamber, 'Rendezvous para reposicionamiento r�pido. Trademark vigila flancos. Tour De Force es letal a distancia.').
consejo_agente(deadlock, 'GravNet bloquea rushes. Sonic Sensor detecta movimiento. Annihilation elimina grupos.').
consejo_agente(vyse, 'Haunt revela enemigos. Ravenous controla espacio. Nightfall es excelente para post-planta.').

% -------------------------
% Sinergias entre agentes
% -------------------------
sinergia(jett, sova, 'Sova revela con dron/flechas y Jett entra con dash/updraft').
sinergia(raze, skye, 'Skye flashea con Guiding Light mientras Raze usa Boom Bot para limpiar el sitio').
sinergia(viper, sage, 'Viper divide el sitio con muro t�xico y Sage bloquea rotaciones con muro helado').
sinergia(fade, breach, 'Fade revela con Prowlers + Breach aturde con Fault Line para entrada coordinada').
sinergia(omen, chamber, 'Omen cubre con humos mientras Chamber controla �ngulos largos con Tour de Force').
sinergia(astra, killjoy, 'Astra controla zonas con Cosmic Divide + Killjoy asegura �rea con Lockdown').
sinergia(neon, breach, 'Breach aturde con Flashpoint y Neon entra velozmente con Relay Bolt').
sinergia(cypher, sage, 'Cypher vigila flancos con trips + Sage cura y retrasa pushes con Slow Orbs').
sinergia(harbor, fade, 'Harbor inunda zonas con Cove + Fade revela con Haunt para ejecuciones').
sinergia(clove, gekko, 'Clove controla visi�n con smokes + Gekko molesta con Wingman y Dizzy').
            