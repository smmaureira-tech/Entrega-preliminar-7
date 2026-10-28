# Verificación de sitios

## Estado al 28/10/2026: ningún sitio verificado todavía

El entorno donde trabaja Claude no tiene permiso para abrir estos sitios: la política de red de la sesión rechaza la conexión. Por eso **ninguna fila está verificada** y el directorio sigue vacío. Nada de lo que aparece abajo se ha comprobado abriendo el sitio.

- «Origen: tu lista» = enviado por la autora del recurso (captura de LinkedIn). La descripción de áreas viene de esa publicación, no de una comprobación.
- «Origen: propuesta» = sitio sugerido por Claude como candidato. Solo es una idea para revisar.

| # | Sitio | URL | Origen | Áreas o roles (según la fuente, sin verificar) | Alcance geográfico | Oferta más reciente comprobada | Fecha de revisión | Evidencia | Decisión |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Kickresume (enlace corto) | kickresu.me/ZHTaHiF | Tu lista | Herramienta para crear CV, no es una bolsa de empleo | — | — | — | No verificado. El enlace corto oculta la dirección final y podría ser un enlace de referido | **Excluir** del directorio de empleos (se puede retomar en una futura sección de herramientas) |
| 2 | Wellfound | wellfound.com | Tu lista | Startups y tecnología | No verificado | No verificado | — | No se pudo abrir | **Pendiente** |
| 3 | Working Nomads | workingnomads.com | Tu lista | Tech, marketing, diseño, ventas | No verificado | No verificado | — | No se pudo abrir | **Pendiente** |
| 4 | Jobspresso | jobspresso.co | Tu lista | Tecnología, marketing, atención al cliente, producto | No verificado | No verificado | — | No se pudo abrir | **Pendiente** |
| 5 | JustRemote | justremote.co | Tu lista | Varias categorías | No verificado | No verificado | — | No se pudo abrir | **Pendiente** |
| 6 | SkipTheDrive | skipthedrive.com | Tu lista | Tecnología, ventas, finanzas, RR. HH. | No verificado | No verificado | — | No se pudo abrir | **Pendiente** |
| 7 | RemoteJobs.io | remotejobs.io | Tu lista | Varios sectores y niveles | No verificado | No verificado | — | No se pudo abrir | **Pendiente** |
| 8 | NoDesk | nodesk.co | Tu lista | Tecnología y startups | No verificado | No verificado | — | No se pudo abrir | **Pendiente** |
| 9 | Jobgether | jobgether.com | Tu lista | Varias; recomendación según perfil | No verificado | No verificado | — | No se pudo abrir | **Pendiente** |
| 10 | EU Remote Jobs | euremotejobs.com | Tu lista | Varias | Según tu lista, orientado a Europa | No verificado | — | No se pudo abrir | **Pendiente.** Probablemente excluir si solo acepta residentes de Europa |
| 11 | LinkIT | Falta la dirección | Tu mensaje (confirmaste que quieres agregarlo) | — | — | — | — | Una búsqueda web no encontró un sitio con este nombre; falta la URL exacta | **Pendiente** |
| 12 | Get on Board | getonbrd.com | Propuesta | Tecnología | Latinoamérica | No verificado | — | Solo resultados de búsqueda (blog del sitio y prensa) | **Pendiente** |
| 13 | We Work Remotely | weworkremotely.com | Propuesta | Por comprobar | Por comprobar | No verificado | — | Ninguna | **Pendiente** |
| 14 | Remotive | remotive.com | Propuesta | Por comprobar | Por comprobar | No verificado | — | Ninguna | **Pendiente** |
| 15 | Himalayas | himalayas.app | Propuesta | Por comprobar | Por comprobar | No verificado | — | Ninguna | **Pendiente** |
| 16 | Torre | torre.ai | Propuesta | Por comprobar | Por comprobar | No verificado | — | Ninguna | **Pendiente** |
| 17 | Workana (freelance) | workana.com | Propuesta | Por comprobar | Latinoamérica (por comprobar) | No verificado | — | Ninguna | **Pendiente** |

---

## Criterios para decidir

**Incluir** solo si se cumple todo esto:
1. El sitio abre y muestra ofertas remotas reales.
2. Hay ofertas con **fecha visible**, y la más reciente tiene **menos de 30 días**.
3. Al abrir 2 ofertas al azar, el enlace funciona y lleva a la oferta o a la empresa.
4. Se puede saber si acepta postulantes desde Latinoamérica, o el sitio permite filtrar por región.
5. Postular no cuesta dinero. Si tiene funciones de pago, se indica en la ficha.

**Excluir** si el sitio está caído, duplica otro de la lista, no tiene ofertas comprobables, su última oferta tiene más de 60 días o pide pagos para postular.

**Pendiente** si falta algún dato. Un sitio pendiente **no se publica**.

---

## Rutina de verificación (una vez al mes, unos 3 minutos por sitio)

Una verificación vale **solo para el día en que se hizo**. Las ofertas cambian a diario y un sitio que hoy funciona puede cerrar mañana. Por eso cada ficha de la página muestra su fecha de verificación.

Para cada sitio:
1. Ábrelo en el navegador, en modo incógnito para que no influyan tus sesiones.
2. Busca la oferta más reciente y anota su fecha.
3. Abre 2 ofertas y comprueba que el enlace funciona.
4. Revisa si aceptan postulantes desde Latinoamérica.
5. En `index.html`, actualiza `verificado` (la fecha de hoy) y `ultimaOferta`. Si no cumple los criterios, borra el bloque del sitio.
6. Actualiza su fila en esta tabla.

Ayuda opcional: más adelante se puede programar un revisor automático y gratuito en GitHub Actions, que avise cuando un enlace deja de abrir. Solo comprobaría que los enlaces cargan. No revisaría si hay ofertas nuevas, ni extraería contenido de los sitios. La revisión de ofertas sigue siendo manual.
