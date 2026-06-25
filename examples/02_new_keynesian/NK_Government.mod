// ============================================================================
// Modelo:      New-Keynesian con Gobierno y Dinero (cashless limit)
// Referencia:  Galí (2015) Ch.3 + extensión con gasto fiscal AR(1)
//              Problem Set 2, Q4 — Macroeconomics III (130648)
//              Universidad del Pacífico, 2026-01
// Dynare:      6.x (compatible con 5.x)
// Descripción: Economía cerrada sin capital. Hogar CRRA con saldos reales.
//              Firmas intermedias con tecnología lineal en trabajo y fijación
//              de precios Calvo. Gobierno financia gasto con impuesto de suma fija.
//              Banco central controla crecimiento monetario (AR1).
//              15 variables endógenas, 15 ecuaciones.
//
// Variables:   C N Y w mc Pi p_star Xh1 Xh2 it mt vP A gM G
// Shocks:      eps_A (tecnología), eps_M (monetario), eps_G (gasto fiscal)
//
// Estado estacionario: analítico (steady_state_model), basado en derivaciones
//              del alumno (Q4_Derivaciones_Detalladas.pdf).
// ============================================================================

// ---- Variables endógenas (15) ----
var
    C       // consumo privado
    N       // horas trabajadas (sin cota superior — spec. Barro-King)
    Y       // producto agregado
    w       // salario real  w ≡ W/P
    mc      // costo marginal real  mc = w/A
    Pi      // inflación bruta  Π ≡ P_t / P_{t-1}
    p_star  // precio de reset relativo  p# ≡ P#/P
    Xh1     // suma recursiva normalizada X̂₁ ≡ X₁/Pᵉ
    Xh2     // suma recursiva normalizada X̂₂ ≡ X₂/P^{ε-1}
    it      // tasa de interés nominal (neta)
    mt      // saldos reales  m ≡ M/P
    vP      // dispersión de precios  v^P ≡ ∫(P_i/P)^{-ε}di
    A       // productividad agregada (TFP)
    gM      // tasa de crecimiento monetario  g^M ≡ ln(M_t)-ln(M_{t-1})
    G       // gasto público real
;

// ---- Shocks exógenos ----
varexo
    eps_A   // innovación de tecnología
    eps_M   // innovación monetaria
    eps_G   // innovación de gasto fiscal
;

// ---- Parámetros ----
parameters
    beta    // factor de descuento
    sigma   // curvatura CRRA (inverso EIS)
    chi     // elasticidad de Frisch inversa (en labor supply)
    theta   // peso de la desutilidad del trabajo
    epsilon // elasticidad de sustitución entre variedades  ε > 1
    phi     // probabilidad de no ajuste Calvo  φ ∈ (0,1)
    psi     // peso de saldos reales en utilidad
    rho_A   // persistencia de tecnología
    sA      // desv. est. del shock de tecnología
    rho_M   // persistencia del crecimiento monetario
    sM      // desv. est. del shock monetario
    gMbar   // media del crecimiento monetario  ḡ^M
    gs      // participación del gasto público en Y  G̅/Ȳ
    rho_G   // persistencia del gasto de gobierno
    sG      // desv. est. del shock fiscal
;

// ---- Calibración (Tabla Q4, PS2) ----
beta    = 0.99;
sigma   = 1;
chi     = 1;
theta   = 1;
epsilon = 11;
phi     = 0.75;
psi     = 1;
rho_A   = 0.9;
sA      = 0.01;
rho_M   = 0.5;
sM      = 0.01;
gMbar   = 0.005;
gs      = 0.20;
rho_G   = 0.9;
sG      = 0.01;

// ============================================================================
// BLOQUE DE MODELO — 15 ecuaciones
// Notación: (+1) = expectativa en t de variable en t+1
//           (-1) = valor determinado en t-1
// ============================================================================
model;

// [1] Ecuación de Euler (bonos nominales)
//     C^{-σ} = β(1+i_t) E_t[C_{t+1}^{-σ} / Π_{t+1}]
C^(-sigma) = beta*(1+it)*C(+1)^(-sigma)/Pi(+1);

// [2] Oferta de trabajo (labor supply)
//     θ N^χ = C^{-σ} w_t   (FOC del hogar w.r.t. N)
theta*N^chi = C^(-sigma)*w;

// [3] Demanda de dinero
//     ψ/m_t = C^{-σ} · i_t/(1+i_t)   (costo de oportunidad del dinero)
psi/mt = C^(-sigma)*it/(1+it);

// [4] Costo marginal real
//     mc_t = w_t / A_t   (tecnología lineal → MC nominal = W/A)
mc = w/A;

// [5] Precio óptimo de reset relativo
//     p#_t = [ε/(ε-1)] · X̂₁_t / X̂₂_t
p_star = (epsilon/(epsilon-1))*Xh1/Xh2;

// [6] Suma recursiva X̂₁ (numerador del precio óptimo)
//     X̂₁_t = C_t^{-σ} mc_t Y_t + βφ E_t[Π_{t+1}^ε X̂₁_{t+1}]
Xh1 = C^(-sigma)*mc*Y + beta*phi*Pi(+1)^epsilon*Xh1(+1);

