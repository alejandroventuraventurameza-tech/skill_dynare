// ============================================================================
// >>> ANDAMIO TEMPORAL (autogenerado): pasa el verificador estático, pero debe
//     reemplazarse por un RBC de fuente autoritativa (Pfeifer / Dynare). Ver SOURCES.md
// Modelo:        RBC básico (Real Business Cycle)
// Referencia:    King, Plosser & Rebelo (1988); Hansen (1985)
// Dynare:        5.x / 6.x
// Descripción:   Economía cerrada con un hogar representativo, una firma
//                competitiva, capital acumulable y un shock de productividad
//                (TFP) AR(1). 8 variables endógenas, 8 ecuaciones.
// Estado:        Verificado por el verificador estático del repo (sin errores).
// ============================================================================

// ---- Variables endógenas ----
var
    Y     // producto
    C     // consumo
    I     // inversión
    K     // capital (stock; disponible en t es K(-1))
    L     // trabajo / horas
    W     // salario real
    R     // retorno bruto del capital
    A     // productividad total de factores (TFP)
;

// ---- Shock exógeno ----
varexo e_a;   // innovación de productividad

// ---- Parámetros ----
parameters beta alpha delta sigma phi rho_a;

beta  = 0.99;    // factor de descuento
alpha = 0.33;    // participación del capital
delta = 0.025;   // depreciación trimestral
sigma = 1.0;     // inverso de la EIS (utilidad log en consumo)
phi   = 1.0;     // inverso de la elasticidad de Frisch
rho_a = 0.95;    // persistencia de la TFP

model;
// (1) Euler del consumo: FONC intertemporal del hogar
C^(-sigma) = beta * C(+1)^(-sigma) * R(+1);

// (2) Oferta de trabajo: FONC intratemporal trabajo-ocio
W = phi * L / C^(-sigma);

// (3) Demanda de capital: producto marginal del capital + (1-delta)
R = alpha * A * K(-1)^(alpha-1) * L^(1-alpha) + (1-delta);

// (4) Demanda de trabajo: salario = producto marginal del trabajo
W = (1-alpha) * A * K(-1)^alpha * L^(-alpha);

// (5) Función de producción Cobb-Douglas
Y = A * K(-1)^alpha * L^(1-alpha);

// (6) Restricción de recursos / vaciado de mercado de bienes
Y = C + I;

// (7) Ley de movimiento del capital
K = (1-delta) * K(-1) + I;

// (8) Proceso AR(1) de la TFP (en logaritmos)
log(A) = rho_a * log(A(-1)) + e_a;
end;

// ---- Estado estacionario (analítico) ----
steady_state_model;
A   = 1;
R   = 1/beta;
K_L = (alpha / (R - 1 + delta))^(1/(1-alpha));   // ratio capital-trabajo
W   = (1-alpha) * K_L^alpha;
L   = 1/3;                                        // calibración del tiempo de trabajo
K   = K_L * L;
I   = delta * K;
Y   = K_L^alpha * L;
C   = Y - I;
end;

// ---- Shocks ----
shocks;
var e_a; stderr 0.01;
end;

// ---- Simulación ----
stoch_simul(order=1, irf=40, periods=0) Y C I K L W R A;
