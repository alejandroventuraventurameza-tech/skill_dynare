"""Pruebas del mini-bootcamp: cada solución pasa y cada starter falla."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dynare_translate.core import bootcamp  # noqa: E402


def test_hay_lecciones():
    assert len(bootcamp.LESSONS) >= 3
    assert len(bootcamp.lesson_titles()) == len(bootcamp.LESSONS)


def test_cada_solucion_pasa_el_checker():
    for l in bootcamp.LESSONS:
        passed, _ = l["check"](l["solution"])
        assert passed, f"La solución de {l['id']} debería pasar"


def test_cada_starter_falla():
    for l in bootcamp.LESSONS:
        passed, _ = l["check"](l["starter"])
        assert not passed, f"El starter de {l['id']} debería fallar (si no, es trivial)"


def test_helpers_por_titulo():
    titles = bootcamp.lesson_titles()
    assert "Ejercicio" in bootcamp.lesson_intro(titles[0])
    assert bootcamp.lesson_starter(titles[0]).strip() != ""
    # check_lesson devuelve markdown de feedback
    fb = bootcamp.check_lesson(titles[0], bootcamp.lesson_solution(titles[0]))
    assert "✅" in fb
