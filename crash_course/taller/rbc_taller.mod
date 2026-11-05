// ============================================================================
//  rbc_taller.mod  --  el modelo RBC, hueco por hueco
//  Crash course de Dynare (Ventura & Echevarria). Dynare 7.1 (compatible 6.x).
//
//  TALLER: completa los huecos  ???  numerados [H1]...[H20], etapa por etapa,
//  en el orden de los bloques de un .mod (handout, sec. 3.2). Dynare solo corre
//  cuando no queda ningun  ???  activo: completa H1-H18 (etapas 1 a 4) y luego
//  avanza por los tres PUNTOS DE CONTROL de la etapa 5, corriendo cada vez
//      >> dynare rbc_taller
//  y comparando con README.md. Si Dynare se detiene en una linea con  ???,
//  te falta ese hueco.
//
//  El modelo (handout, Cap. 2):
//    Hogar:       max E0 sum_t beta^t [ ln c_t + theta*ln(1 - h_t) ]
//                 s.a. c_t + i_t = w_t h_t + r_t k_{t-1}
//    Firma:       y_t = a_t * k_{t-1}^(1-alpha) * h_t^alpha
//    Capital:     k_t = (1-delta) k_{t-1} + i_t
//    PTF:         ln a_t = phi ln a_{t-1} + sigma_eps eps_t,   eps_t ~ N(0,1)
//  Timing de Dynare: k es el capital ELEGIDO en t; k(-1) es el que se usa en t.
// ============================================================================

// ---- Interruptor de depreciacion (parte G.5 de la PD06) --------------------
//   dynare rbc_taller               -> delta = 0.025 (caso base)
//   dynare rbc_taller -DDELTA1=1    -> delta = 1     (Long-Plosser)
@#ifndef DELTA1
@#define DELTA1 = 0
@#endif

// ============================================================================
//  ETAPA 1. EL PREAMBULO: variables, choque y parametros    (handout 3.2.1)
// ============================================================================

// [H1] Declara las 8 variables endogenas, en este orden: producto y, consumo c,
//      inversion i, capital k, horas h, tasa de alquiler r, salario w y
//      productividad a. Opcional: un long_name para cada una.
var
    ???
;

// [H2] Declara el choque de productividad, eps.
varexo ???;

parameters alpha beta delta phi sigma_eps theta hss
           r_ss k_ss y_ss i_ss c_ss w_ss;

// ---- Calibracion: King y Rebelo (1999), economia trimestral ----------------
alpha     = 0.667;     // participacion del trabajo
beta      = 0.984;     // factor de descuento
@#if DELTA1 == 1
delta     = 1;         // depreciacion total
@#else
delta     = 0.025;     // caso base
@#endif
phi       = 0.979;     // persistencia de la PTF
sigma_eps = 0.0072;    // desviacion estandar del choque
hss       = 0.20;      // horas en estado estacionario (objetivo)

// ---- Estado estacionario en forma cerrada (handout 2.2; PD06, parte C) -----
// [H3] La Euler en estado estacionario despeja r_ss.
r_ss  = ???;
// [H4] De la demanda de capital y la produccion: k_ss en funcion de hss y r_ss.
k_ss  = ???;
y_ss  = k_ss^(1 - alpha)*hss^alpha;
// [H5] Ley de movimiento en estado estacionario.
i_ss  = ???;
// [H6] Vaciado del mercado de bienes en estado estacionario.
c_ss  = ???;
w_ss  = alpha*y_ss/hss;
// [H7] Calibra theta para que la oferta de trabajo se cumpla con h = hss.
theta = ???;

// ============================================================================
//  ETAPA 2. EL MODELO: 8 ecuaciones para 8 variables         (handout 3.2.2)
// ============================================================================
model;

// [H8] Euler: FOC del hogar respecto al capital. El retorno relevante es el
//      de MANANA.
[name = 'Euler']
1/c = ???;

// [H9] Oferta de trabajo: FOC del hogar respecto a las horas.
[name = 'Oferta de trabajo']
??? = w;

// [H10] Demanda de capital. Cuidado con el timing del capital.
[name = 'Demanda de capital']
r = (1 - alpha)*y/???;

// [H11] Demanda de trabajo.
[name = 'Demanda de trabajo']
w = ???;

// [H12] Funcion de produccion.
[name = 'Produccion']
y = a*???^(1 - alpha)*h^alpha;

// [H13] Ley de movimiento del capital.
[name = 'Ley de movimiento']
k = ???;

// [H14] Vaciado del mercado de bienes.
[name = 'Vaciado de bienes']
y = ???;

// [H15] Proceso de la PTF, en logaritmos.
[name = 'PTF']
log(a) = ???;

end;

// ============================================================================
//  ETAPA 3. EL ESTADO ESTACIONARIO                          (handout 3.2.3)
//  Dynare solo evalua estas expresiones: no resuelve nada.
// ============================================================================
steady_state_model;
// [H16] La productividad en estado estacionario (ojo: a, no ln a).
a = ???;
r = r_ss;
h = hss;
// [H17] Completa las cinco que faltan con los parametros de la Etapa 1.
k = ???;
y = ???;
i = ???;
c = ???;
w = ???;
end;

// ============================================================================
//  ETAPA 4. EL CHOQUE                                       (handout 3.2.4)
// ============================================================================
shocks;
// [H18] eps es N(0,1) y sigma_eps ya lo escala DENTRO de la ecuacion de la PTF.
var eps; stderr ???;
end;

// ============================================================================
//  ETAPA 5. CALCULO                                          (handout 3.2.5)
// ============================================================================
steady;     // PUNTO DE CONTROL 1: tabla STEADY-STATE RESULTS
resid;      //                      y residuos en 0.000000
// [H19] PUNTO DE CONTROL 2. Cuando el control 1 este bien, quita las // de la
//       linea siguiente y escribe el comando que calcula los valores propios
//       y verifica la condicion de Blanchard-Kahn.
// ???;

// [H20] PUNTO DE CONTROL 3. Quita las // y completa: solucion de PRIMER orden
//       e IRF de 40 periodos.
// stoch_simul(order = ???, irf = ???, graph_format = pdf) y c i k h r w a;

