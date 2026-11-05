# Slides: Un crash course de Dynare

Presentación de la sesión de 3 horas (con una pausa de 10 minutos). Adapta la plantilla
Beamer del curso: formato 4:3, portada negra y blanca, paleta y cabecera por secciones.

| Archivo | Función |
|---|---|
| `1_main.tex` | Archivo principal |
| `2_preamble.tex` | Plantilla, más colores del handout, estilo de código Dynare y `\num{}` |
| `configuracion.tex` | Fuente, tamaños de portada, subtítulo y cabecera |
| `3_content.tex` | Portada y orden de las secciones |
| `s1_motivacion.tex` … `s5_cierre.tex` | Una sección por archivo; cada slide lleva `label` y notas `\note{}` |
| `4_bibliography.bib` | Referencias, separadas por `keywords` en dos slides |
| `images/` | Logo e IRF generadas con Dynare 7.1 y `graficar_irfs.m` |

## Estructura (57 slides)

| Sección | Minutos | Slides |
|---|---|---|
| Motivación | 0–20 | portada a `objetivos` |
| Modelo | 20–50 | `impulso` a `reparto` |
| Dynare (taller en vivo) | 50–115 | `preprocesador` a `donde-guarda` |
| Pausa | 115–125 | `pausa` |
| Resultados | 125–165 | `receta` a `graficos` |
| Cierre | 165–180 | `vs-datos` a `referencias-modelo` |

Las cifras de la sección de resultados salen de la regla de decisión de Dynare 7.1
(`handout/rbc_analytical.mod`) pasada a elasticidades. Coinciden con las de la
presentación de la recitación 01 y con `oo_.irfs`.

## Compilación

XeLaTeX y Biber, igual que la plantilla:

```powershell
xelatex 1_main.tex
biber 1_main
xelatex 1_main.tex
xelatex 1_main.tex
```
