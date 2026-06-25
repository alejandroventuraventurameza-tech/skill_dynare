# Guion del pitch — MacroBuilt (formato YC, 7 min)

> **Qué es esto:** el guion EXPLÍCITO de lo que debo decir, lámina por lámina,
> alineado al deck en `deck/MacroBuilt.pdf` (17 láminas). Lo que está en
> *cursiva entre comillas* es lo que digo casi literal; lo demás son notas.
>
> **Demo en vivo:** https://huggingface.co/spaces/resaca2014/dynare-translate
> **Regla de oro:** 7 minutos. El demo (lámina 7) es el corazón — no me paso en las slides.

---

## Mapa de tiempos (cronómetro)

| Tiempo | Láminas | Bloque |
|---|---|---|
| 0:00–0:45 | 1–2 | Hook (portada + one-liner) |
| 0:45–1:45 | 3–4 | El problema + el insight (cifras) |
| 1:45–2:15 | 5–6 | La solución + arquitectura (rápido) |
| **2:15–5:30** | **7** | **DEMO EN VIVO (el corazón, ~3 min)** |
| 5:30–6:00 | 8–9 | Mercado + modelo de negocio |
| 6:00–6:25 | 10–11 | Competencia + moat (rápido) |
| 6:25–6:45 | 12–13 | Tracción + founder |
| 6:45–7:00 | 14–15–16 | Roadmap (1 línea) + the ask + cierre |
| — | 17 | Fuentes (anexo: NO se presenta, solo respaldo en Q&A) |

> Si voy tarde: recorto láminas 10 y 14 a una frase cada una. Nunca recorto el demo.

---

## Guion lámina por lámina

### Lámina 1 — Portada
**Digo (mientras aparece el logo):**
*"Buenos días. Soy Alejandro Ventura, estudiante de Economía y TA de Macro II y
Macro Internacional acá en la UP. Les presento **MacroBuilt: tu laboratorio
macroeconómico**."*
> Nota: no leer la URL todavía; la usaré en el demo. Energía alta, esto es el saludo.

### Lámina 2 — One-liner
**Digo (despacio, es la promesa):**
*"En una frase: **llevamos los modelos DSGE de la pizarra a un modelo que corre
—correcto, verificado y explicado— para que los estudiantes de macro dejen de
memorizar y empiecen a experimentar**."*
> Pausa de 1 segundo después de "experimentar". Que cale.

### Lámina 3 — El problema
**Digo:**
*"El problema que vivo todos los días como TA: en macro de pregrado **derivamos**
modelos hermosos en la pizarra… y ahí se quedan. Concretarlos exige Dynare, que
casi nadie domina. Encuestamos a 59 estudiantes de macro y **el 71% nunca usó
Dynare**. Es como enseñar física sin dejar entrar nunca al laboratorio."*
> Señalo la cifra 71% en la figura. Esa es el ancla emocional.

### Lámina 4 — El insight (por qué ahora)
**Digo:**
*"¿Y por qué no usan ChatGPT? Lo intentan. Pero la IA genérica produce código
**plausible pero incorrecto**, y el alumno no tiene cómo darse cuenta: **el 64%
no pudo verificar si el código de la IA estaba bien**. Lo que hoy lo hace posible:
LLMs baratísimos como DeepSeek y OCR gratis. La pieza que faltaba no era traducir
—era **verificar**."*
> Transición clave: "verificar" me conecta con la solución.

### Lámina 5 — La solución
**Digo (rápido, son 4 cosas):**
*"MacroBuilt hace cuatro cosas: **traduce** las ecuaciones a un .mod listo;
**verifica** que esté correcto —sin usar IA—; **explica** cada bloque con la
intuición económica; y si está en la pizarra, lee la **foto**. Y enseña con un
**bootcamp** que se autocorrige."*
> No me detengo aquí: lo van a VER en 30 segundos.

### Lámina 6 — Arquitectura (el moat técnico)
**Digo:**
*"Una cosa importante antes del demo: **esto no es un wrapper de ChatGPT**. El
corazón es un **verificador determinista**, propio, que chequea conteo de
ecuaciones, símbolos, timing y las condiciones de Blanchard-Kahn. Lo validamos
contra **185 modelos publicados** de la Macro Model Base. Y si encuentra un error,
**se auto-repara**."*
> Señalo el bucle de auto-reparación en el diagrama. Aquí gano credibilidad técnica.

