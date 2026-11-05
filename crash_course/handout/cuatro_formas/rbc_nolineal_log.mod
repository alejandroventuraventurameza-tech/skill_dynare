// ============================================================================
//  Forma 2 de 4 -- NO LINEAL, variables en LOGARITMOS
//  Cada variable es el logaritmo de la original: lx = ln(x). Donde aparecia x
//  se escribe exp(lx). Dynare linealiza en lx, de modo que las IRF y la regla
//  de decision estan en desviaciones LOGARITMICAS (x 100 = % respecto al EE):
//  las mismas unidades que las variables con gorro del Cap. 2.
// ============================================================================
var ly (long_name='ln producto')  lc (long_name='ln consumo')  li (long_name='ln inversion')
    lk (long_name='ln capital')   lh (long_name='ln horas')    lr (long_name='ln tasa de alquiler')
    lw (long_name='ln salario')   la (long_name='ln productividad');
varexo eps (long_name='choque de productividad');

@#include "calibracion.inc"

model;
  [name = 'Euler']                1/exp(lc) = beta*(1/exp(lc(+1)))*(exp(lr(+1)) + 1 - delta);
  [name = 'Oferta de trabajo']    theta*exp(lc)/(1 - exp(lh)) = exp(lw);
  [name = 'Demanda de capital']   exp(lr) = (1 - alpha)*exp(ly)/exp(lk(-1));
  [name = 'Demanda de trabajo']   exp(lw) = alpha*exp(ly)/exp(lh);
  [name = 'Produccion']           exp(ly) = exp(la)*exp(lk(-1))^(1 - alpha)*exp(lh)^alpha;
  [name = 'Ley de movimiento']    exp(lk) = (1 - delta)*exp(lk(-1)) + exp(li);
  [name = 'Vaciado de bienes']    exp(ly) = exp(lc) + exp(li);
  [name = 'PTF']                  la = phi*la(-1) + sigma_eps*eps;
end;

// en logaritmos, el EE es el logaritmo del EE en niveles (y ln a_ss = 0)
steady_state_model;
  la = 0;  lr = log(r_ss);  lh = log(hss);  lk = log(k_ss);
  ly = log(y_ss);  li = log(i_ss);  lc = log(c_ss);  lw = log(w_ss);
end;

shocks;  var eps; stderr 1;  end;

steady;  check;
stoch_simul(order = 1, irf = 40, graph_format = pdf) ly lc li lk lh lr lw la;
