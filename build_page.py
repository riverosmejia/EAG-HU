# -*- coding: utf-8 -*-
"""Genera index.html para EAG-HU: 44 HUs del MVP de EAG Ingenieros (SECOP II)."""
import html as H

# (id, prioridad, issue, actor, capacidad, valor, [criterios])
E1 = ("E1", "Acceso, roles y aislamiento",
      "Permitir el uso del sistema solo a personas invitadas, con dos roles y controles efectivos en backend y datos.",
      "MVP-04", [
("HU-01","P0","MVP-04","Usuario invitado","acceder mediante un enlace de autenticación válido","usar el sistema sin registro público ni contraseña gestionada por la aplicación",
 ["El acceso exige una invitación vigente y una sesión válida.",
  "Un token ausente, inválido o vencido recibe 401.",
  "La interfaz no expone registro público ni permite elegir rol u organización."]),
("HU-02","P0","MVP-04","Usuario autenticado","consultar mi sesión y cerrar sesión","confirmar mi identidad, rol y pertenencia antes de trabajar",
 ["La sesión muestra únicamente identidad y pertenencia propias.",
  "El backend valida firma, expiración, issuer y audience configurados.",
  "Tras retirar la membresía, las rutas protegidas dejan de autorizar al usuario; la limitación del TTL del proveedor queda visible."]),
("HU-03","P0","MVP-04","Administrador","crear, revocar y consultar invitaciones de EAG","controlar quién puede ingresar a la organización",
 ["Solo el administrador ejecuta estas acciones desde el backend.",
  "El cliente no puede escoger role ni organization_id en el cuerpo.",
  "Cada acción genera auditoría sin tokens, secretos ni correos en metadata.",
  "El reenvío solo se habilita cuando exista una operación de proveedor comprobada; mientras tanto se informa como no disponible."]),
("HU-04","P0","MVP-04","Administrador","aplicar permisos por rol y recurso","evitar acceso horizontal, escalada de privilegios y exposición entre organizaciones",
 ["Un usuario autenticado sin permiso recibe 403.",
  "El rol y la organización se resuelven en el servidor, no desde claims o campos confiados al navegador.",
  "Las pruebas negativas cubren recursos ajenos, escritura directa y claves privilegiadas en cliente o logs."]),
])

E2 = ("E2", "Oportunidades SECOP II",
      "Incorporar oportunidades oficiales de forma idempotente y facilitar su búsqueda sin inventar cobertura ni datos.",
      "MVP-02 · MVP-05 · MVP-06", [
("HU-05","P0","MVP-02 / MVP-05","Sistema","sincronizar oportunidades desde los conjuntos oficiales verificados","mantener un catálogo trazable a SECOP II",
 ["Cada oportunidad conserva ID, enlace, fuente, campos originales relevantes y fecha de consulta.",
  "La consulta usa filtros permitidos, paginación, timeout, reintentos limitados y manejo de cuota.",
  "Una ejecución de red acotada se distingue de fixtures y mocks."]),
("HU-06","P0","MVP-05","Administrador","ejecutar una sincronización manual autorizada","actualizar el catálogo cuando sea necesario y observar su resultado",
 ["Solo un rol autorizado puede iniciar la operación.",
  "Repetir o reintentar un lote no crea duplicados.",
  "Éxitos parciales, 429, timeouts y registros pendientes quedan visibles y reanudables."]),
("HU-07","P1","MVP-05","Sistema","ejecutar una sincronización periódica incremental","detectar cambios tardíos sin recorrer indiscriminadamente toda la fuente",
 ["Horario, zona horaria y ventana incremental son configurables.",
  "El campo temporal usado corresponde al esquema real verificado.",
  "La propuesta de 06:00 America/Bogota y 7 días no se activa como decisión definitiva sin validación."]),
("HU-08","P0","MVP-06","Analista","listar, ordenar, paginar y filtrar oportunidades","encontrar casos relevantes para revisión",
 ["Filtros y resultados provienen de la API, sin datos mock en producción.",
  "Se muestran carga, vacío, error y datos desactualizados.",
  "Los controles son operables con teclado y en pantalla estrecha."]),
("HU-09","P1","MVP-06","Analista","guardar y reutilizar filtros de trabajo","repetir búsquedas frecuentes con criterios consistentes",
 ["Solo se ofrecen campos disponibles y verificados.",
  "Los filtros personales se distinguen de la configuración compartida.",
  "Solo usuarios autorizados modifican filtros compartidos de EAG."]),
("HU-10","P0","MVP-06","Analista","abrir el detalle de una oportunidad y volver al listado","examinar sus datos oficiales sin perder el contexto de búsqueda",
 ["El detalle muestra ID, enlace oficial, fuente y última sincronización.",
  "Datos ausentes se presentan como desconocidos, no como cero.",
  "Al volver se conservan filtros, orden y página."]),
])

