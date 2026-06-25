# Encuesta de validación — Dynare Translate / Bootcamp DSGE

**Público:** alumnos de Macroeconomía II y Macroeconomía Internacional (UP)
**Canal:** WhatsApp (grupos de clase)
**Objetivo:** evidencia para el pitch ("Problema & validación", rúbrica 3/20) + caracterización del cliente + medir predisposición de quienes aún no programan.
**Tiempo estimado:** ~4 minutos.

> **Forma rápida de crearla:** ejecuta el script `crear_encuesta_form.gs` (Google Apps Script) — arma el formulario completo, con la lógica condicional, automáticamente. Esta versión en texto es el respaldo manual.
>
> **Nota:** al pedir el correo, la encuesta es **confidencial** (no anónima): el correo deduplica respuestas e invita al beta.

---

## Lógica condicional (importante)

- **"Nivel con Dynare" = "Nunca lo he usado"** → salta directo al bloque final **"Antes de irte..."** (no-usuarios). No ve el bloque de dolor (no tendría sentido).
- **"¿Has intentado replicar...?" = "Nunca lo intenté"** → se salta la pregunta de **horas** (no programó), pero sí responde frustración y obstáculos.
- **"¿Has usado IA?" = "No"** → se salta el bloque de **experiencia con IA**.
- Al terminar el bloque de solución (usuarios), el formulario se **envía** (no cae en el bloque de no-usuarios).

---

## Mensaje de introducción (descripción del formulario)

¡Hola! 👋 Soy Alejandro, su TA de Macro. Esta encuesta es **confidencial** y toma **~4 minutos**.

(Tu correo solo lo uso para no duplicar respuestas e invitarte a probar el beta; no se comparte con nadie más.)

Con sus respuestas estoy construyendo una herramienta para que las próximas generaciones de pregrado en la UP puedan **unir la parte analítica (lo de la pizarra) con el código en Dynare** — sin sufrir tanto en el camino.

¿List@s para ser parte del cambio? 🚀

---

## Página 1 — Perfil

**Correo institucional UP** — *(texto, obligatorio, debe terminar en `@alum.up.edu.pe`)*

**¿Cuántos años tienes?** — *(número, 15–80)*

**Sexo** — Femenino / Masculino / Prefiero no decir / Otro

**¿Qué carrera estudias?** *(lista desplegable, obligatorio)*
Economía · Finanzas · Administración · Contabilidad · Marketing · Negocios Internacionales · Ingeniería Empresarial · Ingeniería de la Información · Derecho · Política, Filosofía y Economía · Humanidades Digitales · Ingeniería en Innovación y Diseño

**¿En qué semestre ingresaste a la UP?** *(lista desplegable, obligatorio)* — el ciclo en que empezaste, no el actual. Opciones 2026-I … 2018-I y "Antes de 2018". *(Con esto calculamos después los años/ciclo aprox.)*

**¿Qué curso(s) de macroeconomía llevas o llevaste?** *(selección múltiple, obligatorio)*
Economía General II · Macroeconomía I · Macroeconomía del Corto Plazo · Macroeconomía II · Macroeconomía Internacional · Macroeconomía III · Ninguno de estos (aún)

**¿Qué herramientas de programación manejas?** *(selección múltiple)*
Ninguna · Excel · Python · R · Stata · EViews · MATLAB u Octave · Dynare

**¿Cuál es tu nivel con Dynare?** *(opción única, obligatorio — RAMIFICA)*
Nunca lo he usado *(→ salta a "Antes de irte...")* / Lo intenté y lo abandoné / Lo uso, pero con mucha dificultad / Lo uso con relativa soltura

---

## Página 2 — Tu experiencia programando en Dynare

**¿Has intentado replicar un paper o un modelo (RBC, New Keynesian, etc.) en Dynare?** *(opción única — RAMIFICA)*
Sí, y lo logré / Sí, pero solo a medias / Lo intenté y no pude / Nunca lo intenté *(→ se salta la pregunta de horas)*

