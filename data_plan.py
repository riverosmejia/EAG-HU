# -*- coding: utf-8 -*-
"""Datos del Plan de Acción del MVP de EAG Ingenieros (SECOP II).

Resultado de la auditoría técnica del 2026-09-10 y de la replanificación del
2026-09-17, tras confirmarse que EAG no aporta reunión, muestra ni validación.

Cambio de estrategia: el proyecto deja de depender de entregables de EAG. Se
construye el flujo completo con datos públicos reales de SECOP II, un Supabase
self-hosted propio y un grafo LangGraph como orquestador del análisis.

Consumido por build_page.py (versión rápida) y build_docs.py (versión detallada).
Estructura: tuplas ordenadas, nunca HTML.
"""

META = ("3.0", "2026-09-18")

RESUMEN = [
 ("Objetivo", "Construir una aplicación web productiva (React + FastAPI + LangGraph) que consulte oportunidades de SECOP II, reúna y procese documentos, compare requisitos con el perfil de la empresa y produzca un borrador de evaluación revisado por humanos antes de generar el informe."),
 ("Estrategia", "El proyecto no depende de entregables de EAG. Se construye con datos públicos reales de SECOP II, un Supabase self-hosted propio y un perfil empresarial cargable desde la plataforma. La demostración de valor no espera autorización externa."),
 ("Flujo", "Sincronizar SECOP → filtrar → cargar/descargar documentos → validar y poner en cuarentena → extraer texto/OCR → extraer requisitos (grafo LangGraph) → validar citas → comparar con el perfil → borrador → interrupción para revisión humana → aprobación → PDF → correo autorizado."),
 ("Datos", "APIs oficiales de SECOP II (procesos p6dx-8zbt y documentos dmgg-8hin) y de SECOP I (procesos f789-7hwg, 78 campos verificados), actualizadas por Socrata. Sin automatización de la interfaz web. La relación entre procesos y archivos no quedó confirmada en el spike, por lo que la carga manual de documentos es el camino principal."),
 ("Conocimiento", "Base de conocimiento propia de la empresa: los documentos que se suben se fragmentan, se indexan con representación vectorial y se recuperan por significado. Toda respuesta cita el fragmento y su origen; sin fragmento relevante se responde que no hay evidencia."),
]

# (capa, tecnología, decisión, etiqueta corta para versión rápida)
STACK = [
 ("Frontend", "React · TypeScript · Vite · React Query · Tailwind", "Cliente TypeScript generado desde OpenAPI. Reutiliza el sistema de diseño ya definido para el proyecto.", "React + Vite"),
 ("Backend", "Python 3.12 · FastAPI · Pydantic · SQLAlchemy · Alembic", "API versionada + OpenAPI; autorización resuelta en servidor (HU-04).", "FastAPI"),
 ("Datos", "Supabase self-hosted propio (Postgres 17 · Auth · Storage)", "Stack aislado y dedicado al proyecto, con red, volúmenes y puertos propios. Sin dependencia de cuentas de EAG ni de terceros.", "Supabase propio"),
 ("Orquestación", "LangGraph con checkpointer en Postgres", "Reemplaza a Celery + Redis. El grafo orquesta el pipeline de análisis y su estado persistido es la propia auditoría del análisis.", "LangGraph"),
 ("Scheduler", "Cron del sistema → endpoint de sincronización", "Menos piezas y menos superficie que un planificador embebido.", "Cron"),
 ("IA", "Adaptador intercambiable · modelo configurable", "Salidas JSON validadas por esquema versionado · tope de gasto mensual · caché por hash · documentos tratados como datos no confiables.", "Adaptador IA"),
 ("Recuperación", "pgvector sobre el Postgres propio", "Sin servicio vectorial externo: los vectores viven en la misma base que el resto de los datos, así que una consulta no cruza límites de confianza ni añade otro proveedor que autorizar.", "pgvector"),
 ("Fragmentación", "Corte por estructura + solapamiento", "Se respeta la jerarquía del documento; el solapamiento evita perder una cláusula partida entre dos fragmentos.", "Chunking"),
 ("Representación", "Modelo de embeddings versionado", "El modelo y su versión se guardan junto al índice. Reindexar con otro modelo no mezcla vectores de espacios distintos.", "Embeddings"),
 ("OCR", "Tesseract", "Se activa por umbral explícito y configurable; conserva página y advertencias de calidad.", "Tesseract"),
 ("Antivirus", "ClamAV", "Escaneo por archivo y por miembro de ZIP; un fallo del antivirus no equivale a archivo limpio (HU-13).", "ClamAV"),
 ("PDF", "WeasyPrint", "Fuentes con soporte completo para español.", "WeasyPrint"),
 ("Errores", "Observabilidad sin contenido sensible", "Sin archivos, tokens, credenciales ni fragmentos de pliegos en logs ni alertas (HU-39).", "Logs seguros"),
]