E3 = ("E3", "Expediente documental seguro",
      "Reunir documentos de la oportunidad con controles de seguridad, versiones y faltantes explícitos.",
      "MVP-07", [
("HU-11","P0","MVP-07","Analista","obtener los documentos disponibles desde SECOP II","formar el expediente de la oportunidad con su origen comprobable",
 ["La descarga usa dominios permitidos, timeout, tamaño máximo y redirecciones validadas.",
  "Cada archivo conserva origen, hash, versión, fecha y estado.",
  "Descarga encontrada no se presenta como expediente completo."]),
("HU-12","P0","MVP-07","Analista","cargar documentos complementarios de una oportunidad SECOP II","completar el expediente cuando la fuente oficial no permita obtenerlos",
 ["La carga manual exige oportunidad oficial existente y permiso sobre ella.",
  "Se aceptan inicialmente PDF, DOCX y XLSX válidos; ZIP se rechaza salvo controles seguros explícitos.",
  "El origen manual queda diferenciado del origen SECOP."]),
("HU-13","P0","MVP-07","Sistema","validar y poner en cuarentena cada archivo","impedir que contenido peligroso o simulado avance al procesamiento",
 ["Se validan extensión, firma/MIME, nombre seguro y límites configurables.",
  "Se bloquean ejecutables, macros, path traversal, tipo simulado y SSRF.",
  "Un fallo del antivirus no equivale a archivo limpio; un archivo en cuarentena no se procesa."]),
("HU-14","P0","MVP-07","Usuario autorizado","consultar o descargar documentos privados","revisar evidencia sin exponerla públicamente",
 ["El backend autoriza cada recurso y el almacenamiento permanece privado.",
  "Los enlaces firmados tienen vida breve y no se registran con contenido sensible.",
  "Las pruebas cubren acceso permitido y denegado."]),
("HU-15","P0","MVP-07","Analista","ver el inventario, las versiones y los documentos faltantes","saber si el expediente permite un análisis defendible",
 ["Cada elemento muestra origen, versión, estado de lectura y retención.",
  "Los documentos esperados pero ausentes se registran como faltantes.",
  "Un expediente incompleto limita las conclusiones y no se interpreta como ausencia de requisitos."]),
])

E4 = ("E4", "Extracción de texto y OCR",
      "Convertir archivos aprobados en texto trazable sin ocultar fallos ni mezclar versiones.",
      "MVP-08", [
("HU-16","P0","MVP-08","Sistema","extraer texto de PDF, DOCX y XLSX aprobados","habilitar análisis posterior conservando la estructura de origen",
 ["Fixtures sintéticas por formato producen texto y localizadores verificables.",
  "El proceso respeta límites de páginas, memoria, tiempo y reintentos.",
  "Archivos corruptos, cifrados o fuera de presupuesto terminan con error visible y recuperable."]),
("HU-17","P0","MVP-08","Sistema","aplicar OCR básico cuando un PDF no tenga texto suficiente","recuperar contenido de escaneados sin fingir precisión",
 ["OCR se activa por un criterio explícito y configurable.",
  "El resultado conserva página y advertencias de calidad.",
  "Texto vacío o OCR deficiente pasa a revisión manual, no a éxito silencioso."]),
("HU-18","P0","MVP-08","Analista","consultar estados y advertencias de extracción","identificar qué documento requiere reemplazo, reintento o revisión humana",
 ["Se distinguen pendiente, procesando, completado con advertencias y fallido.",
  "La causa y el siguiente paso se muestran sin contenido sensible en logs.",
  "Un reintento controlado no duplica trabajo completado para el mismo hash y versión."]),
("HU-19","P0","MVP-08","Analista","navegar del texto extraído a su localizador","verificar cada fragmento contra documento, página, sección o celda",
 ["Documento, localizador y versión acompañan cada fragmento.",
  "El localizador permite comprobación manual en una muestra autorizada.",
  "Reprocesar una versión nueva no modifica silenciosamente resultados anteriores."]),
])

E5 = ("E5", "Perfil y evidencias empresariales",
      "Mantener una fuente empresarial autorizada, versionada y verificable para las comparaciones.",
      "MVP-09", [
("HU-20","P0","MVP-09","Administrador","registrar experiencia y contratos de EAG","sustentar requisitos de experiencia con datos y soportes",
 ["Se registran objeto/especialidad, rol, fechas, valor/moneda cuando aplique y soporte.",
  "Cada evidencia tiene documento, localizador, versión y vigencia o queda pendiente.",
  "Datos desconocidos no se convierten en cero."]),
("HU-21","P0","MVP-09","Administrador","registrar personal y sus credenciales","contrastar perfiles requeridos sin exponer datos innecesarios",
 ["Se incluyen identificador interno, rol, formación, experiencia y certificaciones/vigencias pertinentes.",
  "El acceso sigue la matriz de permisos y minimiza datos personales.",
  "Un perfil incompleto conduce a pendiente o revisión, no a incapacidad definitiva."]),
("HU-22","P0","MVP-09","Administrador","registrar capacidades, equipos y disponibilidad acreditada","evaluar requisitos técnicos y operativos con soporte",
 ["Tipo, cantidad, características y disponibilidad usan unidades explícitas.",
  "La evidencia se marca pendiente o verificada por revisión humana.",
  "Una afirmación sin soporte no puede sustentar un cumple."]),
("HU-23","P0","MVP-09","Administrador","registrar información financiera, legal y documental","comparar indicadores y vigencias exigidos por una oportunidad",
 ["Período, valores, moneda/unidad, fórmula y soporte quedan identificados.",
  "Las fechas y números se validan; vacío, desconocido y cero son distintos.",
  "Solo se exponen los datos necesarios al rol autorizado."]),
("HU-24","P0","MVP-09","Administrador","editar el perfil creando una nueva versión e historial","preservar qué evidencia se usó en cada análisis",
 ["La edición guarda autor, fecha, motivo y estado pendiente/verificado.",
  "Los análisis existentes mantienen referencia a la versión comparada.",
  "La política de retención del perfil maestro se distingue de la de documentos de oportunidad."]),
])