### Lámina 7 — DEMO EN VIVO  ⭐ (el corazón, ~3 min)
> **Tener el video de respaldo abierto en otra pestaña por si falla el internet.**

**Paso 1 — Traducir (digo mientras pego):**
*"Vamos a verlo. Estas son las ecuaciones de un RBC, las que cualquier alumno
deriva en clase. Las pego… y traduzco."*

**Paso 2 — Mostrar el resultado:**
*"Acá está el .mod listo para correr. Miren esto: **el verificador me da el check
verde** —el modelo está bien planteado— y además **me explica cada bloque**. Esto
es lo que ChatGPT no te da: la certeza de que está correcto."*

**Paso 3 — Foto de pizarra:**
*"¿Y si lo tengo escrito a mano? Una foto."* (subo la foto → OCR → traduzco)
*"Lo leyó y lo tradujo igual."*

**Paso 4 — Bootcamp:**
*"Y para quien arranca de cero, un bootcamp interactivo que **se corrige solo** con
el mismo verificador."* (muestro una lección y el progreso)

> Cierre del demo: *"Eso es MacroBuilt funcionando, hoy, en vivo."* Vuelvo a las slides.

### Lámina 8 — Mercado
**Digo:**
*"¿Quién paga? Empezamos por la UP como beachhead: **1,605 estudiantes de Economía**,
cifra oficial 2025. Cada año, unos **180 a 360 pasan por cursos con Dynare**.
Vendiéndole al departamento, eso es **~S/29 mil al año solo en la UP, y ~S/55–60 mil
sumando PUCP**."*
> La cifra 1,605 es oficial (UP); decirlo con seguridad.

### Lámina 9 — Modelo de negocio
**Digo:**
*"El modelo es **BYOK: cada usuario pone su propia API key**. Una traducción cuesta
medio centavo de dólar, así que nuestro costo variable es casi cero —**margen cercano
al 100%**. Cobramos por la experiencia, no por el cómputo. Tres planes: Free,
Estudiante Pro a S/19 al mes, e **Institucional desde S/4,900 al año por sección**.
El motor es el institucional: como TA, le vendo directo al departamento."*

### Lámina 10 — Competencia (rápido)
**Digo:**
*"Nadie cubre los tres a la vez. Los repos de expertos son potentes pero para
posgrado. La IA genérica es accesible pero se equivoca. Los cursos caros son para
posgrado. **MacroBuilt es el único accesible, correcto y pedagógico a la vez**."*
> Una frase y avanzo; la tabla habla sola.

### Lámina 11 — Moat
**Digo:**
*"¿Por qué es difícil de copiar? Cuatro razones: el **verificador con corpus real**;
mi **founder-market fit** —soy TA de los cursos exactos, tengo el canal—; los
**efectos de red** del bootcamp y la comunidad; y los **datos** de dónde se traban
los alumnos."*

### Lámina 12 — Tracción
**Digo:**
*"Validación: la encuesta de 59 personas, donde **el 86% de los que no usan Dynare
dijo que usaría la herramienta**. El producto está **desplegado y vivo**. Y ya lo
probaron usuarios reales en entrevistas."*
> Si tuve entrevistas en vivo recientes, AÑADIR aquí 1 frase concreta (ver pendiente abajo).

### Lámina 13 — Founder
**Digo:**
*"¿Por qué yo? Porque **vivo el problema**: soy TA de esos cursos, las aulas son mi
canal, y como RA en macro sé cómo debe verse un buen .mod y dónde fallan las IAs.
Soy solo founder, y me apalanco en agentes de IA como co-CTO para iterar rápido."*

### Lámina 14 — Roadmap (1 línea)
**Digo:**
*"Hacia adelante: bootcamp profesional, una comunidad de macroeconomistas que
programan, y más allá de Dynare —Python y R. La visión: **cambiar cómo se aprende
macro, del pizarrón al laboratorio**."*

