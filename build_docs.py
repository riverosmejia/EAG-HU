# -*- coding: utf-8 -*-
"""Genera docs/index.html: versión documentación del documento de HUs de EAG.

Diseño de documentación técnica (estilo mkdocs/material): sidebar fija con
navegación jerárquica, buscador en vivo, scrollspy, admoniciones, contenido
en columna de lectura. Distinto del diseño de propuesta (build_page.py).
"""
import html as H
import os
from data_hus import EPICAS, PENDIENTES, EXCLUSIONES, FLOW, ACTORS

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
os.makedirs(OUT, exist_ok=True)


def esc(s):
    return H.escape(s, quote=False)


# ---------- Nav tree (sidebar) ----------
# items: (id_anchor, label, children:[(anchor,label)])
nav = []
nav.append(("como-leer", "Cómo leer este documento", []))
nav.append(("actores", "Actores y responsabilidades", []))
nav.append(("reglas", "Reglas transversales", []))
nav.append(("flujo", "Secuencia principal", []))
nav.append(("mapa", "Mapa de épicas", []))
for e in EPICAS:
    code, title, _, _, hus = e
    kids = [(f"{h[0].lower()}", h[0]) for h in hus]
    nav.append((f"e{code.lower()}", f"{code} · {title}", kids))
nav.append(("pendientes", "Pendientes de validación", []))
nav.append(("cierre", "Criterio de cierre", []))
nav.append(("exclusiones", "Exclusiones explícitas", []))

nav_html = ""
for anchor, label, kids in nav:
    k = ""
    if kids:
        k = "<ul class='subnav'>" + "".join(
            f"<li><a href='#{a}' data-nav>{l}</a></li>" for a, l in kids
        ) + "</ul>"
    nav_html += f"<li class='nav-item'><a href='#{anchor}' data-nav>{esc(label)}</a>{k}</li>\n"

# ---------- Admonition helper ----------
def admon(kind, title, body):
    icons = {
        "note": '<circle cx="12" cy="12" r="9"/><path d="M12 16v-5M12 8h.01"/>',
        "warning": '<path d="M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>',
    }
    return f'''<div class="adm adm-{kind}">
<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{icons[kind]}</svg>
<div><p class="adm-title">{title}</p>{body}</div>
</div>'''


# ---------- HU section (documento, no card) ----------
def hu_section(hid, pri, issue, actor, cap, valor, crits):
    pill = f'<span class="pri pri-{pri.lower()}">{pri}</span>'
    lis = "".join(f"<li>{esc(c)}</li>" for c in crits)
    return f'''<article class="hu" id="{hid.lower()}">
<h4><span class="hu-id">{hid}</span>{pill}<span class="issue-tag">{esc(issue)}</span></h4>
<p class="narr">Como <strong>{esc(actor)}</strong>, quiero <strong>{esc(cap)}</strong>, para {esc(valor)}.</p>
<h5>Criterios de aceptación</h5>
<ul class="crit">{lis}</ul>
</article>'''


# ---------- Épica section ----------
def epic_section(e):
    code, title, desc, issues, hus = e
    hus_html = "\n".join(hu_section(*h) for h in hus)
    return f'''<section class="epic-sec" id="e{code.lower()}">
<h2><span class="epic-code">{code}</span>{esc(title)}</h2>
<p class="epic-desc">{esc(desc)}</p>
<p class="epic-issues">Trazabilidad: <code>{esc(issues)}</code> · {len(hus)} historias</p>
{hus_html}
</section>'''


actors_rows = "\n".join(
    f"<tr><td class='rowhead'>{esc(a[0])}</td><td>{esc(a[2])}</td></tr>" for a in ACTORS)
flow_ol = "".join(f"<li><strong>{esc(w)}</strong> — {esc(wh)}</li>" for w, wh in FLOW)
epic_map_rows = "\n".join(
    f"<tr><td class='rowhead'>{e[0]}</td><td>{esc(e[1])}</td>"
    f"<td><code>HU-{e[4][0][0].split('-')[1]} a HU-{e[4][-1][0].split('-')[1]}</code></td>"
    f"<td><code>{esc(e[3])}</code></td></tr>"
    for e in EPICAS)
