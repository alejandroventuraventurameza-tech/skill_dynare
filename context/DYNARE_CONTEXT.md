# Dynare — Contexto para LLMs

Este archivo es el punto de entrada para que un LLM entienda cómo funciona Dynare y pueda generar código correcto. Se irá ampliando con cada sesión de trabajo.

---

## ¿Qué es Dynare?

Dynare es un preprocesador y conjunto de rutinas para MATLAB/Octave (y también Julia) diseñado para resolver, simular y estimar modelos de equilibrio general dinámico estocástico (DSGE). Su sintaxis es declarativa: el usuario describe las ecuaciones del modelo, y Dynare resuelve el sistema.

**Versiones relevantes:** 4.x, 5.x, 6.x (este repo apunta a 5.x/6.x).

---

## Estructura de un archivo `.mod`

Un archivo Dynare tiene bloques bien definidos que SIEMPRE aparecen en este orden:

```
1. var           — variables endógenas
2. varexo        — variables exógenas (shocks)
3. varexo_det    — variables exógenas determinísticas (opcional)
4. parameters    — parámetros del modelo
5. model;        — bloque de ecuaciones
   ...
   end;
6. initval;      — valores iniciales / estado estacionario (opcional)
   ...
   end;
7. steady_state_model;  — estado estacionario analítico (opcional pero recomendado)
   ...
   end;
8. shocks;       — varianzas/covarianzas de los shocks
   ...
   end;
9. Comandos de simulación/estimación (stoch_simul, estimation, etc.)
```

---

## Bloque `var`

Declara todas las variables endógenas del modelo. Las variables pueden ser en niveles, logaritmos, o desviaciones del estado estacionario — el usuario decide la interpretación.

```dynare
var Y C I K L W R A;
```

**Regla crítica:** TODA variable que aparece en el bloque `model` debe estar declarada en `var` (o `varexo`). Si no, Dynare dará error.

**Notación temporal:**
- `X` = valor en el período t (presente)
- `X(-1)` = valor en t-1 (período anterior)
- `X(+1)` = valor en t+1 (esperanza en t del valor en t+1)

---

## Bloque `varexo`

Declara los shocks exógenos del modelo.

```dynare
varexo e_a e_g e_m;
```

Los shocks son innovaciones i.i.d. con media cero. Su varianza se especifica en el bloque `shocks`.

---

## Bloque `parameters`

Declara y **asigna** los valores de los parámetros. La asignación puede ir en este mismo bloque o fuera de él.

```dynare
parameters beta alpha delta rho_a sigma_a;

beta  = 0.99;
alpha = 0.33;
delta = 0.025;
rho_a = 0.90;
sigma_a = 0.01;
```

**Error común:** Declarar un parámetro pero olvidar asignarle un valor. Dynare puede ejecutar sin error aparente pero los resultados serán incorrectos (el parámetro valdrá 0).

---

## Bloque `model`

Es el corazón del archivo. Contiene todas las ecuaciones del modelo en forma implícita (= 0 implícito, o con `=`).

```dynare
model;

// Ecuación de Euler del consumidor
C^(-sigma) = beta * C(+1)^(-sigma) * (1 + R(+1) - delta);

// Condición de primer orden del trabajo
W = chi * L^(eta) / C^(-sigma);

// Restricción de recursos
Y = C + I;

// Función de producción
Y = A * K(-1)^alpha * L^(1-alpha);

// Ley de movimiento del capital
K = (1 - delta) * K(-1) + I;

// Proceso AR(1) para la productividad
log(A) = rho_a * log(A(-1)) + e_a;

end;
```

**Reglas críticas del bloque model:**
1. El número de ecuaciones DEBE ser igual al número de variables endógenas (`var`).
2. Cada ecuación termina con `;`
3. `//` es comentario de una línea; `/* ... */` es comentario multilínea
4. Las expectativas se escriben con `(+1)`: `X(+1)` = E_t[X_{t+1}]
5. Los rezagos se escriben con `(-1)`: `X(-1)` = X_{t-1}
6. Dynare NO distingue entre mayúsculas y minúsculas en versiones antiguas — mejor usar nombres consistentes.

