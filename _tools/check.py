#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador de cardiolopezclemente.com

Comprueba que el sitio cumple las reglas descritas en CLAUDE.md.
Solo biblioteca estándar. Se ejecuta desde la raíz del repo:

    python3 _tools/check.py

Salida: lista de ERROR (incumple una regla) y AVISO (revisar).
Código de salida 1 si hay algún ERROR.
"""
import re, os, sys, json, glob, collections

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)

BASE = "https://cardiolopezclemente.com"
NAP = "Clínica Elche Salud · Pl. del Bisbe Siuri, Entresuelo B · 03201 Elche (Alicante)"
TEL = "tel:+34662637540"
DOCTORALIA = "doctoralia.es/jose-carlos-lopez-clemente"

# Páginas sin plantilla completa: no se les aplican las reglas de contenido
ESPECIALES = {"primera-consulta.html", "404.html"}
LEGALES = lambda f: f.startswith("legal/")

MAX_IMG_KB = 260          # por encima de esto, avisar
DESC_MIN, DESC_MAX = 100, 200

errores, avisos = [], []
def E(f, m): errores.append(f"{f}: {m}")
def A(f, m): avisos.append(f"{f}: {m}")

paginas = sorted(glob.glob("**/*.html", recursive=True))
contenido = [f for f in paginas if f not in ESPECIALES and not LEGALES(f)]
docs = {}
for f in paginas:
    docs[f] = open(f, encoding="utf-8").read()

def ruta(f):
    return "/" if f == "index.html" else "/" + f[:-5]

# ---------------------------------------------------------------- 1. HEAD
for f in contenido:
    s = docs[f]
    head = s.split("</head>")[0]

    if "<title>" not in head:
        E(f, "sin <title>")
    m = re.search(r'name="description"\s+content="(.*?)"', head, re.S)
    if not m:
        E(f, "sin meta description")
    else:
        n = len(m.group(1).strip())
        if not (DESC_MIN <= n <= DESC_MAX):
            A(f, f"meta description de {n} caracteres (rango habitual {DESC_MIN}-{DESC_MAX})")

    c = re.search(r'rel="canonical"\s+href="(.*?)"', head)
    if not c:
        E(f, "sin canonical")
    else:
        esperado = BASE + ruta(f)
        if c.group(1) != esperado:
            E(f, f"canonical {c.group(1)} — se esperaba {esperado}")

    for meta in ('og:title', 'og:description', 'og:url', 'og:image',
                 'og:locale', 'og:site_name'):
        if f'"{meta}"' not in head:
            E(f, f"falta {meta}")
    if 'name="twitter:card"' not in head:
        E(f, "falta twitter:card")
    ogi = re.search(r'property="og:image" content="(.*?)"', head)
    if ogi:
        rel = ogi.group(1).replace(BASE + "/", "")
        if not rel.startswith("img/"):
            E(f, f"og:image fuera de /img/: {ogi.group(1)}")
        elif not os.path.exists(rel):
            E(f, f"og:image apunta a un archivo inexistente: {rel}")

    for meta in ('og:image', 'og:locale', 'og:site_name', 'canonical', '<title>'):
        pat = f'"{meta}"' if ":" in meta else meta
        if head.count(pat) > 1:
            E(f, f"{meta} duplicado")

# --------------------------------------------------- 2. analítica y plantilla
for f in paginas:
    s = docs[f]
    if f == "primera-consulta.html":
        continue
    if '<script src="/consent.js" defer></script>' not in s:
        E(f, "falta consent.js")
    if "googletagmanager.com/gtag/js" in s:
        E(f, "lleva el snippet suelto de gtag.js (debe cargarse solo desde consent.js)")
    if "<nav" not in s:
        E(f, "sin nav")
    if f != "404.html":
        if NAP not in s:
            E(f, "el NAP del footer no coincide exactamente")
        if TEL not in s:
            E(f, "sin enlace tel: canónico")

# ------------------------------------------------------------- 3. JSON-LD
for f in paginas:
    for i, b in enumerate(re.findall(r'<script type="application/ld\+json">(.*?)</script>',
                                     docs[f], re.S)):
        try:
            json.loads(b)
        except Exception as e:
            E(f, f"JSON-LD #{i+1} no parsea: {e}")

for f in sorted(glob.glob("articulos/*.html")):
    s = docs[f]
    for campo in ("datePublished", "dateModified"):
        if campo not in s:
            E(f, f"artículo sin {campo} en el JSON-LD")
    if 'class="referencias"' not in s:
        A(f, "artículo sin bloque de Referencias")
    if 'class="ig-promo"' not in s:
        A(f, "artículo sin bloque ig-promo")

# --------------------------------------------- 4. estructura y relacionados
for f in contenido:
    s = docs[f]
    b = s.split("</head>")[1]
    if b.count("<h1") != 1:
        E(f, f"{b.count('<h1')} etiquetas <h1> (debe haber exactamente 1)")
    if "cta-section" not in b:
        E(f, "sin sección CTA final")
    if DOCTORALIA not in b:
        A(f, "sin enlace a Doctoralia en el cuerpo")
    for t in ("section", "div", "a", "footer", "nav"):
        o = len(re.findall(r"<%s[\s>]" % t, b))
        c = len(re.findall(r"</%s>" % t, b))
        if o != c:
            E(f, f"<{t}> descuadrado: {o} aperturas / {c} cierres")
    carpeta = f.split("/")[0]
    if carpeta in ("articulos", "motivos", "servicios", "pruebas"):
        if "articles-grid" not in b:
            E(f, "sin bloque de 3 tarjetas relacionadas")
        else:
            i_cta, i_rel = b.find("cta-section"), b.find("articles-grid")
            if i_rel < i_cta:
                A(f, "el bloque de relacionados va antes de la CTA (debe ir después)")
    if carpeta in ("motivos", "servicios") and "cta-movil" not in b:
        E(f, "sin barra CTA flotante de móvil")

# ------------------------------------------------------ 5. rutas y enlaces
paths = {ruta(f) for f in paginas}
entrantes = collections.Counter()
for f in paginas:
    s = docs[f]
    if "../../" in s:
        E(f, "usa ../../ (solo se permite un nivel)")
    esperado_css = "style.css" if "/" not in f else "../style.css"
    if f not in ("404.html", "primera-consulta.html"):
        if f'href="{esperado_css}"' not in s:
            E(f, f"no enlaza {esperado_css}")
    b = s.split("</head>")[1]
    nav = re.search(r"<nav.*?</nav>", b, re.S)
    foot = re.search(r"<footer.*?</footer>", b, re.S)
    core = b.replace(nav.group(0), "") if nav else b
    if foot:
        core = core.replace(foot.group(0), "")
    for h in re.findall(r'href="(/[^"]*)"', core):
        k = h.split("#")[0].split("?")[0].rstrip("/") or "/"
        k = k[:-5] if k.endswith(".html") else k
        if k in paths:
            entrantes[k] += 1
        else:
            E(f, f"enlace interno roto: {h}")

for f in contenido:
    r = ruta(f)
    if entrantes.get(r, 0) == 0:
        A(f, "página huérfana: 0 enlaces entrantes fuera de nav y footer")

# ---------------------------------------------------------- 6. imágenes
for f in paginas:
    for img in re.findall(r"<img[^>]*>", docs[f]):
        if "logo.webp" in img:
            continue
        falta = [a for a in ("width=", "height=", "alt=", "loading=") if a not in img]
        if falta:
            E(f, f"<img> sin {', '.join(x.rstrip('=') for x in falta)}: {img[:70]}...")

for i in sorted(glob.glob("img/*")):
    if os.path.isfile(i) and not i.endswith(".md"):
        kb = os.path.getsize(i) / 1024
        if kb > MAX_IMG_KB:
            A(i, f"pesa {kb:.0f} KB (umbral {MAX_IMG_KB} KB)")

# ----------------------------------------------------------- 7. sitemap
if os.path.exists("sitemap.xml"):
    sm = open("sitemap.xml", encoding="utf-8").read()
    en_sitemap = {u.replace(BASE, "") or "/" for u in re.findall(r"<loc>(.*?)</loc>", sm)}
    en_sitemap = {u.rstrip("/") or "/" for u in en_sitemap}
    debe_estar = {ruta(f) for f in contenido}
    for r in sorted(debe_estar - en_sitemap):
        E("sitemap.xml", f"falta la URL {r}")
    for r in sorted(en_sitemap - debe_estar):
        E("sitemap.xml", f"URL que ya no existe: {r}")
    for u in re.findall(r"<url>(.*?)</url>", sm, re.S):
        loc = re.search(r"<loc>(.*?)</loc>", u).group(1)
        for tag in ("lastmod", "changefreq", "priority"):
            if f"<{tag}>" not in u:
                A("sitemap.xml", f"{loc} sin <{tag}>")
    for m in re.findall(r"<lastmod>(.*?)</lastmod>", sm):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", m):
            E("sitemap.xml", f"lastmod con formato raro: {m}")
else:
    E("sitemap.xml", "no existe")

# ------------------------------------------------- 8. reglas editoriales
for f in paginas:
    s = docs[f]
    if re.search(r"plan nutricional individualizado", s, re.I):
        E(f, 'usa "plan nutricional individualizado" (debe ser "orientación y resolución de dudas")')
    if "consulta" in f or f == "index.html":
        for m in re.findall(r"consulta[^.]{0,60}?(\d+\s*[–-]\s*\d+)\s*minutos", s, re.I):
            E(f, f"duración de consulta como rango ({m} minutos): debe ser siempre 60 minutos")
if "certificado" in docs.get("servicios/reconocimiento-cardiologico-elche.html", "").lower():
    A("servicios/reconocimiento-cardiologico-elche.html",
      'menciona "certificado" (la omisión es deliberada)')

# --------------------------------------------------------------- informe
print(f"Revisadas {len(paginas)} páginas.\n")
if errores:
    print(f"ERRORES ({len(errores)}):")
    for e in errores:
        print("  ✗", e)
    print()
if avisos:
    print(f"AVISOS ({len(avisos)}):")
    for a in avisos:
        print("  ·", a)
    print()
if not errores and not avisos:
    print("Todo correcto.")
elif not errores:
    print("Sin errores. Solo avisos, revisables a criterio.")
sys.exit(1 if errores else 0)
