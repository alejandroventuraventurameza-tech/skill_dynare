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
vars    = {'a', 'y', 'c', 'i', 'k', 'h', 'w', 'r'};
titulos = {'Productividad, {\ita}_t', ...
           'Producto, {\ity}_t', ...
           'Consumo, {\itc}_t', ...
           ['Inversi' o_ac 'n, {\iti}_t'], ...
           'Capital, {\itk}_t', ...
           'Horas, {\ith}_t', ...
           'Salario real, {\itw}_t', ...
           'Tasa de alquiler, {\itr}_t'};
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
fig = figure('Color', 'w', 'Units', 'centimeters', 'Position', [2 2 24 11.5]);
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
    plot(ax, [1 T], [0 0], ':', 'Color', gris, 'LineWidth', 0.8); hold(ax, 'on');
    plot(ax, t, irf, '-', 'Color', azul, 'LineWidth', 1.6);
    hold(ax, 'off');

    title(ax, titulos{j}, 'FontWeight', 'normal', 'FontSize', 10, 'Color', tinta);
    set(ax, 'FontName', fuente, 'FontSize', 8.5, 'Box', 'off', 'TickDir', 'out', ...
            'XColor', tinta, 'YColor', tinta, 'XGrid', 'on', 'YGrid', 'on', ...
            'GridAlpha', 0.12, 'XLim', [1 T], 'XTick', [1 10 20 30 40]);
    ax.YAxis.Exponent = 0;                      % sin factores x10^-3
    ax.Title.FontName = fuente;

    % Si la respuesta es nula, un eje simetrico pequeno lo hace evidente.
    if max(abs(irf)) < 1e-10, ylim(ax, [-0.1 0.1]); end

    if mod(j-1, 4) == 0, ylabel(ax, '% desv. del EE', 'Color', tinta); end
    if j > 4,            xlabel(ax, 'Trimestres',      'Color', tinta); end
end

titulo = sprintf(['Respuesta a un choque de productividad de una desviaci' o_ac ...
                  'n est' char(225) 'ndar  (\\sigma_\\epsilon = %.2f%%,  \\delta = %g)'], ...
                  100*sigma, delta);
title(tl, titulo, 'FontName', fuente, 'FontSize', 11.5, 'Color', tinta);

% ---- 5. Exportar --------------------------------------------------------------
if abs(delta - 1) < 1e-12, archivo = 'irf_matlab_delta1'; else, archivo = 'irf_matlab_base'; end
if ~exist('assets', 'dir'), mkdir('assets'); end
destino = fullfile('assets', [archivo '.pdf']);
if exist('exportgraphics', 'file')
    exportgraphics(fig, destino, 'ContentType', 'vector');
else
    set(fig, 'PaperUnits', 'centimeters', 'PaperSize', [24 11.5], ...
             'PaperPosition', [0 0 24 11.5]);
    print(fig, destino, '-dpdf');
end
fprintf('Figura guardada en %s\n', destino);