pend_rows = "\n".join(
    f"<tr><td>{esc(d)}</td><td><code>{esc(h)}</code></td><td>{esc(r)}</td></tr>"
    for d, h, r in PENDIENTES)
excl_lis = "".join(f"<li>{esc(x)}</li>" for x in EXCLUSIONES)
epics_html = "\n".join(epic_section(e) for e in EPICAS)

total_hus = sum(len(e[4]) for e in EPICAS)

CSS = """
:root{
  --bg:#fff;--bg-page:#fafbfb;--ink:#1a2623;--ink-2:#3d4c48;--muted:#6b7a75;
  --line:#e5e9e8;--line-2:#d3dbd9;--accent:#0f766e;--accent-strong:#0b5e58;--accent-soft:#e9f4f2;
  --ok:#1a7f4e;--warn:#b45309;--warn-soft:#fdf3e3;--warn-line:#ecd9b5;
  --mono:'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
  --sans:'IBM Plex Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  --sidebar-w:292px;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:24px}
body{font-family:var(--sans);color:var(--ink);background:var(--bg-page);font-size:15.5px;line-height:1.65;-webkit-font-smoothing:antialiased}
::selection{background:var(--accent-soft)}
a{color:var(--accent-strong);text-decoration:none}
a:hover{text-decoration:underline}
code{font-family:var(--mono);font-size:.85em;background:#f0f3f2;border:1px solid var(--line);border-radius:5px;padding:1px 6px;color:var(--ink-2)}
strong{font-weight:600}

/* ---------- Sidebar ---------- */
.sidebar{position:fixed;top:0;left:0;bottom:0;width:var(--sidebar-w);background:#fff;border-right:1px solid var(--line);
  display:flex;flex-direction:column;z-index:40;transition:transform .22s ease}
.side-brand{display:flex;align-items:center;gap:10px;padding:18px 20px 14px;border-bottom:1px solid var(--line)}
.side-brand svg{flex:none}
.side-brand .t{font-weight:700;font-size:14.5px;line-height:1.25}
.side-brand .v{font-family:var(--mono);font-size:10.5px;color:var(--muted);display:block;margin-top:2px}
.side-search{padding:14px 16px;border-bottom:1px solid var(--line)}
.side-search input{width:100%;font-family:var(--sans);font-size:13.5px;padding:9px 12px;border:1px solid var(--line-2);
  border-radius:8px;background:var(--bg-page);color:var(--ink);outline:none;transition:border-color .15s,box-shadow .15s}
.side-search input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(15,118,110,.15)}
.side-search .nores{display:none;font-size:12px;color:var(--muted);padding:8px 4px 0}
.side-nav{flex:1;overflow-y:auto;padding:12px 8px 24px}
.side-nav>ul{list-style:none}
.nav-item>a{display:block;padding:7px 12px;border-radius:7px;font-size:13.5px;font-weight:500;color:var(--ink-2);line-height:1.35}
.nav-item>a:hover{background:var(--bg-page);text-decoration:none;color:var(--accent-strong)}
.nav-item>a.active{background:var(--accent-soft);color:var(--accent-strong);font-weight:600}
.subnav{list-style:none;margin:2px 0 6px;padding-left:14px;border-left:2px solid var(--line)}
.subnav a{display:block;padding:4px 12px;font-family:var(--mono);font-size:11.5px;color:var(--muted);border-radius:6px}
.subnav a:hover{text-decoration:none;color:var(--accent-strong);background:var(--bg-page)}
.subnav a.active{color:var(--accent-strong);font-weight:600}
.side-foot{padding:12px 20px;border-top:1px solid var(--line);font-family:var(--mono);font-size:10.5px;color:var(--muted)}

/* ---------- Content ---------- */
.content{margin-left:var(--sidebar-w)}
.doc{max-width:820px;margin:0 auto;padding:48px 40px 96px}
h1{font-size:30px;letter-spacing:-.5px;font-weight:700;line-height:1.15;margin-bottom:6px}
h2{font-size:22px;letter-spacing:-.3px;font-weight:700;margin:0 0 4px}
h3{font-size:17px;font-weight:700;margin:36px 0 10px;scroll-margin-top:24px}
h4{font-size:15px;font-weight:600;margin:26px 0 8px}
h5{font-family:var(--mono);font-size:10.5px;font-weight:600;letter-spacing:1.2px;text-transform:uppercase;color:var(--muted);margin:12px 0 6px}
.doc-header{border-bottom:1px solid var(--line);padding-bottom:22px;margin-bottom:28px}
.doc-header .kicker{font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:var(--accent);margin-bottom:10px}
.doc-header .meta{font-family:var(--mono);font-size:12px;color:var(--muted);margin-top:10px}
.doc-header .lead{color:var(--ink-2);margin-top:12px;font-size:15.5px}
.doc>section{margin:38px 0}
.doc>section>h2{scroll-margin-top:24px}
.sec-kicker{font-family:var(--mono);font-size:10.5px;font-weight:600;letter-spacing:1.4px;text-transform:uppercase;color:var(--accent);margin-bottom:6px}
.section-sub{color:var(--muted);font-size:14px;margin-bottom:16px}

/* ---------- Admonitions ---------- */
.adm{display:flex;gap:12px;padding:14px 16px;border-radius:10px;margin:16px 0;font-size:14px;line-height:1.55;border:1px solid}
.adm svg{width:18px;height:18px;flex:none;margin-top:2px}
.adm .adm-title{font-weight:600;margin-bottom:2px}
.adm-note{background:var(--accent-soft);border-color:rgba(15,118,110,.22);color:var(--ink-2)}
.adm-note svg{stroke:var(--accent)}
.adm-warning{background:var(--warn-soft);border-color:var(--warn-line);color:#6d4a12}
.adm-warning svg{stroke:var(--warn)}

/* ---------- Tables ---------- */
.tbl-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:#fff;margin:16px 0}
table.doc-t{width:100%;border-collapse:collapse;font-size:13.5px}
table.doc-t th,table.doc-t td{padding:11px 14px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}
table.doc-t thead th{font-family:var(--mono);font-size:10.5px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:var(--muted);background:var(--bg-page)}
table.doc-t tbody tr:last-child td{border-bottom:none}
table.doc-t td.rowhead{font-family:var(--mono);font-size:12px;font-weight:600;color:var(--ink-2);background:var(--bg-page);white-space:nowrap}

/* ---------- Flow (secuencia) ---------- */
ol.flow{list-style:none;counter-reset:paso;margin:14px 0}
ol.flow li{counter-increment:paso;position:relative;padding:8px 0 8px 44px;border-left:2px solid var(--line);margin-left:14px;font-size:14px;color:var(--ink-2)}
ol.flow li::before{content:counter(paso,decimal-leading-zero);position:absolute;left:-14px;top:6px;width:28px;height:28px;border-radius:50%;
  background:var(--accent);color:#fff;font-family:var(--mono);font-size:10.5px;font-weight:600;display:flex;align-items:center;justify-content:center}
ol.flow li:last-child{border-left-color:transparent}
ol.flow strong{color:var(--ink)}

/* ---------- Épicas ---------- */
.epic-sec{border-top:1px solid var(--line);padding-top:30px;margin-top:34px}
.epic-code{font-family:var(--mono);font-size:12px;font-weight:600;color:#fff;background:var(--accent);border-radius:7px;padding:3px 9px;margin-right:10px;vertical-align:3px}
.epic-desc{color:var(--ink-2);margin:6px 0 4px}
.epic-issues{font-family:var(--mono);font-size:12px;color:var(--muted);margin-bottom:8px}
.epic-sec{scroll-margin-top:24px}

/* ---------- HU ---------- */
.hu{background:#fff;border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:14px 0;scroll-margin-top:24px}
.hu h4{margin:0 0 8px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.hu-id{font-family:var(--mono);font-size:14px;font-weight:600;color:var(--accent-strong)}
.pri{font-family:var(--mono);font-size:10px;font-weight:600;padding:2px 8px;border-radius:99px}
.pri-p0{background:#e6f3ec;color:var(--ok);border:1px solid rgba(26,127,78,.3)}
.pri-p1{background:var(--warn-soft);color:var(--warn);border:1px solid var(--warn-line)}
.issue-tag{font-family:var(--mono);font-size:10px;color:var(--muted);border:1px solid var(--line);border-radius:6px;padding:2px 7px;background:var(--bg-page)}
.narr{font-size:14.5px;color:var(--ink)}
.narr strong{color:var(--accent-strong);font-weight:600}
.crit{list-style:none;margin-top:6px}
.crit li{font-size:13.5px;color:var(--ink-2);padding-left:20px;position:relative;margin-bottom:5px;line-height:1.55}
.crit li::before{content:"";position:absolute;left:2px;top:8px;width:6px;height:6px;border-radius:2px;background:var(--accent)}
mark{background:#fdeeb8;border-radius:3px;padding:0 2px}

/* ---------- Back to top / mobile ---------- */
.top-link{font-family:var(--mono);font-size:11px;position:static}
.menu-btn{display:none;position:fixed;bottom:18px;right:18px;z-index:60;width:48px;height:48px;border-radius:50%;border:1px solid var(--line-2);
  background:var(--accent);color:#fff;cursor:pointer;box-shadow:0 8px 22px rgba(15,118,110,.4);align-items:center;justify-content:center}
.overlay{display:none;position:fixed;inset:0;background:rgba(16,32,30,.35);z-index:35}

/* ---------- Responsive ---------- */
@media (max-width:960px){
  .sidebar{transform:translateX(-100%)}
  .sidebar.open{transform:none;box-shadow:0 0 60px rgba(16,32,30,.18)}
  .content{margin-left:0}
  .doc{padding:32px 20px 96px}
  .menu-btn{display:flex}
  .overlay.show{display:block}
}
@media print{
  .sidebar,.menu-btn,.overlay,.side-search{display:none!important}
  .content{margin:0}
  .doc{max-width:none;padding:0}
  .hu,.adm,.tbl-wrap{break-inside:avoid}
  *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
"""