**Errores comunes en el bloque model:**
- Usar `exp()` / `log()` de forma inconsistente (si trabajas con log-linealización manual vs. niveles)
- Olvidar que las variables de stock (K, B) tienen un período de rezago: `K(-1)` es el capital disponible en t
- Confundir `R` (tasa de retorno bruta) con `r` (tasa neta): si `R = 1 + r`, la Euler es `1 = beta * (C(+1)/C)^(-sigma) * R(+1)` no `(1 + r(+1))`
- Escribir el lado derecho de una ecuación sin igualar: `Y = C + I` es correcto; `Y - C - I` también funciona (Dynare asume `= 0`)

---

## Bloque `steady_state_model`

Permite especificar el estado estacionario analíticamente. Esto es mucho más robusto que dejar que Dynare lo resuelva numéricamente.

```dynare
steady_state_model;

A    = 1;
R    = 1/beta;
mc   = (epsilon - 1) / epsilon;     // markup en NK
K_Y  = alpha / (R - 1 + delta);     // ratio capital-producto
I_Y  = delta * K_Y;
C_Y  = 1 - I_Y;
Y    = (K_Y^alpha)^(1/(1-alpha));
K    = K_Y * Y;
I    = I_Y * Y;
C    = C_Y * Y;
L    = Y / K^alpha;                  // de la función de producción
W    = (1 - alpha) * Y / L;

end;
```

**Reglas:**
- Las variables deben asignarse en orden (primero las que no dependen de otras)
- Aquí las variables son valores de estado estacionario, sin notación temporal
- Si el estado estacionario es en logaritmos, recuerda que `log(X_ss) = 0` si `X_ss = 1`

---

## Bloque `shocks`

Especifica la varianza (o covarianza) de los shocks.

```dynare
shocks;

var e_a;
stderr 0.01;    // desviación estándar del shock de productividad

var e_m;
stderr 0.0025;  // shock de política monetaria

// Para una matriz de varianza-covarianza:
// var e_a, e_g = 0.0001;  // covarianza entre e_a y e_g

end;
```

**Nota:** `stderr` especifica la desviación estándar. También se puede usar `var` para especificar la varianza directamente.

---

## Comando `stoch_simul`

El comando principal para simular un modelo DSGE estocástico. Resuelve el modelo y calcula momentos, IRFs, etc.

```dynare
stoch_simul(order=1, irf=20, periods=0);
```

**Opciones más usadas:**
- `order=1` — aproximación de primer orden (log-lineal). `order=2` para segundo orden.
- `irf=20` — calcular IRFs de 20 períodos
- `periods=0` — no hacer simulación estocástica (solo momentos analíticos)
- `periods=500` — simular 500 períodos
- `hp_filter=1600` — aplicar filtro HP con lambda=1600
- `nograph` — no mostrar gráficos
- `noprint` — no imprimir resultados en pantalla
- `var_list` — lista de variables para las que calcular IRFs (si se omite, calcula para todas)

**Ejemplo completo:**
```dynare
stoch_simul(order=1, irf=40, periods=0, hp_filter=1600) Y C I K L W R;
```

---

## Condiciones de Blanchard-Kahn (BK)

Después de resolver el modelo, Dynare reporta si se satisfacen las condiciones BK:
- **Variables predetermined** (estado): variables que aparecen con rezago `(-1)` en el modelo
- **Variables forward-looking** (jump): variables que aparecen con adelanto `(+1)`

Para una solución única y estable:
```
# de valores propios explosivos = # de variables forward-looking
```

Si Dynare dice `"Blanchard Kahn conditions are not satisfied"`:
- Demasiados eigenvalues explosivos → modelo sobredeterminado o mal especificado
- Muy pocos eigenvalues explosivos → indeterminación (equilibrios múltiples)

---

## Errores frecuentes y cómo resolverlos

### Error: "The following endogenous variables are not used in the model block"
- Una variable declarada en `var` no aparece en ninguna ecuación
- Solución: eliminarla de `var` o añadir la ecuación que la determina