# Decisiones de la auditoría original: (id, título, decisión)
DECISIONES_CRITICAS = [
 ("A1", "Modelado de roles",
  "2 roles base (Administrador, Analista) + permiso fino «approve/send» asignable. El Aprobador/Gerencia se implementa como permiso configurable, no como rol separado. Alinea HU-33 a HU-37 y resuelve la contradicción con el plan original."),
 ("A2", "Pliegos en ZIP",
  "Se admiten con extracción en sandbox y controles explícitos: ratio anti zip-bomb, profundidad máxima 5, tamaño por miembro, escaneo antivirus por miembro, sin symlinks ni path traversal. Preserva la cobertura real de SECOP frente a HU-12."),
 ("A3", "Arquitectura de autorización",
  "FastAPI como capa de autoridad (conexión service_role; RLS para Storage y bucket privado). Permisos resueltos en servidor, nunca en claims del navegador (HU-04). Evita confiar en RLS para datos de negocio."),
 ("A4", "Aprobación por snapshot",
  "Al aprobar se congela una versión del análisis (expediente + perfil + decisiones). Cambios posteriores crean una versión nueva; no se invalida retroactivamente (HU-34 se cumple congelando, no invalidando)."),
 ("A5", "Autonomía de datos",
  "El proyecto NO espera la autorización de tratamiento de datos de EAG. El perfil empresarial se carga desde la plataforma con datos aportados por el usuario autorizado, y el piloto se ejecuta con oportunidades públicas de SECOP II. La autorización pasa de bloqueante externo a política interna documentada."),
]

DECISIONES_ADOPTADAS = [
 ("B1", "Límites de archivos",
  "20 MB por archivo y 100 MB por oportunidad como punto de partida, calibrables con la muestra real. Más viable para OCR en contenedor que los 50/300 MB originales."),
 ("B2", "Presupuesto de IA",
  "Tope de gasto mensual por variable de entorno (HU-27); fragmentación del pliego por categorías antes de llamar; modelo configurable; caché por hash y versión para no repetir llamadas."),
 ("B3", "HUs de ampliación",
  "HU-45 a HU-48 propuestas (usuarios existentes, auditoría, configuración general, notificaciones): cubren los gaps frente a las pantallas prometidas. Con más usuarios y sin EAG, la administración propia gana importancia."),
 ("B4", "Scheduler",
  "Cron del sistema llamando al endpoint de sincronización; menos piezas y menos superficie operativa que un planificador dentro de la aplicación."),
 ("B5", "Verificación temprana de SECOP",
  "Ya ejecutada en el spike: la API de procesos funciona, la relación con el dataset de archivos NO se confirmó. Se construye sobre lo verificado y la carga manual cubre el resto."),
 ("B6", "Camino crítico realista",
  "El grafo de análisis (extracción de requisitos + validación de citas + comparación) es la pieza donde el proyecto se gana o se pierde. Se planifica en 3 semanas y no se comprime."),
 ("B7", "Orquestación con LangGraph",
  "El grafo reemplaza a Celery + Redis. Nodos: ingesta → extracción de texto → extracción de requisitos → validación de citas → comparación → borrador. La revisión humana se implementa con interrupción del grafo y checkpointer en Postgres, de modo que el estado del análisis sobrevive reinicios y es auditable."),
 ("B9", "Recuperación con cita obligatoria",
  "El sistema responde únicamente con fragmentos recuperados de los documentos de la empresa y cita documento, página y fragmento textual. Sin fragmento que supere el umbral de relevancia, responde que no hay evidencia en lugar de completar con conocimiento general. Es la diferencia entre un asistente que ayuda a decidir y uno que inventa capacidad empresarial en una licitación pública."),
 ("B10", "Vectores en la base propia",
  "pgvector sobre el mismo Postgres, sin servicio vectorial externo. Añadir otro proveedor multiplicaría las autorizaciones necesarias y haría que una consulta cruzara un límite de confianza que hoy no existe. El índice se versiona por modelo de representación para no mezclar espacios vectoriales distintos."),
 ("B11", "Base de conocimiento separada del expediente",
  "Los documentos de la empresa —certificados, contratos, hojas de vida— son permanentes y reutilizables; los de una oportunidad son temporales y se purgan. Mezclarlos haría que la retención de 30 días borrara evidencia empresarial que debe durar, o al contrario, que un documento caducado siguiera sustentando cumplimientos."),
 ("B12", "Cobertura declarada de cada plataforma",
  "SECOP I y SECOP II se sincronizan por separado y la interfaz declara qué cubre cada una y cuándo se actualizó. Una plataforma no sincronizada se muestra como tal: presentarla como «sin resultados» haría creer que una oportunidad no existe cuando solo falta actualizarla. Verificado: SECOP I expone 78 campos frente a los 59 de SECOP II, con esquemas distintos que no se fuerzan a equivaler."),
 ("B8", "Aislamiento de infraestructura",
  "Base de datos, autenticación, almacenamiento y credenciales pertenecen al proyecto. Ningún componente de producción queda bajo cuentas o accesos de EAG."),
]