JS = """
(function(){
"use strict";
/* menú móvil */
var sb=document.querySelector('.sidebar'),ov=document.querySelector('.overlay'),mb=document.querySelector('.menu-btn');
mb.addEventListener('click',function(){sb.classList.toggle('open');ov.classList.toggle('show');});
ov.addEventListener('click',function(){sb.classList.remove('open');ov.classList.remove('show');});

/* buscador: filtra nav + resalta coincidencias en HU visibles */
var q=document.getElementById('doc-search');
var nores=document.getElementById('search-nores');
var items=[].slice.call(document.querySelectorAll('.nav-item'));
var subs=[].slice.call(document.querySelectorAll('.subnav li'));
q.addEventListener('input',function(){
  var v=q.value.trim().toLowerCase(),hits=0;
  items.forEach(function(li){
    var txt=li.firstChild.textContent.toLowerCase();
    var match=txt.indexOf(v)>-1;
    var subMatch=false;
    var s=li.querySelector('.subnav');
    if(s){
      [].slice.call(s.querySelectorAll('li')).forEach(function(sli){
        var sm=sli.textContent.toLowerCase().indexOf(v)>-1;
        sli.style.display=(v&&sm)?'':'none';
        if(sm)subMatch=true;
      });
      }
    li.style.display=(match||subMatch||!v)?'':'none';
    if(v&&(match||subMatch))hits++;
  });
  nores.style.display=(v&&!hits)?'block':'none';
});

/* scrollspy */
var links={};[].slice.call(document.querySelectorAll('[data-nav]')).forEach(function(a){links[a.getAttribute('href').slice(1)]=a;});
var spy=new IntersectionObserver(function(es){
  es.forEach(function(en){
    if(en.isIntersecting){
      var id=en.target.id;
      [].slice.call(document.querySelectorAll('[data-nav].active')).forEach(function(a){a.classList.remove('active');});
      if(links[id]){
        links[id].classList.add('active');
        var p=links[id].closest('.nav-item');
        if(p)p.querySelector(':scope > a').classList.add('active');
      }
    }
  });
},{rootMargin:'-10% 0px -80% 0px'});
document.querySelectorAll('section[id],article[id]').forEach(function(el){spy.observe(el);});
})();
"""

