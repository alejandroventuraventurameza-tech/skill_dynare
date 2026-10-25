// ============================================================================
//  rbc_analytical.mod
//  Modelo RBC con solución analítica — economía cerrada, con trabajo endógeno.
//  Compañero del handout "Un crash course de Dynare" (Ventura & Echevarría).
//  Calibración: King & Rebelo (1999).  Probado con Dynare 7.1 (compat. 6.x).
//
//  Hogar:        max  E0 Σ β^t [ ln c_t + θ ln(1 - h_t) ]     (Long-Plosser 1983)
//  Tecnología:   y_t = a_t · k_t^(1-α) · h_t^α                 (α = labor share)
//  TFP:          ln a_t = φ ln a_{t-1} + σ_ε ε_t,  ε_t ~ N(0,1)
//
//  8 variables endógenas, 8 ecuaciones.  θ no se fija: se calibra desde
//  h_ss = 0.20 con la oferta de trabajo en estado estacionario.
//  Con δ = 0.025 → θ ≈ 3.342389;  con δ = 1 (Long-Plosser) → θ ≈ 3.968301.
//
//  Convención de timing de Dynare ("stock al final del período"):
//      k      = capital elegido en t          (= k_{t+1} del papel)
//      k(-1)  = capital en uso al inicio de t  (= k_t    del papel)
//
//  Estilo (ver §"Estilo" del handout): nombres cortos por legibilidad en este
//  material introductorio. En código de producción conviene la convención de
//  Marco Ortiz —parámetros en MAYÚSCULAS con inicial duplicada (AALPHA, BBETA,
//  DDELTA)— para evitar colisiones con funciones de MATLAB (beta, gamma).
// ============================================================================

// ---- Interruptor de depreciación (para el ejercicio δ=1) -------------------
//   DELTA1 = 0  → δ = 0.025  (caso base)
//   DELTA1 = 1  → δ = 1      (depreciación total; θ se recalibra solo)
@#define DELTA1 = 0

// ---- Variables endógenas (8) ----------------------------------------------
var
    y  (long_name='producto')
    c  (long_name='consumo')
    i  (long_name='inversión')
    k  (long_name='capital (fin de período)')
    h  (long_name='horas trabajadas')
    r  (long_name='tasa de alquiler del capital')
    w  (long_name='salario real')
    a  (long_name='productividad total de factores')
;

// ---- Choque exógeno --------------------------------------------------------
varexo
    eps (long_name='innovación de productividad, N(0,1)')
;

// ---- Parámetros ------------------------------------------------------------
parameters
    alpha       // participación del trabajo en el producto (labor share)
    beta        // factor de descuento
    delta       // tasa de depreciación del capital
    phi         // persistencia del AR(1) de la TFP
    sigma_eps   // desv. est. de la innovación de productividad
    theta       // peso del ocio en la utilidad (CALIBRADO desde h_ss)
    hss         // horas en estado estacionario (objetivo de calibración)
    // --- valores de estado estacionario en forma cerrada ---
    r_ss k_ss y_ss i_ss c_ss w_ss
;

// ============================================================================
//  CALIBRACIÓN  (King & Rebelo, 1999 — economía trimestral)
// ============================================================================
alpha     = 0.667;      // labor share (King-Rebelo 1999)
beta      = 0.984;      // discount factor (King-Rebelo 1999)
@#if DELTA1 == 1
delta     = 1;          // depreciación total (Long-Plosser 1983)
@#else
delta     = 0.025;      // caso base (King-Rebelo 1999)
@#endif
phi       = 0.979;      // persistencia de la TFP (King-Rebelo 1999)
sigma_eps = 0.0072;     // desv. est. del choque de productividad (King-Rebelo 1999)
hss       = 0.20;       // horas en EE (objetivo de calibración)

// ---- Estado estacionario analítico -----------------------------------------
// a_ss = 1 (⇒ ln a_ss = 0). Los niveles de EE NO dependen de θ, así que se
// calculan primero y luego la oferta de trabajo despeja θ.
//   Euler en EE:        r_ss = 1/β - (1-δ)
//   Demanda de capital: y_ss/k_ss = r_ss/(1-α)
//   Producción:         k_ss = h_ss · [(1-α)/r_ss]^(1/α)
r_ss = 1/beta - (1 - delta);
k_ss = hss*((1 - alpha)/r_ss)^(1/alpha);
y_ss = k_ss^(1 - alpha)*hss^alpha;
i_ss = delta*k_ss;                      // ley de movimiento en EE
c_ss = y_ss - i_ss;                     // vaciado de mercado en EE
w_ss = alpha*y_ss/hss;                  // demanda de trabajo en EE

// ---- Calibración endógena de θ ---------------------------------------------
//   Oferta de trabajo en EE:  θ·c_ss/(1-h_ss) = w_ss  ⇒  θ = w_ss(1-h_ss)/c_ss
theta = w_ss*(1 - hss)/c_ss;

// ============================================================================
//  BLOQUE DEL MODELO — 8 ecuaciones
// ============================================================================
model;

[name = 'Euler (FOC hogar, capital)']
1/c = beta*(1/c(+1))*(r(+1) + 1 - delta);

[name = 'Oferta de trabajo (FOC hogar, horas)']
theta*c/(1 - h) = w;

[name = 'Demanda de capital (FOC firma)']
r = (1 - alpha)*y/k(-1);

[name = 'Demanda de trabajo (FOC firma)']
w = alpha*y/h;

[name = 'Función de producción']
y = a*k(-1)^(1 - alpha)*h^alpha;

[name = 'Ley de movimiento del capital']
k = (1 - delta)*k(-1) + i;

[name = 'Vaciado del mercado de bienes']
y = c + i;

[name = 'Proceso AR(1) de la TFP (en logs)']
log(a) = phi*log(a(-1)) + sigma_eps*eps;

end;

// ============================================================================
//  ESTADO ESTACIONARIO ANALÍTICO
//  (mapea los valores cerrados a las variables del modelo; Dynare no resuelve
//   nada numéricamente, solo evalúa)
// ============================================================================
steady_state_model;
a = 1;
r = r_ss;
h = hss;
k = k_ss;
y = y_ss;
i = i_ss;
c = c_ss;
w = w_ss;
end;

// ============================================================================
//  SHOCKS
//  eps está estandarizado ~ N(0,1); sigma_eps escala el choque DENTRO de la
//  ecuación de la TFP. Resultado idéntico a declarar 'stderr sigma_eps'.
// ============================================================================
shocks;
var eps; stderr 1;
end;

// ============================================================================
//  REPRODUCIBILIDAD
//  Fija la semilla para que las simulaciones sean replicables bit a bit.
// ============================================================================
set_dynare_seed(123);

// ============================================================================
//  RESOLUCIÓN Y DIAGNÓSTICOS
//    steady → resid → check → stoch_simul   (de lo más básico a lo más fino)
// ============================================================================
steady;     // calcula el EE (debe coincidir con la Tabla del estado estacionario)
resid;      // residuos de cada ecuación en el EE (deben ser ≈ 0.000000)
check;      // valores propios + condición de Blanchard-Kahn

// Primer orden (log-linealización), IRFs de 40 períodos a un choque de 1 s.d.
// y momentos teóricos. Para momentos del CICLO (comparables con datos) añadir
// hp_filter=1600. graph_format=pdf evita el bug de exportación a .eps de
// varias versiones de MATLAB.
stoch_simul(order = 1, irf = 40, graph_format = pdf) y c i k h r w a;
