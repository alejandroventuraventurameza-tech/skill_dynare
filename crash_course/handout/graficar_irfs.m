%% graficar_irfs.m -- Funciones de impulso-respuesta con estilo para el handout
%
%  Uso (desde la carpeta crash_course/handout):
%      >> dynare rbc_analytical              % caso base (delta = 0.025)
%      >> graficar_irfs
%  o bien
%      >> dynare rbc_analytical -DDELTA1=1   % depreciacion total
%      >> graficar_irfs
%
%  Lee oo_.irfs y oo_.steady_state y grafica cada IRF como desviacion
%  PORCENTUAL respecto al estado estacionario: 100 * (x_t - x_ss) / x_ss.
%  Es la misma unidad que las variables con gorro del Capitulo 2
%  (x_hat = ln(x/x_ss) ~ (x - x_ss)/x_ss), asi que las IRF de Dynare y las
%  derivadas a mano se comparan directamente.
%
%  Exporta assets/irf_matlab_base.pdf (o irf_matlab_delta1.pdf si delta = 1).
%
%  Idea tomada de Galindo, Montecinos y Ortiz (2024), cap. 2,
%  irfs_nolineal_log.m (Fig. 2.12): Dynare grafica las IRF con los nombres
%  internos y sin unidades; unas pocas lineas de MATLAB las vuelven legibles.
%
%  Nota: el archivo es ASCII puro (los acentos se escriben con char(...)),
%  para que se vea igual en Windows, macOS y Linux sin problemas de codificacion.
%  Requiere MATLAB R2019b o posterior (tiledlayout).

% ---- 0. Comprobaciones -------------------------------------------------------
if ~exist('oo_', 'var') || ~isfield(oo_, 'irfs')
    error('graficar_irfs:sinIRF', ...
          'No hay IRF en memoria. Corre antes:  dynare rbc_analytical');
end

% ---- 1. Que graficar y como llamarlo ----------------------------------------
% Orden economico: el choque, luego el producto y sus usos, los factores y
% sus precios.  Cada titulo nombra la variable y su simbolo en el handout.
o_ac = char(243);                 % o con tilde
sep  = [',' char(160) ' '];       % coma + espacio fijo: la cursiva no se pega
vars    = {'a', 'y', 'c', 'i', 'k', 'h', 'w', 'r'};
titulos = {['Productividad'      sep '{\ita}_t'], ...
           ['Producto'           sep '{\ity}_t'], ...
           ['Consumo'            sep '{\itc}_t'], ...
           ['Inversi' o_ac 'n'   sep '{\iti}_t'], ...
           ['Capital'            sep '{\itk}_t'], ...
           ['Horas'              sep '{\ith}_t'], ...
           ['Salario real'       sep '{\itw}_t'], ...
           ['Tasa de alquiler'   sep '{\itr}_t']};
choque = 'eps';

% ---- 2. Estilo (coherente con el handout) ------------------------------------
azul  = [0.00 0.00 0.55];         % darkblue del handout
gris  = [0.55 0.55 0.55];         % linea de cero
tinta = [0.15 0.15 0.15];         % texto y ejes
fuente = 'Palatino Linotype';     % la fuente del handout (mathpazo)
if ~any(strcmp(listfonts, fuente)), fuente = 'Times New Roman'; end

% ---- 3. Datos de la corrida ---------------------------------------------------
nombres = cellstr(M_.endo_names);
pnames  = cellstr(M_.param_names);
delta   = M_.params(strcmp(pnames, 'delta'));
sigma   = M_.params(strcmp(pnames, 'sigma_eps'));
T       = options_.irf;           % horizonte de la IRF (irf = 40)
t       = 1:T;                    % en Dynare, el periodo 1 es el impacto

% ---- 4. Figura ------------------------------------------------------------------
% Tamano = ancho de texto del handout (15.5 cm), para insertarlo sin escalar:
% asi los 8 pt de los ejes se imprimen como 8 pt.
ancho = 15.5;  alto = 8.6;     % cm
fig = figure('Color', 'w', 'Units', 'centimeters', 'Position', [2 2 ancho alto]);
tl  = tiledlayout(fig, 2, 4, 'TileSpacing', 'compact', 'Padding', 'compact');

for j = 1:numel(vars)
    v     = vars{j};
    campo = [v '_' choque];
    xss   = oo_.steady_state(strcmp(nombres, v));

    % Dynare NO guarda las IRF que son practicamente cero (p. ej., las horas
    % con delta = 1).  En ese caso la respuesta es nula y la dibujamos como tal.
    if isfield(oo_.irfs, campo)
        irf = 100 * oo_.irfs.(campo) / xss;
    else
        irf = zeros(1, T);
    end

    ax = nexttile(tl);
    % La linea de cero solo se dibuja si aporta: cuando la IRF la cruza o es
    % nula.  Si la serie es siempre positiva, la base del eje ya cumple ese rol.
    nula = max(abs(irf)) < 1e-10;
    if nula || min(irf) < 0
        plot(ax, [1 T], [0 0], ':', 'Color', gris, 'LineWidth', 0.8); hold(ax, 'on');
    end
    plot(ax, t, irf, '-', 'Color', azul, 'LineWidth', 1.3);
    hold(ax, 'off');

    title(ax, titulos{j}, 'FontWeight', 'normal', 'FontSize', 9, 'Color', tinta);
    set(ax, 'FontName', fuente, 'FontSize', 7.5, 'Box', 'off', 'TickDir', 'out', ...
            'XColor', tinta, 'YColor', tinta, 'XGrid', 'on', 'YGrid', 'on', ...
            'GridAlpha', 0.12, 'XLim', [1 T], 'XTick', [1 10 20 30 40], ...
            'TickLength', [0.02 0.02]);
    ax.YAxis.Exponent = 0;                      % sin factores x10^-3
    ax.Title.FontName = fuente;

    % Si la respuesta es nula, un eje simetrico pequeno lo hace evidente.
    if nula, ylim(ax, [-0.1 0.1]); end

    if mod(j-1, 4) == 0, ylabel(ax, '% desv. del EE', 'Color', tinta); end
    if j > 4,            xlabel(ax, 'Trimestres',      'Color', tinta); end
end

% sigma, epsilon y delta como glifos de la fuente (char) y no como \sigma del
% interprete TeX: asi el epsilon es el mismo del handout y no la variante lunada.
titulo = sprintf(['Respuesta a un choque de productividad de una desviaci' o_ac ...
                  'n est' char(225) 'ndar  (' char(963) '_{' char(949) '} = %.2f%%,  ' ...
                  char(948) ' = %g)'], 100*sigma, delta);
title(tl, titulo, 'FontName', fuente, 'FontSize', 9.5, 'Color', tinta);

% ---- 5. Exportar --------------------------------------------------------------
if abs(delta - 1) < 1e-12, archivo = 'irf_matlab_delta1'; else, archivo = 'irf_matlab_base'; end
if ~exist('assets', 'dir'), mkdir('assets'); end
destino = fullfile('assets', [archivo '.pdf']);
if exist('exportgraphics', 'file')
    exportgraphics(fig, destino, 'ContentType', 'vector');
else
    set(fig, 'PaperUnits', 'centimeters', 'PaperSize', [ancho alto], ...
             'PaperPosition', [0 0 ancho alto]);
    print(fig, destino, '-dpdf');
end
fprintf('Figura guardada en %s\n', destino);
