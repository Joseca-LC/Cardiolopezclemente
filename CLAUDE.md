# CLAUDE.md — cardiolopezclemente.com

Reglas del sitio extraídas del código existente. Todo lo que sigue describe lo que
ya se hace en el repositorio: no son propuestas ni convenciones nuevas.

---

## 1. Qué es este repo

Web personal del Dr. José Carlos López Clemente, cardiólogo en Elche (Clínica Elche
Salud). Objetivo: captación de pacientes para la consulta privada y posicionamiento
local.

- HTML estático puro. Sin framework, sin CMS, sin build.
- CSS: un `style.css` global + un bloque `<style>` inline por página (ver §6).
- JS: solo `consent.js` y el `onclick` inline del menú hamburguesa. Nada más.
- Publicación: GitHub Pages + Cloudflare. `CNAME` = `cardiolopezclemente.com`.
- Repo: github.com/Joseca-LC/Cardiolopezclemente

Flujo de trabajo real: JC edita desde la interfaz web de GitHub, sin terminal. Los
entregables se preparan como archivos completos listos para arrastrar y soltar, con
la estructura de carpetas ya montada y sin ediciones manuales pendientes.

---

## 2. Estructura de archivos

```
/                       index.html · sobre-mi.html · preguntas-frecuentes.html
                        404.html · primera-consulta.html
                        style.css · consent.js · sitemap.xml · robots.txt · CNAME
                        articulos-web.md · posts-google.md
/motivos/               9 páginas   — síntoma o diagnóstico por el que el paciente busca
/servicios/             6 páginas   — lo que se ofrece y se cobra
/pruebas/               4 páginas   — ecg · ett · holter · esfuerzo
/articulos/             7 páginas   — blog
/legal/                 aviso-legal.html · privacidad.html · cookies.html
/img/                   todas las imágenes
```

`primera-consulta.html` es una redirección `noindex` a
`/servicios/consulta-cardiologica-elche`. No tiene nav, footer ni CSS. **No tocar.**

### Nombres de archivo

| Carpeta | Patrón | Ejemplo |
|---|---|---|
| `/motivos/` | `<sintoma>-elche.html` | `soplo-cardiaco-elche.html` |
| `/servicios/` | `<servicio>-elche.html` | `ecocardiograma-elche.html` |
| `/pruebas/` | nombre corto sin sufijo | `ett.html`, `holter.html` |
| `/articulos/` | slug descriptivo, sin `-elche` | `taquicardia-en-reposo.html` |
| `/legal/` | nombre corto | `cookies.html` |

Todo en minúsculas, guiones, sin acentos ni ñ. El slug del archivo es literalmente
la URL: se sirve sin extensión (`/motivos/soplo-cardiaco-elche`).

Imágenes en `/img/`, todas `.webp` (salvo `og.jpg`), con prefijo por sección:
`mot-` motivos · `serv-` servicios · `prueba-` pruebas · `blog-` artículos ·
`ig-1..4` grid de Instagram de la home. Marca: `logo.webp`, `perfil.webp`,
`sobre-hero.webp`, `og.jpg`.

Las imágenes de Gemini salen como PNG con extensión `.webp` y pesan 6–7 MB: hay que
convertirlas a WebP real a 1600 px de ancho antes de subirlas.

### Rutas

- Páginas de raíz: `style.css`, `img/...`
- Subcarpetas: `../style.css`, `../img/...` — **un solo nivel, nunca `../../`**
- `404.html` usa rutas absolutas (`/style.css`, `/img/...`) porque se sirve desde
  cualquier profundidad de URL.
- Enlaces internos: **siempre absolutos y sin extensión** → `/motivos/...`,
  `/servicios/...`, `/articulos/...`. La única excepción son los enlaces a `/legal/`,
  que sí llevan `.html`.

---

## 3. El `<head>`