E6 = ("E6", "Extracción estructurada de requisitos",
      "Identificar requisitos mediante un adaptador de IA, conservando evidencia, límites y revisión.",
      "MVP-10", [
("HU-25","P0","MVP-10","Analista","obtener requisitos estructurados del expediente","reducir lectura inicial sin perder categorías, condiciones ni fuente",
 ["La salida cumple un esquema tipado y no decide participación ni cumplimiento final.",
  "Cada requisito incluye categoría, texto, documento, localizador, fragmento y versión.",
  "Salida inválida, truncada o ambigua se rechaza o marca para revisión."]),
("HU-26","P0","MVP-10","Sistema","validar las citas de cada requisito contra el texto fuente","evitar requisitos inventados o referencias inexistentes",
 ["Fragmento y localizador deben encontrarse o justificarse mediante una validación reproducible.",
  "Una alucinación de fuente bloquea el requisito automático.",
  "Los documentos se tratan como datos no confiables; instrucciones embebidas no cambian las reglas del sistema."]),
("HU-27","P0","MVP-10","Administrador","configurar el proveedor y los límites operativos de IA","controlar coste, repetición y tratamiento de información",
 ["Modelo, prompt, esquema y configuración quedan versionados sin contenido sensible en logs.",
  "Se limitan tokens, lotes, concurrencia, reintentos y llamadas repetidas por hash/versión.",
  "El envío de documentos internos exige autorización empresarial específica y secretos solo en backend."]),
("HU-28","P0","MVP-10","Analista","ver advertencias e incertidumbres de extracción","saber qué requisito necesita lectura humana",
 ["Se muestran ambigüedad, evidencia faltante, error de proveedor y posibles conflictos.",
  "La ausencia de salida del modelo no se interpreta como ausencia de requisitos.",
  "La evaluación real se diferencia de pruebas con mocks y reporta tamaño de muestra."]),
])

E7 = ("E7", "Comparación, revisión y aprobación humana",
      "Producir un borrador explicable y corregible, sin sustituir la decisión empresarial.",
      "MVP-11", [
("HU-29","P0","MVP-11","Sistema","comparar fechas, cantidades e indicadores con reglas deterministas","obtener resultados reproducibles para condiciones objetivas",
 ["Las reglas manejan límites, unidades, monedas, períodos y vigencias explícitos.",
  "Cada cálculo conserva entradas, regla, resultado y motivo.",
  "Valores faltantes o incompatibles pasan a revisión manual."]),
("HU-30","P0","MVP-11","Analista","comparar requisitos semánticos con evidencias de EAG","obtener una propuesta explicable para revisión",
 ["Se muestran por separado fuente del requisito y evidencia empresarial.",
  "No se afirma cumplimiento sin evidencia suficiente, vigente y compatible.",
  "Contradicciones, ambigüedad o soportes ilegibles quedan visibles."]),
("HU-31","P0","MVP-11","Analista","clasificar cada requisito con estados controlados","usar un lenguaje consistente y auditable",
 ["Solo se permiten cumple, cumple_parcialmente, no_cumple y revision_manual.",
  "Falta de evidencia no genera cumple ni no_cumple automáticamente.",
  "Cumple parcialmente solo aplica a un requisito divisible bajo criterio validado; mientras no exista, no se asigna automáticamente."]),
("HU-32","P0","MVP-11","Analista","revisar y corregir el borrador con justificación","resolver errores y dejar pendientes explícitos",
 ["Puede cambiar estado, evidencia u observación registrando autor, fecha y motivo.",
  "La salida automática inicial se conserva para medir discrepancias.",
  "Requisitos no aplicables permanecen en revision_manual hasta acordar evidencia y tratamiento."]),
("HU-33","P0","MVP-11","Aprobador autorizado","aprobar una versión concreta del análisis","habilitar el informe final solo después de revisión humana",
 ["La aprobación guarda usuario, fecha y versiones de expediente, perfil y análisis.",
  "Pendientes y limitaciones siguen visibles.",
  "Aprobar no equivale a postular, adjudicar ni decidir automáticamente participar."]),
("HU-34","P0","MVP-11","Sistema","invalidar la aprobación cuando cambien entradas o resultados","impedir que un informe use evidencia desactualizada",
 ["Cambios de documento, perfil, requisito, evidencia o decisión crean una nueva versión.",
  "La aprobación anterior deja de habilitar informe o envío.",
  "La interfaz explica qué cambió y qué revisión debe repetirse."]),
])

E8 = ("E8", "Informe y comunicación controlada",
      "Entregar un informe aprobado, trazable y seguro a destinatarios autorizados.",
      "MVP-12", [
("HU-35","P0","MVP-12","Analista","previsualizar el informe del análisis aprobado","verificar su contenido y presentación antes del envío",
 ["El informe identifica oportunidad, versión, aprobador, fecha, requisitos, evidencias y limitaciones.",
  "El backend bloquea el PDF final si la aprobación no está vigente.",
  "Tablas largas y caracteres españoles se renderizan sin recortes."]),
("HU-36","P0","MVP-12","Usuario autorizado","descargar el PDF final aprobado","conservar una salida legible sin exponer el expediente completo",
 ["La descarga exige permiso por recurso y usa almacenamiento privado.",
  "El PDF no añade afirmaciones sin evidencia ni adjunta soportes por defecto.",
  "La generación queda auditada con la versión correspondiente."]),
("HU-37","P0","MVP-12","Usuario autorizado","enviar el informe a destinatarios configurados","compartir el resultado sin duplicados ni envíos indiscriminados",
 ["Solo destinatarios autorizados pueden seleccionarse y el backend vuelve a validar aprobación.",
  "Una clave de idempotencia evita correos duplicados durante reintentos.",
  "Destino, estado e intentos quedan auditados sin contenido sensible; pruebas reales usan únicamente bandeja autorizada."]),
])

E9 = ("E9", "Retención, operación y recuperación",
      "Completar controles operativos antes de tratar documentos reales en producción.",
      "MVP-13", [
("HU-38","P0","MVP-13","Administrador","aplicar la política de retención a datos de oportunidad","eliminar oportunamente archivos, texto, análisis, informes y copias de trabajo",
 ["Un reloj controlado prueba el plazo configurado y el origen del cómputo.",
  "La purga cubre derivados y evita resurrección tras una restauración.",
  "El plazo propuesto de 30 días no se presenta como política definitiva hasta validación de EAG y backups."]),
("HU-39","P0","MVP-13","Equipo operador","monitorear tareas, fallos y alertas","detectar problemas sin registrar contenido empresarial",
 ["Se observan sincronización, extracción, IA, correo y colas fallidas con estados técnicos.",
  "Logs y alertas excluyen archivos, credenciales, tokens y fragmentos sensibles.",
  "Reintentos tienen límites y los fallos no se ocultan como éxito."]),
("HU-40","P0","MVP-13","Equipo operador","restaurar backups y ejecutar rollback probado","recuperar el servicio respetando accesos y purgas",
 ["Staging exige autenticación y no expone claves privilegiadas ni buckets públicos.",
  "Se ensayan restauración y rollback con evidencia reproducible.",
  "La restauración reaplica tombstones o purgas pendientes."]),
("HU-41","P0","MVP-13","Responsable empresarial","autorizar el tratamiento de datos y proveedores externos","decidir conscientemente qué información puede procesarse",
 ["Se documentan finalidad, datos enviados, retención y controles del proveedor.",
  "No se contratan ni configuran servicios pagos sin autorización específica.",
  "store=false no se presenta por sí solo como retención cero."]),
])

