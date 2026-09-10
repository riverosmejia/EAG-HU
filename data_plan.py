# -*- coding: utf-8 -*-
"""Datos del Plan de Acción del MVP de EAG Ingenieros (SECOP II).

Resultado de la auditoría técnica del 2026-09-10 sobre el plan de implementación
original y las 44 HUs. Consumido por build_page.py (versión rápida) y
build_docs.py (versión detallada).
Estructura: tuplas ordenadas, nunca HTML.
"""

META = ("1.1", "2026-09-10")

RESUMEN = [
 ("Objetivo", "Construir en 12 semanas una aplicación web productiva (React + FastAPI) que consulte oportunidades de SECOP II, reúna y procese documentos, compare requisitos con la información de EAG y produzca un borrador de evaluación revisado por humanos antes de generar el informe."),
 ("Flujo", "Sincronizar SECOP → filtrar → descargar/cargar documentos → validar → extraer texto/OCR → identificar requisitos → comparar con EAG → borrador → revisión humana → aprobación → PDF → correo autorizado."),
 ("Datos", "APIs oficiales de procesos (p6dx-8zbt) y documentos (dmgg-8hin), actualizadas por Socrata. Sin automatización de la interfaz web de SECOP."),
]

# (capa, tecnología, decisión, etiqueta corta para versión rápida)
STACK = [
 ("Frontend", "React · TypeScript · Vite · React Query · Tailwind", "Desplegado en Vercel; cliente TypeScript generado desde OpenAPI.", "React + Vite"),
 ("Backend", "Python 3.12 · FastAPI · Pydantic · SQLAlchemy · Alembic", "API /api/v1 + OpenAPI; autorización resuelta en servidor (HU-04).", "FastAPI"),
 ("Datos", "Supabase PostgreSQL · Auth · Storage", "Bucket privado + URLs firmadas cortas (HU-14); RLS solo para Storage, no para negocio (A3).", "Supabase"),
 ("Asíncrono", "Celery + Redis", "Redis como add-on externo (Redis Cloud / Upstash); presupuestado.", "Celery + Redis"),
 ("Scheduler", "Cron de Render → POST /sync-runs", "Decisión B4: menos piezas que Celery Beat.", "Cron Render"),
 ("IA", "Adaptador intercambiable · OpenAI Responses API inicial", "store=false · tope de gasto mensual configurable · salidas JSON validadas por esquema · chunking por categorías (B2).", "OpenAI API"),
 ("OCR", "Tesseract", "Worker Celery con ≥2 GB RAM; umbral de «texto suficiente» calibrado en semana 1.", "Tesseract"),
 ("Antivirus", "ClamAV", "Escaneo por archivo/miembro en worker; un fallo del antivirus no equivale a limpio (HU-13).", "ClamAV"),
 ("PDF", "WeasyPrint", "Fuentes con soporte español en la imagen Docker de Render.", "WeasyPrint"),
 ("Correo", "Resend", "Invitaciones + informes; idempotencia por clave (HU-37).", "Resend"),
 ("Errores", "Sentry", "Sin contenido sensible en logs ni alertas (HU-39).", "Sentry"),
]

# Decisiones de la auditoría: (id, título, decisión)
DECISIONES_CRITICAS = [
 ("A1", "Modelado de roles",
  "2 roles base (Administrador, Analista) + permiso fino «approve/send» asignable. El Aprobador/Gerencia se implementa como permiso configurable, no como rol separado. Alinea HU-33 a HU-37 y resuelve la contradicción con el plan original."),
 ("A2", "Pliegos en ZIP",
  "Se admiten con extracción en sandbox y controles explícitos: ratio anti zip-bomb, profundidad máxima 5, tamaño por miembro, escaneo antivirus por miembro, sin symlinks ni path traversal. Resuelve la contradicción con HU-12 y preserva la cobertura real de SECOP."),
 ("A3", "Arquitectura de autorización",
  "FastAPI como capa de autoridad (conexión service_role; RLS solo para Storage y bucket privado). Permisos resueltos en servidor, nunca en claims del navegador (HU-04). Evita el pitfall de confiar en RLS para datos de negocio."),
 ("A4", "Aprobación por snapshot",
  "Al aprobar se congela una versión del análisis (expediente + perfil + decisiones). Cambios posteriores crean una versión nueva; no se invalida retroactivamente (HU-34 se cumple congelando, no invalidando)."),
 ("A5", "Hito externo bloqueante",
  "Autorización escrita de tratamiento de datos + muestra real de licitaciones como hito de la semana 1. Sin este hito, el piloto (semanas 11-12) no se cierra."),
]

