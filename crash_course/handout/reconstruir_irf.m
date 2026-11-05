%% reconstruir_irf.m -- Reconstruye a mano las IRF de Dynare a partir de oo_.dr
%
%  Uso (desde la carpeta crash_course/handout):
%      >> dynare rbc_analytical
%      >> reconstruir_irf
%
%  A primer orden, la solucion de Dynare es
%      x_t - x_ss = ghx * (s_{t-1} - s_ss) + ghu * u_t,
%  donde s son los estados (k, a) y TODAS las filas de ghx y ghu estan en el
%  "orden DR" (oo_.dr.order_var), no en el orden en que se declararon las
%  variables. Este script propaga un choque de una desviacion estandar con
%  esas dos matrices y compara el resultado con oo_.irfs.
%
%  Inspirado en Galindo, Montecinos y Ortiz (2024), cap. 2, nota [3] de la
%  sec. 2.4.8, sobre el orden de las filas de oo_.dr.ghx y oo_.dr.ghu.

if ~exist('oo_', 'var') || ~isfield(oo_, 'dr')
    error('reconstruir_irf:sinSolucion', ...
          'No hay solucion en memoria. Corre antes:  dynare rbc_analytical');
end

dr   = oo_.dr;
iv   = dr.inv_order_var;            % declaracion -> fila en orden DR
est  = iv(dr.state_var);            % filas DR de los estados (k, a)
T    = options_.irf;                % horizonte (40)
n    = M_.endo_nbr;                 % numero de variables endogenas (8)

% ---- 1. Propagar el choque (todo en orden DR) ------------------------------
x = zeros(n, T);
x(:, 1) = dr.ghu * sqrt(M_.Sigma_e(1, 1));   % impacto: choque de 1 desv. est.
for t = 2:T
    x(:, t) = dr.ghx * x(est, t-1);          % solo los estados propagan
end

% ---- 2. Comparar con oo_.irfs, variable por variable -----------------------
nombres = M_.endo_names;
fprintf('\n%-6s %12s %12s %14s\n', 'Var.', 'Mi impacto', 'Dynare', 'Max |dif|');
for j = 1:n
    campo = [nombres{j} '_eps'];
    mia   = x(iv(j), :);                     % fila DR de la variable declarada j
    if isfield(oo_.irfs, campo)
        dyn = oo_.irfs.(campo);
    else
        dyn = zeros(1, T);                   % Dynare no guarda IRF nulas
    end
    fprintf('%-6s %12.6f %12.6f %14.2e\n', nombres{j}, mia(1), dyn(1), max(abs(mia - dyn)));
end

% ---- 3. El error tipico: leer ghx en orden de declaracion -------------------
fprintf('\nFila 2 de ghx (la "segunda" variable):     [%8.4f %8.4f]  <- es %s, no %s\n', ...
        dr.ghx(2, :), nombres{dr.order_var(2)}, nombres{2});
fprintf('Fila de %s en ghx, via inv_order_var:      [%8.4f %8.4f]\n', ...
        nombres{2}, dr.ghx(iv(2), :));
