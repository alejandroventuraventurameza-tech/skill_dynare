// ============================================================================
//  Forma 1 de 4 -- NO LINEAL, variables en NIVELES
//  Es el mismo modelo de rbc_analytical.mod. Dynare lo linealiza en niveles:
//  las IRF y la regla de decision estan en desviaciones respecto al EE
//  (x_t - x_ss), en las unidades de cada variable.
// ============================================================================
var y (long_name='producto')  c (long_name='consumo')  i (long_name='inversion')
    k (long_name='capital')   h (long_name='horas')    r (long_name='tasa de alquiler')
    w (long_name='salario')   a (long_name='productividad');
varexo eps (long_name='choque de productividad');

@#include "calibracion.inc"

model;
  [name = 'Euler']                1/c = beta*(1/c(+1))*(r(+1) + 1 - delta);
  [name = 'Oferta de trabajo']    theta*c/(1 - h) = w;
  [name = 'Demanda de capital']   r = (1 - alpha)*y/k(-1);
  [name = 'Demanda de trabajo']   w = alpha*y/h;
  [name = 'Produccion']           y = a*k(-1)^(1 - alpha)*h^alpha;
  [name = 'Ley de movimiento']    k = (1 - delta)*k(-1) + i;
  [name = 'Vaciado de bienes']    y = c + i;
  [name = 'PTF']                  log(a) = phi*log(a(-1)) + sigma_eps*eps;
end;

steady_state_model;
  a = 1;  r = r_ss;  h = hss;  k = k_ss;  y = y_ss;  i = i_ss;  c = c_ss;  w = w_ss;
end;

shocks;  var eps; stderr 1;  end;

steady;  check;
stoch_simul(order = 1, irf = 40, graph_format = pdf) y c i k h r w a;
