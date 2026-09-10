# -*- coding: utf-8 -*-
"""Genera docs/index.html: versión documentación del documento de HUs de EAG.

Sistema de diseño: Stripi-Inspired (ver skill stripi-design-system)
- Mesh gradiente (cream/orange/lavender/indigo/ruby) en banda superior
- Inter weight 300 con tracking negativo en display, ss01 global
- Indigo #533afd único color de acción; pill buttons
- tnum en IDs y números; hairlines #e3e8ee; banda cream #f5e9d4 para avisos
"""
import html as H
import os
from data_hus import EPICAS, PENDIENTES, EXCLUSIONES, FLOW, ACTORS
from data_plan import (RESUMEN, STACK, DECISIONES_CRITICAS, DECISIONES_ADOPTADAS,
                       DECISIONES_OPCIONALES, SEMANAS, RIESGOS, PREGUNTAS_EAG,
                       HUS_AMPLIACION, CRITERIOS_ACEPTACION, INCONSISTENCIAS_RESUELTAS, META)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
os.makedirs(OUT, exist_ok=True)


def esc(s):
    return H.escape(s, quote=False)


# ---------- Nav tree ----------
nav = []
nav.append(("plan", "Plan de acción", [
    ("plan-resumen", "Resumen ejecutivo"),
    ("plan-decisiones", "Decisiones adoptadas"),
    ("plan-stack", "Stack y arquitectura"),
    ("plan-semanas", "Semanas de implementación"),
    ("plan-riesgos", "Riesgos y mitigación"),
    ("plan-eag", "Preguntas a EAG"),
]))
nav.append(("como-leer", "Cómo leer este documento", []))
nav.append(("actores", "Actores y responsabilidades", []))
nav.append(("reglas", "Reglas transversales", []))
nav.append(("flujo", "Secuencia principal", []))
nav.append(("mapa", "Mapa de épicas", []))
for e in EPICAS:
    code, title, _, _, hus = e
    kids = [(f"{h[0].lower()}", h[0]) for h in hus]
    nav.append((f"e{code.lower()}", f"{code} · {title}", kids))
nav.append(("ampliaciones", "Ampliaciones propuestas", []))
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


def admon(kind, title, body):
    icons = {
        "note": '<circle cx="12" cy="12" r="9"/><path d="M12 16v-5M12 8h.01"/>',
        "warning": '<path d="M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>',
    }
    return f'''<div class="adm adm-{kind}">
<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{icons[kind]}</svg>
<div><p class="adm-title">{title}</p>{body}</div>
</div>'''


def hu_section(hid, pri, issue, actor, cap, valor, crits):
    pill = f'<span class="pri pri-{pri.lower()}">{pri}</span>'
    lis = "".join(f"<li>{esc(c)}</li>" for c in crits)
    return f'''<article class="hu" id="{hid.lower()}">
<h4><span class="hu-id">{hid}</span>{pill}<span class="issue-tag">{esc(issue)}</span></h4>
<p class="narr">Como <strong>{esc(actor)}</strong>, quiero <strong>{esc(cap)}</strong>, para {esc(valor)}.</p>
<h5>Criterios de aceptación</h5>
<ul class="crit">{lis}</ul>
</article>'''


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
    f"<td class='tnum'><code>HU-{e[4][0][0].split('-')[1]} a HU-{e[4][-1][0].split('-')[1]}</code></td>"
    f"<td><code>{esc(e[3])}</code></td></tr>"
    for e in EPICAS)
pend_rows = "\n".join(
    f"<tr><td>{esc(d)}</td><td><code>{esc(h)}</code></td><td>{esc(r)}</td></tr>"
    for d, h, r in PENDIENTES)
excl_lis = "".join(f"<li>{esc(x)}</li>" for x in EXCLUSIONES)
epics_html = "\n".join(epic_section(e) for e in EPICAS)

total_hus = sum(len(e[4]) for e in EPICAS)
ver, fecha = META