DECISIONES_OPCIONALES = [
 ("C1", "Exportación CSV/Excel del tablero", "P1 en backlog; no bloquea el MVP."),
 ("C2", "Umbrales numéricos go/no-go", "Falsos cumplimientos aceptables y precisión mínima por campo; se fijan como criterio propio y documentado, no como validación de EAG."),
]

# (fase, nombre, duración, detalle/hitos, [entregables])
FASES = [
 ("F0", "Infraestructura propia", "2–3 días",
  "Levantar un Supabase self-hosted aislado (red, volúmenes y puertos propios) y aplicar las migraciones de acceso ya escritas en el PR #19. Provisionar el usuario administrador que bloqueaba la validación real de autenticación.",
  ["Stack Supabase operativo y aislado",
   "3 migraciones de acceso aplicadas (roles, RLS, RPC de invitaciones)",
   "Usuario administrador provisionado con perfil y membresía",
   "PR #20 fusionado e issue #3 cerrada"]),
 ("F1", "Autenticación real verificada", "3–4 días",
  "Validar de extremo a extremo el trabajo de autenticación que ya existe y está en verde en CI pero nunca se probó contra un proveedor real: inicio de sesión, rol resuelto por la API, persistencia de sesión y cierre de sesión.",
  ["Login, sesión persistida y logout verificados con evidencia real",
   "PR #19 fusionado e issue #4 cerrada",
   "Permiso «approve/send» añadido (A1)",
   "Decisión documentada sobre el flujo passwordless descartado"]),
 ("F2", "SECOP real y persistencia", "1 semana",
  "Convertir el spike verificado en un conector operacional sobre el dataset de procesos que sí se comprobó. Sincronización idempotente, programada y observable.",
  ["Cliente SECOP con paginación, timeout, reintentos y manejo de cuota",
   "Modelo de oportunidades con ID, URL, fuente y fechas originales preservados",
   "Sincronización idempotente y reanudable ante fallos parciales",
   "Ejecución diaria programada y métricas por ejecución"]),
 ("F3", "Cobertura SECOP I y II", "4–5 días",
  "Ampliar la fuente única a las dos plataformas. Verificado con datos reales: SECOP I expone 78 campos frente a los 59 de SECOP II y sus esquemas no son equivalentes, así que la normalización no puede forzar correspondencias que no existen.",
  ["Conector de SECOP I junto al de SECOP II, con origen preservado por oportunidad",
   "Normalización que no inventa equivalencias entre esquemas distintos",
   "Detección de duplicados entre plataformas sin fusionar sin evidencia",
   "Filtro y distinción por plataforma en el listado",
   "Cobertura y fecha de actualización declaradas por plataforma"]),
 ("F4", "Tablero de oportunidades", "4–5 días",
  "Interfaz de trabajo del analista sobre datos reales: listado, filtros, orden, detalle y filtros guardados, con estados de carga, vacío, error y datos desactualizados.",
  ["Listado paginado con filtros y orden sobre datos reales",
   "Detalle con enlace oficial, fuente y última sincronización",
   "Filtros guardados personales y compartidos",
   "Interfaz accesible y responsive con el sistema de diseño del proyecto"]),
 ("F5", "Expediente documental seguro", "1,5 semanas",
  "Reunir los documentos de cada oportunidad. Como la relación entre datasets no quedó confirmada, la carga manual es el camino principal y la descarga desde SECOP un complemento donde el spike sí verificó URLs.",
  ["Carga manual de documentos por oportunidad",
   "Descarga controlada desde los hosts verificados",
   "Validación de tipo, firma, tamaño, nombres seguros y bloqueo de ejecutables y macros",
   "Cuarentena con antivirus; un fallo del antivirus nunca equivale a archivo limpio",
   "Almacenamiento privado con enlaces firmados de vida corta",
   "Hash, versión, origen, estado, faltantes y fecha de retención por archivo"]),
 ("F6", "OCR y extracción de texto", "1 semana",
  "Convertir los archivos aprobados en texto trazable, conservando el localizador exacto de cada fragmento para poder verificar cualquier afirmación posterior.",
  ["Extracción de PDF, DOCX y XLSX con localizadores verificables",
   "OCR activado por umbral explícito y configurable",
   "Estados de extracción y advertencias de calidad visibles al analista",
   "Navegación del texto extraído a su localizador en el documento"]),
 ("F7", "Perfil empresarial", "1 semana",
  "Formulario desde la plataforma para cargar la información de la empresa: experiencia, contratos, personal, equipos e información financiera y legal, con evidencias y vigencias.",
  ["Carga y edición del perfil desde la interfaz",
   "Evidencias privadas con documento, localizador, versión y vigencia",
   "Versionado con autor, fecha y motivo, para saber qué evidencia sustentó cada análisis",
   "Política de retención del perfil maestro diferenciada de los documentos de oportunidad"]),
 ("F8", "Grafo de análisis (LangGraph)", "3 semanas",
  "El camino crítico del proyecto. Un grafo que orquesta la extracción de requisitos con IA, valida cada cita contra el texto fuente, compara con el perfil y produce un borrador, deteniéndose para la revisión humana antes de cualquier aprobación.",
  ["Grafo con checkpointer en Postgres: el estado del análisis sobrevive reinicios y es auditable",
   "Extracción estructurada de requisitos con esquema versionado y evidencia por requisito",
   "Validación reproducible de citas: una cita no encontrada bloquea el requisito automático",
   "Documentos tratados como datos no confiables; instrucciones embebidas no alteran las reglas",
   "Reglas deterministas para fechas, cantidades, monedas, períodos e indicadores",
   "Estados controlados: cumple, cumple_parcialmente, no_cumple, revision_manual",
   "Interrupción del grafo para revisión y aprobación humana por snapshot",
   "Tope de gasto mensual y caché por hash para controlar el coste de IA"]),
 ("F9", "Base de conocimiento y RAG", "2 semanas",
  "Los documentos que aporta la empresa se fragmentan, se indexan con representación vectorial y se recuperan por significado. Es lo que permite contrastar un requisito con evidencia real en lugar de con una lista de campos.",
  ["Carga de documentos de empresa con categoría, vigencia y estado de verificación",
   "Fragmentación que respeta la estructura del documento y conserva página o sección",
   "Índice vectorial con pgvector, versionado por modelo de representación",
   "Consulta en lenguaje natural con cita obligatoria de documento, página y fragmento",
   "Respuesta de «sin evidencia» cuando ningún fragmento supera el umbral de relevancia",
   "Reindexación y reemplazo que invalidan los fragmentos anteriores",
   "Vista de los fragmentos recuperados con su puntuación y origen"]),
 ("F10", "Comparación asistida por recuperación", "1,5 semanas",
  "Conectar el grafo de análisis con la base de conocimiento: cada requisito extraído del pliego se contrasta con la evidencia recuperada, y el resultado se propone con la fuente a la vista.",
  ["Borrador de cumplimiento por requisito con la evidencia que lo sustenta",
   "Sin evidencia suficiente el estado es revision_manual, nunca no_cumple",
   "La evidencia vencida deja de sustentar un cumple",
   "Cada propuesta es corregible y la corrección queda registrada",
   "Registro de intentos de instrucción embebida en documentos recuperados"]),
 ("F11", "Informe y envío controlado", "4–5 días",
  "Generar el informe del análisis aprobado y enviarlo únicamente a destinatarios autorizados, con idempotencia y auditoría.",
  ["Vista previa y PDF con oportunidad, versión, aprobador, requisitos, evidencias y limitaciones",
   "El PDF se bloquea si la aprobación no está vigente",
   "Envío con clave de idempotencia y destinatarios autorizados",
   "Auditoría de envíos sin contenido sensible"]),
 ("F12", "Retención y operación", "1 semana",
  "Completar los controles operativos antes de tratar documentos reales en producción.",
  ["Purga configurable de archivos, texto, análisis, informes y derivados",
   "Restauración y reversión probadas con evidencia reproducible",
   "Observabilidad sin archivos, credenciales, tokens ni fragmentos sensibles",
   "Endurecimiento y despliegue con entorno de pruebas autenticado"]),
 ("F13", "Cierre y demostración", "3–4 días",
  "Demostración de extremo a extremo con oportunidades públicas reales y entrega del manual operativo.",
  ["Recorrido completo demostrable con datos públicos reales",
   "Manual breve de operación y protocolo de medición",
   "Decisión go/no-go con criterios propios documentados como tales",
   "Registro de limitaciones y pendientes verificables"]),
]

