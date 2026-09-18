# -*- coding: utf-8 -*-
"""Genera index.html (landing propuesta) con el sistema de diseño Stripi-Inspired.

Mesh gradiente en el hero, Inter 300 con tracking negativo, indigo #533afd
como único CTA, pills, tnum, banda cream para interludios.
"""
import html as H
import os
from data_hus import EPICAS, PENDIENTES, EXCLUSIONES, FLOW, ACTORS
from data_plan import RESUMEN, STACK, DECISIONES_CRITICAS, FASES, META

OUT = os.path.dirname(os.path.abspath(__file__))


def esc(s):
    return H.escape(s, quote=False)


epic_map_rows = "\n".join(
    f"<tr><td class='rowhead tnum'>{e[0]}</td><td>{esc(e[1])}</td>"
    f"<td class='tnum'>HU-{e[4][0][0].split('-')[1]} → HU-{e[4][-1][0].split('-')[1]}</td>"
    f"<td class='tnum'>{esc(e[3])}</td><td class='tnum'>{len(e[4])}</td></tr>"
    for e in EPICAS)

pend_rows = "\n".join(
    f"<tr><td>{esc(d)}</td><td class='tnum'><code>{esc(h)}</code></td><td>{esc(r)}</td></tr>"
    for d, h, r in PENDIENTES)

excl_lis = "".join(f"<li>{esc(x)}</li>" for x in EXCLUSIONES)
flow_html = "".join(
    f"<li><strong>{esc(w)}</strong><span>— {esc(wh)}</span></li>"
    for w, wh in FLOW)
actors_html = "\n".join(
    f"<div class='actor'><h3>{esc(a[0])}</h3><span class='role'>{esc(a[1])}</span><p>{esc(a[2])}</p></div>"
    for a in ACTORS)

total_hus = sum(len(e[4]) for e in EPICAS)
ver, fecha = META

plan_lis = "".join(f"<li><strong>{esc(a)}:</strong> {esc(t)}</li>" for a, t in RESUMEN)
stack_pills = "".join(f'<span class="stat-pill">{esc(s)}</span>' for _c, _t, _d, s in STACK)
dec_cards_q = "".join(
    f'<div class="dec"><b><span class="tag">Crítica</span>{esc(d)} · {esc(ti)}</b>{esc(te)}</div>'
    for d, ti, te in DECISIONES_CRITICAS)
sem_q = "".join(
    f'<li><strong>{esc(cod)} · {esc(nom)}</strong><span>{esc(dur)} — {esc(det[:150])}</span></li>'
    for cod, nom, dur, det, _ent in FASES)