# ---------- Plan de acción ----------
def dec_card(did, tag, cls, titulo, texto):
    return f'''<article class="hu">
<h4><span class="hu-id">{did}</span><span class="pri {cls}">{tag}</span></h4>
<p class="narr"><strong>{esc(titulo)}.</strong> {esc(texto)}</p>
</article>'''

dec_crit = "".join(dec_card(d, "Crítica", "pri-p0", t, x) for d, t, x in DECISIONES_CRITICAS)
dec_ado = "".join(dec_card(d, "Adoptada", "pri-p1", t, x) for d, t, x in DECISIONES_ADOPTADAS)
dec_opc = "".join(dec_card(d, "Opcional", "pri-p1", t, x) for d, t, x in DECISIONES_OPCIONALES)

stack_rows = "".join(
    f"<tr><td class='rowhead'>{esc(c)}</td><td>{esc(t)}</td><td>{esc(d)}</td></tr>"
    for c, t, d, _s in STACK)
sem_rows = "".join(
    f"<tr><td class='rowhead tnum'>{esc(s)}</td><td><strong>{esc(f)}</strong></td><td>{esc(d)}</td></tr>"
    for s, f, d in SEMANAS)

def sev_pill(sv):
    cls = "pri-p0" if sv == "Alta" else "pri-p1"
    return f'<span class="pri {cls}">{esc(sv)}</span>'

ries_rows = "".join(
    f"<tr><td>{esc(r)}</td><td>{esc(m)}</td><td>{sev_pill(sv)}</td></tr>"
    for r, m, sv in RIESGOS)
inco_rows = "".join(
    f"<tr><td class='rowhead'>{esc(p)}</td><td>{esc(c)}</td><td>{esc(r)}</td></tr>"
    for p, c, r in INCONSISTENCIAS_RESUELTAS)
q_lis = "".join(f"<li>{esc(q)}</li>" for q in PREGUNTAS_EAG)
resumen_lis = "".join(f"<li><strong>{esc(a)}:</strong> {esc(t)}</li>" for a, t in RESUMEN)
criterios_note = admon("note", "Criterios de aceptación del MVP",
    "<ul class='crit'>" + "".join(f"<li>{esc(c)}</li>" for c in CRITERIOS_ACEPTACION) + "</ul>")

ampl_html = "".join(
    hu_section(hid, pri, "Ampliación", actor, cap, valor, crits)
    for hid, pri, actor, cap, valor, crits in HUS_AMPLIACION)

plan_html = f'''<section id="plan">
<div class="sec-kicker">01</div>
<h2>Plan de acción</h2>
<p class="section-sub">Plan de implementación del MVP (12 semanas) con las decisiones y mejoras adoptadas en la auditoría técnica del 10 de septiembre de 2026. Sujeto a validación de EAG.</p>

<section class="plan-sub" id="plan-resumen">
<h3>Resumen ejecutivo</h3>
{admon("note", "Qué construye el MVP", "<ul class='crit'>" + resumen_lis + "</ul>")}
{criterios_note}
</section>

<section class="plan-sub" id="plan-decisiones">
<h3>Decisiones adoptadas</h3>
<p class="section-sub">Las decisiones de la auditoría, priorizadas. Resuelven inconsistencias del plan original y riesgos técnicos; las preguntas que requieren decisión de EAG se listan al final de la sección.</p>
<h4>Críticas · bloquean diseño o cronograma</h4>
{dec_crit}
<h4>Recomendadas · mejoran viabilidad</h4>
{dec_ado}
<h4>Opcionales · backlog</h4>
{dec_opc}
</section>

<section class="plan-sub" id="plan-stack">
<h3>Stack y arquitectura</h3>
<p class="section-sub">Decisión A3: FastAPI es la capa de autoridad; RLS queda solo para Storage con bucket privado. El scheduler se resuelve con cron de Render (B4).</p>
<div class="tbl-wrap"><table class="doc-t">
<thead><tr><th>Capa</th><th>Tecnología</th><th>Decisión / nota</th></tr></thead>
<tbody>
{stack_rows}
</tbody>
</table></div>
</section>

<section class="plan-sub" id="plan-semanas">
<h3>Implementación por semanas</h3>
<p class="section-sub">Doce semanas con hitos. Semanas 07-08 son el camino crítico (extracción IA + validación de citas con normalización OCR); semana 01 incluye el hito externo A5 (autorización y muestra de EAG).</p>
<div class="tbl-wrap"><table class="doc-t">
<thead><tr><th>Semana</th><th>Foco</th><th>Hitos y decisiones aplicadas</th></tr></thead>
<tbody>
{sem_rows}
</tbody>
</table></div>
</section>

<section class="plan-sub" id="plan-riesgos">
<h3>Riesgos y mitigación</h3>
<p class="section-sub">Inconsistencias del plan original detectadas en la auditoría y cómo quedaron resueltas.</p>
<div class="tbl-wrap"><table class="doc-t">
<thead><tr><th>Punto</th><th>Contradicción detectada</th><th>Resolución</th></tr></thead>
<tbody>
{inco_rows}
</tbody>
</table></div>
<p class="section-sub" style="margin-top:18px">Riesgos operativos con su mitigación y severidad.</p>
<div class="tbl-wrap"><table class="doc-t">
<thead><tr><th>Riesgo</th><th>Mitigación</th><th>Severidad</th></tr></thead>
<tbody>
{ries_rows}
</tbody>
</table></div>
</section>

<section class="plan-sub" id="plan-eag">
<h3>Preguntas que requieren decisión de EAG</h3>
<p class="section-sub">Bloqueantes de producto o cronograma. Cada una indica la recomendación técnica del equipo.</p>
<ol class="qlist">{q_lis}</ol>
</section>
</section>'''

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
  --sidebar-w:292px;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:24px}
