// ============================================================================
//  Modelo:      RBC con solución analítica  (economía cerrada, con trabajo)
//  Curso:       Macroeconomía II — Recitation 01, parte (G) "Beyond the blackboard"
//  Autoría:     Ventura & Echevarría
//  Calibración: King & Rebelo (1999)
//  Dynare:      7.0  (compatible con 6.x)
//
//  Hogar representativo:   max  E0 Σ β^t [ ln c_t + θ ln(1 - h_t) ]
//  Tecnología:             y_t = a_t · k_t^(1-α) · h_t^α        (α = labor share)
//  TFP:                    ln a_t = φ ln a_{t-1} + ε_t,  ε_t ~ N(0, σ_ε²)
//
//  8 variables endógenas, 8 ecuaciones.
//  θ NO se fija externamente: se calibra desde h_ss = 0.20 usando la oferta
//  de trabajo en estado estacionario (parte C).  Con δ=0.025 → θ≈3.342389;
//  con δ=1 → θ≈3.968301.
//
//  Convención de timing (Dynare, "stock al final del período"):
//      k        = capital elegido en t  (= k_{t+1} del enunciado)
//      k(-1)    = capital disponible al inicio de t  (= k_t del enunciado)
// ============================================================================

// ---- Interruptor de depreciación (parte G) --------------------------------
// DELTA1 = 0  → δ = 0.025  (caso base, G.1–G.4)
// DELTA1 = 1  → δ = 1      (depreciación total, G.5; θ se recalibra solo)
@#define DELTA1 = 0

// ---- Variables endógenas (8) ----------------------------------------------
var
    y       // producto
    c       // consumo
    i       // inversión
    k       // capital (fin de período; k(-1) = capital en uso hoy)
    h       // horas trabajadas
    r       // tasa real de alquiler del capital  (MPK)
    w       // salario real
    a       // productividad total de factores (TFP)
;

// ---- Shock exógeno ----------------------------------------------------------
varexo
    eps     // innovación de productividad,  eps ~ N(0, sigma_eps^2)
;

// ---- Parámetros -------------------------------------------------------------
parameters
    alpha       // participación del trabajo en producción (labor share)
    beta        // factor de descuento
    delta       // tasa de depreciación del capital
    phi         // persistencia del AR(1) de la TFP
    sigma_eps   // desv. est. de la innovación de productividad
    theta       // peso del ocio en utilidad  (CALIBRADO desde h_ss)
    hss         // target de horas en EE
    // --- valores de estado estacionario (forma cerrada, parte C) ---
    r_ss k_ss y_ss i_ss c_ss w_ss
;

// ============================================================================
//  CALIBRACIÓN  (King & Rebelo, 1999)
// ============================================================================
alpha     = 0.667;      // labor share
beta      = 0.984;      // discount factor
@#if DELTA1 == 1
delta     = 1;          // depreciación total (G.5)
@#else
delta     = 0.025;      // caso base (G.1–G.4)
@#endif
phi       = 0.979;      // persistencia de la TFP
sigma_eps = 0.0072;     // desv. est. del shock de productividad
hss       = 0.20;       // horas en EE (target de calibración)

// ---- Estado estacionario analítico (parte C) -------------------------------
// a_ss = 1  ⇒  ln a_ss = 0.  Los valores de EP NO dependen de θ, de modo que
// se calculan primero y luego se usa la oferta de trabajo para despejar θ.
//
//   Euler en EE:           r_ss = 1/β - (1-δ)
//   Demanda de capital:    r_ss = (1-α) y_ss / k_ss   ⇒   y_ss/k_ss = r_ss/(1-α)
//   Producción:            y_ss/k_ss = (h_ss/k_ss)^α  ⇒   k_ss = h_ss·[(1-α)/r_ss]^(1/α)
r_ss = 1/beta - (1 - delta);
k_ss = hss*((1 - alpha)/r_ss)^(1/alpha);
y_ss = k_ss^(1 - alpha)*hss^alpha;
i_ss = delta*k_ss;                      // de la ley de movimiento en EE
c_ss = y_ss - i_ss;                     // del vaciado de mercado en EE
w_ss = alpha*y_ss/hss;                  // demanda de trabajo en EE

// ---- Calibración endógena de θ (parte G) -----------------------------------
// Oferta de trabajo en EE:   θ·c_ss/(1 - h_ss) = w_ss   ⇒   θ = w_ss(1 - h_ss)/c_ss
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
log(a) = phi*log(a(-1)) + eps;

end;

// ============================================================================
//  ESTADO ESTACIONARIO ANALÍTICO
//  (mapea los valores cerrados de la parte C a las variables del modelo)
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
//  ε_t ~ N(0, σ_ε²).  La desv. est. entra directo en el bloque shocks.
// ============================================================================
shocks;
var eps; stderr sigma_eps;
end;

// ============================================================================
//  RESOLUCIÓN Y DIAGNÓSTICOS
// ============================================================================
steady;     // calcula el EE (debe coincidir con la parte C)
resid;      // residuos de cada ecuación en el EE (deben ser ≈ 0)
check;      // valores propios + condición de Blanchard-Kahn

// Primer orden (log-linealización), IRFs de 40 períodos a un shock de 1 s.d.
// y momentos teóricos (periods=0 por defecto).
// Para momentos de ciclo económico (comparables con datos) añadir hp_filter=1600.
stoch_simul(order = 1, irf = 40) y c i k h r w a;