html_doc = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EAG MVP · Documentación · Historias de usuario</title>
<meta name="description" content="Documentación de las {total_hus} historias de usuario del MVP de EAG Ingenieros S.A.S. (SECOP II): épicas, criterios de aceptación, pendientes y exclusiones.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cpath d='M16 2 28 9v14L16 30 4 23V9z' fill='%230f766e'/%3E%3Cpath d='M11 16.5l3.5 3.5L21 13' stroke='%23fff' stroke-width='2.5' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>

<aside class="sidebar">
  <div class="side-brand">
    <svg width="26" height="26" viewBox="0 0 32 32" aria-hidden="true"><path d="M16 2 28 9v14L16 30 4 23V9z" fill="#0f766e"/><path d="M11 16.5l3.5 3.5L21 13" stroke="#fff" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <div>
      <span class="t">EAG MVP · HU</span>
      <span class="v">Versión 1.0 · 2026-09-07</span>
    </div>
  </div>
  <div class="side-search">
    <input id="doc-search" type="search" placeholder="Buscar épica o HU…" aria-label="Buscar en el documento">
    <p class="nores" id="search-nores">Sin resultados. Prueba con otro término (p. ej. HU-12, OCR, retención).</p>
  </div>
  <nav class="side-nav" aria-label="Contenido">
    <ul>
{nav_html}
    </ul>
  </nav>
  <div class="side-foot">riverosmejia/EAG-HU · propuesta sujeta a validación de EAG</div>
