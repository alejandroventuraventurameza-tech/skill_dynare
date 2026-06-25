# HANDOFF — MacroBuilt (lee esto primero)

> Documento de traspaso para continuar el proyecto con total claridad.
> Última actualización: 2026-06-22.

## Qué es MacroBuilt
"**MacroBuilt — Tu laboratorio macroeconómico**". Producto que traduce las
ecuaciones de un modelo DSGE (que el estudiante deriva a mano) a **código Dynare**
correcto, **verificado** y **explicado**, con foto de pizarra (OCR), un bootcamp
interactivo y un verificador determinista. Para estudiantes de macro de pregrado.

Es el **proyecto final** del curso "Data Science con Python" (UP, Prof. Alexander
Quispe), formato startup YC (individual / solo founder).

## DEADLINE
**Presenta el MARTES 23 de junio de 2026, 08:05–08:15 am** (slot 4, día 1). Sin prórroga.

## Estado: TODO listo salvo el deck
- **Demo desplegado y vivo:** https://huggingface.co/spaces/resaca2014/dynare-translate
  (4 pestañas: Traducir, Foto de pizarra, Bootcamp, Verificar offline). Usuario HF: **resaca2014**.
- **Landing web:** `index.html` (lista para GitHub Pages; falta que él active Pages).
- **Repo GitHub:** rama `first_branch`. Despliegue a HF vía GitHub Action `.github/workflows/deploy-hf.yml`
  (instantánea orphan; descarta todos los .pdf y los CSV de la encuesta del Space).
  Secrets/vars en GitHub: `HF_TOKEN` (secret), `HF_USERNAME`, `HF_SPACE_NAME` (vars).
  Secret en el Space: `DEEPSEEK_API_KEY`.

## >>> TAREA PENDIENTE (lo único grande que falta) <<<
**Armar el PITCH DECK en Beamer.**
- El usuario dejará su **template Beamer en `skill_dynare/deck/`** (.tex + .sty/.cls/tema/logo).
- Construir el `.tex` usando el contenido ya escrito en **`docs/PITCH.md`** (deck slide
  por slide + guion de 7 min) y los assets de `assets/` y `docs/research/figuras/`.
- **MUY IMPORTANTE (pedido explícito):** que NO quede apachurrado. Una idea por lámina,
  ~16–20 slides, visualmente clarísimo. Sin miedo a usar varias slides.
- **Hay LaTeX en el entorno** (`pdflatex`/`xelatex`): compilar y revisar el PDF
  renderizado lámina por lámina (convertir a imágenes con pdftoppm y mirarlas) para
  garantizar que nada salga cargado.
- Falta de él: capturas del demo (si no, usar placeholders/assets), URL de GitHub Pages.

### Pendientes del usuario (no del AI)
Grabar video demo 2–3 min · tomar capturas de la app · commit/push de todo lo
pendiente + activar GitHub Pages · ensayar con el guion de `docs/PITCH.md`.

## Mapa del repo (lo importante)
- `app.py` — UI Gradio (4 pestañas, tema branded, hero con logo).
- `dynare_translate/core/verifier.py` — **verificador determinista** (sin LLM, 24 tests). El moat.
  Reconoce el macro-processor de Dynare; valida conteo, símbolos, timing, BK.
- `dynare_translate/core/translator.py` — traductor multi-proveedor (DeepSeek por defecto) + auto-reparación.
- `dynare_translate/core/prompts.py` — system prompt desde `context/DYNARE_CONTEXT.md` + few-shot.
- `dynare_translate/core/ocr.py` — OCR (rapidocr-onnxruntime = modelos PaddleOCR PP-OCRv4).
- `dynare_translate/core/bootcamp.py` — 4 lecciones autocorregidas por el verificador, progresión por fases.
- `context/DYNARE_CONTEXT.md` — base de conocimiento (incluye timing oficial citado + patrones NK reales del MMB).
- `docs/PITCH.md` — **deck + guion de 7 min (usar para el Beamer)**.
- `docs/MODELO_NEGOCIO.md` — BYOK, pricing, mercado con cifras OFICIALES UP.
- `docs/COMPETENCIA_Y_ASK.md` — tabla de competencia, moat, the ask.
- `docs/FOUNDER.md` — bio + founder-market fit.
- `docs/CHECKLIST_ENTREGA.md` — cumplimiento de requisitos del profe.
- `docs/research/` — encuesta (notebook `analisis_encuesta.ipynb`, `HALLAZGOS.md`, `figuras/`),
  `Resultados_entrevistas_MacroBuilt.docx` (validación cualitativa con fuentes), `UP_matriculados_pregrado_2025.pdf`.
- `assets/` — logo (svg+png), `arquitectura.png`, `founder_avatar.png`/`founder_alejandro.jpg`,
  `hoja_demo_rbc.png` (hoja impresa para el OCR), `lore_photo.jpeg` (manuscrito real que sí lee el OCR).
- `mmb-rep-master/` — 185 .mod reales del MMB (**GITIGNOREADO**, referencia local).

## Cifras clave (para el pitch)
- Encuesta n=59: **71%** nunca usó Dynare · **64%** no pudo verificar el código de la IA · **86%** de no-usuarios usaría la herramienta.
- Verificador validado contra **185 modelos publicados del MMB**.
- Mercado UP (oficial 2025-II): Economía = **1,605** matriculados · SOM ~180–360 alumnos/año por Dynare → **~S/29k/año UP, ~S/55–60k con PUCP**.
- Modelo: **BYOK** (margen ~100%); planes Free / Estudiante Pro S/19-mes / Institucional desde S/4,900/año-sección.

## GOTCHAS del entorno (importante)
- **El mount TRUNCA escrituras a veces** (Edit/Write/python-write cortan el final).
  Preferir `cat > file <<'EOF'` (heredoc) y SIEMPRE verificar con `tail`/`ast.parse`/`wc` tras escribir.
- Los `.pyc` de `__pycache__` quedan **bloqueados** (no se borran). Para tests usar
  `PYTHONPYCACHEPREFIX=/tmp/x python -m pytest tests/ -q -p no:cacheprovider`.
- **Archivos que sube el usuario al chat NO llegan al filesystem**; sí llegan cuando los
  guarda en la carpeta `skill_dynare/` (mount). Pedirle que los deje ahí.
- No usar `curl` para URLs (restricción); GitHub sirve los `.mod` como binario vía web_fetch
  (no se pueden leer así) → pedir que deje los `.mod` en la carpeta.
- Commits: estilo **conventional commits**; el usuario usa **GitHub Desktop**.

## Roadmap / visión (post-martes, en ROADMAP.md)
Curar few-shot con código real (Pfeifer/MMB con atribución) · destilar el manual completo
a `DYNARE_CONTEXT.md` · bootcamp profesional (videos, evaluaciones, proyecto final) →
comunidad de macroeconomistas que programan → más allá de Dynare (Python, R).
