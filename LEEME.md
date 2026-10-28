# Trabajo remoto: directorio de sitios por área

Página de un solo archivo (`index.html`) que organiza sitios de empleo remoto por área o rol. Es un recurso voluntario para compañeras de Latinoamérica.

**Lo que hace:** muestra los sitios con descripción, enlace y etiquetas. Permite elegir un área, buscar por palabra y filtrar por idioma, región y costo. También permite copiar un enlace a una búsqueda (por ejemplo, solo «Diseño UX/UI») para compartirlo.

**Lo que NO hace:** no tiene suscripciones, no envía alertas ni correos y no publica ofertas. Tampoco guarda datos de nadie. Solo recuerda en el navegador de cada persona su último filtro.

---

## 1. Probarla en tu computadora

1. Descarga `index.html`. En GitHub: abre el archivo y pulsa el botón **Download raw file**.
2. Haz doble clic en el archivo. Se abre en tu navegador. No necesita internet ni instalar nada.
3. Después de editarlo, guarda el archivo y recarga la página (F5).

## 2. Agregar, cambiar o quitar sitios

Todo está al principio de `index.html`, en la sección **LISTA DE SITIOS**.

Para agregar un sitio, copia este bloque dentro de `const SITIOS = [` … `];` y cambia los textos:

```js
{
  nombre: "Nombre del sitio",
  url: "https://direccion-del-sitio.com",
  descripcion: "Qué ofrece y para quién es útil.",
  areas: ["Diseño UX/UI"],
  idioma: ["Español", "Inglés"],
  region: "Latinoamérica",
  costo: "Gratis",
  verificado: "2026-10-28",
  ultimaOferta: "2026-10-27"
},
```

Reglas:
- Los textos van **entre comillas** y cada línea termina con **coma**.
- El nombre de cada área debe escribirse **exactamente** como en la lista `AREAS`.
- Para quitar un sitio, borra su bloque completo, desde `{` hasta `},`.
- Si la página queda en blanco después de editar, casi siempre falta una coma o unas comillas. Revisa el último bloque que tocaste.

Para editar desde GitHub, sin descargar nada: abre `index.html`, pulsa el lápiz (**Edit**), haz los cambios y pulsa **Commit changes**. Si la página está publicada, se actualiza en uno o dos minutos.

- `verificado` es **obligatorio**. Si un sitio no tiene esa fecha, la página no lo muestra. Así ningún sitio sin comprobar llega al directorio.

**Mantenimiento:** sigue la rutina de `VERIFICACION.md`.

## 3. Publicarla gratis con GitHub Pages

1. En el repositorio, ve a **Settings → Pages**.
2. En **Branch**, elige la rama donde está `index.html` y la carpeta `/ (root)`. Pulsa **Save**.
3. En uno o dos minutos aparecerá el enlace público, con la forma `https://<tu-usuario>.github.io/<repositorio>/`.

Notas:
- Para usar GitHub Pages gratis, el repositorio debe ser **público**. Todo lo que contenga el repositorio será visible.
- La página no usa servicios externos, cookies ni seguimiento, así que no recoge datos de quien la visita.

## 4. Formulario de sugerencias (opcional)

Crea un Google Form o un formulario de Tally y pega su enlace en `FORMULARIO_SUGERENCIAS = "";`, entre las comillas. Aparecerá un enlace al pie de la página. Si el formulario pide correo u otros datos personales, indica para qué los usarás.