CSS = """
:root{
  --primary:#533afd;--primary-deep:#4434d4;--primary-press:#2e2b8c;--primary-soft:#665efd;
  --primary-subdued:#b9b9f9;--brand-dark:#1c1e54;
  --ink:#0d253d;--ink-2:#273951;--mute:#64748d;
  --canvas:#ffffff;--canvas-soft:#f6f9fc;--cream:#f5e9d4;
  --hairline:#e3e8ee;--hairline-input:#a8c3de;
  --ruby:#ea2261;--lemon:#9b6829;
  --shadow-1:rgba(0,55,112,.08) 0 1px 3px;
  --shadow-2:rgba(0,55,112,.08) 0 8px 24px, rgba(0,55,112,.04) 0 2px 6px;
  --sans:'Inter','SF Pro Display',system-ui,-apple-system,sans-serif;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:84px}
body{font-family:var(--sans);color:var(--ink);background:var(--canvas);font-weight:300;
  font-size:15px;line-height:1.5;font-feature-settings:"ss01";-webkit-font-smoothing:antialiased}
::selection{background:var(--primary-subdued)}
a{color:var(--primary);text-decoration:none}
a:hover{text-decoration:underline}
code{font-family:var(--sans);font-weight:400;font-size:.85em;background:var(--canvas-soft);
  border:1px solid var(--hairline);border-radius:4px;padding:1px 6px;color:var(--ink-2)}
strong{font-weight:500}
.wrap{max-width:1160px;margin:0 auto;padding:0 24px}
.tnum{font-feature-settings:"tnum";letter-spacing:-.2px}

/* ---------- Topbar sobre mesh ---------- */
.topbar{position:absolute;top:0;left:0;right:0;z-index:50}
.topbar-inner{display:flex;align-items:center;justify-content:space-between;gap:16px;height:64px}
.brand{display:flex;align-items:center;gap:10px;font-weight:400;font-size:14.5px;letter-spacing:-.2px;color:var(--ink)}
.brand .sub{color:var(--mute);font-weight:300}
.topbar nav{display:flex;gap:22px;font-size:14px;font-weight:300}
.topbar nav a{color:var(--ink-2)}
.btn-pill{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:400;color:#fff;
  background:var(--primary);border:none;padding:8px 16px;border-radius:9999px;cursor:pointer;transition:background .15s}
.btn-pill:hover{background:var(--primary-deep)}
.btn-pill:active{background:var(--primary-press)}
.btn-pill.ghost{background:var(--canvas);color:var(--primary);border:1px solid var(--primary)}
.btn-pill.ghost:hover{background:var(--canvas-soft)}
.btn-pill.dark{background:var(--brand-dark)}
.btn-pill.dark:hover{background:#16183f}

/* ---------- Mesh hero ---------- */
.hero{position:relative;padding:132px 0 72px;overflow:hidden}
.hero::before{content:"";position:absolute;inset:0;z-index:-1;
  background:
    radial-gradient(42% 100% at 3% 45%, rgba(245,233,212,.95), transparent 60%),
    radial-gradient(38% 90% at 24% 25%, rgba(249,150,80,.4), transparent 62%),
    radial-gradient(44% 100% at 50% 40%, rgba(178,132,255,.45), transparent 65%),
    radial-gradient(50% 115% at 77% 30%, rgba(83,58,253,.7), transparent 65%),
    radial-gradient(36% 90% at 100% 50%, rgba(234,34,97,.5), transparent 60%);
  filter:blur(4px)}
.hero::after{content:"";position:absolute;left:0;right:0;bottom:0;height:120px;z-index:-1;
  background:linear-gradient(180deg,transparent,var(--canvas))}
.eyebrow{font-size:10px;font-weight:400;letter-spacing:.1px;text-transform:uppercase;
  color:var(--primary-deep);background:var(--canvas);display:inline-flex;padding:4px 10px;border-radius:9999px;
  border:1px solid var(--hairline);box-shadow:var(--shadow-1)}
.hero h1{font-size:56px;font-weight:300;line-height:1.03;letter-spacing:-1.4px;margin:20px 0 18px;max-width:820px}
.hero h1 em{font-style:normal;color:var(--primary)}
.hero p.lead{font-size:16px;color:var(--ink-2);max-width:740px;line-height:1.45}
.stat-row{display:flex;gap:8px;margin-top:26px;flex-wrap:wrap}
.stat-pill{background:var(--canvas);border:1px solid var(--hairline);border-radius:9999px;
  padding:8px 16px;font-size:14px;color:var(--ink-2);box-shadow:var(--shadow-1);font-feature-settings:"tnum"}
.stat-pill b{color:var(--primary-deep);font-weight:500;font-size:16px}
.hero-note{margin:1.1rem 0 0;max-width:62ch;padding:.95rem 1.15rem;border-radius:12px;
  background:rgba(255,255,255,.72);border:1px solid rgba(83,58,253,.18);
  font-size:.9rem;line-height:1.6;color:var(--ink-2)}
.hero-cta{margin-top:30px;display:flex;gap:10px;flex-wrap:wrap}

/* ---------- Secciones ---------- */
section{padding:64px 0}
.band-soft{background:var(--canvas-soft)}
.band-cream{background:var(--cream)}
.sec-head{margin-bottom:34px}
.sec-kicker{font-size:10px;font-weight:400;letter-spacing:.1px;text-transform:uppercase;color:var(--primary-deep);
  background:var(--primary-subdued);display:inline-flex;padding:3px 10px;border-radius:9999px;margin-bottom:12px}
.sec-title{font-size:32px;font-weight:300;letter-spacing:-.64px;line-height:1.1}
.sec-sub{color:var(--mute);margin-top:10px;max-width:720px;font-size:15px}

/* ---------- Actores ---------- */
.actors{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.actor{background:var(--canvas);border:1px solid var(--hairline);border-radius:12px;padding:28px;box-shadow:var(--shadow-1)}
.actor h3{font-size:20px;font-weight:300;letter-spacing:-.2px}
.actor .role{display:inline-block;font-size:10px;font-weight:400;letter-spacing:.1px;text-transform:uppercase;
  color:var(--primary-deep);background:var(--primary-subdued);border-radius:9999px;padding:3px 8px;margin:8px 0}
.actor p{font-size:14px;color:var(--ink-2);line-height:1.45}

/* ---------- Flow ---------- */
ol.flow{list-style:none;counter-reset:paso;columns:2;column-gap:48px;margin-top:8px}
ol.flow li{counter-increment:paso;position:relative;padding:9px 0 9px 46px;border-bottom:1px solid var(--hairline);
  break-inside:avoid;font-size:14.5px;color:var(--ink-2)}
ol.flow li::before{content:counter(paso,decimal-leading-zero);position:absolute;left:0;top:9px;width:30px;height:30px;
  border-radius:9999px;background:var(--brand-dark);color:#fff;font-size:10px;font-weight:400;font-feature-settings:"tnum";
  display:flex;align-items:center;justify-content:center}
ol.flow strong{display:inline;color:var(--ink);font-weight:500}
ol.flow span{display:block;font-size:13px;color:var(--mute)}

/* ---------- Mapa épicas ---------- */
.tbl-wrap{overflow-x:auto;border:1px solid var(--hairline);border-radius:12px;background:var(--canvas);box-shadow:var(--shadow-1)}
table.doc-t{width:100%;border-collapse:collapse;font-size:14px;font-weight:300;min-width:720px}
table.doc-t th,table.doc-t td{padding:12px 16px;text-align:left;vertical-align:top;border-bottom:1px solid var(--hairline)}
table.doc-t thead th{font-size:10px;font-weight:400;letter-spacing:.1px;text-transform:uppercase;color:var(--mute);background:var(--canvas-soft)}
table.doc-t tbody tr:last-child td{border-bottom:none}
table.doc-t td.rowhead{font-weight:400;color:var(--primary-deep);background:var(--canvas-soft);white-space:nowrap}
table.doc-t td.tnum{font-feature-settings:"tnum";letter-spacing:-.2px}
table.doc-t td a{font-weight:400}
.callout{display:flex;gap:12px;align-items:flex-start;margin-top:20px;padding:16px 18px;border-radius:12px;
  font-size:14px;line-height:1.5;border:1px solid var(--hairline)}
.callout svg{width:18px;height:18px;flex:none;margin-top:2px}
.callout.note{background:var(--canvas-soft);color:var(--ink-2)}
.callout.note svg{stroke:var(--primary)}
.callout.cream{background:var(--cream);color:var(--ink)}
.callout.cream svg{stroke:var(--lemon)}
.callout.warn{background:var(--canvas);color:var(--ink-2);border-color:var(--hairline)}
.callout.warn svg{stroke:var(--lemon)}

/* ---------- Plan (versión rápida) ---------- */
.stack-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.dec-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin-top:16px}
.dec{background:var(--canvas);border:1px solid var(--hairline);border-radius:12px;padding:18px;
  box-shadow:var(--shadow-1);font-size:13.5px;line-height:1.48;color:var(--ink-2)}
.dec b{display:block;color:var(--primary-deep);font-weight:500;font-size:13px;margin-bottom:6px;letter-spacing:-.1px}
.dec .tag{display:inline-block;font-size:10px;font-weight:400;letter-spacing:.1px;text-transform:uppercase;
  color:var(--primary-deep);background:var(--primary-subdued);border-radius:9999px;padding:2px 8px;margin-right:6px;vertical-align:1px}

/* ---------- Footer ---------- */
footer{background:var(--canvas);border-top:1px solid var(--hairline);padding:64px 0;font-size:13px;color:var(--mute)}
.foot{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
.foot a{color:var(--mute)}
.foot a:hover{color:var(--primary)}

.reveal{opacity:0;transform:translateY(14px);transition:opacity .5s ease,transform .5s ease}
.reveal.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}.reveal{opacity:1;transform:none;transition:none}}

@media (max-width:960px){
  .topbar nav{display:none}
  .hero{padding:104px 0 56px}
  .hero h1{font-size:40px;letter-spacing:-1px}
  .actors{grid-template-columns:repeat(2,1fr)}
  ol.flow{columns:1}
}
@media (max-width:640px){
  .hero h1{font-size:34px;letter-spacing:-.8px}
  section{padding:46px 0}
  .actors{grid-template-columns:1fr}
}
@media print{
  .topbar,.hero-cta,.topbar nav{display:none!important}
  .hero{padding:26px 0 14px}
  .hero::before,.hero::after{display:none}
  .reveal{opacity:1;transform:none}
  .actors{grid-template-columns:repeat(2,1fr)}
  ol.flow{columns:2}
  .hu,.adm,.tbl-wrap,.actor{break-inside:avoid;box-shadow:none}
  section{padding:18px 0}
  footer{display:none}
  *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
"""

page = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EAG Ingenieros · MVP · Plan de acción e Historias de Usuario</title>
<meta name="description" content="Plan de acción (12 semanas) e {total_hus} historias de usuario propuestas para el MVP de la plataforma de análisis de oportunidades de SECOP II de EAG Ingenieros S.A.S. {len(EPICAS)} épicas funcionales. Versión {ver} · {fecha}.">
<meta property="og:title" content="EAG Ingenieros · MVP · Plan de acción e Historias de Usuario">
<meta property="og:description" content="Plan de acción (12 semanas) e {total_hus} historias de usuario propuestas para el MVP de la plataforma de análisis de oportunidades de SECOP II de EAG Ingenieros S.A.S.">
<meta property="og:type" content="website">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cpath d='M16 2 30 10v12L16 30 2 22V10z' fill='%23533afd'/%3E%3Cpath d='M11 16.5l3.5 3.5L21 13' stroke='%23fff' stroke-width='2.5' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>

<header class="topbar">
  <div class="wrap topbar-inner">
    <div class="brand">
      <svg width="24" height="24" viewBox="0 0 32 32" aria-hidden="true"><path d="M16 2 30 10v12L16 30 2 22V10z" fill="#533afd"/><path d="M11 16.5l3.5 3.5L21 13" stroke="#fff" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <span>EAG Ingenieros <span class="sub">· MVP · Historias de Usuario</span></span>
    </div>
    <nav aria-label="Secciones">
      <a href="#como-leer">Cómo leerlo</a>
      <a href="#flujo">Flujo</a>
      <a href="#plan">Plan</a>
      <a href="#mapa">Épicas</a>
      <a href="#pendientes">Pendientes</a>
      <a href="docs/" style="color:var(--primary);font-weight:400">Documentación →</a>
    </nav>
    <a class="btn-pill" href="docs/">Ver documentación</a>
  </div>
