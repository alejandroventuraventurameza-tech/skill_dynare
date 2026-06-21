# Plan de entrega — Startup "Dynare Translate / Bootcamp DSGE"

**Presentas:** martes 23 de junio, 08:05–08:15 am (slot 4, día 1).
**Hoy:** sábado 20. Tienes ~3 días. Sin prórroga.

## Principio rector
La rúbrica da **5/20 al demo VIVO desplegado** (lo más pesado). Regla de oro:
**tener algo corriendo online HOY, aunque sea mínimo, y recién después agregarle capas.**
No dejar el deploy para el final — es donde todos se queman.

## Stack fijado
- **Cerebro:** Claude API (traducir + explicar) — herramienta del curso #1.
- **Verificador:** agente que chequea #ecuaciones=#variables, Blanchard-Kahn, timing — diferenciador (crewAI = herramienta #2).
- **OCR pizarra (wow / why now):** PaddleOCR — herramienta #3 (función estrella, opcional).
- **Frontend + deploy:** Gradio en Hugging Face Spaces (URL pública gratis).
- **Repo:** GitHub público, commits repartidos cada día.

---

## SÁBADO 20 (hoy) — Esqueleto + deploy temprano
- [x] Encuesta lanzada y recibiendo respuestas.
- [ ] Crear el Space en Hugging Face y desplegar un "hola mundo" en Gradio (probar el pipeline de deploy YA).
- [ ] Definir el *input contract*: qué pega el usuario (FONCs en texto/LaTeX, lista de variables y parámetros).
- [ ] v0 del traductor: caja de texto → llamada a Claude API → muestra un .mod (aunque sin verificar todavía).
- [ ] Commit inicial del repo del producto + README mínimo.
- **Meta del día:** una URL pública donde pegas ecuaciones y sale *algo*.

## DOMINGO 21 — Núcleo inteligente + explicación
- [ ] Prompt system con las reglas de Dynare (reusar `context/DYNARE_CONTEXT.md`).
- [ ] Agente verificador: conteo de ecuaciones, BK, timing `K(-1)`, principio de Taylor.
- [ ] Capa bootcamp: explicación por bloque (qué es market clearing, qué FONC es de quién).
- [ ] Probar con 2–3 modelos (RBC y NK simple) que el .mod corra de verdad.
- [ ] Desplegar v1 funcional. Commit.
- [ ] **Si va bien:** OCR de pizarra (foto → PaddleOCR → texto → traductor).
- **Meta del día:** demo que traduce, verifica y explica un RBC/NK correctamente, online.

## LUNES 22 — Pulido + pitch + evidencia
- [ ] Cerrar la encuesta o tomar corte; tabular respuestas → 3–4 gráficos para "Problema & validación".
- [ ] Pitch deck (formato YC, sus 14 secciones) en PDF → `docs/`.
- [ ] Grabar video demo de 2–3 min (Loom/YouTube) como **plan B** si falla internet.
- [ ] README profesional + diagrama de arquitectura + sección "herramientas del curso usadas y dónde".
- [ ] 3 alumnos reales prueban el demo y dejan feedback (tracción).
- [ ] Revisar que no haya secretos commiteados (`git log -p` buscando api_key/token).
- **Meta del día:** todo listo y subido; solo queda ensayar.

## MARTES 23 (AM) — Presentación
- [ ] Ensayo cronometrado del pitch: 7 min (problema 1' – demo en vivo 3–4' – mercado/modelo 1' – tracción/ask 1').
- [ ] Demo en vivo abierto + video de respaldo listo.
- [ ] Presentas 08:05.

---

## Riesgos y mitigación
- **El deploy falla en vivo** → video de respaldo grabado el lunes (obligatorio).
- **El .mod no corre** → tener 2 ejemplos "de oro" pre-cargados que sí corren para el demo.
- **Alcance excesivo (solo founder)** → si el domingo el OCR se complica, se descarta sin culpa; el traductor+verificador+explicación ya es un demo de sobra.
- **Pocas respuestas a la encuesta** → con ~10 honestas basta para citar; insistir en los grupos.
