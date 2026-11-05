// ============================================================================
//  calibracion.inc -- parametros y estado estacionario COMUNES a las cuatro
//  formas de escribir el modelo. Se incorpora en cada .mod con
//      @#include "calibracion.inc"
//  Un solo lugar para la calibracion: cambiar un valor aqui cambia las cuatro.
//  King y Rebelo (1999); delta = 1 corresponde a Long y Plosser (1983).
// ============================================================================
@#ifndef DELTA1
@#define DELTA1 = 0
@#endif

parameters alpha beta delta phi sigma_eps theta hss
           r_ss k_ss y_ss i_ss c_ss w_ss;

alpha     = 0.667;      // participacion del trabajo
beta      = 0.984;      // factor de descuento
@#if DELTA1 == 1
delta     = 1;          // depreciacion total (Long-Plosser)
@#else
delta     = 0.025;      // caso base
@#endif
phi       = 0.979;      // persistencia de la PTF
sigma_eps = 0.0072;     // desv. est. del choque
hss       = 0.20;       // horas en EE (objetivo)

// estado estacionario en forma cerrada (Cap. 2, sec. 2.2)
r_ss  = 1/beta - (1 - delta);
k_ss  = hss*((1 - alpha)/r_ss)^(1/alpha);
y_ss  = k_ss^(1 - alpha)*hss^alpha;
i_ss  = delta*k_ss;
c_ss  = y_ss - i_ss;
w_ss  = alpha*y_ss/hss;
theta = w_ss*(1 - hss)/c_ss;   // calibrado para que h_ss = 0.20