E10 = ("E10", "Piloto, medición y decisión de lanzamiento",
      "Validar utilidad, calidad y riesgos con usuarios y datos autorizados antes de cerrar el MVP.",
      "MVP-14", [
("HU-42","P0","MVP-14","Responsable del piloto","comparar el análisis manual y asistido sobre las mismas entradas","medir tiempo y errores sin sesgos evitables",
 ["Se fijan previamente muestra, versiones, referencia humana, alcance y umbrales.",
  "Se miden por separado tiempo transcurrido, procesamiento, revisión, corrección y trabajo humano.",
  "Se reportan tamaño de muestra, denominadores, fallos y falsos cumplimientos; 60% no es garantía ni resultado demostrado."]),
("HU-43","P0","MVP-14","Analista y administrador","ejecutar UAT y recibir un manual breve","confirmar que el flujo puede operarse de forma segura",
 ["El recorrido extremo a extremo usa usuarios y datos autorizados.",
  "Incidencias, capacitación y aceptación o rechazo se registran con responsables.",
  "Si faltan datos o usuarios, se entrega el protocolo pero el piloto sigue pendiente."]),
("HU-44","P0","MVP-14","Gerencia","tomar una decisión go/no-go basada en evidencia","evitar lanzar con riesgos críticos o calidad insuficiente",
 ["La decisión incluye métricas, limitaciones, incidencias y pendientes.",
  "Falsos cumplimientos o riesgos críticos de seguridad no resueltos bloquean el lanzamiento.",
  "La revisión humana final queda registrada; el sistema no decide autónomamente participar en una licitación."]),
])

EPICAS = [E1, E2, E3, E4, E5, E6, E7, E8, E9, E10]

PENDIENTES = [
 ("Muestra real autorizada y documentos mínimos del perfil","HU-20 a HU-34, HU-42","Comercial, áreas aportantes y Gerencia"),
 ("Cobertura real de pliegos y relación entre datasets SECOP","HU-05, HU-11, HU-15","Equipo técnico + Comercial"),
 ("Horario y ventana incremental","HU-07","Administrador / operación"),
 ("Límites de 50 MB por archivo y 300 MB por oportunidad","HU-13, HU-16","EAG + equipo técnico"),
 ("Criterios por tipo para cumple parcialmente y no aplica","HU-31, HU-32","Comercial y áreas competentes"),
 ("Personas o roles autorizados para aprobar y enviar","HU-33 a HU-37","Gerencia"),
 ("Inicio del plazo de 30 días, maestros, auditoría y backups","HU-38, HU-40","Gerencia + legal/operación"),
 ("Proveedor de IA, datos permitidos, retención y presupuesto","HU-27, HU-41","Gerencia + responsable de datos"),
 ("Umbrales, tamaño de muestra y criterio go/no-go","HU-42 a HU-44","Gerencia + revisor designado"),
]

EXCLUSIONES = [
 "Postulación automática de ofertas o decisión autónoma de participar.",
 "Garantía de adjudicación, precisión no medida o reducción de tiempo presentada como resultado.",
 "Fuentes distintas de SECOP II en la primera versión.",
 "Registro manual de oportunidades; la carga manual se limita a documentos complementarios de una oportunidad SECOP II.",
 "WhatsApp, Telegram, facturación, aplicación móvil y personalizaciones avanzadas.",
 "Buckets públicos, enlaces permanentes, expedientes completos adjuntos por defecto o contenido sensible en observabilidad.",
 "Uso de documentos internos con un proveedor externo sin autorización empresarial específica.",
]

FLOW = [
 ("SECOP II","Sincronización y detalle de oportunidades oficiales"),
 ("Expediente","Documentos con origen, versión y cuarentena"),
 ("Extracción","Texto y OCR trazables por localizador"),
 ("Requisitos","Extracción estructurada con IA y citas validadas"),
 ("Perfil EAG","Evidencias empresariales versionadas"),
 ("Comparación","Propuesta explicable y corregible"),
 ("Revisión","Estados controlados y justificación"),
 ("Aprobación","Solo después de revisión humana"),
 ("PDF","Informe aprobado y trazable"),
 ("Correo autorizado","Solo a destinatarios configurados"),
]

ACTORS = [
 ("Analista","ROL OPERATIVO","Busca oportunidades, reúne documentos, revisa requisitos, corrige resultados y prepara el borrador.",
  '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-6 8-6s8 2 8 6"/>'),
 ("Administrador","ROL DE GESTIÓN","Gestiona acceso, configuración compartida, perfil empresarial y operación autorizada.",
  '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09a1.65 1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33h.01a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82v.01a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>'),
 ("Aprobador / Gerencia","ROL DECISOR","Aprueba una versión del análisis y toma la decisión empresarial. Su designación exacta está pendiente.",
  '<path d="M9 12l2 2 4-4"/><circle cx="12" cy="12" r="9"/>'),
 ("Sistema / Equipo operador","ROL TÉCNICO","Ejecuta procesos controlados y mantiene seguridad, trazabilidad, retención y recuperación.",
  '<rect x="2" y="4" width="20" height="14" rx="2"/><path d="M8 21h8M12 18v3"/>'),
]

