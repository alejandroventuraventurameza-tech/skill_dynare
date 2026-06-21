"""
app.py — Interfaz Gradio de Dynare Translate (entrypoint para Hugging Face Spaces).

Dos modos:
  1. "Traducir":  pegas la economía del modelo (FONCs, variables, parámetros) y
     obtienes un .mod correcto + explicación pedagógica. Usa la API de Anthropic.
  2. "Verificar":  pegas un .mod y el verificador estático te dice si compilará
     y por qué. NO necesita API key — funciona 100% offline (ideal para el demo
     en vivo aunque falle la red).
"""

from __future__ import annotations

import os

import gradio as gr

from dynare_translate.core.translator import translate
from dynare_translate.core.verifier import analyze

# --------------------------------------------------------------------------- #
# Ejemplos precargados ("de oro")
# --------------------------------------------------------------------------- #

EXAMPLE_INPUT_RBC = """\
Modelo: RBC básico (economía cerrada, hogar y firma representativos).
Notación: variables en niveles. El capital disponible en t es K(-1).

Variables endógenas: Y (producto), C (consumo), I (inversión), K (capital),
L (trabajo), W (salario real), R (retorno bruto del capital), A (TFP).
Shock: e_a (innovación de productividad).
Parámetros: beta=0.99, alpha=0.33, delta=0.025, sigma=1, phi=1, rho_a=0.95.

Ecuaciones (ya derivadas):
1. Euler del consumo: C^(-sigma) = beta * E[C(+1)^(-sigma) * R(+1)]
2. Oferta de trabajo: W = phi * L / C^(-sigma)
3. Retorno del capital: R = alpha * A * K(-1)^(alpha-1) * L^(1-alpha) + (1-delta)
4. Salario = PMgL: W = (1-alpha) * A * K(-1)^alpha * L^(-alpha)
5. Producción: Y = A * K(-1)^alpha * L^(1-alpha)
6. Vaciado de bienes: Y = C + I
7. Capital: K = (1-delta) * K(-1) + I
8. TFP AR(1): log(A) = rho_a * log(A(-1)) + e_a
"""

_HERE = os.path.dirname(os.path.abspath(__file__))
_GOLDEN_MOD = os.path.join(_HERE, "examples", "01_rbc", "rbc_basic.mod")


def _load_golden_mod() -> str:
    try:
        with open(_GOLDEN_MOD, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return "// (ejemplo no disponible)"


# --------------------------------------------------------------------------- #
# Callbacks
# --------------------------------------------------------------------------- #

def do_translate(economic_input: str):
    """Traduce la entrada económica a .mod y devuelve (código, verificación, explicación)."""
    result = translate(economic_input)
    if result.error and not result.mod_code:
        msg = f"### ⚠️ No se pudo traducir\n\n{result.error}"
        return "", msg, ""
    report_md = result.report.to_markdown() if result.report else ""
    if result.repairs:
        report_md = (f"_Auto-reparación aplicada: {result.repairs} iteración(es)._\n\n"
                     + report_md)
    return result.mod_code, report_md, result.explanation


def do_verify(mod_text: str):
    """Verifica estáticamente un .mod pegado por el usuario (offline)."""
    if not mod_text or not mod_text.strip():
        return "### ℹ️ Pega un archivo .mod para verificarlo."
    return analyze(mod_text).to_markdown()


# --------------------------------------------------------------------------- #
# UI
# --------------------------------------------------------------------------- #

def build_demo() -> gr.Blocks:
    with gr.Blocks(title="Dynare Translate", theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            "# 🧮 Dynare Translate\n"
            "**Convierte la pizarra en un laboratorio.** Tú derivas la economía; "
            "nosotros la traducimos a código Dynare correcto, verificado y "
            "explicado paso a paso. Para estudiantes de macro de pregrado."
        )

        with gr.Tab("Traducir economía → Dynare"):
            gr.Markdown(
                "Pega las ecuaciones que ya derivaste (FONCs, vaciado de mercado, "
                "leyes de movimiento), tus variables y tu calibración."
            )
            inp = gr.Textbox(
                label="Descripción económica del modelo",
                lines=16, value=EXAMPLE_INPUT_RBC,
            )
            btn = gr.Button("Traducir a Dynare", variant="primary")
            out_code = gr.Code(label="Archivo .mod", language="python")
            out_report = gr.Markdown(label="Verificación estática")
            out_expl = gr.Markdown(label="Explicación por bloque (bootcamp)")
            btn.click(do_translate, inputs=inp,
                      outputs=[out_code, out_report, out_expl])

        with gr.Tab("Verificar un .mod (offline)"):
            gr.Markdown(
                "Pega un archivo .mod y el verificador estático te dirá si "
                "compilará y por qué. **No necesita conexión ni API key.**"
            )
            vin = gr.Code(label="Tu archivo .mod", language="python",
                          value=_load_golden_mod())
            vbtn = gr.Button("Verificar", variant="primary")
            vout = gr.Markdown()
            vbtn.click(do_verify, inputs=vin, outputs=vout)

        gr.Markdown(
            "---\n*Hecho para los alumnos de Macroeconomía II y Macroeconomía "
            "Internacional de la UP. El verificador es determinista y de código "
            "abierto; la traducción usa la API de Anthropic.*"
        )
    return demo


if __name__ == "__main__":
    build_demo().launch()
