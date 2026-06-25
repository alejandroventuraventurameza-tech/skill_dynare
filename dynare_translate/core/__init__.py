"""Núcleo del producto: traducción y verificación de modelos DSGE a Dynare.

Capas:
- verifier:  análisis estático determinista de un archivo .mod (sin LLM).
- prompts:   construcción del system prompt a partir de la base de conocimiento.
- translator: traducción entrada económica -> .mod usando la API de Anthropic.
"""

from .verifier import analyze, Report  # noqa: F401
