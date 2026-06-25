# CLAUDE.md — Instrucciones para el modelo

Este archivo contiene instrucciones específicas para que Claude trabaje correctamente en este repositorio de Dynare.

---

## Contexto del proyecto

Este repositorio es una base de conocimiento para modelado DSGE en Dynare. El objetivo es que Claude pueda:
1. Generar código Dynare correcto y bien comentado.
2. Detectar y corregir errores en modelos existentes.
3. Adaptar modelos de la literatura a Dynare.

El usuario tiene experiencia intermedia en Dynare y DSGE. Los modelos objetivo incluyen NK, economías abiertas, fricciones financieras, y modelos avanzados (HANK).

---

## Antes de escribir cualquier código Dynare

1. **Lee `context/DYNARE_CONTEXT.md`** — contiene la guía de sintaxis y errores comunes.
2. **Verifica el conteo de ecuaciones** — #ecuaciones debe ser igual a #variables en `var`.
3. **Verifica la notación temporal** — `X(-1)` para rezagos, `X(+1)` para expectativas.
4. **Identifica variables de estado vs. jump** — para anticipar si se cumplirán las condiciones BK.

---

## Estructura del repositorio

```
docs/          — Documentación oficial de Dynare (user guide, papers de referencia)
examples/      — Modelos de ejemplo completamente comentados
  01_rbc/            — Real Business Cycle
  02_new_keynesian/  — New Keynesian
  03_open_economy/   — Economías abiertas
  04_financial_frictions/ — Fricciones financieras
  05_advanced/       — HANK, mercados incompletos
templates/     — Plantillas base para cada tipo de modelo
reference/     — Guías rápidas de sintaxis y errores
context/       — Contexto para LLMs
```

---

## Estándar de calidad para archivos `.mod`

Todo archivo `.mod` en este repositorio debe:

1. Comenzar con un encabezado que incluya:
   - Nombre del modelo
   - Referencia bibliográfica (si aplica)
   - Versión de Dynare
   - Breve descripción del modelo
   
2. Tener comentarios en cada bloque explicando su propósito.

3. Tener comentarios en cada ecuación explicando la intuición económica.

4. Incluir el estado estacionario analítico en `steady_state_model` cuando sea posible.

5. Verificar que corre sin errores antes de commitearlo.

---

## Errores que Claude debe evitar

- Usar nombres de variables que choquen con funciones de MATLAB/Octave (p.ej., `gamma`, `beta` son funciones, pero también son parámetros comunes — en Dynare esto está permitido, pero en el preámbulo MATLAB hay que tener cuidado).
- Olvidar que el capital disponible en t es `K(-1)`, no `K`.
- Especificar reglas de Taylor con coeficiente de inflación ≤ 1 (viola el principio de Taylor → indeterminación).
- Mezclar modelos en logaritmos con modelos en niveles sin documentarlo.
- Omitir el valor de algún parámetro (el warning de Dynare puede pasarse por alto pero el resultado es incorrecto).

---

## Flujo de trabajo recomendado

Cuando el usuario pide escribir un nuevo modelo:
1. Identificar el tipo de modelo y buscar el template correspondiente en `templates/`.
2. Revisar si hay un ejemplo similar en `examples/`.
3. Escribir las ecuaciones con comentarios inline.
4. Especificar el estado estacionario analíticamente.
5. Verificar el conteo de ecuaciones y variables.
6. Añadir el bloque de shocks y el comando `stoch_simul`.
7. Documentar el archivo con el encabezado estándar.
