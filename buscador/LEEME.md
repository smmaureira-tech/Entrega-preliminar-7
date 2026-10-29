# Buscador privado de ofertas remotas

Página para uso personal. Muestra ofertas de trabajo remoto reales y permite buscarlas por cargo (en español o inglés), área, país, fecha y fuente.

- `pagina.html`: la página del buscador, publicada como Artifact privado en claude.ai.
- `../herramientas/actualizar_ofertas.py`: reúne las ofertas y genera `ofertas.json`.
  El archivo `ofertas.json` no se guarda en el repositorio.

## Fuentes (solo canales oficiales y permitidos)
| Fuente | Canal | Condiciones |
|---|---|---|
| Get on Board | API pública v0 | Su robots.txt permite el uso «reference» y prohíbe usar su contenido para entrenar IA. Aquí solo se muestran datos básicos con enlace a la oferta. |
| Himalayas | API pública (`/jobs/api/search`) | Búsqueda por país (CL, MX, AR, CO, PE, BR, UY). |
| We Work Remotely | RSS oficial | — |
| Working Nomads | API `exposed_jobs` | Solo las 38 ofertas más recientes. |
| Jobicy | API pública (`geo=latam`) | Pide citar a Jobicy y enlazar la oferta original. Su robots.txt permite el uso por IA. |
| Remotive | API pública | Pide como máximo 4 consultas al día, citar a Remotive y enlazar la oferta. Las ofertas llegan con 24 h de retraso. |

Sin búsqueda automática (sitios sin API, o con reglas que lo impiden): Jobspresso, cuyo robots.txt bloquea su feed; Jobgether; Wellfound; Kaszek y LinkIT. La página los muestra como enlaces.

## Idioma y traducciones
El idioma de cada oferta se detecta por su descripción, no solo por el título. Al 29/10/2026 había 129 ofertas remotas en español, sobre todo de Get on Board y Himalayas. La página muestra primero «Solo en español». La página muestra el título traducido al español, con el original debajo, y tiene un filtro «Idioma de la oferta». Las traducciones están en `traducciones.json` (título original → español). Al actualizar, los títulos nuevos sin traducción quedan listados en `traducciones.json.faltan.txt`, y Claude los traduce antes de publicar.

## Actualizar las ofertas
Pídele a Claude: «actualiza las ofertas del buscador». Claude ejecuta:

```
python3 herramientas/actualizar_ofertas.py ofertas.json buscador/traducciones.json
# Si Remotive ya se consultó 4 veces ese día:
SALTAR=Remotive python3 herramientas/actualizar_ofertas.py ofertas.json buscador/traducciones.json
```

Luego vuelve a publicar el Artifact con el nuevo `ofertas.json`. La actualización no es automática: la página muestra la fecha en que se reunieron las ofertas.