</header>

<main>
  <section class="hero">
    <div class="wrap">
      <div class="eyebrow">EAG Ingenieros S.A.S. · MVP · Versión {ver} · {fecha}</div>
      <h1>Plan de acción e historias de usuario del <em>MVP</em></h1>
      <p class="lead">Plataforma de apoyo al análisis de oportunidades de <strong>SECOP II</strong> para EAG Ingenieros S.A.S. Una aplicación web que consulta oportunidades reales, reúne y procesa sus documentos, extrae los requisitos con IA validando cada cita contra el texto fuente, los compara con el perfil de la empresa y produce un borrador que una persona revisa y aprueba antes del informe.</p>
      <div class="hero-note">
        <strong>El proyecto no depende de entregables de EAG.</strong> Se construye con datos públicos reales de SECOP II, base de datos propia y perfil empresarial cargable desde la plataforma. Cada pregunta sin responder tiene una respuesta provisional del equipo, marcada como tal.
      </div>
      <div class="stat-row">
        <span class="stat-pill"><b>{len(FASES)}</b> fases de trabajo</span>
        <span class="stat-pill"><b>{total_hus}</b> historias propuestas</span>
        <span class="stat-pill"><b>{len(EPICAS)}</b> épicas funcionales</span>
        <span class="stat-pill"><b>2</b> roles iniciales</span>
      </div>
      <div class="hero-cta">
        <a class="btn-pill" href="#mapa">Explorar el mapa de épicas</a>
        <a class="btn-pill ghost" href="docs/">Versión documentación</a>
      </div>
    </div>
  </section>

  <section id="plan">
    <div class="wrap">
      <div class="sec-head reveal">
        <div class="sec-kicker">01 · Plan de acción</div>
        <h2 class="sec-title">12 semanas para un MVP defendible</h2>
        <p class="sec-sub">Plan de implementación con las decisiones adoptadas en la auditoría técnica del 10 de septiembre de 2026: resuelve inconsistencias del plan original y los riesgos de costo, cobertura y dependencias. Sujeto a validación de EAG.</p>
      </div>
      <div class="callout note reveal">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 16v-5M12 8h.01"/></svg>
        <span><strong>En una frase:</strong> {esc(RESUMEN[0][1])}</span>
      </div>
      <div class="dec-grid reveal">
{dec_cards_q}
      </div>
      <div class="sec-head reveal" style="margin-top:34px">
        <h2 class="sec-title" style="font-size:24px">Stack</h2>
      </div>
      <div class="stack-row reveal">{stack_pills}</div>
      <div class="sec-head reveal" style="margin-top:34px">
        <h2 class="sec-title" style="font-size:24px">Cadencia por semanas</h2>
      </div>
      <ol class="flow reveal">{sem_q}</ol>
      <div class="hero-cta reveal" style="margin-top:22px">
        <a class="btn-pill" href="docs/#plan">Ver el plan detallado →</a>
        <a class="btn-pill ghost" href="docs/">Versión documentación completa</a>
      </div>
    </div>
  </section>

  <section id="como-leer" class="band-soft">
    <div class="wrap">
      <div class="sec-head reveal">
        <div class="sec-kicker">02 · Cómo leer este documento</div>
        <h2 class="sec-title">Comportamiento necesario, no estado actual</h2>
        <p class="sec-sub">Las historias se agrupan por capacidad y se vinculan con las issues del backlog para facilitar planificación, pruebas y revisión. Formato: narrativa «Como [persona], quiero [capacidad], para [valor]» · criterios observables · prioridad P0 (imprescindible) o P1 (configurable o aplazable) · trazabilidad con la issue.</p>
      </div>
      <div class="actors reveal">
{actors_html}
      </div>
      <div class="callout note reveal">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 16v-5M12 8h.01"/></svg>
        <span><strong>Reglas transversales:</strong> una recomendación no sustituye la decisión humana y el MVP no postula ofertas automáticamente. La fuente del requisito y la evidencia empresarial se conservan por separado (documento, localizador, fragmento y versión). Ausente o desconocido no equivale a cero. Los documentos y textos de licitación son contenido no confiable, nunca instrucciones para el sistema. Archivos, datos personales, secretos y documentos internos permanecen fuera de Git y de logs.</span>
      </div>
    </div>
  </section>

  <section id="flujo">
    <div class="wrap">
      <div class="sec-head reveal">
        <div class="sec-kicker">03 · Mapa del alcance</div>
        <h2 class="sec-title">Secuencia principal</h2>
        <p class="sec-sub">El recorrido de cada oportunidad dentro del MVP. Las capacidades operativas y de retención atraviesan todo el flujo; el piloto valida el resultado completo.</p>
      </div>
      <ol class="flow reveal">{flow_html}</ol>
    </div>
  </section>

  <section id="mapa" class="band-soft">
    <div class="wrap">
      <div class="sec-head reveal">
        <div class="sec-kicker">04 · Mapa de épicas</div>
        <h2 class="sec-title">Las {len(EPICAS)} épicas funcionales</h2>
        <p class="sec-sub">Cada épica agrupa historias y se vincula con las issues del backlog. El detalle completo de las {total_hus} historias está en la versión documentación.</p>
      </div>
      <div class="tbl-wrap reveal">
        <table class="doc-t">
          <thead><tr><th>Épica</th><th>Capacidad</th><th>Historias</th><th>Issues</th><th>Cant.</th></tr></thead>
          <tbody>
{epic_map_rows}
          </tbody>
        </table>
      </div>
      <div class="hero-cta reveal" style="margin-top:22px">
        <a class="btn-pill dark" href="docs/">Ver las {total_hus} historias completas</a>
      </div>
    </div>
  </section>

  <section id="pendientes" class="band-cream">
    <div class="wrap">
      <div class="sec-head reveal">
        <div class="sec-kicker">05 · Pendientes de validación</div>
        <h2 class="sec-title">Decisiones antes de comprometer el alcance</h2>
        <p class="sec-sub">Estas decisiones condicionan historias concretas. Cada una tiene un responsable propuesto.</p>
      </div>
      <div class="tbl-wrap reveal">
        <table class="doc-t">
          <thead><tr><th>Decisión pendiente</th><th>Impacto en historias</th><th>Responsable propuesto</th></tr></thead>
          <tbody>
{pend_rows}
          </tbody>
        </table>
      </div>
      <div class="callout note reveal">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 16v-5M12 8h.01"/></svg>
        <span><strong>Criterio de cierre del MVP:</strong> las {total_hus} historias representan el alcance funcional considerado. Una historia solo puede darse por aceptada con pruebas reproducibles, revisión humana y dependencias técnicas aceptadas. Las historias del piloto no se completan con datos simulados; sin usuarios o muestra autorizada, permanecen pendientes.</span>
      </div>
    </div>
  </section>

  <section id="exclusiones">
    <div class="wrap">
      <div class="sec-head reveal">
        <div class="sec-kicker">06 · Exclusiones explícitas</div>
        <h2 class="sec-title">Lo que este MVP no hace</h2>
        <p class="sec-sub">Límites declarados para evitar expectativas fuera de alcance.</p>
      </div>
      <div class="tbl-wrap reveal" style="padding:24px 28px">
        <ul style="list-style:none;display:flex;flex-direction:column;gap:9px">
{excl_lis}
        </ul>
      </div>
      <div class="callout warn reveal">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/></svg>
        <span><strong>Nota final:</strong> este documento debe revisarse con EAG antes de convertir las historias en compromiso de producto. Los estados de avance, integraciones y resultados del piloto se verifican por separado en las issues y evidencias de prueba.</span>
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap foot">
    <span>EAG Ingenieros S.A.S. · Plan de acción e historias de usuario del MVP · Versión {ver} · {fecha}</span>
    <span class="tnum"><a href="https://github.com/riverosmejia/EAG-HU">riverosmejia/EAG-HU</a> · <a href="docs/">documentación</a></span>
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

with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(page)

import re
hus = sorted(set(re.findall(r"HU-\d+", page)), key=lambda x: int(x.split("-")[1]))
print("index.html generado:", os.path.getsize(os.path.join(OUT, "index.html")), "bytes")
print("HUs referenciadas en mapa:", len(set(hus)))
