// ============================================================================
// Modelo:      RBC con Preferencias Barro-King
// Referencia:  Barro & King (1984); King, Plosser & Rebelo (1988)
//              Problem Set 2, Q3 — Macroeconomics III (130648)
//              Universidad del Pacífico, 2026-01
// Dynare:      6.x (compatible con 5.x)
// Descripción: Economía cerrada con capital acumulable, firma competitiva y
//              preferencias Barro-King: u(C,N) = ln(C) - χ N^{1+η}/(1+η).
//              Esta especificación separa la elasticidad Frisch (1/η) del
//              nivel de horas en estado estacionario.
//              9 variables endógenas, 9 ecuaciones.
//              Se corre dos veces: η=1 (Frisch=1) y η=2 (Frisch=0.5).
//
// Variables:   y c i k n w rk a prod
// Shock:       eps_a (productividad TFP, AR1)
// ============================================================================

// ---- Variables endógenas (9) ----
var
    y       // producto  Y_t = A_t K_t^α N_t^{1-α}
    c       // consumo privado
    i       // inversión
    k       // capital fin de período  K_{t+1}  [en modelo: k(-1) = K_t]
    n       // horas trabajadas
    w       // salario real  w_t = (1-α) Y_t / N_t
    rk      // retorno del capital  R^k_t = α Y_t / K_t
    a       // productividad TFP
    prod    // productividad laboral  Y_t/N_t  (para tabla de momentos)
;

// ---- Shock exógeno ----
varexo
    eps_a   // innovación de TFP  ~ N(0,1); desv. est. efectiva = sigma_e
;

// ---- Parámetros ----
parameters
    beta      // factor de descuento
    alpha     // participación del capital en producción
    delta     // tasa de depreciación trimestral
    rho       // persistencia del proceso AR(1) de TFP
    sigma_e   // desv. est. del shock de TFP
    eta       // elasticidad de Frisch inversa  (Frisch = 1/η)
    chi       // peso de la desutilidad del trabajo (calibrado para N̄ = 1/3)
    n_target  // target de horas en EE
    rk_ss     // retorno del capital en EE  (función de β, δ)
    kn        // ratio capital-trabajo en EE  K/N
    yn        // ratio producto-trabajo en EE  Y/N
    cn        // ratio consumo-trabajo en EE  C/N
;

// ============================================================================
// CALIBRACIÓN BASE  (Tabla Q3, PS2)
// Los ratios rk_ss, kn, yn, cn no dependen de η → se calculan una sola vez.
// chi depende de η → se recalcula antes de cada simulación.
// ============================================================================

alpha    = 0.33;
beta     = 0.995;
delta    = 0.025;
rho      = 0.979;
sigma_e  = 0.009;
n_target = 1/3;

// Ratios de estado estacionario (independientes de η)
// De la Euler en EE: R^k = 1/β - (1-δ)
rk_ss = 1/beta - (1 - delta);

// De R^k = α(K/N)^{α-1} → K/N = (R^k/α)^{1/(α-1)}
kn = (rk_ss/alpha)^(1/(alpha - 1));

// Y/N = (K/N)^α  con A=1
yn = kn^alpha;

// C/N = Y/N - δ·K/N  (de la restricción de recursos en EE)
cn = yn - delta*kn;

// chi se fijará antes de cada run (ver abajo)

// ============================================================================
// BLOQUE DE MODELO — 9 ecuaciones
// Convención Dynare: k = K_{t+1} (capital elegido al final de t)
//                   k(-1) = K_t  (capital disponible al inicio de t)
// ============================================================================
model;

// [1] Ecuación de Euler  (FOC intertemporal del hogar w.r.t. K_{t+1})
//     1/C_t = β E_t[(R^k_{t+1} + 1-δ) / C_{t+1}]
//     Con utilidad log en consumo → MU_C = 1/C
1/c = beta*(1/c(+1))*(rk(+1) + 1 - delta);

// [2] Oferta de trabajo  (FOC intratemporal w.r.t. N_t)
//     -χN_t^η + (1/C_t)·w_t = 0  →  χN_t^η = w_t/C_t
//     Barro-King: MU_N = χN^η, MU_C = 1/C
chi*n^eta = w/c;