</aside>
<div class="overlay"></div>
<button class="menu-btn" aria-label="Abrir menú">
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
</button>

<main class="content">
<div class="doc">

<header class="doc-header">
  <div class="kicker">EAG Ingenieros S.A.S. · MVP · Documentación</div>
  <h1>Historias de usuario del MVP</h1>
  <p class="lead">Plataforma de apoyo al análisis de oportunidades de SECOP II. Este documento describe el comportamiento considerado necesario para completar el MVP —no el estado actual de implementación— y está sujeto a revisión humana y validación de EAG.</p>
  <p class="meta">{total_hus} historias · {len(EPICAS)} épicas · Base: CONTEXTO.md, CASO_DE_USO.md, MATRIZ_DE_PERMISOS.md, BACKLOG.md, MVP-01 a MVP-14 · Versión 1.0, 7 de septiembre de 2026</p>
</header>

<section id="como-leer">
  <div class="sec-kicker">01</div>
  <h2>Cómo leer este documento</h2>
  <p class="section-sub">Las historias se agrupan por capacidad y se vinculan con las issues del backlog para facilitar planificación, pruebas y revisión.</p>
  <div class="tbl-wrap"><table class="doc-t">
    <thead><tr><th>Elemento</th><th>Convención</th></tr></thead>
    <tbody>
      <tr><td class="rowhead">Narrativa</td><td>Como [persona], quiero [capacidad], para [valor].</td></tr>
      <tr><td class="rowhead">Criterios</td><td>Condiciones observables que permiten aceptar o rechazar la historia.</td></tr>
      <tr><td class="rowhead">Prioridad</td><td><span class="pri pri-p0">P0</span> imprescindible para un MVP seguro y defendible · <span class="pri pri-p1">P1</span> importante, pero configurable o aplazable si la validación reduce el alcance.</td></tr>
      <tr><td class="rowhead">Trazabilidad</td><td>Issue principal del backlog que implementa o valida la historia (etiqueta junto al ID).</td></tr>
    </tbody>
  </table></div>
</section>