# (riesgo, mitigación, severidad)
RIESGOS = [
 ("Relación entre datasets de SECOP no confirmada (procesos ↔ archivos)",
  "La carga manual de documentos es el camino principal, no un respaldo. No se construye sobre una relación no verificada.", "Alta"),
 ("Costo y latencia de IA sobre pliegos completos",
  "Fragmentación por categorías, tope de gasto mensual, caché por hash y modelo configurable.", "Alta"),
 ("El grafo de análisis es el camino crítico y concentra el riesgo del proyecto",
  "Empezar con un grafo lineal y sin autonomía: nodos deterministas, salidas validadas por esquema y validación de citas obligatoria. No se comprime el plazo.", "Alta"),
 ("Calidad de OCR en pliegos escaneados",
  "Umbral de texto suficiente calibrado desde el inicio; OCR deficiente conduce a revisión manual, nunca a éxito silencioso.", "Media"),
 ("Prompt injection y alucinación de citas",
  "Documentos tratados como datos no confiables (HU-26); validación reproducible de citas; un requisito sin fuente verificable queda bloqueado.", "Media"),
 ("Reclamo de propiedad sobre el software",
  "Repositorio, base de datos y credenciales a nombre del proyecto. Autoría registrada en el historial de commits. Sin entrega de credenciales ni accesos administrativos de producción.", "Alta"),
 ("El sistema afirma capacidad empresarial que la empresa no tiene",
  "B9: toda afirmación sobre la empresa exige fragmento citado y verificable. Sin evidencia suficiente el estado es revision_manual, nunca cumple. En una licitación pública, un cumplimiento inventado no es un error de interfaz: es una oferta temeraria.", "Alta"),
 ("Recuperación que devuelve fragmentos irrelevantes como si fueran evidencia",
  "HU-56: se muestran los fragmentos recuperados con su puntuación y se distingue el citado de los solo recuperados. El umbral se calibra con documentos reales antes del piloto.", "Alta"),
 ("Coste de IA multiplicado por la recuperación",
  "B2 y HU-57: tope mensual, caché por hash y versión, y fragmentación acotada. La recuperación reduce el texto enviado al modelo frente a pasarle el pliego completo.", "Media"),
 ("Esquemas de SECOP I y II no equivalentes",
  "B12: no se fuerzan correspondencias. Un campo que solo existe en una plataforma queda desconocido en la otra, nunca vacío ni cero.", "Media"),
 ("Acumulación de deuda en autenticación sin probar",
  "Se resuelve en la Fase 1, la primera semana de trabajo. Es lo primero que se cierra.", "Media"),
]