// [3] Demanda de trabajo  (producto marginal del trabajo = salario)
//     w_t = (1-α) A_t K_t^α N_t^{-α} = (1-α) Y_t/N_t
w = (1 - alpha)*y/n;

// [4] Demanda de capital  (producto marginal del capital)
//     R^k_t = α A_t K_t^{α-1} N_t^{1-α} = α Y_t / K_t
//     Nota: K_t = k(-1) en notación Dynare
rk = alpha*y/k(-1);

// [5] Función de producción Cobb-Douglas
//     Y_t = A_t K_t^α N_t^{1-α}
y = a*k(-1)^alpha*n^(1 - alpha);

// [6] Ley de movimiento del capital
//     K_{t+1} = (1-δ)K_t + I_t
k = (1 - delta)*k(-1) + i;

// [7] Restricción de recursos  (vaciado del mercado de bienes)
//     Y_t = C_t + I_t   (economía cerrada, sin gobierno)
y = c + i;

// [8] Proceso AR(1) de la TFP en logaritmos
//     ln A_t = ρ ln A_{t-1} + σ_ε · ε_t,   ε_t ~ N(0,1)
log(a) = rho*log(a(-1)) + sigma_e*eps_a;

// [9] Productividad laboral  (variable auxiliar para momentos)
//     prod_t = Y_t / N_t
prod = y/n;

end;

// ============================================================================
// ESTADO ESTACIONARIO ANALÍTICO
// Derivación completa en Q3 parte (b):
//   - EE de Euler → R^k = 1/β-(1-δ)
//   - Firmas en EE → K/N, Y/N, C/N, w
//   - Labor supply en EE → N = n_target  (por construcción de χ)
// ============================================================================
steady_state_model;

// TFP normalizada a 1 en EE
a    = 1;

// Retorno del capital (de la Euler en EE)
rk   = rk_ss;

// Horas: fijadas al target (chi calibrado para que esto se cumpla exactamente)
n    = n_target;

// Capital, producto, consumo, inversión (usando ratios K/N, Y/N, C/N)
k    = kn*n;
y    = yn*n;
c    = cn*n;
i    = delta*k;

// Salario real en EE: w = (1-α)(Y/N)
w    = (1 - alpha)*y/n;

// Productividad laboral en EE
prod = y/n;

end;

// ============================================================================
// SHOCKS
// eps_a ~ N(0,1); la desv. est. efectiva está incorporada en sigma_e
// dentro de la ecuación [8]: log(a) = rho*log(a(-1)) + sigma_e*eps_a
// ============================================================================
shocks;
var eps_a; stderr 1;
end;

// ============================================================================
// ============================================================
//   SIMULACIÓN 1 — η = 1  (Elasticidad de Frisch = 1)
// ============================================================
// ============================================================================

// Calibrar χ para η=1 y N̄ = 1/3
// De χN^η = w/C en EE: χ = (1-α)·yn / (cn · N_target^{1+η})
eta = 1;
chi = (1 - alpha)*yn / (cn*n_target^(1 + eta));

resid;        // Muestra residuos del modelo en el EE (debe ser ≈ 0)
steady;       // Calcula y verifica el estado estacionario
check;        // Condición Blanchard-Kahn

// stoch_simul: orden 1, IRF de 50 períodos, log-linealización automática,
// filtro HP (λ=1600) para los momentos, salida en PDF
stoch_simul(order=1, irf=50, loglinear, hp_filter=1600, graph_format=pdf)
    y c i k n w rk prod;

// ============================================================================
// ============================================================
//   SIMULACIÓN 2 — η = 2  (Elasticidad de Frisch = 0.5)
// ============================================================
// ============================================================================

// Recalibrar χ para η=2  (N̄ = 1/3 sigue siendo el target)
// Con mayor η, la oferta de trabajo es menos elástica → χ es mayor
eta = 2;
chi = (1 - alpha)*yn / (cn*n_target^(1 + eta));

// Los ratios rk_ss, kn, yn, cn no cambian (no dependen de η)
// Solo cambian chi y eta → recalcular EE y BK
resid;
steady;
check;

stoch_simul(order=1, irf=50, loglinear, hp_filter=1600, graph_format=pdf)
    y c i k n w rk prod;
