# Pitch deck + guion — MacroBuilt (formato YC, 7 min)

Demo en vivo: https://huggingface.co/spaces/resaca2014/dynare-translate
Assets en `assets/` · figuras de la encuesta en `docs/research/figuras/`.

---

## Deck slide por slide

**1 · Portada.** Logo `assets/macrobuilt_logo.png`. "MacroBuilt — Tu laboratorio
macroeconómico". Founder: Alejandro Ventura Meza. URL del demo + del website.

**2 · One-liner.** *"Llevamos los modelos DSGE de la pizarra a un modelo que
corre — correcto, verificado y explicado — para que los estudiantes de macro
dejen de memorizar y empiecen a experimentar."*

**3 · Problema.** Memorizar modelos sin concretarlos. Cifra ancla:
**71% de los alumnos de macro nunca ha usado Dynare** (encuesta n=59).
Asset: `figuras/seg_nivel.png`.

**4 · Insight / Why now.** La IA genérica se equivoca en Dynare y el alumno no
lo nota: **64% no pudo verificar si el código estaba bien**. Hoy es posible por
LLMs baratos (DeepSeek) + OCR gratis (PaddleOCR). Asset: `figuras/ia_corregir.png`.

**5 · Solución.** MacroBuilt: traduce ecuaciones → `.mod`, **verifica** (sin LLM),
**explica** cada bloque, lee **foto de pizarra**, y enseña en un **bootcamp**.
Asset: captura de la pestaña "Traducir".

**6 · Producto y arquitectura.** Asset: `assets/arquitectura.png`.
Lo clave: el **verificador determinista** (no es un wrapper de un LLM) +
auto-reparación. Validado contra **185 modelos reales del MMB**.

**7 · DEMO EN VIVO** (3–4 min). Pegar ecuaciones → traducir → mostrar ✅ +
explicación → foto de pizarra → bootcamp con progreso. Plan B: video de respaldo.

**8 · Mercado.** TAM ~1.2M universitarios Perú (SUNEDU) → ~25–35k de Economía.
SAM: UP + PUCP. **SOM: UP, 1,605 econ; ~180–360 alumnos/año por Dynare →
~S/29k/año institucional solo UP, ~S/55–60k con PUCP.** Fuente oficial UP.

**9 · Modelo de negocio.** **BYOK** (margen ~100%). 3 planes: Free / Estudiante
Pro (S/19/mes) / Institucional (desde S/4,900/año por sección). El motor: vender
al departamento (canal directo del founder como TA).

**10 · Competencia & moat.** Tabla (`docs/COMPETENCIA_Y_ASK.md`): ocupamos el
cuadrante accesible + correcto + pedagógico. Moat: verificador + corpus real +
canal institucional + comunidad.

**11 · Tracción.** Encuesta n=59 (validación) + **[TUS INSIGHTS de las 3+
entrevistas en vivo aquí]** + capturas de WhatsApp.

**12 · Founder.** Foto `assets/founder_avatar.png` + founder–market fit
(`docs/FOUNDER.md`): TA de los cursos exactos, vive el problema.

**13 · Roadmap.** Bootcamp profesional (videos, evaluaciones, proyecto final) →
comunidad de macroeconomistas que programan → más allá de Dynare (Python, R).

**14 · The ask.** Piloto pagado de 1 semestre con el Depto. de Economía UP +
~S/6,000 semilla → **300 usuarios activos + primer contrato institucional** →
abre PUCP.

---

## Guion cronometrado (7 min)

**(0:00–1:00) Problema.** "Soy Alejandro, TA de Macro en la UP. Veo algo todos
los días: los alumnos memorizan modelos pero nunca los concretan. Encuestamos a
59 y el 71% nunca tocó Dynare, pese a ser estudiantes de macro. Y cuando le
piden ayuda a una IA, esta se equivoca — y el 64% ni se da cuenta."

**(1:00–4:30) Solución + DEMO en vivo.** "MacroBuilt es su laboratorio
macroeconómico." → Pegar las ecuaciones del RBC → traducir → mostrar el `.mod`,
el ✅ del verificador y la explicación. → "Y si están en la pizarra, una foto."
(foto → OCR → traducir). → "Y para aprender, un bootcamp que se autocorrige."
(mostrar la lección con el progreso). Recalcar: *el verificador es determinista,
no un wrapper de IA; validado contra 185 modelos publicados.*

**(4:30–5:30) Mercado + modelo.** "El cliente: 1,605 estudiantes de Economía solo
en la UP; ~180–360 pasan por Dynare al año. Vendemos al departamento: ~S/29 mil
al año solo en la UP, ~S/55–60 mil con PUCP. Margen ~100% porque el usuario pone
su propia API key."

**(5:30–6:30) Tracción + competencia.** "Validado con encuesta y con [N] usuarios
reales que ya lo probaron en vivo. Nadie cubre los tres a la vez: accesible,
correcto y pedagógico." (insights de las entrevistas).

**(6:30–7:00) Ask + visión.** "Pedimos un piloto pagado de un semestre con el
Depto. de Economía de la UP. Con eso llegamos a 300 usuarios y el primer contrato
institucional. La visión: una comunidad de macroeconomistas que programan, mucho
más allá de Dynare."

---

## Tips de sustentación

- El **demo en vivo es obligatorio** y vale mucho: ten el video de respaldo abierto.
- Prepárate para que te pidan **explicar/modificar código en vivo**: repasa
  `verifier.py` (el moat) y `app.py`.
- Cronometra: 7 min exactos. El demo es el corazón — no te pases en las slides.