### Lámina 15 — The ask
**Digo (claro y directo):**
*"El pedido: un **piloto de un semestre** con el Departamento de Economía de la UP
—unas 6 secciones de Macro II y Macro Internacional— y un **semilla de apenas
S/3,000** para hosting y producir las primeras lecciones del bootcamp. Pido poco
capital **a propósito**: con BYOK, hosting gratis y open source, el costo de operar
es mínimo. **Lo valioso es el acceso, no el cheque.** Con eso llego a **300 usuarios
activos y mi primer contrato institucional**, y abro PUCP."*

### Lámina 16 — Cierre
**Digo:**
*"MacroBuilt: tu laboratorio macroeconómico. **Gracias** —¿probamos el demo en vivo
si quedan preguntas?"*

### Lámina 17 — Fuentes (anexo)
> No se presenta. Está para respaldar cualquier cifra si me la cuestionan en Q&A.

---

## El presupuesto, en detalle (para defender el "S/3,000")

Tienes razón en que cuesta poco — y eso es una **fortaleza**, no una debilidad.
Úsalo como argumento de eficiencia de capital.

**Por qué el costo de operar es casi cero:**
- **BYOK:** el usuario paga sus tokens (~US$0.005/traducción). Nuestro costo variable ≈ **US$0**.
- **Verificador:** corre local, sin LLM → **gratis**.
- **Hosting:** Hugging Face Spaces en free tier → **S/0** (o un upgrade chico si hay carga).
- **Stack open source:** sin licencias.

**Semilla de ~S/3,000 para 12 meses (itemizado):**

| Rubro | Monto (S/) | Nota |
|---|---:|---|
| Hosting + dominio (`macrobuilt.app`) | ~400 | HF free tier o upgrade chico + dominio/email |
| Producir las primeras ~8 lecciones del bootcamp | ~1,800 | Grabación + edición ligera (yo grabo) |
| Clave administrada de respaldo + buffer de APIs | ~500 | Para demos y usuarios sin key propia |
| Diseño / materiales / imprevistos | ~300 | — |
| **Total** | **~3,000** | Cubre un semestre de piloto con holgura |

**Cómo lo digo si me preguntan "¿por qué tan poco?":**
*"Porque la arquitectura es barata por diseño. El pedido de plata es chico; el
verdadero pedido es el acceso a las aulas para el piloto. El dinero institucional
de verdad llega después, con la licencia por sección (S/4,900/año)."*

> Nota: el contrato institucional (S/4,900/sección/año) es el **ingreso**, no el
> gasto. La semilla de S/3,000 es aparte y mínima.

---

## Q&A — preguntas que me van a hacer (y mi respuesta)

- **"¿Por qué pagar si ChatGPT es gratis?"**
  *"Porque ChatGPT se equivoca y el alumno no lo nota —el 64% de la encuesta no
  pudo verificar el código. Lo que vendo es la **certeza**: el verificador + el
  corpus de 185 modelos reales. Ese es el valor, no el texto."*

- **"¿Y si DeepSeek sube precios o desaparece?"**
  *"El motor es **agnóstico**: cambio de proveedor con una variable (DeepSeek hoy,
  OpenAI u otro mañana). Y con BYOK el riesgo de precio lo absorbe el usuario, no yo."*

- **"¿Cuánto cuesta correr esto?"**
  *"Casi nada: BYOK = ~US$0 por usuario, el verificador corre local gratis y el
  hosting es free tier. Por eso pido tan poca semilla."*

- **"¿Disposición a pagar comprobada?"**
  Honesto: *"La encuesta capturó fuerte **interés** (86% usaría la herramienta),
  pero por un fallo de ruteo no medí bien la disposición a pagar del segmento con
  experiencia. Por eso el piloto: validar pricing con uso real."*

- **"Muéstrame el código / modifícalo en vivo."**
  Repaso antes: `dynare_translate/core/verifier.py` (el moat) y `app.py`.

- **"¿Esto es defendible o lo copia cualquiera?"**
  Lámina 11: verificador + corpus real + canal institucional (soy TA) + comunidad.

---

## Checklist 60 segundos antes de subir

- [ ] Demo abierto en la pestaña + **video de respaldo** en otra pestaña.
- [ ] Ecuaciones del RBC copiadas y listas para pegar.
- [ ] Foto de pizarra a mano para el OCR.
- [ ] Cronómetro a la vista. Respiro. El demo es lo que vende.