CSS = """
:root{
  --bg:#ffffff;--bg-soft:#f6f8f8;--bg-accent:#eef7f6;--ink:#10201e;--ink-2:#33423f;--muted:#64716e;
  --line:#e3e8e7;--line-strong:#cdd6d4;--accent:#0f766e;--accent-strong:#0b5e58;--accent-soft:#e6f4f2;
  --ok:#1a7f4e;--warn:#b45309;--danger:#b42318;--radius:14px;--radius-sm:9px;
  --shadow-card:0 1px 2px rgba(16,32,30,.05);
  --shadow-rec:0 18px 44px -18px rgba(15,118,110,.35),0 2px 6px rgba(16,32,30,.06);
  --mono:'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
  --sans:'IBM Plex Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:84px}
body{font-family:var(--sans);color:var(--ink);background:var(--bg);line-height:1.55;font-size:16px;-webkit-font-smoothing:antialiased}
::selection{background:var(--accent-soft)}
a{color:var(--accent-strong);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1160px;margin:0 auto;padding:0 24px}
.mono{font-family:var(--mono)}
.topbar{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.9);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.topbar-inner{display:flex;align-items:center;justify-content:space-between;gap:16px;height:60px}
.brand{display:flex;align-items:center;gap:10px;font-weight:600;font-size:14px}
.brand .sub{color:var(--muted);font-weight:500}
.topbar nav{display:flex;gap:22px;font-size:13.5px;font-weight:500}
.topbar nav a{color:var(--ink-2)}
.topbar nav .pill{font-family:var(--mono);font-size:11.5px;background:var(--accent-soft);color:var(--accent-strong);padding:6px 10px;border-radius:99px;margin-left:8px}
.btn-print{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:12.5px;font-weight:600;color:#fff;background:var(--accent);border:1px solid var(--accent);padding:9px 14px;border-radius:var(--radius-sm);cursor:pointer;transition:background .15s}
.btn-print:hover{background:var(--accent-strong)}
.hero{padding:72px 0 44px;background:linear-gradient(180deg,var(--bg-soft) 0%,var(--bg) 100%);border-bottom:1px solid var(--line)}
.eyebrow{font-family:var(--mono);font-size:12px;font-weight:600;letter-spacing:1.6px;text-transform:uppercase;color:var(--accent);display:flex;align-items:center;gap:10px}
.eyebrow::before{content:"";width:26px;height:1.5px;background:var(--accent)}
.hero h1{font-size:clamp(30px,4.4vw,50px);line-height:1.08;letter-spacing:-1.2px;font-weight:700;margin:18px 0;max-width:820px}
.hero h1 em{font-style:normal;color:var(--accent)}
.hero p.lead{font-size:17.5px;color:var(--ink-2);max-width:780px}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:34px;max-width:620px}
.stat{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:18px 20px;box-shadow:var(--shadow-card)}
.stat .n{font-family:var(--mono);font-size:34px;font-weight:600;letter-spacing:-1px;color:var(--accent)}
.stat .l{font-size:12.5px;color:var(--muted);margin-top:2px}
.drivers{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px}
.drivers span{font-family:var(--mono);font-size:12.5px;color:var(--ink-2);border:1px solid var(--line-strong);background:#fff;padding:8px 13px;border-radius:99px}
.hero-cta{margin-top:30px;display:flex;gap:12px;flex-wrap:wrap}
.cta{display:inline-flex;align-items:center;gap:8px;font-weight:600;font-size:14.5px;padding:12px 20px;border-radius:var(--radius-sm)}
.cta.primary{background:var(--accent);color:#fff}
.cta.primary:hover{background:var(--accent-strong);text-decoration:none}
.cta.ghost{border:1px solid var(--line-strong);color:var(--ink-2)}
.cta.ghost:hover{background:var(--bg-soft);text-decoration:none}
section{padding:64px 0}
.sec-head{margin-bottom:34px}
.sec-kicker{font-family:var(--mono);font-size:11.5px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:var(--accent)}
.sec-title{font-size:clamp(24px,3vw,34px);letter-spacing:-.6px;font-weight:700;margin-top:8px}
.sec-sub{color:var(--muted);margin-top:10px;max-width:760px;font-size:15.5px}
.callout{display:flex;gap:12px;align-items:flex-start;margin-top:22px;padding:16px 18px;background:var(--accent-soft);border:1px solid rgba(15,118,110,.25);border-radius:var(--radius-sm);font-size:14px;color:var(--ink-2)}
.callout.warn{background:#fff8ec;border-color:rgba(180,83,9,.3)}
.callout.warn svg{stroke:var(--warn)}
.callout svg{flex:none;margin-top:2px;stroke:var(--accent)}
.flowgrid{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-top:8px}
.flow{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:18px 16px;display:flex;flex-direction:column;gap:6px;box-shadow:var(--shadow-card)}
.flow .step{font-family:var(--mono);font-size:10px;font-weight:600;letter-spacing:1px;color:var(--accent)}
.flow .what{font-size:14.5px;font-weight:600;line-height:1.3}
.flow .why{font-size:12px;color:var(--muted);line-height:1.45}
.actors{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.actor{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:22px 20px;box-shadow:var(--shadow-card)}
.actor .icon{width:38px;height:38px;border-radius:10px;background:var(--accent-soft);display:flex;align-items:center;justify-content:center;margin-bottom:12px}
.actor h3{font-size:15.5px;font-weight:700}
.actor .role{font-size:11px;font-family:var(--mono);color:var(--accent-strong);margin-top:2px;letter-spacing:.8px}
.actor p{font-size:13px;color:var(--ink-2);margin-top:8px;line-height:1.5}
.epics{display:grid;grid-template-columns:repeat(5,1fr);gap:16px}
.epic{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:20px 18px;box-shadow:var(--shadow-card);display:flex;flex-direction:column;gap:10px;color:var(--ink);transition:border-color .15s,transform .15s}
.epic:hover{border-color:var(--accent);transform:translateY(-2px);text-decoration:none}
.epic .e-no{font-family:var(--mono);font-size:10.5px;font-weight:600;letter-spacing:1.2px;color:var(--muted)}
.epic h3{font-size:14.5px;font-weight:700;line-height:1.25}
.epic .hu-range{font-family:var(--mono);font-size:11px;color:var(--accent-strong);margin-top:auto}
.epic .issue{font-family:var(--mono);font-size:10px;color:var(--muted);border-top:1px solid var(--line);padding-top:8px}
.detail{display:grid;grid-template-columns:64px 1fr;gap:22px;padding:36px 0;border-top:1px solid var(--line)}
.detail .dnum{font-family:var(--mono);font-size:13px;font-weight:600;color:var(--accent-strong);padding-top:3px}
.detail h3{font-size:20px;letter-spacing:-.3px;font-weight:700}
.detail .dsub{font-family:var(--mono);font-size:12px;color:var(--muted);margin-top:3px}
.detail>p{margin-top:12px;font-size:15px;color:var(--ink-2);max-width:860px}
.hus{margin-top:20px;display:flex;flex-direction:column;gap:12px;max-width:900px}
.hu{background:#fff;border:1px solid var(--line);border-radius:var(--radius-sm);padding:16px 18px}
.hu-head{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.hu-id{font-family:var(--mono);font-size:12.5px;font-weight:600;color:var(--accent-strong)}
.pill-p0,.pill-p1{font-family:var(--mono);font-size:10px;font-weight:600;letter-spacing:.6px;padding:3px 8px;border-radius:99px}
.pill-p0{background:#e8f6ef;color:var(--ok);border:1px solid rgba(26,127,78,.25)}
.pill-p1{background:#fff8ec;color:var(--warn);border:1px solid rgba(180,83,9,.25)}
.pill-issue{font-family:var(--mono);font-size:10px;color:var(--muted);background:var(--bg-soft);padding:3px 8px;border-radius:6px;border:1px solid var(--line)}
.hu-narr{font-size:14px;color:var(--ink);margin-top:8px;line-height:1.5}
.hu-narr em{font-style:normal;color:var(--accent-strong);font-weight:600}
.hu-crit{margin:10px 0 0;padding:0;list-style:none;display:flex;flex-direction:column;gap:5px}
.hu-crit li{font-size:13px;color:var(--ink-2);padding-left:20px;position:relative;line-height:1.5}
.hu-crit li::before{content:"";position:absolute;left:2px;top:8px;width:6px;height:6px;border-radius:2px;background:var(--accent)}
.table-scroll{overflow-x:auto;border:1px solid var(--line);border-radius:var(--radius);background:#fff}
table.cmp{width:100%;border-collapse:collapse;min-width:760px}
table.cmp th,table.cmp td{padding:13px 16px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line);font-size:13.5px}
table.cmp thead th{font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:var(--muted);background:var(--bg-soft);position:sticky;top:60px;z-index:2}
table.cmp td.rowhead{font-family:var(--mono);font-size:11.5px;font-weight:600;color:var(--muted);background:var(--bg-soft);width:170px}
table.cmp tbody tr:last-child td{border-bottom:none}
table.cmp td .mono{font-size:12px;color:var(--ink-2)}
footer{border-top:1px solid var(--line);background:var(--bg-soft);padding:34px 0;font-size:13px;color:var(--muted)}
.foot{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
.reveal{opacity:0;transform:translateY(14px);transition:opacity .5s ease,transform .5s ease}
.reveal.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}.reveal{opacity:1;transform:none;transition:none}}
@media (max-width:1080px){.epics{grid-template-columns:repeat(3,1fr)}.flowgrid{grid-template-columns:repeat(3,1fr)}}
@media (max-width:980px){.actors{grid-template-columns:repeat(2,1fr)}.topbar nav{display:none}}
@media (max-width:640px){
 .hero{padding:52px 0 30px}section{padding:46px 0}
 .detail{grid-template-columns:1fr;gap:10px}
 .stats{grid-template-columns:repeat(3,1fr)}
 .epics{grid-template-columns:1fr 1fr}
 .flowgrid{grid-template-columns:1fr 1fr}
 .actors{grid-template-columns:1fr}
 .brand .sub{display:none}
}
@media print{
 @page{margin:14mm 12mm}
 body{font-size:11.5px}
 .topbar{position:static;backdrop-filter:none}
 .btn-print,.hero-cta,.topbar nav{display:none!important}
 .hero{padding:26px 0 14px;background:none}
 .reveal{opacity:1;transform:none}
 .epics{grid-template-columns:repeat(3,1fr)}
 .actors{grid-template-columns:repeat(2,1fr)}
 .flowgrid{grid-template-columns:repeat(5,1fr)}
 .flow,.actor,.hu{break-inside:avoid}
 .detail{padding:14px 0;break-inside:avoid}
 .table-scroll{overflow:visible}table.cmp{min-width:0}table.cmp thead th{position:static}
 footer{display:none}
 *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
"""

