"""Pruebas offline de la capa de traducción (no llaman a la API)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dynare_translate.core.translator import (  # noqa: E402
    extract_dynare_block, extract_explanation, translate,
)


def test_extract_dynare_block_with_fence():
    text = "Intro\n```dynare\nvar x;\nmodel;\nx=1;\nend;\n```\nfin"
    assert extract_dynare_block(text) == "var x;\nmodel;\nx=1;\nend;"


def test_extract_block_without_fence_returns_text():
    text = "var x; model; x=1; end;"
    assert extract_dynare_block(text) == "var x; model; x=1; end;"


def test_extract_explanation_removes_code():
    text = "Antes\n```dynare\nvar x;\n```\n## Explicación\nDefine x."
    expl = extract_explanation(text)
    assert "var x;" not in expl
    assert "Define x." in expl


def test_translate_empty_input():
    r = translate("")
    assert not r.ok
    assert "vac" in (r.error or "").lower()


def test_translate_without_api_key_degrades():
    # Sin la API key del proveedor debe devolver error claro, nunca lanzar.
    saved = {k: os.environ.pop(k, None)
             for k in ("DEEPSEEK_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY")}
    try:
        r = translate("var x; x = 1;")
        assert not r.ok
        assert "API_KEY" in (r.error or "")
    finally:
        for k, v in saved.items():
            if v is not None:
                os.environ[k] = v


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    ok = 0
    for fn in fns:
        try:
            fn(); print(f"PASS  {fn.__name__}"); ok += 1
        except AssertionError as e:
            print(f"FAIL  {fn.__name__}: {e}")
    print(f"\n{ok}/{len(fns)} OK")
    sys.exit(0 if ok == len(fns) else 1)
