/**
 * Crea automáticamente la encuesta de validación en Google Forms.
 *
 * CÓMO USAR (4 pasos, ~1 minuto):
 *  1. Entra a https://script.google.com  ->  "Nuevo proyecto".
 *  2. Borra todo lo que haya y pega ESTE archivo completo.
 *  3. Pulsa "Ejecutar" (Run). Autoriza con tu cuenta Google cuando lo pida.
 *  4. Abre el "Registro de ejecución" (Ctrl+Enter): ahí aparece el link para
 *     EDITAR y el link para COMPARTIR (este último es el que mandas por WhatsApp).
 *
 * LÓGICA CONDICIONAL:
 *  - Si en "nivel con Dynare" responde "Nunca lo he usado" -> salta al bloque
 *    final para NO-USUARIOS (predisposición a aprender). No ve el bloque de dolor.
 *  - Si ha usado Dynare -> entra al bloque de dolor.
 *  - La pregunta de horas solo aparece si intentó replicar un modelo
 *    (si responde "Nunca lo intenté", se la salta).
 *  - El bloque de experiencia con IA solo aparece si responde que sí usó IA.
 */
function crearEncuestaDynare() {
  var form = FormApp.create('Encuesta DSGE / Dynare — Macro UP');

  form.setDescription(
    '¡Hola! 👋 Soy Alejandro, su TA de Macro. Esta encuesta es CONFIDENCIAL y toma ~4 minutos.\n\n' +
    '(Tu correo solo lo uso para no duplicar respuestas e invitarte a probar el beta; ' +
    'no se comparte con nadie más.)\n\n' +
    'Con sus respuestas estoy construyendo una herramienta para que las próximas generaciones ' +
    'de pregrado en la UP puedan unir la parte analítica (lo de la pizarra) con el código en ' +
    'Dynare — sin sufrir tanto en el camino.\n\n' +
    '¿List@s para ser parte del cambio? 🚀'
  );
  form.setCollectEmail(false); // capturamos el correo con un campo validado (abajo)
  form.setProgressBar(true);

  // ===== PÁGINA 1 — Perfil =====
  form.addSectionHeaderItem().setTitle('Perfil');

  // Correo institucional UP (validado a @alum.up.edu.pe)
  var correo = form.addTextItem()
    .setTitle('Correo institucional UP')
    .setHelpText('Debe terminar en @alum.up.edu.pe')
    .setRequired(true);
  correo.setValidation(
    FormApp.createTextValidation()
      .setHelpText('Usa tu correo institucional, p. ej. nombre.apellido@alum.up.edu.pe')
      .requireTextMatchesPattern('.+@alum\\.up\\.edu\\.pe$')
      .build()
  );

  // Edad (número entero)
  var edad = form.addTextItem().setTitle('¿Cuántos años tienes?');
  edad.setValidation(
    FormApp.createTextValidation()
      .setHelpText('Ingresa un número (años).')
      .requireNumberBetween(15, 80)
      .build()
  );

  // Sexo
  form.addMultipleChoiceItem()
    .setTitle('Sexo')
    .setChoiceValues(['Femenino', 'Masculino', 'Prefiero no decir', 'Otro']);

  // Carrera (lista oficial de pregrado UP)
  form.addListItem()
    .setTitle('¿Qué carrera estudias?')
    .setRequired(true)
    .setChoiceValues([
      'Economía',
      'Finanzas',
      'Administración',
      'Contabilidad',
      'Marketing',
      'Negocios Internacionales',
      'Ingeniería Empresarial',
      'Ingeniería de la Información',
      'Derecho',
      'Política, Filosofía y Economía',
      'Humanidades Digitales',
      'Ingeniería en Innovación y Diseño'
    ]);

  // Semestre de ingreso a la UP (en vez de ciclo; luego calculamos años aprox.)
  form.addListItem()
    .setTitle('¿En qué semestre ingresaste a la UP?')
    .setHelpText('El ciclo en que empezaste tu carrera (no el actual).')
    .setRequired(true)
    .setChoiceValues([
      '2026-I', '2025-II', '2025-I', '2024-II', '2024-I',
      '2023-II', '2023-I', '2022-II', '2022-I', '2021-II', '2021-I',
      '2020-II', '2020-I', '2019-II', '2019-I', '2018-II', '2018-I',
      'Antes de 2018'
    ]);

  // Cursos de macro (selección múltiple)
  form.addCheckboxItem()
    .setTitle('¿Qué curso(s) de macroeconomía llevas o llevaste?')
    .setHelpText('Marca todos los que apliquen.')
    .setRequired(true)
    .setChoiceValues([
      'Economía General II',
      'Macroeconomía I',
      'Macroeconomía del Corto Plazo',
      'Macroeconomía II',
      'Macroeconomía Internacional',
      'Macroeconomía III',
      'Ninguno de estos (aún)'
    ]);

  // Herramientas de programación (caracteriza al cliente)
  form.addCheckboxItem()
    .setTitle('¿Qué herramientas de programación manejas?')
    .setHelpText('Marca todas las que apliquen.')
    .setChoiceValues([
      'Ninguna',
      'Excel',
      'Python',
      'R',
      'Stata',
      'EViews',
      'MATLAB u Octave',
      'Dynare'
    ]);

  // Nivel con Dynare  (RAMIFICA: "Nunca lo he usado" -> bloque no-usuarios)
  var p_nivel = form.addMultipleChoiceItem()
    .setTitle('¿Cuál es tu nivel con Dynare?')
    .setRequired(true);

  // ===== PÁGINA 2a — El dolor =====
  var pb_dolor = form.addPageBreakItem().setTitle('Tu experiencia programando en Dynare');

  // ¿Intentó replicar? (RAMIFICA: "Nunca lo intenté" -> salta la pregunta de horas)
  var p_replicar = form.addMultipleChoiceItem()
    .setTitle('¿Has intentado replicar un paper o un modelo (RBC, New Keynesian, etc.) en Dynare?');

  // ===== PÁGINA 2b — Horas (solo si intentó) =====
  var pb_horas = form.addPageBreakItem().setTitle('Tiempo invertido');

  form.addMultipleChoiceItem()
    .setTitle('La última vez que programaste un modelo, ¿cuántas horas le dedicaste hasta que corrió (o hasta que te rendiste)?')
    .setChoiceValues(['Menos de 2', '2–5', '5–10', '10–20', 'Más de 20']);

  // ===== PÁGINA 2c — El dolor (cont.) =====
  var pb_dolor2 = form.addPageBreakItem().setTitle('Obstáculos');

  form.addScaleItem()
    .setTitle('¿Qué tan frustrante te resultó programar en Dynare?')
    .setBounds(1, 5)
    .setLabels('Nada', 'Muchísimo');

  form.addCheckboxItem()
    .setTitle('¿Cuál fue tu mayor obstáculo?')
    .setHelpText('Marca todos los que apliquen.')
    .setChoiceValues([
      'La sintaxis propia de Dynare',
      'Errores de Blanchard-Kahn / indeterminación',
      'Calcular el estado estacionario (steady state)',
      'Traducir mis ecuaciones (FONCs) a código',
      'Entender qué hace cada bloque del .mod',
      'Errores que no entiendo qué significan',
      'Interpretar los resultados (IRFs, momentos)'
    ]);

  // ===== PÁGINA 3 — Cómo lo resuelves hoy =====
  var pb_resuelves = form.addPageBreakItem().setTitle('Cómo lo resuelves hoy');

  form.addCheckboxItem()
    .setTitle('Cuando te trabas programando en Dynare, ¿qué haces?')
    .setHelpText('Marca todos los que apliquen.')
    .setChoiceValues([
      'Le pregunto al profesor o al TA',
      'Busco en el foro de Dynare',
      'Reviso webs de investigadores (Pfeifer, Mutschler, MMB)',
      'Le pido ayuda a una IA (ChatGPT / Claude / Gemini)',
      'Copio/adapto el código de un compañero',
      'Me rindo / entrego incompleto'
    ]);

  // ¿Usó IA? (RAMIFICA: "No" -> salta el bloque de experiencia con IA)
  var p_usoia = form.addMultipleChoiceItem()
    .setTitle('¿Has usado IA (ChatGPT, Claude, Gemini) para escribir o corregir código Dynare?');

  // ===== PÁGINA 4 — Tu experiencia con IA =====
  var pb_ia = form.addPageBreakItem().setTitle('Tu experiencia con IA');

  form.addMultipleChoiceItem()
    .setTitle('Cuando usaste IA para Dynare, ¿con qué frecuencia te dio código con errores que tuviste que corregir?')
    .setChoiceValues(['Siempre', 'Casi siempre', 'A veces', 'Casi nunca']);

  form.addMultipleChoiceItem()
    .setTitle('Cuando la IA se equivocaba, ¿pudiste darte cuenta y corregirlo?')
    .setChoiceValues([
      'Sí, solo/a',
      'Sí, pero con ayuda de alguien más',
      'No: entregué/usé el código sin estar seguro/a de si estaba bien'
    ]);

  // ===== PÁGINA 5 — La solución (para quienes SÍ han usado Dynare) =====
  var pb_sol_users = form.addPageBreakItem().setTitle('La solución');

  form.addMultipleChoiceItem()
    .setTitle('Si existiera una herramienta que traduce tus ecuaciones a código Dynare correcto y te explica cada paso, ¿la usarías?')
    .setChoiceValues(['Definitivamente sí', 'Probablemente sí', 'Tal vez', 'No']);

  form.addMultipleChoiceItem()
    .setTitle('¿Pagarías por una herramienta así?')
    .setChoiceValues([
      'No pagaría',
      'Sí, si es barata (≤ S/ 20 al mes)',
      'Sí, hasta S/ 50 al mes',
      'Solo si es gratis para estudiantes'
    ]);

  // ===== PÁGINA 6 — Para quienes NUNCA han programado un modelo =====
  var pb_no = form.addPageBreakItem().setTitle('Antes de irte...');

  form.addMultipleChoiceItem()
    .setTitle('Más allá de las ecuaciones en la pizarra de tus cursos de macro, ¿te gustaría aprender a llevar esos modelos a código para simularlos, graficarlos y experimentar con ellos (verlos como un laboratorio)?')
    .setChoiceValues(['Definitivamente sí', 'Me da curiosidad', 'Tal vez', 'No me llama la atención']);

  form.addCheckboxItem()
    .setTitle('¿Qué te ha frenado para aprender a programar modelos macro?')
    .setHelpText('Marca todos los que apliquen.')
    .setChoiceValues([
      'No sé por dónde empezar',
      'Me parece muy difícil',
      'No tengo tiempo',
      'No sabía que se podía',
      'Nunca me lo propusieron en clase'
    ])
    .showOtherOption(true);

  form.addMultipleChoiceItem()
    .setTitle('Si existiera una herramienta que te enseña paso a paso a programar y experimentar con estos modelos, ¿la usarías?')
    .setChoiceValues(['Definitivamente sí', 'Probablemente sí', 'Tal vez', 'No']);

  // -------- DEFINICIÓN DE LAS RAMIFICACIONES (al final, ya con las páginas creadas) --------

  // Nivel con Dynare: si "Nunca lo he usado" -> bloque no-usuarios; resto -> sigue al dolor.
  p_nivel.setChoices([
    p_nivel.createChoice('Nunca lo he usado', pb_no),
    p_nivel.createChoice('Lo intenté y lo abandoné', FormApp.PageNavigationType.CONTINUE),
    p_nivel.createChoice('Lo uso, pero con mucha dificultad', FormApp.PageNavigationType.CONTINUE),
    p_nivel.createChoice('Lo uso con relativa soltura', FormApp.PageNavigationType.CONTINUE)
  ]);

  // ¿Intentó replicar?: si "Nunca lo intenté" -> salta horas; resto -> ve horas.
  p_replicar.setChoices([
    p_replicar.createChoice('Sí, y lo logré', FormApp.PageNavigationType.CONTINUE),
    p_replicar.createChoice('Sí, pero solo a medias', FormApp.PageNavigationType.CONTINUE),
    p_replicar.createChoice('Lo intenté y no pude', FormApp.PageNavigationType.CONTINUE),
    p_replicar.createChoice('Nunca lo intenté', pb_dolor2)
  ]);

  // ¿Usó IA?: "Sí" -> ve experiencia con IA; "No" -> salta a la solución.
  p_usoia.setChoices([
    p_usoia.createChoice('Sí', FormApp.PageNavigationType.CONTINUE),
    p_usoia.createChoice('No', pb_sol_users)
  ]);

  // Al terminar "La solución" (usuarios), enviar el formulario (no caer en el bloque no-usuarios).
  pb_sol_users.setGoToPage(FormApp.PageNavigationType.SUBMIT);

  Logger.log('FORM LISTO ✅');
  Logger.log('Editar:    ' + form.getEditUrl());
  Logger.log('Compartir: ' + form.getPublishedUrl());
}