Orden exacto, tomado de `/articulos/tension-arterial-normal-por-edad.html`, que es la
página más reciente y completa y funciona como plantilla:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="canonical" href="https://cardiolopezclemente.com/RUTA" />

    <title>…</title>
    <meta name="description" content="…">

    <meta property="og:title" content="…">
    <meta property="og:description" content="…">
    <meta property="og:url" content="https://cardiolopezclemente.com/RUTA">
    <meta property="og:type" content="article">
    <meta property="og:image" content="https://cardiolopezclemente.com/img/og.jpg">

    <link rel="stylesheet" href="../style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,400;0,600;0,700;1,400;1,600&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">

    <!-- JSON-LD: bloques separados, uno por schema -->

    <style> /* CSS específico de esta página */ </style>
<script src="/consent.js" defer></script>
</head>
```

**Reglas duras**

- `canonical` sin extensión y sin barra final, salvo la home (`.../`) y `/legal/*.html`.
- `title`: `<Tema en Title Case> | Cardiólogo Elche` en motivos y artículos ·
  `<Servicio o prueba> en Elche | Dr. López Clemente` en servicios y pruebas.
  Excepciones vivas: `disnea-cansancio` y `dolor-toracico` cierran con `| Elche`.
- `meta description`: 105–190 caracteres, en la práctica casi todas 130–160. Termina
  con `Cardiólogo en Elche.` o `Clínica Elche Salud.`
- `og:image` siempre `https://cardiolopezclemente.com/img/og.jpg`. No hay imágenes OG
  por página.
- `og:type` = `article` en todas las páginas de contenido; `website` solo en la home.
- Todas las páginas de contenido llevan además `og:locale` (`es_ES`), `og:site_name`
  y `<meta name="twitter:card" content="summary_large_image">`. Las legales, el 404 y
  `primera-consulta.html` no.
- Páginas legales, `404.html` y `primera-consulta.html` llevan
  `<meta name="robots" content="noindex, follow">` (el 404, `noindex` a secas).
- **`<script src="/consent.js" defer></script>` va en todas las páginas con nav**,
  como última línea antes de `</head>`. **Nunca añadir el snippet suelto de gtag.js**:
  duplicaría el pageview y saltaría el consentimiento.

### JSON-LD por tipo de página

Bloques `<script type="application/ld+json">` independientes, uno por schema:

| Página | Schemas |
|---|---|
| `index.html` | `WebSite` (`@id` `#website`) + `Physician` (`@id` `#physician`, con `alumniOf`, `memberOf`, `worksFor` → `MedicalClinic`, `openingHoursSpecification`) |
| `sobre-mi.html` | `Physician` completo + `BreadcrumbList` |
| `/motivos/`, `/articulos/` | `MedicalWebPage` + `BreadcrumbList` (+ `FAQPage` si la página tiene acordeón o preguntas) |
| `/pruebas/`, servicios de prueba | `MedicalProcedure` + `BreadcrumbList` |
| Servicios de consulta | `MedicalBusiness` + `BreadcrumbList` |
| `preguntas-frecuentes.html` | `FAQPage` (22 preguntas) + `BreadcrumbList` |
| `/legal/` | solo `BreadcrumbList` |

Dentro de `MedicalWebPage` / `MedicalProcedure`:
`author` (o `provider`) = objeto `Physician` con
`@id: https://cardiolopezclemente.com/#physician`, `medicalSpecialty: "Cardiology"`,
`telephone: "+34662637540"`, `priceRange: "€€"`, `image` → `perfil.webp`,
`url` → `/sobre-mi` y `address` `PostalAddress` con el NAP canónico.
Además: `medicalAudience: ["Patient"]`, `about` → `MedicalCondition`,
`inLanguage: "es-ES"`, `isPartOf` → `{"@id": ".../#website"}`.

En `/articulos/` se añaden además `datePublished` y `dateModified` (`AAAA-MM-DD`),
justo antes de `inLanguage`. La fecha **no** se muestra en la página: vive solo en el
JSON-LD, para no envejecer visualmente contenido que es atemporal.

`BreadcrumbList` de 3 niveles: Inicio → sección → página.
Segundo nivel según carpeta: `/#blog` para artículos y pruebas, `/#servicios` para
servicios, «Motivos de consulta» para motivos.

---

## 4. Estructura del `<body>`

```
<nav>                                   ← idéntico en todas las páginas
<header class="hero hero-page">         ← "hero hero-page" en interiores; "hero" en la home
  <div class="hero-content container">
    <p class="location-top">Cardiólogo en Elche · Clínica Elche Salud</p>
    <h1>Texto <span class="text-red">destacado</span></h1>
    <p class="hero-p">subtítulo de una línea</p>
<section class="section"><div class="container"><div class="service-content">
    ... contenido: h2.section-title + p + componentes ...
<section class="section bg-light"> ... bloques secundarios ...
<section class="section bg-light cta-section">   ← CTA de conversión
<section class="section container">     ← "Otros X": 3 tarjetas relacionadas
<footer>                                ← idéntico en todas las páginas
<div class="cta-movil">                 ← solo en /motivos/ y /servicios/, tras el footer
```

- Un solo `<h1>` por página, en el hero, con una palabra en `<span class="text-red">`.
- Todos los `<h2>` de contenido llevan `class="section-title"`.
- Subtítulos internos: `<h3>` dentro de tarjetas, o `p.sub-h3`.
- El nav y el footer son bloques fijos: se copian literalmente. Lo único que cambia
  en el nav es la ruta del logo (`img/logo.webp` en raíz, `../img/logo.webp` en
  subcarpetas, `/img/logo.webp` en el 404).
- La `cta-movil` (barra flotante Llamar / Pedir cita) va justo antes de `</body>`,
  solo en motivos y servicios. Artículos y pruebas no la llevan.
- Toda `<img>` lleva `width`, `height`, `alt` y `loading="lazy"`. Sin excepción.

### CTA final — patrón fijo

```html
<section class="section bg-light cta-section">
  <div class="container">
    <h2 class="section-title">¿Pregunta directa al lector?</h2>
    <p class="lead">Una o dos frases. Consulta cardiológica en Elche.</p>
    <div class="cta-group">
      <a href="https://www.doctoralia.es/jose-carlos-lopez-clemente/cardiologo-dietista-nutricionista/elche" target="_blank" class="btn-main">Pedir cita en Doctoralia</a>
      <a href="/RUTA-RELACIONADA" class="btn-sub">Texto secundario</a>
    </div>
  </div>
</section>
```

`btn-main` va siempre a Doctoralia. `btn-sub` a la página interna más relevante.

### Artículos: bloques propios

- `div.articulo-meta` bajo el `h1`, con `span.articulo-tag` (`Categoría · Categoría`)
  y `span.articulo-autor` (`Por <strong>Dr. José Carlos López Clemente</strong> ·
  Cardiólogo y Dietista-Nutricionista`). **No se muestra fecha.**
- `div.referencias` antes del CTA, con `<h2>Referencias</h2>` y `<ol>` de citas en
  formato Vancouver abreviado (autor, título, revista en `<em>`, año, volumen, páginas).
- `a.ig-promo`: bloque negro que enlaza a un post concreto de Instagram, con
  `target="_blank" rel="noopener"`. Va tras el último `h2` de contenido.
- Sección final `Otros artículos` con `div.articles-grid` y 3 `a.article-card`.
  **Va después de la `cta-section` y antes del `<footer>`**, no antes del CTA.

Equivalentes por carpeta: `Otros motivos de consulta`, `Otras pruebas diagnósticas`,
`Otros servicios`.

---

## 5. Nav y footer

Se copian tal cual desde cualquier página existente. El footer es byte a byte
idéntico en las 33 páginas con nav; el NAP no varía **ni un carácter**:

```
Clínica Elche Salud · Pl. del Bisbe Siuri, Entresuelo B · 03201 Elche (Alicante) · 662 63 75 40
```

Teléfono en enlaces: `tel:+34662637540`. Colegiado nº 03/3009562.
Enlace de cita, siempre este y con `target="_blank"`:
`https://www.doctoralia.es/jose-carlos-lopez-clemente/cardiologo-dietista-nutricionista/elche`

---

## 6. Sistema de CSS

Dos capas. No hay una tercera.

**`style.css`** (global, 23 secciones numeradas en comentarios): variables, reset,
tipografía, layout, navegación, hero, botones, section titles, bio, tarjetas de
servicio y artículo, sección Instagram, blog/categorías, info cards, timeline, tags,
CTA, footer, páginas secundarias, información práctica, utilidades y responsive, menú
hamburguesa, CTA flotante móvil.

Clases globales que se usan en casi todas las páginas y **no se redefinen**:
`.container` `.section` `.bg-light` `.hero` `.hero-page` `.hero-content`
`.location-top` `.hero-p` `.text-red` `.section-title` `.lead` `.service-content`
`.cta-section` `.cta-group` `.btn-main` `.btn-sub` `.info-card` `.service-list`
`.articles-grid` `.article-card` `.category-tag` `.read-more` `.mobile-br`
`.cta-movil` + nav y footer.

**Bloque `<style>` inline por página**: todo lo específico de esa página. Es donde
viven los componentes (`.alarma`, `.tabla-ta`, `.mecanismos-grid`, `.checklist-grid`,
`.score-tabla`, `.lipid-tabla`, `.nyha-tabla`, `.prueba-badges`, `.ig-promo`,
`.referencias`, `.stats-grid`, `.destacado`, `.fases-lista`, `.pasos-lista`…).

Consecuencia práctica: un componente se replica copiando **su CSS y su HTML** desde
la página que ya lo usa. Nada de esto está en `style.css` y no hay que moverlo allí.

Variables de marca (`:root` en `style.css`):
`--rojo` #b80101 · `--rojo-oscuro` #8b0000 · `--negro` #0f0f0f · `--blanco` #ffffff ·
`--crema` #faf6f0 · `--crema-claro` #fdfaf4 · escala `--gris-100..900` ·
`--font-display` Fraunces · `--font-body` DM Sans · `--space-*` · `--radius-*` ·
`--sombra-*` · `--transition`.
Usar siempre las variables, nunca el hex literal.

### Componentes disponibles (y dónde copiarlos)

| Componente | Página de referencia |
|---|---|
| Acordeón FAQ con JS | `preguntas-frecuentes.html` |
| Bloque de alarma con cabecera roja | `articulos/tension-arterial-normal-por-edad.html` |
| Lista de alarma con puntos | `motivos/insuficiencia-cardiaca-elche.html` |
| Tabla con código de colores | `motivos/hipertension-arterial-elche.html` (`.ta-tabla`) |
| Tabla SCORE2 y grid FRCV | `servicios/riesgo-cardiovascular-elche.html` |
| Tabla de objetivos LDL | `motivos/colesterol-alto-elche.html` |
| Grid de mecanismos 2×2 | `articulos/apnea-sueno.html` |
| Pasos numerados verticales | `servicios/ecocardiograma-elche.html` |
| Checklist numerado | `motivos/dolor-toracico-elche.html` |
| Badges de prueba | `pruebas/ecg.html` |
| Tags tipo pastilla | `servicios/holter-ecg-elche.html` (`.cuando-tag`) |
| Diario de síntomas (bloque negro) | `servicios/holter-ecg-elche.html` |
| Stats negras / macro grid % | `articulos/dieta-japonesa.html`, `articulos/dieta-dash.html` |
| Bloque destacado con borde rojo | `articulos/taquicardia-en-reposo.html` (`.destacado`) |
| `ig-promo` | `articulos/tension-arterial-normal-por-edad.html` |
| Sección Instagram de la home | `index.html` |

---

## 7. Tono y reglas editoriales

El lector tipo es un paciente con conocimiento basal muy bajo. Esto **no** es
divulgación técnica ni contenido científico.

- Lenguaje accesible, frases cortas, sin jerga sin explicar. No alarmista.
- Segunda persona («tus cifras», «si notas»), nunca «el paciente».
- Se admiten cifras y clasificaciones cuando aportan (NYHA, SCORE2, objetivos LDL),
  siempre con una frase que las traduzca.
- Los artículos cierran con `Referencias` reales (guías ESC, documentos SEA…). Los
  motivos y servicios, no.

**No revertir:**

- Duración de consulta: **siempre 60 minutos**, nunca un rango.
- Nutrición: **«orientación y resolución de dudas»**, nunca «plan nutricional
  individualizado».
- Reconocimiento cardiológico: omisión deliberada de cualquier mención a certificados
  oficiales o aptitudes.
- Segunda opinión: tono colaborativo, nunca competitivo con otros médicos.
- Una página por intención de búsqueda, no por tema. Si dos páginas comparten más de
  dos secciones, se fusionan.

---

## 8. Enlazado interno

- Cada motivo enlaza a la prueba que lo resuelve y al servicio que lo cubre.
- Cada servicio y cada prueba enlazan de vuelta a los motivos relacionados.
- Los artículos enlazan a motivos y servicios dentro del texto, no solo al final.
- Sección de 3 tarjetas relacionadas al final de motivos, servicios, pruebas y
  artículos.
- La home lista **todas** las páginas de las cuatro carpetas: 6 servicios,
  9 motivos, 4 pruebas y los 7 artículos. Publicar algo nuevo implica añadir su
  tarjeta a `index.html`.
- Nada debe quedar con 0 enlaces entrantes fuera del nav y el footer.

---

## 9. Analítica y consentimiento

GA4 `G-E78Z4BSEDG`, cargado **exclusivamente** desde `/consent.js`, que implementa
Consent Mode v2 (todo denegado por defecto), pinta el banner de cookies, guarda la
decisión en `localStorage` (`clc-cookie-consent`) y dispara por delegación de eventos:

- `clic_llamar` — cualquier `href` que empiece por `tel:`
- `clic_doctoralia` — cualquier `href` que contenga `doctoralia.es`

Los eventos solo llegan a GA4 si el usuario aceptó. `window.clcGestionarCookies()`
reabre el banner desde `/legal/cookies.html`.

Consecuencia: los botones de llamada y de cita **no llevan `onclick` de tracking**.
Basta con que el `href` sea el correcto.

---

## 10. Registros

Dos archivos markdown en la raíz, ambos de mantenimiento manual:

- **`articulos-web.md`** — banco de temas del blog. Sección `## Publicados` numerada,
  con fecha `DD/MM/AAAA` en las entradas recientes; luego `## Pendientes — con
  material en la web` y `## Pendientes — hay que generar el contenido`.
- **`posts-google.md`** — banco de temas de Google Business Profile, con marca
  `— USADO (DD/MM/AAAA)`.

---

## 11. Checklist al publicar una página nueva

1. Crear el HTML copiando `/articulos/tension-arterial-normal-por-edad.html` (o la
   página homóloga de su carpeta) y ajustar rutas relativas según el nivel.
2. `head` completo: canonical, title, description, OG, fuentes, `style.css`,
   JSON-LD del tipo que corresponda, `<style>` inline, `consent.js`.
3. Nav y footer copiados literalmente. NAP sin tocar.
4. Imagen en `/img/` con el prefijo de su sección, convertida a WebP real a 1600 px,
   con `width`, `height`, `alt` y `loading="lazy"`.
5. Sección CTA final con Doctoralia en `btn-main`.
6. En motivos y servicios: añadir `div.cta-movil` antes de `</body>`.
7. Bloque de 3 tarjetas relacionadas (`Otros X`) entre la `cta-section` y el
   `<footer>`. Aprovecharlo para enlazar páginas con pocos enlaces entrantes.
8. **`sitemap.xml`**: añadir la `<url>` con `<loc>` sin extensión, `<lastmod>` en
   `AAAA-MM-DD` y `<priority>` según el tipo — 0.9 consulta cardiológica ·
   0.8 servicios, motivos y páginas principales · 0.7 artículos · 0.6 pruebas.
   (Los tres artículos más antiguos quedaron en 0.6; el criterio vigente es 0.7.)
9. **`index.html`**: añadir la tarjeta en la rejilla de su sección.
10. **Enlaces internos entrantes**: enlazar la página nueva desde al menos dos
    páginas existentes relacionadas.
11. **Registro**: mover el tema a `## Publicados` en `articulos-web.md` con la fecha,
    o marcar `— USADO` en `posts-google.md`.
12. Solicitar indexación de la URL nueva en Google Search Console.

Las páginas legales **no** van al sitemap (son `noindex`).

---

## 12. No tocar

- `primera-consulta.html` — redirección `noindex` en producción.
- El NAP del footer, en ningún carácter.
- El `@id` `#physician` y `#website` de los JSON-LD: son las anclas del grafo.
- `consent.js` salvo que cambie la política de cookies o los eventos de conversión.