<section id="actores">
  <div class="sec-kicker">02</div>
  <h2>Actores y responsabilidades</h2>
  <p class="section-sub">Roles presentes en el MVP y su responsabilidad.</p>
  <div class="tbl-wrap"><table class="doc-t">
    <thead><tr><th>Actor</th><th>Responsabilidad en el MVP</th></tr></thead>
    <tbody>
{actors_rows}
    </tbody>
  </table></div>
</section>

<section id="reglas">
  <div class="sec-kicker">03</div>
  <h2>Reglas transversales</h2>
  {admon("note", "Principios que aplican a todo el MVP",
  "<ul class='crit'>"
  "<li>Una recomendación no sustituye la decisión humana y el MVP no postula ofertas automáticamente.</li>"
  "<li>Fuente del requisito y evidencia empresarial se conservan por separado, con documento, localizador, fragmento y versión.</li>"
  "<li>Ausente o desconocido no equivale a cero; evidencia insuficiente no equivale a cumplimiento ni incumplimiento probado.</li>"
  "<li>Documentos y textos de licitación son contenido no confiable, nunca instrucciones para el sistema.</li>"
  "<li>Archivos, datos personales, secretos y documentos internos permanecen fuera de Git y de logs; las pruebas usan fixtures sintéticas o anonimizadas.</li>"
  "</ul>")}
</section>

<section id="flujo">
  <div class="sec-kicker">04</div>
  <h2>Secuencia principal</h2>
  <p class="section-sub">Las capacidades operativas y de retención atraviesan todo el flujo; el piloto valida el resultado completo. Las dependencias del backlog siguen siendo obligatorias aunque una historia se lea de forma independiente.</p>
  <ol class="flow">{flow_ol}</ol>
</section>

<section id="mapa">
  <div class="sec-kicker">05</div>
  <h2>Mapa de épicas</h2>
  <p class="section-sub">Vista general: cada épica agrupa historias y se vincula con issues del backlog.</p>
  <div class="tbl-wrap"><table class="doc-t">
    <thead><tr><th>Épica</th><th>Capacidad</th><th>Historias</th><th>Issues</th></tr></thead>
    <tbody>
{epic_map_rows}
    </tbody>
  </table></div>
</section>

{epics_html}

<section id="pendientes">
  <div class="sec-kicker">06</div>
  <h2>Pendientes de validación con EAG</h2>
  <p class="section-sub">Decisiones que condicionan historias concretas, con responsable propuesto.</p>
  <div class="tbl-wrap"><table class="doc-t">
    <thead><tr><th>Decisión pendiente</th><th>Impacto en historias</th><th>Responsable propuesto</th></tr></thead>
    <tbody>
{pend_rows}
    </tbody>
  </table></div>
</section>

<section id="cierre">
  <div class="sec-kicker">07</div>
  <h2>Criterio de cierre del MVP</h2>
  {admon("note", "Cuándo se da por aceptada una historia",
  "<p>Las 44 historias representan el alcance funcional considerado. Una historia solo puede darse por aceptada con <strong>pruebas reproducibles, revisión humana y dependencias técnicas aceptadas</strong>. Las historias del piloto no se completan con datos simulados; sin usuarios o muestra autorizada, permanecen pendientes.</p>")}
</section>

<section id="exclusiones">
  <div class="sec-kicker">08</div>
  <h2>Exclusiones explícitas</h2>
  <p class="section-sub">Límites declarados para evitar expectativas fuera de alcance.</p>
  {admon("warning", "Este MVP no hace lo siguiente",
  "<ul class='crit'>" + excl_lis + "</ul>")}
  {admon("warning", "Nota final",
  "<p>Este documento debe revisarse con EAG antes de convertir las historias en compromiso de producto. Los estados de avance, integraciones y resultados del piloto se verifican por separado en las issues y evidencias de prueba.</p>")}
</section>

</div>
</main>

<script>{JS}</script>
</body>
</html>
'''

with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_doc)

import re
ids = sorted(set(re.findall(r"HU-\d+", html_doc)), key=lambda x: int(x.split("-")[1]))
print("docs/index.html generado:", os.path.getsize(os.path.join(OUT, "index.html")), "bytes")
print("HUs únicas:", len(ids))
assert len(ids) == 44
print("OK: 44/44")
