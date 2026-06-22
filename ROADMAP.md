# Roadmap del Proyecto

## Objetivo general
Construir una base de conocimiento completa sobre Dynare que permita a un LLM generar código DSGE correcto y bien especificado.

---

## Fase 1 — Fundamentos (Semana 1-2)
**Meta:** Sentar las bases del repositorio y la documentación de referencia.

- [x] Estructura del repositorio
- [ ] Guía de sintaxis Dynare (`reference/syntax_guide.md`)
- [ ] Cheatsheet de comandos (`reference/commands_cheatsheet.md`)
- [ ] Guía de errores comunes (`reference/common_errors.md`)
- [ ] Contexto para LLM — versión inicial (`context/DYNARE_CONTEXT.md`)
- [ ] Primer modelo RBC básico comentado (`examples/01_rbc/rbc_basic.mod`)
- [ ] Documentación oficial de Dynare (`docs/`)

## Fase 2 — Modelos New Keynesian (Semana 3-4)
**Meta:** Cubrir el modelo NK estándar y sus variantes más comunes.

- [ ] Modelo NK básico (Galí 2008) con regla de Taylor
- [ ] Modelo NK con hábitos en consumo
- [ ] Modelo NK con costos de ajuste de capital
- [ ] Análisis de política monetaria (IRFs ante shocks de tasa de interés)
- [ ] Guía de especificación de reglas de Taylor en Dynare

## Fase 3 — Economías Abiertas (Semana 5-6)
**Meta:** Modelos con sector externo.

- [ ] Modelo SOE (Small Open Economy) básico
- [ ] Modelo con tipo de cambio nominal
- [ ] Modelo de dos países (two-country)
- [ ] Paridad uncovered interest rate y sus variantes
- [ ] Shocks de términos de intercambio

## Fase 4 — Fricciones Financieras (Semana 7-8)
**Meta:** Modelos con sector financiero.

- [ ] Modelo BGG (Bernanke-Gertler-Gilchrist 1999)
- [ ] Modelo con acelerador financiero simplificado
- [ ] Modelo con intermediarios financieros (Gertler-Karadi)
- [ ] Crisis financiera y política macroprudencial

## Fase 5 — Modelos Avanzados (Semana 9+)
**Meta:** Modelos de frontera de la literatura.

- [ ] HANK básico (Heterogeneous Agent New Keynesian)
- [ ] Mercados incompletos (Bewley-Huggett-Aiyagari)
- [ ] Modelos con fricciones de búsqueda y emparejamiento
- [ ] TANK (Two-Agent New Keynesian) como aproximación a HANK

## Fase 6 — Herramientas y Automatización (Continuo)
**Meta:** Facilitar el workflow de modelado.

- [ ] Templates para tipos de modelos más comunes
- [ ] Scripts de diagnóstico (chequeo de BK conditions, rank conditions)
- [ ] Guía de calibración de parámetros
- [ ] Guía de estimación bayesiana en Dynare
- [ ] Prompts optimizados para distintos tipos de modelos

---

## Criterio de calidad para los ejemplos

Cada archivo `.mod` debe incluir:
1. **Encabezado** — descripción del modelo, referencia bibliográfica, versión de Dynare
2. **Comentarios en cada bloque** — explicando qué hace cada sección
3. **Comentarios en cada ecuación** — intuición económica
4. **Valores de estado estacionario** — explicados cuando son no triviales
5. **Verificación** — confirmación de que el modelo corre sin errores

---

## Log de progreso

| Fecha      | Tarea completada                                                          |
|------------|---------------------------------------------------------------------------|
| 2026-05-23 | Estructura base del repositorio creada                                    |
| 2026-06-20 | Visión del proyecto definida: skill de traducción DSGE → Dynare           |
| 2026-06-20 | Decisiones de diseño acordadas (scope, arquitectura, prioridades)         |
| 2026-06-20 | Paper objetivo para caso de prueba: Corsetti & Müller (2006) Twin Deficits|
| 2026-06-20 | Proyecto convertido en proyecto final de curso                            |

---

## Visión de producto (mediano plazo) — de herramienta a comunidad

MacroBuilt no se queda en un traductor. La hoja de ruta es convertir el bootcamp
en una **plataforma de aprendizaje y una comunidad** para macroeconomistas que
programan.

**Bootcamp profesional (evolución del actual):**
- **Videos hechos por profesores** (incluido el founder como TA de la UP).
- **Sección de ejercicios** (la parte práctica), autocorregidos por el verificador.
- **Evaluaciones** y seguimiento de progreso por alumno.
- **Proyecto final**: cada estudiante construye y replica su propio modelo.
- **Certificación**.

**Comunidad y networking:**
- Una **comunidad de programación para macroeconomistas** (foros, mentoría,
  showcase de proyectos, bolsa de RA/tesis).
- Networking entre estudiantes, TAs, profesores e investigadores de LatAm.

**Más allá de Dynare:**
- Expandir a otros lenguajes/entornos del flujo macro-cuantitativo: **Python**
  (modelos, datos, simulación), R, MATLAB/Octave, y herramientas de estimación.
- MacroBuilt como el lugar donde un economista aprende a programar de principio a fin.

**Fases sugeridas:**
1. Hoy: traductor + verificador + bootcamp interactivo (4 lecciones).
2. +3 meses: bootcamp con videos, más lecciones, evaluaciones, certificación.
3. +6 meses: proyectos de alumnos + comunidad/foro + piloto institucional.
4. +12 meses: expansión a Python y otros entornos; networking LatAm.
