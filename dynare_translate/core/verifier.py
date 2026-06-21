"""
verifier.py — Análisis estático determinista de modelos Dynare (.mod).

Este módulo NO usa ningún modelo de lenguaje. Es un analizador puro y
determinista: dado el texto de un archivo .mod, parsea sus bloques y aplica
una serie de chequeos que replican (de forma anticipada, antes de correr
Dynare) los errores más frecuentes que sufre quien programa modelos DSGE.

Es el "agente verificador" del producto, pero en su capa decidible: lo que se
puede afirmar con certeza a partir del texto. El razonamiento económico (qué
FONC corresponde a qué agente, si la regla de Taylor cumple el principio, etc.)
lo realiza la capa LLM por separado; aquí solo vive lo que es comprobable
estáticamente.

Chequeos implementados
----------------------
ERRORES (rompen la compilación en Dynare):
  - Falta el bloque model; ... end;
  - #ecuaciones != #variables endógenas (var)
  - Símbolos usados en el modelo que no están declarados
  - Parámetros declarados sin valor asignado
  - Variables endógenas declaradas que no se usan en el modelo
  - Declaraciones duplicadas

ADVERTENCIAS (no rompen, pero suelen indicar un problema):
  - No hay steady_state_model ni initval
  - No hay bloque shocks
  - No hay comando de simulación/estimación (stoch_simul, estimation, ...)

INFORMACIÓN (para la capa pedagógica / heurística de Blanchard-Kahn):
  - Variables de estado (aparecen con rezago (-1))
  - Variables forward-looking / jump (aparecen con adelanto (+1))
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple

# --------------------------------------------------------------------------- #
# Conjuntos de referencia
# --------------------------------------------------------------------------- #

# Funciones matemáticas y operadores reconocidos por Dynare: NO son variables.
DYNARE_FUNCTIONS: Set[str] = {
    "log", "ln", "log10", "exp", "sqrt", "abs", "sign",
    "sin", "cos", "tan", "asin", "acos", "atan",
    "sinh", "cosh", "tanh", "max", "min",
    "normcdf", "normpdf", "erf", "gamma",
}

# Palabras reservadas / operadores de Dynare que pueden aparecer en el modelo.
DYNARE_KEYWORDS: Set[str] = {
    "STEADY_STATE", "EXPECTATION", "diff", "adl",
}

# Tokens que, si aparecen, indican un comando de simulación/estimación.
SIMULATION_COMMANDS: Tuple[str, ...] = (
    "stoch_simul", "estimation", "simul", "perfect_foresight_solver",
    "discretionary_policy", "ramsey_policy", "osr",
)

# Expresión de un identificador válido de Dynare.
_IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
# Literales numéricos (incluida notación científica): se eliminan antes de
# extraer identificadores, para no confundir el "e" de "1e-3" con una variable.
_NUMBER = re.compile(r"(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?")
# Patrón de temporalidad: Ident(+1), C(-1), A(-2), ...
_TIMING = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(\s*([+-]?\d+)\s*\)")


# --------------------------------------------------------------------------- #
# Reporte
# --------------------------------------------------------------------------- #

@dataclass
class Report:
    """Resultado del análisis estático de un .mod."""

    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    infos: List[str] = field(default_factory=list)
    stats: Dict[str, object] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        """True si no hay errores (sí puede haber advertencias)."""
        return len(self.errors) == 0

    def to_markdown(self) -> str:
        """Render legible para mostrar en la UI."""
        lines: List[str] = []
        if self.ok:
            lines.append("### ✅ Verificación estática: sin errores")
        else:
            lines.append("### ❌ Verificación estática: se encontraron errores")

        if self.errors:
            lines.append("\n**Errores (rompen la compilación):**")
            lines += [f"- ❌ {e}" for e in self.errors]
        if self.warnings:
            lines.append("\n**Advertencias:**")
            lines += [f"- ⚠️ {w}" for w in self.warnings]
        if self.infos:
            lines.append("\n**Diagnóstico (Blanchard-Kahn):**")
            lines += [f"- ℹ️ {i}" for i in self.infos]

        s = self.stats
        if s:
            lines.append("\n**Conteos:**")
            lines.append(
                f"- Variables endógenas: {s.get('n_endogenous', '?')} | "
                f"Ecuaciones: {s.get('n_equations', '?')} | "
                f"Shocks: {s.get('n_exogenous', '?')} | "
                f"Parámetros: {s.get('n_parameters', '?')}"
            )
        return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Utilidades de parseo
# --------------------------------------------------------------------------- #

def strip_comments(text: str) -> str:
    """Elimina comentarios // ..., /* ... */ y % ... preservando saltos de línea."""
    # Comentarios de bloque /* ... */
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.DOTALL)
    # Comentarios de línea // ...  y  % ...
    text = re.sub(r"//[^\n]*", " ", text)
    text = re.sub(r"%[^\n]*", " ", text)
    return text


