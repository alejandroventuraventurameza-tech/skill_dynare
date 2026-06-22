"""
bootcamp.py — Mini-curso "Introducción a Dynare" (estilo Codecademy/DataCamp).

Cada lección tiene teoría + un ejercicio práctico sobre un .mod, y se
**autocorrige al instante** usando el verificador estático determinista. El
verificador es el "auto-grader": no hace falta tener Dynare instalado para que
el alumno reciba feedback inmediato.

Estructura de una lección:
  id, title, theory (markdown), instructions, starter (.mod inicial),
  solution (.mod correcto de referencia), check(code) -> (passed, feedback).
"""

from __future__ import annotations

from typing import Callable, Dict, List, Tuple

from .verifier import analyze


def _default_check(code: str) -> Tuple[bool, str]:
    """Aprueba si el .mod pasa el verificador estático."""
    if not code or not code.strip():
        return False, "Escribe tu solución en el editor y vuelve a comprobar."
    report = analyze(code)
    if report.ok:
        return True, "✅ ¡Correcto! Tu modelo pasa el verificador.\n\n" + report.to_markdown()
    return False, "❌ Aún no. El verificador encontró esto:\n\n" + report.to_markdown()


def _timing_check(code: str) -> Tuple[bool, str]:
    """Como el default, pero exige el timing K(-1) en la función de producción."""
    norm = (code or "").replace(" ", "")
    if "K^alpha" in norm and "K(-1)^alpha" not in norm:
        return False, (
            "❌ Casi. Recuerda: el capital disponible para producir **hoy** es "
            "`K(-1)`, no `K`. Corrige la función de producción."
        )
    return _default_check(code)


# --------------------------------------------------------------------------- #
# Lecciones
# --------------------------------------------------------------------------- #

LESSONS: List[Dict] = [
    {
        "id": "L1",
        "title": "El esqueleto de un .mod y el bloque var",
        "theory": (
            "Un archivo Dynare (`.mod`) tiene bloques en un orden fijo:\n\n"
            "- `var` — variables **endógenas** (las que el modelo resuelve)\n"
            "- `varexo` — shocks exógenos\n"
            "- `parameters` — parámetros y sus valores\n"
            "- `model; ... end;` — las ecuaciones\n"
            "- `shocks; ... end;` y `stoch_simul(...)`\n\n"
            "**Regla de oro:** toda variable que aparece en el bloque `model` "
            "debe estar declarada en `var` (o `varexo`). Si falta una, Dynare "
            "da error."
        ),
        "instructions": (
            "La variable **A** (productividad) se usa en el modelo pero **no está "
            "declarada**. Agrégala al bloque `var` y comprueba."
        ),
        "starter": (
            "var Y C;\n"
            "varexo e_a;\n"
            "parameters rho;\n"
            "rho = 0.9;\n\n"
            "model;\n"
            "Y = A;\n"
            "log(A) = rho*log(A(-1)) + e_a;\n"
            "C = Y;\n"
            "end;\n"
        ),
        "solution": (
            "var Y C A;\n"
            "varexo e_a;\n"
            "parameters rho;\n"
            "rho = 0.9;\n\n"
            "model;\n"
            "Y = A;\n"
            "log(A) = rho*log(A(-1)) + e_a;\n"
            "C = Y;\n"
            "end;\n"
        ),
        "check": _default_check,
    },
    {
        "id": "L2",
        "title": "El conteo: #ecuaciones = #variables",
        "theory": (
            "Dynare exige que el número de **ecuaciones** del bloque `model` sea "
            "igual al número de **variables endógenas** en `var`. Si hay 3 "
            "variables, tienen que haber 3 ecuaciones que las determinen.\n\n"
            "Si el conteo no cuadra, verás: *'The model doesn't have the same "
            "number of equations and endogenous variables'*."
        ),
        "instructions": (
            "Hay **3 variables** (Y, C, I) pero solo **2 ecuaciones**. Agrega una "
            "ecuación que determine **C** (por ejemplo, `C = 0.6*Y;`)."
        ),
        "starter": (
            "var Y C I;\n"
            "varexo e;\n"
            "parameters delta;\n"
            "delta = 0.1;\n\n"
            "model;\n"
            "Y = C + I;\n"
            "I = delta*Y + e;\n"
            "end;\n"
        ),
        "solution": (
            "var Y C I;\n"
            "varexo e;\n"
            "parameters delta;\n"
            "delta = 0.1;\n\n"
            "model;\n"
            "Y = C + I;\n"
            "I = delta*Y + e;\n"
            "C = 0.6*Y;\n"
            "end;\n"
        ),
        "check": _default_check,
    },
    {
        "id": "L3",
        "title": "El timing: el capital es K(-1)",
        "theory": (
            "En Dynare el **tiempo** importa: `X(-1)` es el rezago (t-1) y "
            "`X(+1)` es la expectativa (E_t X_{t+1}).\n\n"
            "Las variables de **stock** (como el capital K) disponibles para "
            "producir **hoy** son las acumuladas hasta **ayer**: por eso en la "
            "función de producción se usa **`K(-1)`**, no `K`. Es el error de "
            "timing más común."
        ),
        "instructions": (
            "La función de producción tiene un error de timing: usa `K` en vez "
            "de `K(-1)`. Corrígela."
        ),
        "starter": (
            "var Y K I;\n"
            "varexo e;\n"
            "parameters alpha delta;\n"
            "alpha = 0.33;\n"
            "delta = 0.1;\n\n"
            "model;\n"
            "Y = K^alpha;\n"
            "K = (1-delta)*K(-1) + I;\n"
            "I = e;\n"
            "end;\n"
        ),
        "solution": (
            "var Y K I;\n"
            "varexo e;\n"
            "parameters alpha delta;\n"
            "alpha = 0.33;\n"
            "delta = 0.1;\n\n"
            "model;\n"
            "Y = K(-1)^alpha;\n"
            "K = (1-delta)*K(-1) + I;\n"
            "I = e;\n"
            "end;\n"
        ),
        "check": _timing_check,
    },
    {
        "id": "L4",
        "title": "Arma tu primer RBC (completa el modelo)",
        "theory": (
            "Ya conoces las piezas: declarar variables, cuadrar el conteo y "
            "respetar el timing. Ahora completa un RBC mínimo.\n\n"
            "Le falta la **restricción de recursos** (el vaciado del mercado de "
            "bienes): todo lo que se produce se consume o se invierte, "
            "`Y = C + I`. Sin ella, sobra una variable (I queda sin determinar)."
        ),
        "instructions": (
            "Agrega la **restricción de recursos** que falta para que el conteo "
            "cuadre y todas las variables queden determinadas."
        ),
        "starter": (
            "var Y C I K A;\n"
            "varexo e_a;\n"
            "parameters alpha delta rho;\n"
            "alpha = 0.33;\n"
            "delta = 0.1;\n"
            "rho = 0.9;\n\n"
            "model;\n"
            "Y = A*K(-1)^alpha;\n"
            "K = (1-delta)*K(-1) + I;\n"
            "log(A) = rho*log(A(-1)) + e_a;\n"
            "C = 0.7*Y;\n"
            "// FALTA: la restriccion de recursos (Y = C + I)\n"
            "end;\n"
        ),
        "solution": (
            "var Y C I K A;\n"
            "varexo e_a;\n"
            "parameters alpha delta rho;\n"
            "alpha = 0.33;\n"
            "delta = 0.1;\n"
            "rho = 0.9;\n\n"
            "model;\n"
            "Y = A*K(-1)^alpha;\n"
            "K = (1-delta)*K(-1) + I;\n"
            "log(A) = rho*log(A(-1)) + e_a;\n"
            "C = 0.7*Y;\n"
            "Y = C + I;\n"
            "end;\n"
        ),
        "check": _default_check,
    },
]