PREGUNTAS_EAG = [
 "¿Se admiten pliegos en ZIP con extracción segura? (recomendado: sí, decisión A2)",
 "¿Quién aprueba y envía el informe? (recomendado: permiso «approve/send» asignable, no rol separado — A1)",
 "¿La retención de 30 días aplica también al informe final aprobado? (recomendado: conservar el informe aprobado como maestro y expirar solo los insumos temporales)",
 "¿Proveedor de IA, tope de presupuesto mensual y autorización escrita para enviar documentos internos (contratos, RUP, hojas de vida, finanzas)?",
 "¿Se confirman los límites 20 MB / 100 MB o se mantienen 50 MB / 300 MB?",
 "¿RUP como fuente estructurada de indicadores financieros, o estados financieros cargados manualmente?",
 "¿Qué umbrales de calidad, errores y mejora permiten aceptar el piloto?",
]

NOTA_PREGUNTAS = ("Estas preguntas siguen abiertas, pero ya no bloquean el trabajo. Cada una tiene una "
 "respuesta provisional adoptada por el equipo y marcada como tal; si EAG responde, se ajusta la "
 "configuración, no se rehace el sistema.")

# HUs de ampliación propuestas (cubren gaps detectados en la auditoría)
HUS_AMPLIACION = [
 ("HU-45", "P1", "Administrador", "gestionar usuarios ya invitados (listar, desactivar, cambiar rol)", "mantener el acceso bajo control sin recrear invitaciones",
  ["Permite listar usuarios activos e inactivos, desactivar cuentas y ajustar permisos con auditoría.",
   "Complementa HU-03, que solo cubre la creación y revocación de invitaciones."]),
 ("HU-46", "P0", "Administrador", "consultar el registro de actividad del sistema", "auditar acciones sin depender de logs técnicos",
  ["Muestra acciones de acceso, sincronización, aprobaciones, envíos y cambios de perfil con actor, fecha y resultado.",
   "Excluye contenido sensible de la observabilidad (HU-39)."]),
 ("HU-47", "P1", "Administrador", "configurar parámetros generales (umbrales, límites, textos)", "ajustar la operación sin desplegar código",
  ["Cubre umbrales de OCR, límites de archivos, textos del informe y ventanas de sincronización.",
   "Complementa HU-27, que solo cubre parámetros de IA."]),
 ("HU-48", "P0", "Analista", "recibir notificaciones de eventos (sync terminada, faltantes, OCR fallido, correo enviado)", "actuar sin revisar el tablero constantemente",
  ["Las notificaciones referencian el recurso sin incluir contenido sensible.",
   "Se entregan en la aplicación y por correo autorizado (HU-37)."]),
]

