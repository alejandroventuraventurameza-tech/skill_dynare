"""
app.py — Interfaz Gradio de Dynare Translate (entrypoint para Hugging Face Spaces).

Tres modos:
  1. "Traducir":  pegas la economía del modelo (FONCs, variables, parámetros) y
     obtienes un .mod correcto + explicación pedagógica. Usa la API (DeepSeek).
     Opción "modo aprendizaje" (bootcamp): explicación más didáctica + ejercicios.
  2. "Foto de pizarra": subes una foto de tus ecuaciones, el OCR (modelos
     PaddleOCR / PP-OCRv4) las lee, las corriges en una caja editable y traduces.
  3. "Verificar":  pegas un .mod y el verificador estático te dice si compilará.
     NO necesita API key — funciona 100% offline (ideal para el demo en vivo).
"""

from __future__ import annotations

import os

import gradio as gr

from dynare_translate.core.translator import translate
from dynare_translate.core.verifier import analyze
from dynare_translate.core.ocr import image_to_text

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

def do_translate(economic_input: str, learning_mode: bool = False):
    """Traduce la entrada económica a .mod (código, verificación, explicación)."""
    result = translate(economic_input, learning_mode=bool(learning_mode))
    if result.error and not result.mod_code:
        return "", f"### ⚠️ No se pudo traducir\n\n{result.error}", ""
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


def do_ocr(image_path: str):
    """Lee las ecuaciones de una foto y devuelve el texto (editable)."""
    if not image_path:
        return "Sube una foto primero."
    try:
        text = image_to_text(image_path)
    except RuntimeError as exc:
        return f"[OCR no disponible] {exc}"
    if not text.strip():
        return ("No se detectó texto. Prueba con una foto más nítida, con buena "
                "luz y las ecuaciones bien marcadas.")
    return text


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

        # ---- Tab 1: Traducir ----
        with gr.Tab("Traducir economía → Dynare"):
            gr.Markdown(
                "Pega las ecuaciones que ya derivaste (FONCs, vaciado de mercado, "
                "leyes de movimiento), tus variables y tu calibración."
            )
            inp = gr.Textbox(
                label="Descripción económica del modelo",
                lines=16, value=EXAMPLE_INPUT_RBC,
            )
            learn = gr.Checkbox(
                label="Modo aprendizaje (explicación más didáctica + ejercicios)",
                value=False,
            )
            btn = gr.Button("Traducir a Dynare", variant="primary")
            out_code = gr.Code(label="Archivo .mod", language="python")
            out_report = gr.Markdown(label="Verificación estática")
            out_expl = gr.Markdown(label="Explicación por bloque (bootcamp)")
            btn.click(do_translate, inputs=[inp, learn],
                      outputs=[out_code, out_report, out_expl])

        # ---- Tab 2: Foto de pizarra ----
        with gr.Tab("Foto de pizarra → Dynare (beta)"):
            gr.Markdown(
                "📷 Sube una **foto de tus ecuaciones** (pizarra o papel). El OCR "
                "(modelos PaddleOCR / PP-OCRv4) las lee y las coloca abajo para que "
                "**las revises y corrijas** antes de traducir.\n\n"
                "_Tip: foto nítida, con buena luz y letra clara. El OCR a veces "
                "confunde `I`↔`1` o `^`↔`~`; corrígelo en la caja antes de traducir._"
            )
            img = gr.Image(type="filepath", label="Foto de tus ecuaciones")
            ocr_btn = gr.Button("Leer ecuaciones (OCR)")
            extracted = gr.Textbox(
                label="Texto leído — revísalo y corrígelo antes de traducir",
                lines=10,
            )
            ocr_btn.click(do_ocr, inputs=img, outputs=extracted)

            learn2 = gr.Checkbox(
                label="Modo aprendizaje (explicación más didáctica + ejercicios)",
                value=False,
            )
            trans_btn2 = gr.Button("Traducir lo leído", variant="primary")
            out_code2 = gr.Code(label="Archivo .mod", language="python")
            out_report2 = gr.Markdown(label="Verificación estática")
            out_expl2 = gr.Markdown(label="Explicación por bloque (bootcamp)")
            trans_btn2.click(do_translate, inputs=[extracted, learn2],
                             outputs=[out_code2, out_report2, out_expl2])

        # ---- Tab 3: Verificar (offline) ----
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
            "abierto; la traducción usa la API de DeepSeek; el OCR usa los modelos "
            "PaddleOCR (PP-OCRv4).*"
        )
    return demo


if __name__ == "__main__":
    build_demo().launch()