body{font-family:var(--sans);color:var(--ink);background:var(--canvas);font-weight:300;
  font-size:15px;line-height:1.5;font-feature-settings:"ss01";-webkit-font-smoothing:antialiased}
::selection{background:var(--primary-subdued)}
a{color:var(--primary);text-decoration:none}
a:hover{text-decoration:underline}
code{font-family:var(--sans);font-weight:400;font-size:.85em;background:var(--canvas-soft);
  border:1px solid var(--hairline);border-radius:4px;padding:1px 6px;color:var(--ink-2);font-feature-settings:"tnum"}
strong{font-weight:500}
.tnum{font-feature-settings:"tnum";letter-spacing:-.2px}

/* ---------- Mesh (banda atmosférica superior) ---------- */
.mesh{position:relative;height:150px;overflow:hidden}
.mesh::before{content:"";position:absolute;inset:-40px;
  background:
    radial-gradient(45% 95% at 5% 55%, rgba(245,233,212,.95), transparent 62%),
    radial-gradient(40% 85% at 26% 30%, rgba(249,150,80,.38), transparent 62%),
    radial-gradient(46% 95% at 52% 45%, rgba(178,132,255,.42), transparent 66%),
    radial-gradient(52% 110% at 78% 35%, rgba(83,58,253,.68), transparent 66%),
    radial-gradient(38% 85% at 100% 55%, rgba(234,34,97,.5), transparent 62%);
  filter:blur(6px)}
.mesh::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 40%,var(--canvas) 100%)}

/* ---------- Sidebar ---------- */
.sidebar{position:fixed;top:0;left:0;bottom:0;width:var(--sidebar-w);background:var(--canvas);
  border-right:1px solid var(--hairline);display:flex;flex-direction:column;z-index:40;transition:transform .22s ease}
.side-brand{display:flex;align-items:center;gap:10px;padding:18px 20px 14px;border-bottom:1px solid var(--hairline)}
.side-brand svg{flex:none}
.side-brand .t{font-weight:400;font-size:14.5px;line-height:1.25;letter-spacing:-.2px}
.side-brand .v{font-size:11px;color:var(--mute);display:block;margin-top:2px;font-feature-settings:"tnum"}
.side-search{padding:14px 16px;border-bottom:1px solid var(--hairline)}
.side-search input{width:100%;font-family:var(--sans);font-weight:300;font-size:14px;padding:9px 12px;
  border:1px solid var(--hairline-input);border-radius:6px;background:var(--canvas);color:var(--ink);outline:none;
  transition:border-color .15s,box-shadow .15s}