DECISIONES_ADOPTADAS = [
 ("B1", "Límites de archivos",
  "20 MB por archivo y 100 MB por oportunidad como punto de partida, calibrables con la muestra real. Más viable para OCR en Render que los 50/300 MB originales."),
 ("B2", "Presupuesto de IA",
  "Tope de gasto mensual por variable de entorno (HU-27); chunking del pliego por categorías antes de llamar; modelo configurable; store=false."),
 ("B3", "HUs de ampliación",
  "HU-45 a HU-48 propuestas (usuarios existentes, auditoría, configuración general, notificaciones): cubren los gaps del plan frente a las pantallas prometidas. Pendientes de validación con EAG."),
 ("B4", "Scheduler",
  "Cron de Render llamando al endpoint de sincronización; menos piezas y superficie que Celery Beat."),
 ("B5", "Verificación temprana de SECOP",
  "Semana 1: verificar la relación real entre los datasets p6dx-8zbt y dmgg-8hin y la vigencia de los enlaces de descarga. Riesgo crítico temprano."),
 ("B6", "Semana 7 realista",
  "La extracción estructurada de requisitos con validación de citas (incluida normalización OCR) se planifica en 2 semanas (7-8). Es el camino crítico."),
]

DECISIONES_OPCIONALES = [
 ("C1", "Exportación CSV/Excel del tablero", "P1 en backlog; no bloquea el MVP."),
 ("C2", "Umbrales numéricos go/no-go", "Falsos cumplimientos aceptables y precisión mínima por campo; acordar con EAG en el hito del piloto."),
]

# (semana, foco, detalle/hitos)
SEMANAS = [
 ("01", "Prueba técnica SECOP", "APIs p6dx-8zbt + dmgg-8hin: relación real entre datasets, descarga de documentos, corpus de evaluación. HITO: autorización de tratamiento de datos (A5) y muestra real (B5)."),
 ("02", "Fundaciones", "Monorepo, CI, ambientes, Supabase, auth por invitación (magic-link), roles + permisos (A1), migraciones, despliegue vacío."),
 ("03", "Cliente Socrata y sincronización", "Cliente Socrata, sincronización + deduplicación, horario configurable (HU-07), reintentos y límites."),
 ("04", "Tablero y detalle", "Filtros, listado, paginación, detalle de oportunidad con datos de última sincronización (HU-08 a HU-10)."),
 ("05", "Expediente documental", "Descarga + carga manual, ZIP seguro (A2), ClamAV, límites 20/100 MB (B1), extracción de texto + OCR, control de archivos (HU-11 a HU-19)."),
 ("06", "Perfil EAG", "Experiencia, contratos, personal, capacidades, finanzas; edición con versión e historial (HU-20 a HU-24)."),
 ("07", "Extracción IA de requisitos", "Extracción estructurada con IA + esquemas versionados; chunking por categorías (B2); tope de gasto mensual; salida tipada con evidencia."),
 ("08", "Validación de citas y comparación", "Validación de citas con normalización OCR (B6); motor determinista de fechas, cantidades e indicadores; estados controlados (HU-26, HU-29, HU-31)."),
 ("09", "Aprobación y entrega", "Aprobación por snapshot (A4), previsualización y PDF (WeasyPrint), correo con idempotencia (HU-33 a HU-37)."),
 ("10", "Operación y retención", "Retención 30 días (job + tombstones), reintentos, backups y rollback probado, monitoreo (Sentry), endurecimiento de seguridad."),
 ("11", "Piloto", "Licitaciones reales con muestra autorizada (depende de A5); medición de tiempo y errores frente al proceso manual (HU-42)."),
 ("12", "Cierre y go/no-go", "Correcciones, documentación, capacitación, decisión go/no-go con umbrales acordados (C2) y revisión humana registrada."),
]

