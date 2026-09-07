# cardiolopezclemente.com

Web personal del Dr. José Carlos López Clemente, cardiólogo en Elche
(Clínica Elche Salud). HTML estático, sin framework ni CMS.

Publicación: GitHub Pages + Cloudflare. La rama `main` es producción.

**Antes de tocar nada, leer [`CLAUDE.md`](CLAUDE.md)**: recoge la plantilla de
página, las convenciones de nombres y rutas, el sistema de CSS, las reglas
editoriales y el checklist de publicación.

## Estructura

| Ruta | Contenido |
|---|---|
| `/` | home, sobre-mí, FAQ, 404, legales |
| `/motivos/` | páginas por síntoma o motivo de consulta |
| `/servicios/` | servicios de la consulta |
| `/pruebas/` | fichas de pruebas diagnósticas |
| `/articulos/` | blog |
| `/img/` | imágenes (WebP, máx. 1600 px de ancho) |

## Archivos clave

- `style.css` — CSS global. Lo específico de cada página va en su `<style>` inline.
- `consent.js` — banner de cookies, Consent Mode v2 y GA4 (`G-E78Z4BSEDG`).
  Es la **única** vía de carga de GA4.
- `sitemap.xml` — 29 URLs. Hay que actualizarlo en cada publicación.
- `articulos-web.md` / `posts-google.md` — bancos de temas y registro de publicado.

## Validación

Antes de publicar un lote de cambios:

```
python3 _tools/check.py
```

Comprueba enlaces rotos, páginas huérfanas, JSON-LD, metadatos, sitemap,
peso de imágenes y las reglas editoriales. Ver `CLAUDE.md`.
