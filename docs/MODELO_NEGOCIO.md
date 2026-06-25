# Modelo de negocio y monetización — MacroBuilt

## Principio de costos: BYOK (Bring Your Own Key)

Los usuarios objetivo (estudiantes de pregrado) tienen poco presupuesto, pero las
APIs LLM son baratísimas (~US$0.005 por traducción con DeepSeek). En vez de
revender tokens —margen frágil y riesgo de saldo—, el usuario **conecta su propia
clave** de API. Nosotros cobramos por la **experiencia** (verificador, bootcamp,
OCR de pizarra, explicación pedagógica, historial), no por el cómputo.

**Consecuencia:** costo variable por usuario ≈ **US$0** → *contribution margin*
cercano al **100%**. Además, la pieza más valiosa —el verificador estático—
corre **local y gratis**, sin tokens.

---

## Segmentos y cómo pagan

1. **B2C estudiante (freemium).** Captura y prueba del producto. Conversión a Pro.
2. **B2B institucional (departamentos / universidades).** *El motor de ingresos*:
   un profesor o departamento decide por 30–200 alumnos a la vez.
3. **Bootcamp por cohortes (pago único).** Curso guiado de 4 semanas + certificado.
4. **B2B profesor / TA.** Generar y **auditar** soluciones de modelos para clase.

---

## Pricing concreto (3 planes)

| Plan | Precio | Incluye |
|------|--------|---------|
| **Free** | S/ 0 | Verificador offline ilimitado · 10 traducciones/mes (con tu key) · 1 módulo del bootcamp |
| **Estudiante Pro** | **S/ 19/mes** o **S/ 49/semestre** | Traducciones ilimitadas (BYOK) · OCR de pizarra · bootcamp completo · historial · exportar .mod |
| **Institucional (Departamento)** | **desde S/ 4,900/año por curso-sección** | Acceso para todos los alumnos del curso · panel del profesor · soporte · onboarding |

Add-on: **Bootcamp cohorte** — **S/ 129 pago único** (4 semanas guiadas + certificado).

Opción de conveniencia (sin BYOK): "clave administrada" con un recargo; el token
(~US$0.005/traducción) deja margen > 90%.

---

## Contribution margin (por usuario)

- **Costo variable con BYOK:** ~US$0 (el token lo paga el usuario). Solo hosting marginal.
- **Verificador:** US$0 (corre local, sin LLM).
- **Con clave administrada:** ~US$0.005/traducción → con cualquier plan pagado, margen > 90%.

---

## Por qué el institucional es el negocio

- **Venta 1 → muchos:** un profesor/departamento decide por decenas de alumnos.
- **Canal directo:** el founder es **TA de Macro II y Macro Internacional en la UP**.
- **Dolor validado (encuesta n=59):** 71% de los alumnos de macro nunca ha usado
  Dynare; el departamento quiere que aprendan más rápido y mejor.

---

## Go-to-market (GTM)

- **Fase 1 — UP (Economía):** piloto en Macroeconomía II y Macroeconomía
  Internacional (acceso directo del founder como TA). Primeros 10–100 usuarios.
- **Fase 2 — Lima/Perú:** otras universidades con DSGE en el currículo (PUCP,
  UNMSM, UNI, etc.). Primeros 1,000 usuarios.
- **Fase 3 — LatAm hispanohablante:** programas de economía y maestrías.

---

## Mercado (TAM / SAM / SOM)

**Ancla (top-down):** SUNEDU registra ~**1.2 millones** de universitarios en Perú
(dic-2023). Economía es una fracción del total; el detalle exacto está en la
plataforma TUNI.PE de SUNEDU.

- **TAM — estudiantes de Economía en LatAm hispanohablante** que llevan macro
  avanzada (donde aparece DSGE/Dynare). Orden de cientos de miles.
  *Perú: estimado ~25–35 mil estudiantes de Economía (≈2–3% de 1.2M; refinar con TUNI.PE).*
- **SAM — programas que usan Dynare/DSGE (Lima/Perú).** Con certeza del founder:
  **UP y PUCP** (Economía con macro avanzada en Dynare); el resto de top peruanas
  (UNMSM, UNI, U. de Lima) por confirmar. **Cifra oficial UP (2025-II):
  Economía = 1,605 matriculados** (Facultad de Economía y Finanzas = 2,115;
  total pregrado UP = 5,739).
- **SOM (12 meses) — la UP como beachhead.** En la UP, los cursos donde aparece
  DSGE (Macro II y Macro Internacional) tienen **3 secciones × ~30 alumnos ≈ 90
  por curso/semestre** → del orden de **~180–360 estudiantes/año** pasan por Dynare.
  - **Vía institucional (el negocio):** ~6 secciones macro-DSGE × S/ 4,900/año
    ≈ **S/ 29,400/año solo en la UP**; sumando PUCP (tamaño comparable)
    ≈ **~S/ 55–60 mil/año** en el beachhead Lima.
  - **Vía B2C (funnel):** de los ~2,115 de Economía UP, una conversión modesta del
    flujo de macro a Estudiante Pro (S/ 49/semestre) aporta ingreso complementario.

*Cifras UP: oficiales de la propia universidad (ver
`docs/research/UP_matriculados_pregrado_2025.pdf`): Economía pregrado 2025-II =
1,605 matriculados (egresados 2025-II = 79). Secciones/alumnos por curso y certeza
de uso de Dynare (UP, PUCP) aportados por el founder como TA.*

*Fuentes: Universidad del Pacífico (matriculados y egresados pregrado 2025);
SUNEDU (https://www.gob.pe/sunedu, TUNI.PE); INEI.*

---

## Riesgos del modelo y mitigación

- **"¿Por qué pagar si ChatGPT es gratis?"** → la IA general se equivoca y el
  alumno no lo nota (64% de la encuesta no pudo verificar el código). Nuestro
  **verificador + corpus de código real** garantizan correctitud: ese es el valor.
- **Adopción institucional lenta** → entrar *bottom-up* con profesores aliados
  antes de las compras formales del departamento.
- **Dependencia de un proveedor LLM** → el motor es **agnóstico** (DeepSeek hoy,
  OpenAI/otros con cambiar una variable); BYOK traslada el riesgo de precio al usuario.

---

## Nota de honestidad (validación)

La encuesta capturó fuerte **interés/demanda** (86% de no-usuarios usaría la
herramienta), pero por un fallo de ruteo **no** capturó *disposición a pagar* del
segmento con experiencia (n=1). El pricing de arriba es una hipótesis a validar en
el piloto de la Fase 1.