**(Solo si intentó) La última vez que programaste un modelo, ¿cuántas horas le dedicaste hasta que corrió (o hasta que te rendiste)?**
Menos de 2 / 2–5 / 5–10 / 10–20 / Más de 20

**¿Qué tan frustrante te resultó programar en Dynare?** *(escala 1–5)*

**¿Cuál fue tu mayor obstáculo?** *(selección múltiple)*
Sintaxis de Dynare · Blanchard-Kahn / indeterminación · steady state · Traducir FONCs a código · Entender cada bloque del .mod · Errores que no entiendo · Interpretar resultados (IRFs, momentos)

---

## Página 3 — Cómo lo resuelves hoy

**Cuando te trabas programando en Dynare, ¿qué haces?** *(selección múltiple)*
Pregunto al profe/TA · Foro de Dynare · Webs (Pfeifer, Mutschler, MMB) · IA (ChatGPT/Claude/Gemini) · Copio de un compañero · Me rindo / entrego incompleto

**¿Has usado IA (ChatGPT, Claude, Gemini) para escribir o corregir código Dynare?** *(opción única — RAMIFICA)*
Sí / No *(→ salta a "La solución")*

---

## Página 4 — Tu experiencia con IA *(solo si usó IA)*

**¿Con qué frecuencia te dio código con errores que tuviste que corregir?**
Siempre / Casi siempre / A veces / Casi nunca

**Cuando la IA se equivocaba, ¿pudiste darte cuenta y corregirlo?**
Sí, solo/a / Sí, con ayuda / No: usé el código sin estar seguro/a de si estaba bien

---

## Página 5 — La solución *(para quienes SÍ han usado Dynare)*

**Si existiera una herramienta que traduce tus ecuaciones a código Dynare correcto y te explica cada paso, ¿la usarías?**
Definitivamente sí / Probablemente sí / Tal vez / No

**¿Pagarías por una herramienta así?**
No pagaría / ≤ S/ 20 al mes / hasta S/ 50 al mes / Solo gratis para estudiantes

→ *(El formulario se envía aquí.)*

---

## Página 6 — "Antes de irte..." *(para quienes NUNCA han programado un modelo)*

**Más allá de las ecuaciones en la pizarra de tus cursos de macro, ¿te gustaría aprender a llevar esos modelos a código para simularlos, graficarlos y experimentar con ellos (verlos como un laboratorio)?**
Definitivamente sí / Me da curiosidad / Tal vez / No me llama la atención

**¿Qué te ha frenado para aprender a programar modelos macro?** *(selección múltiple)*
No sé por dónde empezar · Me parece muy difícil · No tengo tiempo · No sabía que se podía · Nunca me lo propusieron en clase · Otra

**Si existiera una herramienta que te enseña paso a paso a programar y experimentar con estos modelos, ¿la usarías?**
Definitivamente sí / Probablemente sí / Tal vez / No

---

## Qué buscamos de cada respuesta (para el pitch)

| Bloque | Para qué sirve |
|--------|----------------|
| Perfil (edad, sexo, carrera, ingreso, cursos, herramientas) | Caracterizar y segmentar al cliente; estimar años de carrera |
| Horas + frustración + obstáculos | Cuantificar el dolor; definir qué resuelve el producto primero |
| IA falla / no se dieron cuenta | **Insight clave + "why now"**: la IA se equivoca y el alumno ni se entera |
| Solución usuarios (usar/pagar) | Señal de mercado y disposición a pagar (SOM) |
| No-usuarios (interés/barreras) | **TAM ampliado**: predisposición de quienes aún no programan |

---

## Fase 2 (siguiente, no para esta entrega) — análisis textual

Cuando ampliemos la muestra, añadiremos preguntas **abiertas** y haremos **análisis de texto** (limpieza, *embeddings*, *clustering* temático y clasificación con ModernBERT del curso) para extraer patrones de dolor y *quotes* representativas. Esta versión se mantiene 100% cuantitativa para tabular rápido y tener evidencia citable a tiempo.