### Error: "The model doesn't have the same number of equations and endogenous variables"
- Conteo incorrecto: revisa que #ecuaciones = #variables en `var`
- Solución: contar manualmente o buscar una ecuación faltante

### Error: "Impossible to find the steady state"
- El solver numérico no converge al estado estacionario
- Solución: usar `steady_state_model` con solución analítica, o mejorar `initval`

### Error: "The rank condition ISN'T verified"
- Condición de rango de Blanchard-Kahn no se cumple
- Soluciones posibles:
  - Revisar la especificación de la regla de Taylor (coeficiente sobre inflación > 1, principio de Taylor)
  - Revisar si hay variables que deberían ser forward-looking pero no tienen `(+1)`
  - Revisar la normalización del modelo

### Warning: "Some of the parameters have no value"
- Un parámetro declarado no tiene valor asignado (vale 0 por defecto)
- Solución: asignar el valor del parámetro antes del bloque `model`

---

## Convenciones de notación recomendadas

Para mantener consistencia y legibilidad:

```
Variables:
Y, C, I, K   — variables reales en niveles (o logaritmos si se especifica)
Pi           — inflación (o log-inflación)
R, i         — tasa de interés nominal (R = bruta, i = neta)
r            — tasa de interés real
W            — salario real
L, N         — empleo / horas trabajadas
A, Z         — productividad total de factores (TFP)
G            — gasto de gobierno
mc           — costo marginal real
lambda       — multiplicador de Lagrange (utilidad marginal del consumo)

Parámetros:
beta         — factor de descuento
alpha        — participación del capital
delta        — tasa de depreciación
sigma        — inverso de la elasticidad de sustitución intertemporal (EIS)
phi          — inverso de la elasticidad de Frisch
epsilon      — elasticidad de sustitución entre variedades (markup = epsilon/(epsilon-1))
theta        — probabilidad de no ajustar precios (Calvo)
phi_pi       — coeficiente de inflación en regla de Taylor
phi_y        — coeficiente del output gap en regla de Taylor
rho_*        — persistencia de procesos AR(1)
```

---

## Modelo RBC mínimo de referencia

```dynare
// ============================================================
// Modelo RBC básico — referencia mínima
// Basado en: King, Plosser & Rebelo (1988)
// ============================================================

var Y C I K L W R A;
varexo e_a;

parameters beta alpha delta sigma phi rho_a;

beta  = 0.99;
alpha = 0.33;
delta = 0.025;
sigma = 1.0;     // log utility en consumo
phi   = 1.0;     // elasticidad de Frisch inversa
rho_a = 0.95;

model;

// Ecuación de Euler (consumo)
C^(-sigma) = beta * C(+1)^(-sigma) * R(+1);

// Condición trabajo-ocio
W = phi * L / C^(-sigma);

// Tasa de retorno del capital
R = alpha * A * K(-1)^(alpha-1) * L^(1-alpha) + (1-delta);

// Salario real
W = (1-alpha) * A * K(-1)^alpha * L^(-alpha);

// Función de producción
Y = A * K(-1)^alpha * L^(1-alpha);

// Restricción de recursos
Y = C + I;

// Acumulación de capital
K = (1-delta) * K(-1) + I;

// Proceso AR(1) para TFP (en logs)
log(A) = rho_a * log(A(-1)) + e_a;

end;

steady_state_model;

A  = 1;
R  = 1/beta;
mc = 1;
K_L = (alpha / (R - 1 + delta))^(1/(1-alpha));
W   = (1-alpha) * K_L^alpha;
L   = (W / phi) / (1 - delta * K_L / (W * K_L^alpha + (1-delta)*K_L - delta*K_L));
// Simplificación: en muchos casos se calibra L_ss directamente
L   = 1/3;   // un tercio del tiempo trabajando
K   = K_L * L;
I   = delta * K;
Y   = K_L^alpha * L;
C   = Y - I;

end;

shocks;
var e_a;
stderr 0.01;
end;

stoch_simul(order=1, irf=40, periods=0) Y C I K L W R A;
```

