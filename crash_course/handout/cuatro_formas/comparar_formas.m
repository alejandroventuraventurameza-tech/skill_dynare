%% comparar_formas.m -- Corre las cuatro formas del modelo y compara sus IRF
%
%  Uso (desde la carpeta cuatro_formas):
%      >> comparar_formas
%  o, para depreciacion total, defina antes  cf_flag = '-DDELTA1=1';
%
%  Las cuatro formas describen el MISMO modelo; solo cambian las unidades:
%    1. no lineal, niveles   -> IRF en desviaciones en niveles  (x - x_ss)
%    2. no lineal, logs      -> IRF en desviaciones logaritmicas (ln x - ln x_ss)
%    3. lineal, niveles      -> igual que la forma 1
%    4. lineal, logs         -> igual que la forma 2
%  Para compararlas se llevan todas a % de desviacion respecto al EE:
%  las de niveles se dividen por x_ss; las de logs ya estan en esa unidad.
%  A primer orden las cuatro deben coincidir hasta el redondeo numerico.
%
%  Inspirado en Galindo, Montecinos y Ortiz (2024), cap. 2, sec. 2.3.11 y
%  Tabla 2.28, que comparan las cuatro versiones del modelo de Long-Plosser.
%
%  Nota: Dynare corre aqui con 'noclearall' para no borrar las variables de
%  este script entre corrida y corrida; por eso sus nombres empiezan con cf_.

if ~exist('cf_flag', 'var'), cf_flag = ''; end

cf_formas = {'rbc_nolineal_niv', 'rbc_nolineal_log', 'rbc_lineal_niv', 'rbc_lineal_log'};
cf_etiq   = {'1. No lineal, niveles', '2. No lineal, logs', ...
             '3. Lineal, niveles',    '4. Lineal, logs'};
cf_nc     = {'c', 'lc', 'c_d', 'c_h'};          % nombre del consumo en cada forma
cf_nh     = {'h', 'lh', 'h_d', 'h_h'};          % nombre de las horas
cf_niv    = [true false true false];            % forma en niveles?
cf_res    = struct('c', {}, 'h', {});

for cf_f = 1:4
    eval(['dynare ' cf_formas{cf_f} ' noclearall nograph ' cf_flag]);
    cf_pn  = cellstr(M_.param_names);
    cf_css = M_.params(strcmp(cf_pn, 'c_ss'));
    cf_hss = M_.params(strcmp(cf_pn, 'hss'));
    cf_T   = options_.irf;
    cf_c   = zeros(1, cf_T);  cf_h = zeros(1, cf_T);   % IRF nulas no se guardan
    if isfield(oo_.irfs, [cf_nc{cf_f} '_eps']), cf_c = oo_.irfs.([cf_nc{cf_f} '_eps']); end
    if isfield(oo_.irfs, [cf_nh{cf_f} '_eps']), cf_h = oo_.irfs.([cf_nh{cf_f} '_eps']); end
    if cf_niv(cf_f), cf_c = cf_c/cf_css; cf_h = cf_h/cf_hss; end
    cf_res(cf_f).c = 100*cf_c;
    cf_res(cf_f).h = 100*cf_h;
end

% ---- Tabla comparativa ---------------------------------------------------------
cf_t = [1 2 5 10 20 40];
for cf_var = {'c', 'h'}
    v = cf_var{1};
    if v == 'c', tit = 'del consumo'; else, tit = 'de las horas'; end
    fprintf('\nIRF %s a un choque de 1 desv. est. (%% desv. del EE)\n', tit);
    cf_hdr = strcat('t=', strsplit(num2str(cf_t)));
    fprintf('%-24s', 'Forma'); fprintf('%10s', cf_hdr{:}); fprintf('\n');
    for cf_f = 1:4
        fprintf('%-24s', cf_etiq{cf_f}); fprintf('%10.5f', cf_res(cf_f).(v)(cf_t)); fprintf('\n');
    end
    cf_dif = max(arrayfun(@(j) max(abs(cf_res(j).(v) - cf_res(1).(v))), 2:4));
    fprintf('Maxima diferencia con la forma 1: %.2e puntos porcentuales\n', cf_dif);
end
