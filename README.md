---
title: Dynare Translate
emoji: 🧮
colorFrom: indigo
colorTo: blue
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# 🧮 Dynare Translate

**Convertimos la pizarra en un laboratorio.** Dynare Translate toma la economía
que un estudiante ya derivó a mano (FONCs, condiciones de vaciado de mercado,
leyes de movimiento) y la traduce a código **Dynare** correcto, **verificado** y
**explicado paso a paso** — para que los alumnos de macroeconomía de pregrado
dejen de memorizar modelos y empiecen a *jugar* con ellos.

> One-liner: *Hacemos que los estudiantes de macro lleven sus modelos DSGE de la
> pizarra a un modelo que corre, entendiendo cada línea, mediante un traductor a
> Dynare con verificación automática.*

---

## El problema

Programar modelos DSGE en Dynare es doloroso para un estudiante de pregrado: la
sintaxis es única, el material accesible es escaso, los cursos formales son caros
y de posgrado, y cuando delegan el código a una IA genérica, **esta se equivoca a
menudo y el alumno ni se entera** (conteos de ecuaciones, condiciones de
Blanchard-Kahn, *timing* del capital, etc.).

## El insight

Una IA genérica transcribe; nosotros **entendemos el modelo**. Cada ecuación se
reconoce por su rol económico (FONC del hogar, del productor, vaciado de mercado,
regla de política) y, antes de entregar nada, un **verificador determinista**
audita el `.mod`: número de ecuaciones = número de variables, símbolos
declarados, parámetros con valor, clasificación estado/*jump* para Blanchard-Kahn.

---

## Cómo correrlo

### En local
```bash
pip install -r requirements.txt
cp .env.example .env          # coloca tu ANTHROPIC_API_KEY
python app.py                 # abre la interfaz Gradio
```

### Tests
```bash
pip install pytest
python -m pytest tests/ -q
```

### Despliegue
Pensado para **Hugging Face Spaces** (SDK Gradio): el frontmatter de este README
configura el Space y `app.py` es el entrypoint.

---

## Arquitectura

```
.
├── app.py                       # Interfaz Gradio (entrypoint del Space)
├── dynare_translate/            # Paquete del producto
│   └── core/
│       ├── verifier.py          # Verificador estático DETERMINISTA (sin LLM, testeado)
│       ├── prompts.py           # System prompt desde la base de conocimiento
│       └── translator.py        # Traducción vía API de Anthropic + auto-reparación
├── context/DYNARE_CONTEXT.md    # Base de conocimiento (el "cerebro" del prompt)
├── examples/                    # Modelos .mod de oro (verificados)
├── tests/                       # Pruebas del verificador y los extractores
└── docs/research/               # Evidencia de validación (encuesta a alumnos UP)
```

El flujo: **entrada económica → traducción (LLM) → verificación estática →
auto-reparación si hay errores → explicación pedagógica**. El verificador y la
capa LLM están separados a propósito: lo decidible es determinista y testeado; el
razonamiento económico vive en el prompt.

---

## Herramientas del curso usadas

- **API de Claude (Anthropic)** — motor de traducción y explicación
  (`dynare_translate/core/translator.py`).
- **Verificación tipo agente** — auditoría automática del modelo, base del
  "agente verificador" (`dynare_translate/core/verifier.py`).
- **Gradio + despliegue** — interfaz y Space público (`app.py`, frontmatter).

---

## Estado del repositorio como base de conocimiento

Además del producto, este repo es una base de conocimiento DSGE/Dynare en
construcción (ver [`ROADMAP.md`](ROADMAP.md) y [`CLAUDE.md`](CLAUDE.md)), con
ejemplos comentados en `examples/`, contexto para LLMs en `context/` y plantillas
en `templates/`. Orientado a **Dynare 5.x/6.x**.

## Licencia

MIT.