def _extract_block(text: str, keyword: str) -> Tuple[str, bool]:
    """Devuelve (contenido, encontrado) del primer bloque `keyword ...; ... end;`.

    Soporta opciones tras el keyword, p. ej. `model(linear);`.
    """
    pattern = re.compile(
        r"\b" + keyword + r"\b\s*(?:\([^)]*\))?\s*;(.*?)\bend\s*;",
        re.DOTALL | re.IGNORECASE,
    )
    m = pattern.search(text)
    if m:
        return m.group(1), True
    return "", False


def _declared_names(text: str, keyword: str) -> List[str]:
    """Extrae los nombres declarados tras `var`/`varexo`/`parameters` hasta `;`.

    Maneja múltiples declaraciones del mismo tipo y anotaciones entre
    paréntesis o signos $...$ (LaTeX) que se ignoran.
    """
    names: List[str] = []
    # Cada declaración: keyword [opciones] nombres... ;
    pattern = re.compile(
        r"\b" + keyword + r"\b\s*(?:\([^)]*\))?\s*([^;]*);",
        re.IGNORECASE,
    )
    for m in pattern.finditer(text):
        chunk = m.group(1)
        # Quitar anotaciones LaTeX $...$ y (long_name='...')
        chunk = re.sub(r"\$[^$]*\$", " ", chunk)
        chunk = re.sub(r"\([^)]*\)", " ", chunk)
        chunk = re.sub(r"'[^']*'", " ", chunk)
        names.extend(_IDENT.findall(chunk))
    return names


def _strip_all_blocks(text: str, keywords: List[str]) -> str:
    """Elimina por completo los bloques indicados (para aislar asignaciones)."""
    for kw in keywords:
        text = re.sub(
            r"\b" + kw + r"\b\s*(?:\([^)]*\))?\s*;.*?\bend\s*;",
            " ",
            text,
            flags=re.DOTALL | re.IGNORECASE,
        )
    return text


def _split_equations(model_body: str) -> Tuple[List[str], List[str]]:
    """Separa el cuerpo del bloque model en (ecuaciones, variables_locales).

    - Las definiciones model-local `#x = ...;` NO cuentan como ecuaciones.
    - Las etiquetas `[name='...']` se descartan (no son ecuaciones).
    """
    # Quitar etiquetas de ecuación [ ... ]
    body = re.sub(r"\[[^\]]*\]", " ", model_body)
    equations: List[str] = []
    locals_: List[str] = []
    for raw in body.split(";"):
        stmt = raw.strip()
        if not stmt:
            continue
        if stmt.startswith("#"):
            # Definición de variable model-local: #name = expr
            m = re.match(r"#\s*([A-Za-z_][A-Za-z0-9_]*)", stmt)
            if m:
                locals_.append(m.group(1))
            continue
        equations.append(stmt)
    return equations, locals_


def _used_symbols(equations: List[str]) -> Set[str]:
    """Identificadores usados en las ecuaciones, sin números ni temporalidad."""
    used: Set[str] = set()
    for eq in equations:
        cleaned = _NUMBER.sub(" ", eq)
        used.update(_IDENT.findall(cleaned))
    return used


def _assigned_parameters(text_wo_blocks: str, params: Set[str]) -> Set[str]:
    """Detecta qué parámetros reciben un valor (`param = ...;`)."""
    assigned: Set[str] = set()
    for m in re.finditer(r"([A-Za-z_][A-Za-z0-9_]*)\s*=", text_wo_blocks):
        name = m.group(1)
        if name in params:
            assigned.add(name)
    return assigned


# --------------------------------------------------------------------------- #
# Análisis principal
# --------------------------------------------------------------------------- #