# (riesgo, mitigación, severidad)
RIESGOS = [
 ("Cobertura real de SECOP (relación de datasets, ZIP, enlaces)", "B5 en semana 1 + A2 (ZIP seguro) + carga manual de respaldo (HU-12).", "Alta"),
 ("Costo y latencia de IA sobre pliegos completos", "B2: chunking por categorías, tope de gasto mensual, modelo configurable.", "Alta"),
 ("Dependencia de EAG (autorización, muestra, decisiones)", "A5 como hito bloqueante; tabla de pendientes con responsables propuestos.", "Alta"),
 ("Calidad de OCR en escaneados de pliegos", "Umbral de «texto suficiente» calibrado en semana 1; fallo u OCR deficiente pasa a revisión manual (HU-17).", "Media"),
 ("Recursos en Render (OCR + ClamAV)", "Worker Celery con ≥2 GB RAM; add-ons presupuestados (~50-80 USD/mes + IA variable).", "Media"),
 ("Prompt injection y alucinación de citas", "Documentos tratados como datos no confiables (HU-26); validación reproducible de citas; requisito sin fuente bloqueado.", "Media"),
]

PREGUNTAS_EAG = [
 "¿Se admiten pliegos en ZIP con extracción segura? (recomendado: sí, decisión A2)",
 "¿Quién aprueba y envía el informe? (recomendado: permiso «approve/send» asignable, no rol separado — A1)",
 "¿La retención de 30 días aplica también al informe final aprobado? (recomendado: conservar el informe aprobado como maestro y expirar solo los insumos temporales)",
 "¿Proveedor de IA, tope de presupuesto mensual y autorización escrita para enviar documentos internos (contratos, RUP, hojas de vida, finanzas)?",
 "¿Cuándo entrega EAG la muestra real de licitaciones y la autorización de tratamiento de datos? (define si el piloto cierra en 12 semanas)",
 "¿Se confirman los límites 20 MB / 100 MB o se mantienen 50 MB / 300 MB?",
 "¿RUP como fuente estructurada de indicadores financieros, o estados financieros cargados manualmente?",
]

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
 "Sincronizar sin duplicados y aplicar filtros configurables.",
 "Procesar documentos o solicitar carga manual cuando la fuente oficial no los entregue.",
 "Presentar evidencia (documento, localizador, fragmento, versión) para cada requisito.",
 "Impedir generar o enviar informes sin aprobación humana vigente.",
 "Respetar permisos por rol y recurso (acceso horizontal bloqueado).",
 "Eliminar contenido temporal a los 30 días (plazo configurable, sujeto a validación de EAG).",
 "Piloto: reducir al menos 60 % el tiempo de preevaluación frente al proceso manual (medido, no garantizado).",
]

# (punto, contradicción detectada, resolución)
INCONSISTENCIAS_RESUELTAS = [
 ("Roles y aprobación", "El plan original dejaba que el analista aprobara informes; las HUs marcan un Aprobador con designación pendiente.",
  "A1: 2 roles base + permiso fino «approve/send» asignable."),
 ("ZIP", "El plan admitía ZIP; HU-12 lo rechazaba sin controles seguros.",
  "A2: ZIP admitido con extracción en sandbox y controles explícitos."),
 ("Retención 30 días", "El plan lo daba por hecho; HU-38 lo marcaba pendiente de validación.",
  "Configurable y validado por EAG; el informe aprobado se conserva como maestro."),
 ("Límites 50/300 MB", "El plan los fijaba como aceptación; el PDF los listaba pendientes.",
  "B1: 20 MB / 100 MB como punto de partida calibrable."),
 ("Horario 06:00 + 7 días", "El plan lo daba por hecho; HU-07 exigía validar el campo temporal real del dataset.",
  "B5: verificación en semana 1; 06:00 Bogotá / 7 días como configuración inicial."),
]