// [7] Suma recursiva X̂₂ (denominador del precio óptimo)
//     X̂₂_t = C_t^{-σ} Y_t + βφ E_t[Π_{t+1}^{ε-1} X̂₂_{t+1}]
Xh2 = C^(-sigma)*Y + beta*phi*Pi(+1)^(epsilon-1)*Xh2(+1);

// [8] Índice de precios Calvo (condición de agregación)
//     1 = (1-φ)(p#_t)^{1-ε} + φ Π_t^{ε-1}
1 = (1-phi)*p_star^(1-epsilon) + phi*Pi^(epsilon-1);

// [9] Dispersión de precios (acumulación)
//     v^P_t = (1-φ)(p#_t)^{-ε} + φ Π_t^ε v^P_{t-1}
vP = (1-phi)*p_star^(-epsilon) + phi*Pi^epsilon*vP(-1);

// [10] Función de producción agregada (con ineficiencia de dispersión)
//      A_t N_t = Y_t v^P_t
A*N = Y*vP;

// [11] Restricción de recursos (vaciado mercado de bienes)
//      Y_t = C_t + G_t   (sin capital ni inversión)
Y = C + G;

// [12] Ecuación de balances reales
//      g^M_t = ln(m_t) - ln(m_{t-1}) + ln(Π_t)
gM = log(mt) - log(mt(-1)) + log(Pi);

// [13] Proceso AR(1) de tecnología (en logaritmos)
//      ln A_t = ρ_A ln A_{t-1} + s_A ε_{A,t}
log(A) = rho_A*log(A(-1)) + sA*eps_A;

// [14] Proceso AR(1) del crecimiento monetario
//      g^M_t = (1-ρ_M)ḡ^M + ρ_M g^M_{t-1} + s_M ε_{M,t}
gM = (1-rho_M)*gMbar + rho_M*gM(-1) + sM*eps_M;

// [15] Proceso AR(1) del gasto de gobierno (en logaritmos)
//      ln G_t = (1-ρ_G)ln Ḡ + ρ_G ln G_{t-1} + s_G ε_{G,t}
log(G) = (1-rho_G)*log(steady_state(G)) + rho_G*log(G(-1)) + sG*eps_G;

end;

// ============================================================================
// ESTADO ESTACIONARIO ANALÍTICO
// Derivado en Q4_Derivaciones_Detalladas.pdf, Sección 3 (Partes b-i a b-v)
// ============================================================================
steady_state_model;

// [b-i] Inflación de largo plazo y tasa nominal (Fisher)
//   Π = exp(ḡ^M),   1+i = Π/β
Pi   = exp(gMbar);
it   = Pi/beta - 1;
gM   = gMbar;
A    = 1;

// [b-ii] Precio de reset relativo y dispersión de precios en EE
//   p# = [(1 - φΠ^{ε-1})/(1-φ)]^{1/(1-ε)}
//   v^P = (1-φ)(p#)^{-ε} / (1 - φΠ^ε)
p_star = ((1 - phi*Pi^(epsilon-1))/(1-phi))^(1/(1-epsilon));
vP     = (1-phi)*p_star^(-epsilon)/(1 - phi*Pi^epsilon);

// [b-iii] Costo marginal real y salario (con A=1 → w=mc)
//   mc = [(ε-1)/ε] · p# · (1-βφΠ^ε)/(1-βφΠ^{ε-1})
mc = (epsilon-1)/epsilon * p_star * (1-beta*phi*Pi^epsilon)/(1-beta*phi*Pi^(epsilon-1));
w  = mc;

// [b-iv] Producto, consumo, empleo, gasto
//   Y = [mc / (θ v^{Pχ} (1-g_s)^σ)]^{1/(χ+σ)}
//   C = (1-g_s)Y,   N = Y v^P,   G = g_s Y
Y = (mc/(theta*vP^chi*(1-gs)^sigma))^(1/(chi+sigma));
C = (1-gs)*Y;
G = gs*Y;
N = Y*vP;

// [b-v] Sumas recursivas normalizadas y saldos reales
//   X̂₁ = C^{-σ} mc Y / (1-βφΠ^ε)
//   X̂₂ = C^{-σ} Y / (1-βφΠ^{ε-1})
//   m   = ψ(1+i) / [C^{-σ} · i]
Xh1 = C^(-sigma)*mc*Y/(1 - beta*phi*Pi^epsilon);
Xh2 = C^(-sigma)*Y/(1 - beta*phi*Pi^(epsilon-1));
mt  = psi*(1+it)/(C^(-sigma)*it);

end;

// ============================================================================
// SHOCKS
// Los parámetros sA, sM, sG escalan la desv. est. en las ecuaciones del modelo.
// stderr 1 → las innovaciones son N(0,1) y la desv. est. efectiva = s* × 1.
// ============================================================================
shocks;
var eps_A; stderr 1;
var eps_M; stderr 1;
var eps_G; stderr 1;
end;

// ============================================================================
// VERIFICACIÓN Y SIMULACIÓN
// steady  → calcula y verifica el estado estacionario analítico
// check   → verifica condición Blanchard-Kahn
// stoch_simul → perturbación de primer orden, IRFs de 50 períodos
// ============================================================================
steady;
check;

stoch_simul(order=1, irf=50, graph_format=pdf) Y C N Pi it mc w vP mt G;