CRITERIOS_ACEPTACION = [
 "Sincronizar oportunidades reales sin duplicados y con filtros configurables.",
 "Procesar documentos o solicitar carga manual cuando la fuente oficial no los entregue.",
 "Presentar evidencia (documento, localizador, fragmento, versión) para cada requisito.",
 "Impedir generar o enviar informes sin aprobación humana vigente.",
 "Respetar permisos por rol y recurso (acceso horizontal bloqueado).",
 "Eliminar contenido temporal según el plazo configurado, con purga verificable.",
 "Demostrar el recorrido completo de extremo a extremo con oportunidades públicas reales.",
]

# (punto, contradicción detectada, resolución)
INCONSISTENCIAS_RESUELTAS = [
 ("Roles y aprobación", "El plan original dejaba que el analista aprobara informes; las HUs marcan un Aprobador con designación pendiente.",
  "A1: 2 roles base + permiso fino «approve/send» asignable."),
 ("ZIP", "El plan admitía ZIP; HU-12 lo rechazaba sin controles seguros.",
  "A2: ZIP admitido con extracción en sandbox y controles explícitos."),
 ("Retención 30 días", "El plan lo daba por hecho; HU-38 lo marcaba pendiente de validación.",
  "Configurable y verificable con reloj controlado; el informe aprobado se conserva como maestro."),
 ("Límites 50/300 MB", "El plan los fijaba como aceptación; el PDF los listaba pendientes.",
  "B1: 20 MB / 100 MB como punto de partida calibrable."),
 ("Horario 06:00 + 7 días", "El plan lo daba por hecho; HU-07 exigía validar el campo temporal real del dataset.",
  "Se usa el campo temporal verificado en el spike; 06:00 y 7 días como configuración inicial."),
 ("Dependencia de EAG", "El plan y las HUs trataban la autorización y la muestra de EAG como hitos bloqueantes.",
  "A5 / B8: el proyecto no espera entregables de EAG. Perfil cargable desde la plataforma, piloto con datos públicos y credenciales propias."),
 ("Orquestación de tareas", "El plan original usaba Celery + Redis, sin definir dónde vivía el estado del análisis ni la revisión humana.",
  "B7: grafo LangGraph con checkpointer en Postgres; la revisión humana es una interrupción del grafo."),
]
