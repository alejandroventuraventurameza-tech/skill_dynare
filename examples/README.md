# Biblioteca de ejemplos (.mod)

Esta carpeta es el **corpus de referencia** del producto. Los archivos `.mod`
aquí se usan como ejemplos few-shot para la traducción (ver
`dynare_translate/core/prompts.py`, función `load_verified_examples`).

## Estándar de procedencia (IMPORTANTE)

El corpus debe ser **código real, escrito por autores o por el equipo de
Dynare** — NO código generado por una IA. Esa es justamente la ventaja del
producto: aprendemos de fuentes verificadas, no de modelos que pueden
equivocarse.

Fuentes recomendadas para poblar el corpus:
- **Johannes Pfeifer — DSGE_mod** (réplicas verificadas de papers clásicos).
- **Macroeconomic Model Database (MMB)** (modelos estandarizados).
- **Ejemplos oficiales de Dynare** (`.../matlab/examples/` y la documentación).
- **Repos de autores** y materiales de cursos/summer schools.

## Reglas para añadir un ejemplo

1. El `.mod` debe ser de una fuente real y verificable. Anótala en `SOURCES.md`.
2. Respeta la licencia de origen y atribuye al autor (en el encabezado del .mod
   y en `SOURCES.md`).
3. Debe **pasar el verificador estático**; si no, no se usará como few-shot:
   ```bash
   python dynare_translate/core/verifier.py examples/<ruta>.mod
   ```
4. Idealmente, debe **correr en Dynare** sin errores (verificación dinámica).

## Organización

```
examples/
  01_rbc/                 # Real Business Cycle
  02_new_keynesian/       # New Keynesian (RANK)
  03_open_economy/        # Economías abiertas (SOE, two-country)
  04_financial_frictions/ # BGG, Gertler-Karadi
  05_advanced/            # HANK, mercados incompletos
```