def esc(s):
    return H.escape(s, quote=False)

def hu_card(hid, pri, issue, actor, cap, valor, crits):
    pill = f'<span class="pill-p0">{pri}</span>' if pri == "P0" else f'<span class="pill-p1">{pri}</span>'
    lis = "\n".join(f"<li>{esc(c)}</li>" for c in crits)
    return f'''<div class="hu">
<div class="hu-head"><span class="hu-id">{hid}</span>{pill}<span class="pill-issue">{esc(issue)}</span></div>
<p class="hu-narr">Como <em>{esc(actor)}</em>, quiero <em>{esc(cap)}</em>, para {esc(valor)}.</p>
<ul class="hu-crit">
{lis}
</ul>
</div>'''

def epic_detail(no, title, desc, issue, hus):
    cards = "\n".join(hu_card(*h) for h in hus)
    return f'''<article class="detail reveal" id="e{no.lower()}">
<div class="dnum">{no}</div>
<div>
<h3>{esc(title)}</h3>
<div class="dsub">{esc(issue)} · {len(hus)} historias</div>
<p>{esc(desc)}</p>
<div class="hus">
{cards}
</div>
</div>
</article>'''

def epic_card(no, title, hus, issue):
    rng = f"HU-{hus[0][0].split('-')[1]} → HU-{hus[-1][0].split('-')[1]}"
    return f'''<a class="epic" href="#e{no.lower()}">
<span class="e-no">ÉPICA {no}</span>
<h3>{esc(title)}</h3>
<span class="hu-range">{rng}</span>
<span class="issue">{esc(issue)}</span>
</a>'''

