"""
ocr.py — Lectura de ecuaciones desde una foto (OCR) con los modelos PaddleOCR.

Usa rapidocr-onnxruntime: los modelos PP-OCRv4 de PaddleOCR ejecutados sobre
ONNX Runtime. Es ligero (no requiere paddlepaddle) y de buena calidad en texto
impreso/claro. Para manuscrito de pizarra el resultado es aproximado: por eso el
flujo del producto SIEMPRE pasa por una caja de texto editable (humano en el
medio) antes de traducir.

El motor se carga de forma perezosa y la importación está protegida: si el
paquete no está disponible, la app principal sigue funcionando (la pestaña de
imagen avisa que el OCR no está disponible, pero el resto no se cae).
"""

from __future__ import annotations

from typing import List, Tuple

_engine = None


def _get_engine():
    """Carga perezosa del motor PP-OCR (una sola vez)."""
    global _engine
    if _engine is None:
        from rapidocr_onnxruntime import RapidOCR  # import perezoso
        _engine = RapidOCR()
    return _engine


def ocr_available() -> bool:
    """True si el motor OCR puede cargarse en este entorno."""
    try:
        _get_engine()
        return True
    except Exception:
        return False


def _reading_order(item: Tuple) -> Tuple[float, float]:
    """Clave de orden de lectura: primero por fila (y), luego por columna (x)."""
    box = item[0]
    ys = [p[1] for p in box]
    xs = [p[0] for p in box]
    return (min(ys), min(xs))


def image_to_text(image_path: str) -> str:
    """Extrae el texto de una imagen y lo devuelve en orden de lectura.

    Lanza RuntimeError con un mensaje claro si el OCR no está disponible.
    """
    if not image_path:
        return ""
    try:
        engine = _get_engine()
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            "El OCR no está disponible en este entorno "
            f"(no se pudo cargar rapidocr-onnxruntime: {exc})."
        ) from exc

    result, _ = engine(image_path)
    if not result:
        return ""
    items: List[Tuple] = sorted(result, key=_reading_order)
    return "\n".join(str(it[1]).strip() for it in items if str(it[1]).strip())
