// ============================================================================
//  Forma 3 de 4 -- LINEAL, desviaciones en NIVELES
//  Las variables son x_d = x - x_ss (la x con tilde del Cap. 2, sec. 2.4.1).
//  Las ecuaciones son la expansion de Taylor de primer orden en niveles,
//  hecha A MANO; model(linear) le dice a Dynare que no vuelva a linealizar.
//  El EE de todas las variables es 0. Debe dar exactamente la regla de
//  decision de la forma 1.
// ============================================================================
var y_d (long_name='producto, desv. en niveles')  c_d (long_name='consumo, desv. en niveles')
    i_d (long_name='inversion, desv. en niveles') k_d (long_name='capital, desv. en niveles')
    h_d (long_name='horas, desv. en niveles')     r_d (long_name='tasa de alquiler, desv. en niveles')
    w_d (long_name='salario, desv. en niveles')   a_d (long_name='productividad, desv. en niveles');
varexo eps (long_name='choque de productividad');

@#include "calibracion.inc"

model(linear);
  [name = 'Euler']                c_d = c_d(+1) - beta*c_ss*r_d(+1);
  [name = 'Oferta de trabajo']    (1 - hss)*w_d = theta*c_d + w_ss*h_d;
  [name = 'Demanda de capital']   r_d = (1 - alpha)*(y_d/k_ss - (y_ss/k_ss^2)*k_d(-1));
  [name = 'Demanda de trabajo']   w_d = alpha*(y_d/hss - (y_ss/hss^2)*h_d);
  [name = 'Produccion']           y_d = y_ss*a_d + (1 - alpha)*(y_ss/k_ss)*k_d(-1) + alpha*(y_ss/hss)*h_d;
  [name = 'Ley de movimiento']    k_d = (1 - delta)*k_d(-1) + i_d;
  [name = 'Vaciado de bienes']    y_d = c_d + i_d;
  [name = 'PTF']                  a_d = phi*a_d(-1) + sigma_eps*eps;
end;

steady_state_model;
  y_d = 0;  c_d = 0;  i_d = 0;  k_d = 0;  h_d = 0;  r_d = 0;  w_d = 0;  a_d = 0;
end;

shocks;  var eps; stderr 1;  end;

steady;  check;
stoch_simul(order = 1, irf = 40, graph_format = pdf) y_d c_d i_d k_d h_d r_d w_d a_d;
