"""
app.py — Interfaz Gradio de MacroBuilt (entrypoint para Hugging Face Spaces).

MacroBuilt — Tu laboratorio macroeconómico.

Pestañas:
  1. "Traducir":  economía del modelo -> .mod + explicación (modo aprendizaje opc.).
  2. "Foto de pizarra": foto -> OCR (modelos PaddleOCR) -> caja editable -> traducir.
  3. "Bootcamp": mini-curso "Introducción a Dynare", ejercicios autocorregidos.
  4. "Verificar":  pegas un .mod y el verificador estático te dice si compilará.
"""

from __future__ import annotations

import os

import gradio as gr

from dynare_translate.core.translator import translate
from dynare_translate.core.verifier import analyze
from dynare_translate.core.ocr import image_to_text
from dynare_translate.core import bootcamp

# --------------------------------------------------------------------------- #
# Marca y estilo
# --------------------------------------------------------------------------- #

THEME = gr.themes.Soft(
    primary_hue=gr.themes.colors.indigo,
    secondary_hue=gr.themes.colors.blue,
    neutral_hue=gr.themes.colors.slate,
    font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"],
    radius_size=gr.themes.sizes.radius_lg,
)

CSS = """
.gradio-container {max-width: 1080px !important; margin: 0 auto !important;}
#mb-hero {border-radius: 18px; box-shadow: 0 10px 30px rgba(79,70,229,.18);}
.mb-chip {background: rgba(255,255,255,.18); padding: 5px 11px; border-radius: 999px;
          font-size: 12.5px; white-space: nowrap;}
.mb-note {color: var(--body-text-color-subdued); font-size: 13px;}
"""

HERO = """
<div id="mb-hero" style="background:linear-gradient(120deg,#4f46e5 0%,#3b82f6 100%);
     padding:30px 34px; color:#fff;">
  <div style="font-size:30px; font-weight:800; letter-spacing:-.5px;">🧪 MacroBuilt</div>
  <div style="font-size:17px; font-weight:600; margin-top:2px; opacity:.96;">
     Tu laboratorio macroeconómico</div>
  <div style="font-size:14px; margin-top:10px; opacity:.92; max-width:700px; line-height:1.5;">
     De la pizarra a un modelo que corre: traduce tus ecuaciones a código Dynare
     correcto, verificado y explicado paso a paso. Para estudiantes de macro.</div>
  <div style="margin-top:15px; display:flex; gap:8px; flex-wrap:wrap;">
     <span class="mb-chip">✍️ Pega tus ecuaciones</span>
     <span class="mb-chip">📷 Foto de pizarra</span>
     <span class="mb-chip">🎓 Bootcamp interactivo</span>
     <span class="mb-chip">✅ Verificación instantánea</span>
  </div>
</div>
"""

FOOTER = """
<div style="text-align:center; margin-top:14px;" class="mb-note">
  <b>MacroBuilt</b> · Tu laboratorio macroeconómico · Hecho para alumnos de Macro de la UP<br>
  Verificador determinista open-source · Traducción con DeepSeek · OCR con PaddleOCR (PP-OCRv4)
</div>
"""

# --------------------------------------------------------------------------- #
# Ejemplos precargados
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
    result = translate(economic_input, learning_mode=bool(learning_mode))
    if result.error and not result.mod_code:
        return "", f"### ⚠️ No se pudo traducir\n\n{result.error}", ""
    report_md = result.report.to_markdown() if result.report else ""
    if result.repairs:
        report_md = (f"_Auto-reparación aplicada: {result.repairs} iteración(es)._\n\n"
                     + report_md)
    return result.mod_code, report_md, result.explanation


def do_verify(mod_text: str):
    if not mod_text or not mod_text.strip():
        return "### ℹ️ Pega un archivo .mod para verificarlo."
    return analyze(mod_text).to_markdown()


def do_ocr(image_path: str):
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


def on_lesson_change(title: str):
    return bootcamp.lesson_intro(title), bootcamp.lesson_starter(title), ""


def do_check_lesson(title: str, code: str):
    return bootcamp.check_lesson(title, code)


def do_show_solution(title: str):
    return bootcamp.lesson_solution(title)


# --------------------------------------------------------------------------- #
# UI
# --------------------------------------------------------------------------- #

