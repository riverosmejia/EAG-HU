# -*- coding: utf-8 -*-
"""Genera index.html para EAG-HU: 44 HUs del MVP de EAG Ingenieros (SECOP II)."""
import html as H

# (id, prioridad, issue, actor, capacidad, valor, [criterios])
from data_hus import EPICAS, PENDIENTES, EXCLUSIONES, FLOW, ACTORS

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