---

## Recursos externos

- **Documentación oficial:** https://www.dynare.org/manual/
- **Foro de usuarios:** https://forum.dynare.org/
- **Ejemplos en el repositorio de Dynare:** `/matlab/examples/` en la instalación de Dynare
- **Dynare++ (versión standalone):** para modelos de orden superior sin MATLAB

## Fundamentación oficial (manual de Dynare)

Esta sección está **verificada contra el manual de referencia oficial de Dynare**
(*The Model File*, https://www.dynare.org/manual/the-model-file.html), no solo
contra resúmenes secundarios.

**Convención de timing (cita del manual):** *"the default convention is that the
timing of a variable reflects when this variable is decided. The typical example
is for capital stock: since the capital stock used at current period is actually
decided at the previous period, then the capital stock entering the production
function is `k(-1)`, and the law of motion of capital must be written:*
`k = i + (1-delta)*k(-1)`.

Consecuencias autoritativas (manual):
- Dynare usa por defecto el concepto **"stock al final del período"** (*stock at
  the end of the period*), no "al inicio del período".
- *"A predetermined variable — which by definition has been decided in a previous
  period — must have a lag. ... all stock variables must use the 'stock at the
  end of the period' convention."* → por eso el capital productivo hoy es `K(-1)`.
- El comando `predetermined_variables` cambia esa convención (declara variables
  decididas un período antes, con convención "stock al inicio del período"), pero
  internamente Dynare siempre reporta con la convención de fin de período.

**Para el bootcamp:** la lección de timing (`K(-1)`) está alineada con esta cita
oficial. Buen anclaje para enseñar el error más común sin ambigüedad.

---

## Patrones de un modelo New Keynesian (aprendido de CÓDIGO REAL)

*Estudiado de un NK lineal real del MMB: Paoli & Paustian (2017), "Coordinating
Monetary and Macroprudential Policies", replicación del MMB.*

Convenciones que usa el código real y que el traductor debe imitar:

- **`model(linear);`** cuando el modelo está **log-linealizado** (las variables son
  desviaciones respecto al estado estacionario). Evita `exp()/log()`; Dynare trata
  las ecuaciones como lineales. (En niveles se usa `model;` y sí aparecen `log/exp`.)
- **Etiquetas de ecuación** antes de cada ecuación: `[name='Phillips curve']`.
  Documentan qué FONC es cada una; NO cuentan como ecuación. Gran práctica pedagógica.
- **Anotaciones LaTeX** en las declaraciones: `betta $\beta$ // discount factor`
  (nombre de código + símbolo + comentario).
- **Parámetros auxiliares** derivados de otros, en el preámbulo:
  `kap = (eps-1)/varphi;`  `b = 1/(1+phi_ss);`.

Núcleo NK canónico, tal como aparece en el código real:

```dynare
[name='Phillips curve']
pi = kap*((sig+thet)*yg + alfa*(R+b*phi) + eps_m) + betta*pi(+1);
[name='Euler / IS']
R  = sig*(yg(+1)-yg) + (thet+1)/(sig+thet)*sig*(a(+1)-a) + pi(+1);
[name='Taylor rule']
R  = tau*pi + tau_g*yg + eps_R;        // tau > 1 (principio de Taylor)
[name='Technology AR(1)']
a  = rho_a*a(-1) - eta_a;              // un proceso por shock
```

- **Timing NK:** las forward (`pi(+1)`, `yg(+1)`) son *jump*; las predeterminadas
  (`n(-1)`, `R(-1)`, `del(-1)`) son estado.
- **Cierre típico:** `shocks; var eta_x; stderr ...; end;` y luego
  `check; steady; stoch_simul(order=1, irf=...);`.

> *Nota: el corpus completo (MMB, Pfeifer) se usa como referencia local; aquí se
> destilan los PATRONES, no se copia el código (respeto de licencias y atribución).*

---

*Este archivo es un documento vivo — se actualizará con cada sesión de trabajo.*  
*Última actualización: 2026-06-21*
