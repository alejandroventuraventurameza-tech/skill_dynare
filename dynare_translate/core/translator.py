"""
translator.py — Capa de traducción económica -> Dynare con proveedor LLM configurable.

Proveedor por defecto: DeepSeek (API compatible con OpenAI, la más económica).
También soporta OpenAI y Anthropic cambiando la variable LLM_PROVIDER.

Flujo:
  1. Construye el system prompt desde la base de conocimiento (prompts.py).
  2. Pide al modelo el .mod + explicación pedagógica.
  3. Extrae el bloque ```dynare``` y lo pasa por el verificador estático.
  4. Si hay errores, ejecuta un bucle de AUTO-REPARACIÓN (manda el reporte de
     vuelta al modelo) hasta `max_repairs` veces.
  5. Devuelve un TranslationResult con el .mod, la explicación, el reporte del
     verificador y metadatos.

El producto está pensado para ser inter-IA. Por eso la API se encapsula aquí:
cambiar de proveedor (OpenAI, Gemini, modelo open source) solo requiere
reimplementar `_call_llm`.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import List, Optional

from .prompts import build_system_prompt, build_user_prompt, build_repair_prompt
from .verifier import analyze, Report

MAX_TOKENS = int(os.environ.get("DYNARE_MAX_TOKENS", "4096"))

# Proveedor por defecto: DeepSeek (API compatible con OpenAI, la más económica).
# Se puede cambiar con la variable de entorno LLM_PROVIDER.
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "deepseek").lower()

_PROVIDERS = {
    "deepseek": {
        "key_env": "DEEPSEEK_API_KEY",
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat",
        "kind": "openai",          # usa el SDK de OpenAI (API compatible)
    },
    "openai": {
        "key_env": "OPENAI_API_KEY",
        "base_url": None,
        "model": "gpt-4o-mini",
        "kind": "openai",
    },
    "anthropic": {
        "key_env": "ANTHROPIC_API_KEY",
        "base_url": None,
        "model": "claude-sonnet-4-6",
        "kind": "anthropic",
    },
}


def _provider_config(provider: Optional[str] = None) -> dict:
    """Resuelve la configuración del proveedor (con override de modelo por env)."""
    name = (provider or LLM_PROVIDER).lower()
    if name not in _PROVIDERS:
        raise RuntimeError(
            f"Proveedor LLM no soportado: '{name}'. "
            f"Opciones: {', '.join(_PROVIDERS)}."
        )
    cfg = dict(_PROVIDERS[name])
    cfg["provider"] = name
    cfg["model"] = os.environ.get("DYNARE_MODEL", cfg["model"])
    return cfg


_FENCE = re.compile(r"```(?:dynare|matlab|octave)?\s*\n(.*?)```", re.DOTALL)


@dataclass
class TranslationResult:
    mod_code: str
    explanation: str
    report: Optional[Report]
    repairs: int = 0
    attempts: List[str] = field(default_factory=list)
    error: Optional[str] = None

    @property
    def ok(self) -> bool:
        return self.error is None and self.report is not None and self.report.ok


def extract_dynare_block(text: str) -> str:
    """Extrae el primer bloque de código de la respuesta del modelo.

    Si no hay bloque con fence, devuelve el texto tal cual (degradación elegante).
    """
    m = _FENCE.search(text)
    return (m.group(1).strip() if m else text.strip())


def extract_explanation(text: str) -> str:
    """Devuelve la parte fuera del bloque de código (la explicación pedagógica)."""
    explanation = _FENCE.sub("", text).strip()
    # Quitar encabezados sueltos vacíos
    return explanation if explanation else "(sin explicación adicional)"


# --------------------------------------------------------------------------- #
# Llamada al proveedor LLM (encapsulada para ser inter-IA)
# --------------------------------------------------------------------------- #

def _call_llm(system_prompt: str, messages: List[dict],
              provider: Optional[str] = None) -> str:
    """Llama al proveedor LLM configurado. RuntimeError con mensaje claro si falla.

    Soporta proveedores con API compatible con OpenAI (DeepSeek, OpenAI) y
    Anthropic. El proveedor por defecto es DeepSeek (el más económico).
    """
    cfg = _provider_config(provider)
    api_key = os.environ.get(cfg["key_env"])
    if not api_key:
        raise RuntimeError(
            f"Falta la variable de entorno {cfg['key_env']} para el proveedor "
            f"'{cfg['provider']}'. Copia .env.example a .env y coloca tu clave."
        )

    if cfg["kind"] == "openai":
        try:
            from openai import OpenAI  # import perezoso
        except ImportError as exc:
            raise RuntimeError(
                "El paquete 'openai' no está instalado. Ejecuta: "
                "pip install -r requirements.txt"
            ) from exc
        client = OpenAI(api_key=api_key, base_url=cfg["base_url"])
        resp = client.chat.completions.create(
            model=cfg["model"],
            max_tokens=MAX_TOKENS,
            messages=[{"role": "system", "content": system_prompt}] + messages,
        )
        return resp.choices[0].message.content or ""

    # kind == "anthropic"
    try:
        import anthropic  # import perezoso
    except ImportError as exc:
        raise RuntimeError(
            "El paquete 'anthropic' no está instalado. Ejecuta: "
            "pip install -r requirements.txt"
        ) from exc
    client = anthropic.Anthropic(api_key=api_key)
    resp = client.messages.create(
        model=cfg["model"],
        max_tokens=MAX_TOKENS,
        system=system_prompt,
        messages=messages,
    )
    return "".join(
        block.text for block in resp.content if getattr(block, "type", "") == "text"
    )


# --------------------------------------------------------------------------- #
# API pública
# --------------------------------------------------------------------------- #

def translate(economic_input: str, max_repairs: int = 2,
              provider: Optional[str] = None) -> TranslationResult:
    """Traduce una descripción económica a un .mod verificado.

    Parameters
    ----------
    economic_input : str
        FONCs / ecuaciones / variables / parámetros que entrega el investigador.
    max_repairs : int
        Cuántas veces reintentar la auto-reparación si el verificador halla errores.
    provider : str, optional
        Proveedor LLM ("deepseek", "openai", "anthropic"). Por defecto, el de
        la variable de entorno LLM_PROVIDER (DeepSeek).
    """
    if not economic_input or not economic_input.strip():
        return TranslationResult(
            mod_code="", explanation="", report=None,
            error="La entrada económica está vacía.",
        )

    system_prompt = build_system_prompt()
    messages: List[dict] = [
        {"role": "user", "content": build_user_prompt(economic_input)}
    ]

    attempts: List[str] = []
    try:
        raw = _call_llm(system_prompt, messages, provider=provider)
    except RuntimeError as exc:
        return TranslationResult(
            mod_code="", explanation="", report=None, error=str(exc),
        )

    attempts.append(raw)
    mod_code = extract_dynare_block(raw)
    explanation = extract_explanation(raw)
    report = analyze(mod_code)

    repairs = 0
    while not report.ok and repairs < max_repairs:
        repairs += 1
        messages.append({"role": "assistant", "content": raw})
        messages.append(
            {"role": "user",
             "content": build_repair_prompt(mod_code, report.to_markdown())}
        )
        try:
            raw = _call_llm(system_prompt, messages, provider=provider)
        except RuntimeError as exc:
            return TranslationResult(
                mod_code=mod_code, explanation=explanation, report=report,
                repairs=repairs, attempts=attempts, error=str(exc),
            )
        attempts.append(raw)
        mod_code = extract_dynare_block(raw)
        explanation = extract_explanation(raw) or explanation
        report = analyze(mod_code)

    return TranslationResult(
        mod_code=mod_code, explanation=explanation, report=report,
        repairs=repairs, attempts=attempts,
    )