def actor_card(name, role, desc, path):
    return f'''<article class="actor">
<div class="icon"><svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="#0f766e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{path}</svg></div>
<h3>{esc(name)}</h3>
<div class="role">{esc(role)}</div>
<p>{esc(desc)}</p>
</article>'''

def flow_card(i, what, why):
    return f'''<div class="flow"><span class="step">PASO {i}</span><span class="what">{esc(what)}</span><span class="why">{esc(why)}</span></div>'''

epics_cards = "\n".join(epic_card(e[0], e[1], e[4], e[3]) for e in EPICAS)
epics_detail = "\n\n".join(epic_detail(e[0], e[1], e[2], e[3], e[4]) for e in EPICAS)
actors_html = "\n".join(actor_card(*a) for a in ACTORS)
flow_html = "\n".join(flow_card(i+1, w, wh) for i, (w, wh) in enumerate(FLOW))
pend_rows = "\n".join(
    f'<tr><td>{esc(d)}</td><td><span class="mono">{esc(h)}</span></td><td>{esc(r)}</td></tr>'
    for d, h, r in PENDIENTES)
excl_lis = "\n".join(f"<li>{esc(x)}</li>" for x in EXCLUSIONES)

page = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EAG Ingenieros · Historias de Usuario del MVP</title>
<meta name="description" content="44 historias de usuario propuestas para el MVP de la plataforma de análisis de oportunidades de SECOP II de EAG Ingenieros S.A.S. 10 épicas funcionales, 2 roles iniciales. Versión 1.0 · 7 de septiembre de 2026.">
<meta property="og:title" content="EAG Ingenieros · Historias de Usuario del MVP">
<meta property="og:description" content="44 historias de usuario propuestas para el MVP de la plataforma de análisis de oportunidades de SECOP II de EAG Ingenieros S.A.S.">
<meta property="og:type" content="website">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cpath d='M16 2 28 9v14L16 30 4 23V9z' fill='%230f766e'/%3E%3Cpath d='M11 16.5l3.5 3.5L21 13' stroke='%23fff' stroke-width='2.5' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>

<header class="topbar">
  <div class="wrap topbar-inner">
    <div class="brand">
      <svg width="22" height="22" viewBox="0 0 32 32" aria-hidden="true"><path d="M16 2 28 9v14L16 30 4 23V9z" fill="#0f766e"/><path d="M11 16.5l3.5 3.5L21 13" stroke="#fff" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <span>EAG Ingenieros <span class="sub">· MVP · Historias de Usuario</span></span>
    </div>
    <nav aria-label="Secciones">
      <a href="#como-leer">Cómo leerlo</a>
      <a href="#flujo">Flujo</a>
      <a href="#epicas">Épicas <span class="pill">10</span></a>
      <a href="#detalle">Historias <span class="pill">44</span></a>
      <a href="#pendientes">Pendientes</a>
    </nav>
    <button class="btn-print" onclick="window.print()">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
      Exportar PDF
    </button>
  </div>
</header>

