"""
prompts.py — Construcción de los prompts para la capa de traducción (LLM).

La calidad del .mod depende de (a) un buen system prompt con las reglas de
Dynare y (b) ejemplos few-shot de CÓDIGO REAL Y VERIFICADO de autores. La
biblioteca `examples/` contiene .mod reales y atribuidos; este módulo los carga,
los pasa por el verificador estático y solo incluye los que pasan.
"""

from __future__ import annotations

import glob
import os
from typing import List, Tuple

from .verifier import analyze

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
_CONTEXT_PATH = os.path.join(_REPO_ROOT, "context", "DYNARE_CONTEXT.md")
_EXAMPLES_DIR = os.path.join(_REPO_ROOT, "examples")

_FEWSHOT_N = int(os.environ.get("DYNARE_FEWSHOT_N", "2"))
_FEWSHOT_MAX_CHARS = int(os.environ.get("DYNARE_FEWSHOT_MAX_CHARS", "6000"))


def _read(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def load_verified_examples(max_examples: int = _FEWSHOT_N,
                           max_chars: int = _FEWSHOT_MAX_CHARS
                           ) -> List[Tuple[str, str]]:
    """Carga .mod de `examples/` que PASAN el verificador estático."""
    paths = sorted(glob.glob(os.path.join(_EXAMPLES_DIR, "**", "*.mod"),
                             recursive=True))
    out: List[Tuple[str, str]] = []
    for path in paths:
        code = _read(path)
        if not code.strip():
            continue
        if not analyze(code).ok:
            continue
        rel = os.path.relpath(path, _REPO_ROOT)
        out.append((rel, code[:max_chars]))
        if len(out) >= max_examples:
            break
    return out


def _format_examples_block(examples: List[Tuple[str, str]]) -> str:
    if not examples:
        return ("(Aún no hay ejemplos verificados en examples/. Añade .mod reales "
                "y atribuidos para mejorar la calidad de la traducción.)")
    parts = [
        "Estos .mod provienen de la biblioteca curada del repo (código real y "
        "verificado). Úsalos como referencia de estilo, convenciones y calidad. "
        "NO los copies literalmente; adáptalos a la economía solicitada.\n"
    ]
    for i, (rel, code) in enumerate(examples, 1):
        parts.append(f"--- Ejemplo {i}: {rel} ---\n```dynare\n{code}\n```")
    return "\n\n".join(parts)


INPUT_CONTRACT = """\
El investigador entrega la economía YA DERIVADA. Tú NO derives FONCs desde un
paper: solo traduces a sintaxis Dynare correcta. La entrada puede incluir:

  • ECUACIONES: FONCs, condiciones de vaciado de mercado, leyes de movimiento,
    procesos exógenos. En texto o LaTeX.
  • VARIABLES: lista de endógenas (si no se da, dedúcelas de las ecuaciones).
  • SHOCKS: variables exógenas (varexo).
  • PARÁMETROS y CALIBRACIÓN: nombres y valores (si no se dan, declara los
    parámetros y deja un valor placeholder comentado).
  • NOTAS: niveles vs logaritmos, convenciones de timing, etc.
"""

_SYSTEM_TEMPLATE = """\
Eres un traductor experto de modelos DSGE a código Dynare (.mod). Tu única
tarea es convertir la descripción económica de un modelo —que el investigador
ya derivó a mano— en un archivo .mod correcto, bien comentado y que compile.

Eres un INTÉRPRETE, no un derivador: el economista hace el trabajo intelectual;
tú haces la transcripción técnica impecable a sintaxis Dynare.

{input_contract}

=== REGLAS INNEGOCIABLES ===
1. #ecuaciones del bloque `model` DEBE ser igual a #variables endógenas en `var`.
2. Timing: `X(-1)` es rezago (t-1), `X(+1)` es expectativa (E_t X_{{t+1}}).
   El capital disponible en t es `K(-1)`, NO `K`.
3. Toda variable usada en `model` debe estar declarada en `var` o `varexo`.
4. Todo parámetro declarado debe tener un valor asignado.
5. La regla de Taylor debe respetar el principio de Taylor (coef. de inflación > 1),
   o el modelo será indeterminado. Si el usuario da un valor ≤ 1, adviértelo.
6. No uses una variable que choque con un shock; no mezcles logs y niveles sin
   documentarlo.
7. Incluye, cuando sea posible, un bloque `steady_state_model` analítico.
8. Comenta CADA ecuación con su intuición económica (qué agente, qué condición).

=== ESTÁNDAR DE SALIDA ===
Devuelve SIEMPRE, en este orden:
1. El archivo .mod COMPLETO dentro de un bloque de código ```dynare ... ```
   con encabezado (nombre, referencia, versión Dynare, descripción).
2. Después del código, una sección "## Explicación por bloque" donde, en lenguaje
   claro para un alumno de pregrado, expliques qué hace cada bloque y qué
   representa cada ecuación (esta es la capa pedagógica: el bootcamp).

=== BASE DE CONOCIMIENTO DE DYNARE (referencia interna) ===
{context}

=== EJEMPLOS DE ORO (código real, verificado) ===
{examples}
"""


def build_system_prompt() -> str:
    """Ensambla el system prompt completo desde la base de conocimiento."""
    context = _read(_CONTEXT_PATH) or "(base de conocimiento no disponible)"
    examples = _format_examples_block(load_verified_examples())
    return _SYSTEM_TEMPLATE.format(
        input_contract=INPUT_CONTRACT,
        context=context,
        examples=examples,
    )


_LEARNING_ADDENDUM = """\

=== MODO APRENDIZAJE (bootcamp) ===
Además de la explicación por bloque, escribe la explicación de forma extra
didáctica, como para un alumno de pregrado que recién aprende: usa analogías
breves y evita jerga innecesaria. Al final, agrega una sección "## Ejercicios"
con 2 o 3 ejercicios cortos para que el alumno modifique el modelo y vea qué
pasa (p. ej., cambiar un parámetro, añadir un shock, alterar una ecuación),
explicando qué debería observar en cada caso.
"""


def build_user_prompt(economic_input: str, learning_mode: bool = False) -> str:
    """Envuelve la entrada económica del usuario con instrucciones finales.

    Si learning_mode=True, pide explicación más didáctica + ejercicios (bootcamp).
    """
    prompt = (
        "Traduce a Dynare la siguiente descripción económica. Respeta el "
        "estándar de salida (código .mod en bloque ```dynare``` + explicación "
        "por bloque).\n\n"
        "=== ENTRADA ECONÓMICA ===\n"
        f"{economic_input.strip()}\n"
    )
    if learning_mode:
        prompt += _LEARNING_ADDENDUM
    return prompt


def build_repair_prompt(mod_code: str, verifier_report: str) -> str:
    """Prompt de auto-reparación: el verificador halló errores; pide corregir."""
    return (
        "El archivo .mod que generaste tiene errores detectados por el "
        "verificador estático. Corrígelos SIN cambiar la economía del modelo "
        "(misma intención de las ecuaciones); solo arregla sintaxis, conteos, "
        "declaraciones o timing. Devuelve el .mod corregido completo en un "
        "bloque ```dynare``` y una nota breve de qué cambiaste.\n\n"
        "=== .MOD ACTUAL ===\n"
        f"```dynare\n{mod_code}\n```\n\n"
        "=== REPORTE DEL VERIFICADOR ===\n"
        f"{verifier_report}\n"
    )