.side-search input:focus{border-color:var(--primary)}
.side-search .nores{display:none;font-size:12px;color:var(--mute);padding:8px 4px 0}
.side-nav{flex:1;overflow-y:auto;padding:12px 8px 24px}
.side-nav>ul{list-style:none}
.nav-item>a{display:block;padding:7px 12px;border-radius:8px;font-size:13.5px;font-weight:400;color:var(--ink-2);line-height:1.35;letter-spacing:-.1px}
.nav-item>a:hover{background:var(--canvas-soft);text-decoration:none;color:var(--primary-deep)}
.nav-item>a.active{background:var(--primary-subdued);color:var(--primary-deep);font-weight:400}
.subnav{list-style:none;margin:2px 0 6px;padding-left:14px;border-left:1px solid var(--hairline)}
.subnav a{display:block;padding:4px 12px;font-size:11.5px;font-feature-settings:"tnum";letter-spacing:-.1px;color:var(--mute);border-radius:6px}
.subnav a:hover{text-decoration:none;color:var(--primary);background:var(--canvas-soft)}
.subnav a.active{color:var(--primary-deep);font-weight:400}
.side-foot{padding:12px 20px;border-top:1px solid var(--hairline);font-size:10.5px;color:var(--mute)}

/* ---------- Content ---------- */
.content{margin-left:var(--sidebar-w)}
.doc{max-width:820px;margin:0 auto;padding:0 40px 96px}
h1{font-size:44px;font-weight:300;line-height:1.05;letter-spacing:-1.1px}
h2{font-size:28px;font-weight:300;line-height:1.1;letter-spacing:-.5px;margin:0 0 4px}
h3{font-size:19px;font-weight:300;letter-spacing:-.2px;margin:36px 0 10px;scroll-margin-top:24px}
h4{font-size:15px;font-weight:400;margin:0 0 8px}
h5{font-size:10px;font-weight:400;letter-spacing:.1px;text-transform:uppercase;color:var(--mute);margin:12px 0 6px}
.doc-header{padding:38px 0 26px;border-bottom:1px solid var(--hairline);margin-bottom:6px}
.doc-header .kicker{font-size:10px;font-weight:400;letter-spacing:.1px;text-transform:uppercase;
  color:var(--primary-deep);background:var(--primary-subdued);display:inline-flex;padding:4px 8px;border-radius:9999px;margin-bottom:16px}
.doc-header .meta{font-size:13px;color:var(--mute);margin-top:12px;letter-spacing:-.2px}
.doc-header .lead{color:var(--ink-2);margin-top:12px;font-size:16px;line-height:1.45}
.stat-row{display:flex;gap:8px;margin-top:18px;flex-wrap:wrap}
.stat-pill{background:var(--canvas-soft);border:1px solid var(--hairline);border-radius:9999px;
  padding:6px 14px;font-size:13px;color:var(--ink-2);font-feature-settings:"tnum"}
.stat-pill b{color:var(--primary-deep);font-weight:500}
.doc>section{margin:40px 0}
.doc>section>h2{scroll-margin-top:24px}
.sec-kicker{font-size:10px;font-weight:400;letter-spacing:.1px;text-transform:uppercase;color:var(--primary-deep);
  background:var(--primary-subdued);display:inline-flex;padding:3px 8px;border-radius:9999px;margin-bottom:12px}
.section-sub{color:var(--mute);font-size:14px;margin-bottom:16px}

/* ---------- Admonitions ---------- */
.adm{display:flex;gap:12px;padding:16px 18px;border-radius:12px;margin:16px 0;font-size:14px;line-height:1.5;border:1px solid var(--hairline)}
.adm svg{width:18px;height:18px;flex:none;margin-top:2px}
.adm .adm-title{font-weight:500;margin-bottom:2px;letter-spacing:-.1px}
.adm-note{background:var(--canvas-soft);color:var(--ink-2)}
.adm-note svg{stroke:var(--primary)}
.adm-warning{background:var(--cream);color:var(--lemon);border-color:transparent}
.adm-warning svg{stroke:var(--lemon)}
.adm-warning .adm-title,.adm-warning li{color:var(--ink)}