<main>
  <section class="hero">
    <div class="wrap">
      <div class="eyebrow">EAG Ingenieros S.A.S. · MVP · Versión 1.0 · 7 de septiembre de 2026</div>
      <h1>Historias de usuario del <em>MVP</em></h1>
      <p class="lead">Plataforma de apoyo al análisis de oportunidades de <strong>SECOP II</strong> para EAG Ingenieros S.A.S. Este documento es una <strong>propuesta del equipo</strong>: no demuestra aprobación empresarial, cobertura completa de SECOP, integración productiva ni mejoras medidas. Toda decisión final requiere revisión humana y validación de EAG.</p>
      <div class="stats" aria-label="Cifras del alcance">
        <div class="stat"><div class="n">44</div><div class="l">historias propuestas</div></div>
        <div class="stat"><div class="n">10</div><div class="l">épicas funcionales</div></div>
        <div class="stat"><div class="n">2</div><div class="l">roles iniciales</div></div>
      </div>
      <div class="drivers" aria-label="Base documental">
        <span>CONTEXTO.md</span>
        <span>CASO_DE_USO.md</span>
        <span>MATRIZ_DE_PERMISOS.md</span>
        <span>BACKLOG.md</span>
        <span>MVP-01 a MVP-14</span>
      </div>
      <div class="hero-cta">
        <a class="cta primary" href="#epicas">Ver las 10 épicas
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </a>
        <a class="cta ghost" href="#pendientes">Pendientes de validación</a>
      </div>
    </div>
  </section>

  <section id="como-leer">
    <div class="wrap">
      <div class="sec-head reveal">
        <div class="sec-kicker">1 · Cómo leer este documento</div>
        <h2 class="sec-title">Las historias describen el comportamiento necesario, no el estado actual</h2>
        <p class="sec-sub">Se agrupan por capacidad y se vinculan con las issues del backlog para facilitar planificación, pruebas y revisión. Formato: narrativa «Como [persona], quiero [capacidad], para [valor]» · criterios observables de aceptación o rechazo · prioridad P0 (imprescindible para un MVP seguro y defendible) o P1 (importante, configurable o aplazable) · trazabilidad con la issue del backlog.</p>
      </div>

      <div class="actors reveal">
{actors_html}
      </div>

      <div class="callout reveal">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 16v-5M12 8h.01"/></svg>
        <span><strong>Reglas transversales:</strong> una recomendación no sustituye la decisión humana y el MVP no postula ofertas automáticamente. La fuente del requisito y la evidencia empresarial se conservan por separado (documento, localizador, fragmento y versión). Ausente o desconocido no equivale a cero; evidencia insuficiente no equivale a cumplimiento ni incumplimiento probado. Los documentos y textos de licitación son contenido no confiable, nunca instrucciones para el sistema. Archivos, datos personales, secretos y documentos internos permanecen fuera de Git y de logs; las pruebas usan fixtures sintéticas o anonimizadas.</span>
      </div>
    </div>
  </section>

  <section id="flujo" style="background:var(--bg-soft);border-top:1px solid var(--line);border-bottom:1px solid var(--line)">
    <div class="wrap">
      <div class="sec-head reveal">
        <div class="sec-kicker">2 · Mapa del alcance</div>
        <h2 class="sec-title">Secuencia principal</h2>
        <p class="sec-sub">El recorrido de cada oportunidad dentro del MVP. Las capacidades operativas y de retención atraviesan todo el flujo; el piloto valida el resultado completo. Las dependencias del backlog siguen siendo obligatorias aunque una historia se lea de forma independiente.</p>
      </div>

      <div class="flowgrid reveal" aria-label="Secuencia principal del MVP">
{flow_html}
      </div>
    </div>
  </section>

  <section id="epicas">
    <div class="wrap">
      <div class="sec-head reveal">
        <div class="sec-kicker">2 · Mapa del alcance</div>
        <h2 class="sec-title">Las 10 épicas funcionales</h2>
        <p class="sec-sub">Cada épica agrupa historias de usuario y se vincula con las issues del backlog. Haz clic en una épica para ver sus historias.</p>
      </div>

      <div class="epics reveal">
{epics_cards}
      </div>
    </div>
  </section>

  <section id="detalle" style="background:var(--bg-soft);border-top:1px solid var(--line);border-bottom:1px solid var(--line)">
    <div class="wrap">
      <div class="sec-head reveal">
        <div class="sec-kicker">3 · Historias por épica</div>
        <h2 class="sec-title">Las 44 historias, épica por épica</h2>
        <p class="sec-sub">Cada historia incluye su narrativa, criterios de aceptación observables, prioridad y la issue del backlog que la implementa o valida.</p>
      </div>

{epics_detail}
    </div>
  </section>

  <section id="pendientes">
    <div class="wrap">
      <div class="sec-head reveal">
        <div class="sec-kicker">4 · Pendientes de validación con EAG</div>
        <h2 class="sec-title">Decisiones pendientes antes de comprometer el alcance</h2>
        <p class="sec-sub">Estas decisiones condicionan historias concretas. Cada una tiene un responsable propuesto.</p>
      </div>

      <div class="table-scroll reveal">
        <table class="cmp">
          <thead>
            <tr>
              <th scope="col">Decisión pendiente</th>
              <th scope="col">Impacto en historias</th>
              <th scope="col">Responsable propuesto</th>
            </tr>
          </thead>
          <tbody>
{pend_rows}
          </tbody>
        </table>
      </div>

      <div class="callout reveal">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 16v-5M12 8h.01"/></svg>
        <span><strong>Criterio de cierre del MVP:</strong> las 44 historias representan el alcance funcional considerado. Una historia solo puede darse por aceptada con pruebas reproducibles, revisión humana y dependencias técnicas aceptadas. Las historias del piloto no se completan con datos simulados; sin usuarios o muestra autorizada, permanecen pendientes.</span>
      </div>
    </div>
  </section>

  <section id="exclusiones" style="background:var(--bg-soft);border-top:1px solid var(--line)">
    <div class="wrap">
      <div class="sec-head reveal">
        <div class="sec-kicker">5 · Exclusiones explícitas</div>
        <h2 class="sec-title">Lo que este MVP no hace</h2>
        <p class="sec-sub">Límites declarados para evitar expectativas fuera de alcance.</p>
      </div>

      <div class="hu reveal" style="max-width:900px">
        <ul class="hu-crit" style="gap:9px">
{excl_lis}
        </ul>
      </div>

      <div class="callout warn reveal">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/></svg>
        <span><strong>Nota final:</strong> este documento debe revisarse con EAG antes de convertir las historias en compromiso de producto. Los estados de avance, integraciones y resultados del piloto se verifican por separado en las issues y evidencias de prueba.</span>
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap foot">
    <span>EAG Ingenieros S.A.S. · Historias de usuario del MVP · Versión 1.0 · 7 de septiembre de 2026</span>
    <span class="mono">riverosmejia/EAG-HU</span>
  </div>
</footer>

<script>
(function(){{
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var reveals = document.querySelectorAll(".reveal");
  if (reduce || !("IntersectionObserver" in window)) {{
    reveals.forEach(function(el){{ el.classList.add("in"); }});
  }} else {{
    var io = new IntersectionObserver(function(entries){{
      entries.forEach(function(e){{
        if (e.isIntersecting){{ e.target.classList.add("in"); io.unobserve(e.target); }}
      }});
    }}, {{threshold: 0.12, rootMargin: "0px 0px -40px 0px"}});
    reveals.forEach(function(el){{ io.observe(el); }});
  }}
}})();
</script>
</body>
</html>
'''

with open("/home/riveros/EAG-HU/index.html", "w", encoding="utf-8") as f:
    f.write(page)

# Verificación de integridad
import re
ids = re.findall(r'HU-\d+', page)
unique_hus = sorted(set(ids), key=lambda x: int(x.split("-")[1]))
print("HU únicas en el HTML:", len(unique_hus))
print("Primeras:", unique_hus[:3], "Últimas:", unique_hus[-3:])
assert len(unique_hus) == 44, "FALTAN HISTORIAS"
print("OK: 44/44 historias presentes")