def lesson_titles() -> List[str]:
    """Títulos numerados para el selector de la UI."""
    return [f"{i+1}. {l['title']}" for i, l in enumerate(LESSONS)]


def _index_from_title(title: str) -> int:
    titles = lesson_titles()
    return titles.index(title) if title in titles else 0


def lesson_intro(title: str) -> str:
    """Markdown con teoría + instrucciones de la lección."""
    l = LESSONS[_index_from_title(title)]
    return (
        f"### {l['title']}\n\n{l['theory']}\n\n"
        f"---\n\n**🎯 Ejercicio:** {l['instructions']}"
    )


def lesson_starter(title: str) -> str:
    return LESSONS[_index_from_title(title)]["starter"]


def lesson_solution(title: str) -> str:
    return LESSONS[_index_from_title(title)]["solution"]


def check_lesson(title: str, code: str) -> str:
    """Autocorrige el ejercicio y devuelve feedback en markdown."""
    l = LESSONS[_index_from_title(title)]
    check: Callable[[str], Tuple[bool, str]] = l["check"]
    passed, feedback = check(code)
    return feedback


# --------------------------------------------------------------------------- #
# Progresión por fases (bootcamp interactivo)
# --------------------------------------------------------------------------- #

N_LESSONS = len(LESSONS)


def title_at(idx: int) -> str:
    idx = max(0, min(int(idx), N_LESSONS - 1))
    return lesson_titles()[idx]


def intro_at(idx: int) -> str:
    return lesson_intro(title_at(idx))


def starter_at(idx: int) -> str:
    return lesson_starter(title_at(idx))


def solution_at(idx: int) -> str:
    return lesson_solution(title_at(idx))


def passed_feedback(idx: int, code: str):
    """Devuelve (feedback_markdown, passed_bool)."""
    fb = check_lesson(title_at(idx), code)
    return fb, ("✅" in fb)


def render_progress(idx: int, done) -> str:
    """HTML con los pasos del bootcamp: ✓ completado, número actual resaltado."""
    chips = []
    for i in range(N_LESSONS):
        if i < len(done) and done[i]:
            bg, fg, mark = "#16a34a", "#ffffff", "✓"
        elif i == idx:
            bg, fg, mark = "#4f46e5", "#ffffff", str(i + 1)
        else:
            bg, fg, mark = "#e5e7eb", "#6b7280", str(i + 1)
        chips.append(
            f'<span title="{title_at(i)}" style="display:inline-flex;'
            f'align-items:center;justify-content:center;width:30px;height:30px;'
            f'border-radius:999px;background:{bg};color:{fg};font-weight:700;'
            f'font-size:13px;">{mark}</span>'
        )
        if i < N_LESSONS - 1:
            chips.append('<span style="color:#cbd5e1;">—</span>')
    done_n = sum(1 for d in done if d)
    if done_n == N_LESSONS:
        cap = ('<div style="margin-top:8px;font-size:13px;color:#16a34a;'
               'font-weight:600;">🎉 ¡Completaste el bootcamp de introducción!</div>')
    else:
        cap = (f'<div style="margin-top:8px;font-size:13px;color:#6b7280;">'
               f'Progreso: {done_n}/{N_LESSONS} lecciones · completa una para '
               f'desbloquear la siguiente</div>')
    return ('<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">'
            + "".join(chips) + '</div>' + cap)