def analyze(mod_text: str) -> Report:
    """Analiza estáticamente un archivo .mod y devuelve un Report."""
    report = Report()
    text = strip_comments(mod_text)

    # 1) Declaraciones -------------------------------------------------------
    endogenous = _declared_names(text, "var")
    # `varexo` también empieza con "var": separarlos correctamente.
    exogenous = _declared_names(text, "varexo")
    exogenous_det = _declared_names(text, "varexo_det")
    # Quitar de endógenas las que en realidad eran varexo/varexo_det.
    exo_all = set(exogenous) | set(exogenous_det)
    endogenous = [v for v in endogenous if v not in exo_all]
    parameters = _declared_names(text, "parameters")

    endo_set: Set[str] = set(endogenous)
    exo_set: Set[str] = set(exogenous) | set(exogenous_det)
    par_set: Set[str] = set(parameters)

    # Duplicados
    for label, seq in (("var", endogenous), ("varexo", exogenous),
                       ("parameters", parameters)):
        dupes = {n for n in seq if seq.count(n) > 1}
        if dupes:
            report.errors.append(
                f"Declaración duplicada en `{label}`: {', '.join(sorted(dupes))}"
            )

    # 2) Bloque model --------------------------------------------------------
    model_body, has_model = _extract_block(text, "model")
    if not has_model:
        report.errors.append("No se encontró el bloque `model; ... end;`.")
        report.stats = {
            "n_endogenous": len(endo_set),
            "n_exogenous": len(exo_set),
            "n_parameters": len(par_set),
            "n_equations": 0,
        }
        return report

    equations, model_locals = _split_equations(model_body)
    local_set: Set[str] = set(model_locals)
    n_eq = len(equations)

    # 3) Conteo ecuaciones vs variables -------------------------------------
    if n_eq != len(endo_set):
        report.errors.append(
            f"El número de ecuaciones ({n_eq}) no coincide con el número de "
            f"variables endógenas declaradas en `var` ({len(endo_set)}). "
            f"Dynare exige #ecuaciones = #variables endógenas."
        )

    # 4) Símbolos usados vs declarados --------------------------------------
    used = _used_symbols(equations)
    known = (endo_set | exo_set | par_set | local_set
             | DYNARE_FUNCTIONS | DYNARE_KEYWORDS)
    undeclared = sorted(s for s in used if s not in known)
    if undeclared:
        report.errors.append(
            "Símbolos usados en el modelo pero no declarados "
            f"(en var/varexo/parameters): {', '.join(undeclared)}."
        )

    # Variables endógenas declaradas pero no usadas en el modelo.
    unused = sorted(v for v in endo_set if v not in used)
    if unused:
        report.errors.append(
            "Variables declaradas en `var` que no aparecen en ninguna "
            f"ecuación: {', '.join(unused)}. Elimínalas o añade su ecuación."
        )

    # 5) Parámetros sin valor -----------------------------------------------
    text_wo_blocks = _strip_all_blocks(
        text, ["model", "steady_state_model", "initval", "endval",
                "shocks", "estimated_params"]
    )
    assigned = _assigned_parameters(text_wo_blocks, par_set)
    missing_vals = sorted(par_set - assigned)
    if missing_vals:
        report.errors.append(
            "Parámetros declarados sin valor asignado (Dynare los toma como 0): "
            f"{', '.join(missing_vals)}."
        )

    # 6) Bloques estructurales (advertencias) -------------------------------
    _, has_sstate = _extract_block(text, "steady_state_model")
    _, has_initval = _extract_block(text, "initval")
    if not has_sstate and not has_initval:
        report.warnings.append(
            "No hay `steady_state_model` ni `initval`. Dynare intentará hallar "
            "el estado estacionario numéricamente y puede no converger."
        )
    _, has_shocks = _extract_block(text, "shocks")
    if not has_shocks:
        report.warnings.append(
            "No hay bloque `shocks`. Sin varianzas, no habrá IRFs ni momentos."
        )
    if not any(cmd in text for cmd in SIMULATION_COMMANDS):
        report.warnings.append(
            "No se encontró un comando de simulación/estimación "
            "(p. ej. `stoch_simul`). El modelo se resolverá pero no producirá salida."
        )

    # 7) Diagnóstico Blanchard-Kahn (heurística informativa) -----------------
    states: Set[str] = set()
    jumps: Set[str] = set()
    for name, shift in _TIMING.findall(model_body):
        if name in DYNARE_FUNCTIONS or name not in endo_set:
            continue
        s = int(shift)
        if s < 0:
            states.add(name)
        elif s > 0:
            jumps.add(name)
    if states:
        report.infos.append(
            f"Variables de estado (rezago): {', '.join(sorted(states))}."
        )
    if jumps:
        report.infos.append(
            f"Variables forward-looking / jump (adelanto): "
            f"{', '.join(sorted(jumps))}."
        )
    report.infos.append(
        "Recuerda la condición BK: #eigenvalores explosivos debe igualar "
        "#variables forward-looking para una solución única y estable."
    )

    # 8) Estadísticas --------------------------------------------------------
    report.stats = {
        "n_endogenous": len(endo_set),
        "n_exogenous": len(exo_set),
        "n_parameters": len(par_set),
        "n_equations": n_eq,
        "n_states": len(states),
        "n_jumps": len(jumps),
    }
    return report


if __name__ == "__main__":  # pragma: no cover
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as fh:
            print(analyze(fh.read()).to_markdown())
    else:
        print("Uso: python verifier.py modelo.mod")
