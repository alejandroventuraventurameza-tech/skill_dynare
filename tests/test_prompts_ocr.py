"""Pruebas del modo aprendizaje y del módulo OCR (offline / con skip)."""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dynare_translate.core.prompts import build_user_prompt  # noqa: E402


def test_user_prompt_sin_modo_aprendizaje():
    p = build_user_prompt("var x; x=1;", learning_mode=False)
    assert "MODO APRENDIZAJE" not in p
    assert "ENTRADA ECONÓMICA" in p


def test_user_prompt_con_modo_aprendizaje():
    p = build_user_prompt("var x; x=1;", learning_mode=True)
    assert "MODO APRENDIZAJE" in p
    assert "Ejercicios" in p


def test_ocr_module_importable():
    # El módulo debe importarse aunque rapidocr no esté instalado (import perezoso).
    from dynare_translate.core import ocr
    assert hasattr(ocr, "image_to_text")
    assert ocr.image_to_text("") == ""   # ruta vacía -> sin texto, sin excepción


def test_ocr_inference_if_available():
    # Solo corre si rapidocr está instalado (en CI se salta).
    pytest.importorskip("rapidocr_onnxruntime")
    from PIL import Image, ImageDraw
    from dynare_translate.core.ocr import image_to_text
    img = Image.new("RGB", (300, 80), "white")
    ImageDraw.Draw(img).text((10, 25), "Y = C + I", fill="black")
    path = "/tmp/_ocr_test.png"
    img.save(path)
    text = image_to_text(path)
    assert "Y" in text and "C" in text
