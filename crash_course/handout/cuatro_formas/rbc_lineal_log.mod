// ============================================================================
//  Forma 4 de 4 -- LINEAL, desviaciones LOGARITMICAS
//  Las variables son x_h = ln(x/x_ss) (la x con gorro del Cap. 2): es,
//  literalmente, el sistema log-lineal (2.25)-(2.32) del handout.
//  model(linear): Dynare no linealiza. El EE de todas las variables es 0.
//  Debe dar exactamente la regla de decision de la forma 2.
// ============================================================================
var y_h (long_name='producto, desv. log')  c_h (long_name='consumo, desv. log')
    i_h (long_name='inversion, desv. log') k_h (long_name='capital, desv. log')
    h_h (long_name='horas, desv. log')     r_h (long_name='tasa de alquiler, desv. log')
    w_h (long_name='salario, desv. log')   a_h (long_name='productividad, desv. log');
varexo eps (long_name='choque de productividad');

@#include "calibracion.inc"

parameters s_c s_i;          // participaciones del consumo y la inversion en y
s_c = c_ss/y_ss;
s_i = i_ss/y_ss;

model(linear);
  [name = 'Euler']                c_h(+1) - c_h = beta*r_ss*r_h(+1);
  [name = 'Oferta de trabajo']    c_h + (hss/(1 - hss))*h_h = w_h;
  [name = 'Demanda de capital']   r_h = y_h - k_h(-1);
  [name = 'Demanda de trabajo']   w_h = y_h - h_h;
  [name = 'Produccion']           y_h = a_h + (1 - alpha)*k_h(-1) + alpha*h_h;
  [name = 'Ley de movimiento']    k_h = (1 - delta)*k_h(-1) + delta*i_h;
  [name = 'Vaciado de bienes']    y_h = s_c*c_h + s_i*i_h;
  [name = 'PTF']                  a_h = phi*a_h(-1) + sigma_eps*eps;
end;

steady_state_model;
  y_h = 0;  c_h = 0;  i_h = 0;  k_h = 0;  h_h = 0;  r_h = 0;  w_h = 0;  a_h = 0;
end;

shocks;  var eps; stderr 1;  end;

steady;  check;
stoch_simul(order = 1, irf = 40, graph_format = pdf) y_h c_h i_h k_h h_h r_h w_h a_h;