def build_demo() -> gr.Blocks:
    titles = bootcamp.lesson_titles()

    with gr.Blocks(title="MacroBuilt — Tu laboratorio macroeconómico",
                   theme=THEME, css=CSS) as demo:
        gr.HTML(HERO)

        # ---- Tab 1: Traducir ----
        with gr.Tab("✍️ Traducir"):
            gr.Markdown(
                "Pega las ecuaciones que ya derivaste (FONCs, vaciado de mercado, "
                "leyes de movimiento), tus variables y tu calibración."
            )
            inp = gr.Textbox(label="Descripción económica del modelo",
                             lines=16, value=EXAMPLE_INPUT_RBC)
            learn = gr.Checkbox(
                label="Modo aprendizaje (explicación más didáctica + ejercicios)",
                value=False)
            btn = gr.Button("Traducir a Dynare", variant="primary")
            out_code = gr.Code(label="Archivo .mod", language="python")
            out_report = gr.Markdown()
            out_expl = gr.Markdown()
            btn.click(do_translate, inputs=[inp, learn],
                      outputs=[out_code, out_report, out_expl])

        # ---- Tab 2: Foto de pizarra ----
        with gr.Tab("📷 Foto de pizarra"):
            gr.Markdown(
                "Sube una **foto de tus ecuaciones** (pizarra o papel). El OCR "
                "(modelos PaddleOCR / PP-OCRv4) las lee y las coloca abajo para que "
                "**las revises y corrijas** antes de traducir.\n\n"
                "_Tip: foto nítida y con buena luz. El OCR a veces confunde "
                "`I`↔`1` o `^`↔`~`; corrígelo en la caja antes de traducir._"
            )
            img = gr.Image(type="filepath", label="Foto de tus ecuaciones")
            ocr_btn = gr.Button("Leer ecuaciones (OCR)")
            extracted = gr.Textbox(
                label="Texto leído — revísalo y corrígelo antes de traducir",
                lines=10)
            ocr_btn.click(do_ocr, inputs=img, outputs=extracted)
            learn2 = gr.Checkbox(
                label="Modo aprendizaje (explicación más didáctica + ejercicios)",
                value=False)
            trans_btn2 = gr.Button("Traducir lo leído", variant="primary")
            out_code2 = gr.Code(label="Archivo .mod", language="python")
            out_report2 = gr.Markdown()
            out_expl2 = gr.Markdown()
            trans_btn2.click(do_translate, inputs=[extracted, learn2],
                             outputs=[out_code2, out_report2, out_expl2])

        # ---- Tab 3: Bootcamp ----
        with gr.Tab("🎓 Bootcamp"):
            gr.Markdown(
                "**Introducción a Dynare.** Lee la teoría, resuelve el ejercicio "
                "en el editor y pulsa **Comprobar**: el verificador te corrige al "
                "instante (no necesitas tener Dynare instalado)."
            )
            lesson_sel = gr.Radio(choices=titles, value=titles[0],
                                  label="Lecciones")
            lesson_md = gr.Markdown(bootcamp.lesson_intro(titles[0]))
            lesson_code = gr.Code(label="Tu .mod (edítalo y comprueba)",
                                  language="python",
                                  value=bootcamp.lesson_starter(titles[0]))
            with gr.Row():
                check_btn = gr.Button("Comprobar", variant="primary")
                sol_btn = gr.Button("Ver solución")
            lesson_feedback = gr.Markdown()
            lesson_sel.change(on_lesson_change, inputs=lesson_sel,
                              outputs=[lesson_md, lesson_code, lesson_feedback])
            check_btn.click(do_check_lesson, inputs=[lesson_sel, lesson_code],
                            outputs=lesson_feedback)
            sol_btn.click(do_show_solution, inputs=lesson_sel,
                          outputs=lesson_code)

        # ---- Tab 4: Verificar ----
        with gr.Tab("✅ Verificar (offline)"):
            gr.Markdown(
                "Pega un archivo .mod y el verificador estático te dirá si "
                "compilará y por qué. **No necesita conexión ni API key.**"
            )
            vin = gr.Code(label="Tu archivo .mod", language="python",
                          value=_load_golden_mod())
            vbtn = gr.Button("Verificar", variant="primary")
            vout = gr.Markdown()
            vbtn.click(do_verify, inputs=vin, outputs=vout)

        gr.HTML(FOOTER)
    return demo


if __name__ == "__main__":
    build_demo().launch()