/* ---------- Tables ---------- */
.tbl-wrap{overflow-x:auto;border:1px solid var(--hairline);border-radius:12px;background:var(--canvas);margin:16px 0;box-shadow:var(--shadow-1)}
table.doc-t{width:100%;border-collapse:collapse;font-size:14px;font-weight:300}
table.doc-t th,table.doc-t td{padding:12px 14px;text-align:left;vertical-align:top;border-bottom:1px solid var(--hairline)}
table.doc-t thead th{font-size:10px;font-weight:400;letter-spacing:.1px;text-transform:uppercase;color:var(--mute);background:var(--canvas-soft)}
table.doc-t tbody tr:last-child td{border-bottom:none}
table.doc-t td.rowhead{font-weight:400;color:var(--ink-2);background:var(--canvas-soft);white-space:nowrap;letter-spacing:-.1px}
table.doc-t td.tnum{font-feature-settings:"tnum";letter-spacing:-.2px}

/* ---------- Flow ---------- */
ol.flow{list-style:none;counter-reset:paso;margin:14px 0}
ol.flow li{counter-increment:paso;position:relative;padding:8px 0 8px 46px;border-left:1px solid var(--hairline);margin-left:15px;font-size:14px;color:var(--ink-2)}
ol.flow li::before{content:counter(paso,decimal-leading-zero);position:absolute;left:-15px;top:6px;width:30px;height:30px;border-radius:9999px;
  background:var(--brand-dark);color:#fff;font-size:10px;font-weight:400;font-feature-settings:"tnum";letter-spacing:-.2px;display:flex;align-items:center;justify-content:center}
ol.flow li:last-child{border-left-color:transparent}
ol.flow strong{color:var(--ink)}

/* ---------- Épicas ---------- */
.epic-sec{border-top:1px solid var(--hairline);padding-top:30px;margin-top:34px;scroll-margin-top:24px}
.epic-code{font-size:11px;font-weight:400;font-feature-settings:"tnum";color:var(--primary-deep);background:var(--primary-subdued);
  border-radius:9999px;padding:3px 10px;margin-right:10px;vertical-align:3px}
.epic-desc{color:var(--ink-2);margin:6px 0 4px}
.epic-issues{font-size:12px;color:var(--mute);margin-bottom:8px}

/* ---------- HU ---------- */
.hu{background:var(--canvas);border:1px solid var(--hairline);border-radius:12px;box-shadow:var(--shadow-1);
  padding:18px 22px;margin:14px 0;scroll-margin-top:24px}
.hu h4{margin:0 0 8px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.hu-id{font-size:14px;font-weight:400;color:var(--primary-deep);font-feature-settings:"tnum";letter-spacing:-.2px}
.pri{font-size:10px;font-weight:400;letter-spacing:.1px;padding:4px 8px;border-radius:9999px}
.pri-p0{background:var(--primary-subdued);color:var(--primary-deep)}
.pri-p1{background:var(--cream);color:var(--lemon)}
.issue-tag{font-size:10px;font-feature-settings:"tnum";color:var(--mute);border:1px solid var(--hairline);border-radius:9999px;padding:3px 8px;background:var(--canvas-soft)}
.narr{font-size:14.5px;color:var(--ink);line-height:1.5}
.narr strong{color:var(--ink);font-weight:500}
.crit{list-style:none;margin-top:6px}
.crit li{font-size:13.5px;color:var(--ink-2);padding-left:20px;position:relative;margin-bottom:5px;line-height:1.5}
.crit li::before{content:"";position:absolute;left:2px;top:8px;width:6px;height:6px;border-radius:9999px;background:var(--primary)}
mark{background:var(--cream);border-radius:3px;padding:0 2px}

/* ---------- Menú móvil ---------- */
.menu-btn{display:none;position:fixed;bottom:18px;right:18px;z-index:60;width:44px;height:44px;border-radius:9999px;
  border:none;background:var(--primary);color:#fff;cursor:pointer;box-shadow:var(--shadow-2);align-items:center;justify-content:center}
.menu-btn:active{background:var(--primary-press)}
.overlay{display:none;position:fixed;inset:0;background:rgba(13,37,61,.4);z-index:35}

@media (max-width:960px){
  .sidebar{transform:translateX(-100%)}
  .sidebar.open{transform:none;box-shadow:var(--shadow-2)}
  .content{margin-left:0}
  .doc{padding:0 20px 96px}
  .menu-btn{display:flex}
  .overlay.show{display:block}
  h1{font-size:34px;letter-spacing:-.8px}
}
@media print{
  .sidebar,.menu-btn,.overlay,.side-search,.mesh{display:none!important}
  .content{margin:0}
  .doc{max-width:none;padding:0}
  .hu,.adm,.tbl-wrap{break-inside:avoid;box-shadow:none}
  *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}

/* ---------- Plan de acción ---------- */
.plan-sub{margin:32px 0 0;border-top:1px solid var(--hairline);padding-top:26px;scroll-margin-top:24px}
.plan-sub h4{font-size:11px;font-weight:400;letter-spacing:.1px;text-transform:uppercase;color:var(--mute);margin:22px 0 8px}
.dec-tag{font-size:10px;font-weight:400;letter-spacing:.1px;padding:4px 8px;border-radius:9999px}
ol.qlist{list-style:none;counter-reset:q;margin:14px 0}
ol.qlist li{counter-increment:q;position:relative;padding:9px 0 9px 42px;font-size:14px;color:var(--ink-2);line-height:1.5;border-bottom:1px solid var(--hairline)}
ol.qlist li:last-child{border-bottom:none}
ol.qlist li::before{content:counter(q);position:absolute;left:0;top:8px;width:28px;height:28px;border-radius:9999px;
  background:var(--brand-dark);color:#fff;font-size:10px;font-weight:400;font-feature-settings:"tnum";letter-spacing:-.2px;display:flex;align-items:center;justify-content:center}
"""

JS = """
(function(){
"use strict";
var sb=document.querySelector('.sidebar'),ov=document.querySelector('.overlay'),mb=document.querySelector('.menu-btn');
mb.addEventListener('click',function(){sb.classList.toggle('open');ov.classList.toggle('show');});
ov.addEventListener('click',function(){sb.classList.remove('open');ov.classList.remove('show');});

var q=document.getElementById('doc-search');
var nores=document.getElementById('search-nores');
var items=[].slice.call(document.querySelectorAll('.nav-item'));
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
<title>EAG MVP · Plan de acción y documentación · Historias de usuario</title>
<meta name="description" content="Plan de acción (12 semanas) y documentación de las {total_hus} historias de usuario del MVP de EAG Ingenieros S.A.S. (SECOP II): decisiones adoptadas, stack, épicas, criterios, pendientes y exclusiones.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cpath d='M16 2 30 10v12L16 30 2 22V10z' fill='%23533afd'/%3E%3Cpath d='M11 16.5l3.5 3.5L21 13' stroke='%23fff' stroke-width='2.5' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>

<aside class="sidebar">
  <div class="side-brand">
    <svg width="26" height="26" viewBox="0 0 32 32" aria-hidden="true"><path d="M16 2 30 10v12L16 30 2 22V10z" fill="#533afd"/><path d="M11 16.5l3.5 3.5L21 13" stroke="#fff" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <div>
      <span class="t">EAG MVP · Plan + HU</span>
      <span class="v">Versión {ver} · {fecha}</span>
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
  <div class="side-foot">riverosmejia/EAG-HU · plan de acción + {total_hus} HUs · propuesta sujeta a validación de EAG</div>
</aside>
<div class="overlay"></div>
<button class="menu-btn" aria-label="Abrir menú">
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
</button>

<main class="content">
  <div class="mesh" aria-hidden="true"></div>
  <div class="doc">

<header class="doc-header">
  <div class="kicker">EAG Ingenieros S.A.S. · MVP · Plan de acción y documentación</div>
  <h1>Plan de acción y historias de usuario del MVP</h1>
  <p class="lead">Plataforma de apoyo al análisis de oportunidades de SECOP II. Este documento reúne el plan de implementación (12 semanas, con las decisiones adoptadas en la auditoría técnica) y el comportamiento considerado necesario para completar el MVP —no el estado actual de implementación—. Todo está sujeto a revisión humana y validación de EAG.</p>
  <div class="stat-row">
    <span class="stat-pill"><b>{len(SEMANAS)}</b> semanas de plan</span>
    <span class="stat-pill"><b>{total_hus}</b> historias</span>
    <span class="stat-pill"><b>{len(EPICAS)}</b> épicas</span>
    <span class="stat-pill">Base: CONTEXTO.md · CASO_DE_USO.md · MATRIZ_DE_PERMISOS.md · BACKLOG.md · MVP-01 a MVP-14 · Auditoría 2026-09-10</span>
    <span class="stat-pill">Versión {ver} · {fecha}</span>
  </div>
</header>

{plan_html}

<section id="como-leer">
  <div class="sec-kicker">02</div>
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
  <div class="sec-kicker">03</div>
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
  <div class="sec-kicker">04</div>
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
  <div class="sec-kicker">05</div>
  <h2>Secuencia principal</h2>
  <p class="section-sub">Las capacidades operativas y de retención atraviesan todo el flujo; el piloto valida el resultado completo. Las dependencias del backlog siguen siendo obligatorias aunque una historia se lea de forma independiente.</p>
  <ol class="flow">{flow_ol}</ol>
</section>

<section id="mapa">
  <div class="sec-kicker">06</div>
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

<section id="ampliaciones">
  <div class="sec-kicker">07</div>
  <h2>Ampliaciones propuestas</h2>
  <p class="section-sub">HUs adicionales que cubren los huecos detectados en la auditoría frente a las pantallas prometidas por el plan (gestión de usuarios, auditoría, parámetros, notificaciones). Propuestas y pendientes de validación con EAG.</p>
{ampl_html}
</section>

<section id="pendientes">
  <div class="sec-kicker">08</div>
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
  <div class="sec-kicker">09</div>
  <h2>Criterio de cierre del MVP</h2>
  {admon("note", "Cuándo se da por aceptada una historia",
  "<p>Las 44 historias representan el alcance funcional considerado. Una historia solo puede darse por aceptada con <strong>pruebas reproducibles, revisión humana y dependencias técnicas aceptadas</strong>. Las historias del piloto no se completan con datos simulados; sin usuarios o muestra autorizada, permanecen pendientes.</p>")}
</section>

<section id="exclusiones">
  <div class="sec-kicker">10</div>
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
orig = [i for i in ids if int(i.split("-")[1]) <= 44]
ampl = [i for i in ids if int(i.split("-")[1]) > 44]
print("docs/index.html generado:", os.path.getsize(os.path.join(OUT, "index.html")), "bytes")
print("HUs originales:", len(orig), "| ampliaciones:", len(ampl), "| total:", len(ids))
assert len(orig) == 44, f"Se esperaban 44 HUs originales, hay {len(orig)}"
assert sorted(ampl) == ["HU-45", "HU-46", "HU-47", "HU-48"], f"Ampliaciones inesperadas: {ampl}"
print("OK: 44/44 + 4 ampliaciones")
print("Plan: semanas =", len(SEMANAS), "| stack =", len(STACK),
      "| decisiones =", len(DECISIONES_CRITICAS) + len(DECISIONES_ADOPTADAS) + len(DECISIONES_OPCIONALES),
      "| riesgos =", len(RIESGOS), "| preguntas EAG =", len(PREGUNTAS_EAG),
      "| ampliaciones =", len(HUS_AMPLIACION))
assert len(SEMANAS) == 12
assert len(HUS_AMPLIACION) == 4
assert all(k in html_doc for k in
           ["#plan-resumen", "#plan-decisiones", "#plan-stack", "#plan-semanas",
            "#plan-riesgos", "#plan-eag", "#ampliaciones"])
print("OK: plan completo")
