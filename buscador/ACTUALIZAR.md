# Cómo actualizar el buscador (instrucciones para Claude)

Buscador privado: https://claude.ai/artifact/MxbCJi2eAMmTMZ7WhAKH3E
Rama de trabajo: `claude/stoic-fermat-jznhyy` del repositorio `smmaureira-tech/entrega-preliminar-7`.

1. Ubícate en la rama `claude/stoic-fermat-jznhyy` (con `git fetch` y `git checkout`) y trae lo último.
2. Reúne las ofertas (tarda unos 5 minutos; respeta las pausas del script):
   `python3 herramientas/actualizar_ofertas.py /tmp/ofertas.json buscador/traducciones.json`
   - Remotive pide máximo 4 consultas al día. Si ya se consultó hoy, usa `SALTAR=Remotive`.
   - Si una fuente da error, sigue con las demás y menciónalo en el resumen.
3. Si se creó `buscador/traducciones.json.faltan.txt`, traduce cada título al español (formas inclusivas «/a», sin traducir nombres de tecnologías ni de empresas). Agrégalos a `buscador/traducciones.json` (objeto JSON título original → español). Después vuelve a aplicar las traducciones sin consultar las fuentes otra vez:
   `python3 -c "import json,importlib.util as u;s=u.spec_from_file_location('a','herramientas/actualizar_ofertas.py');m=u.module_from_spec(s);s.loader.exec_module(m);d=json.load(open('/tmp/ofertas.json'));print('faltan',len(m.traducir(d['ofertas'],'buscador/traducciones.json')));json.dump(d,open('/tmp/ofertas.json','w'),ensure_ascii=False,separators=(',',':'))"`
   Debe decir `faltan 0`. Borra `traducciones.json.faltan.txt`.
4. Revisa el resultado: cantidad total de ofertas, cuántas están en español (`idioma == "es"`) y cuántas son de los últimos 7 días. Si hay menos de 100 ofertas en total, algo falló: no publiques y explica el problema.
5. Publica con la herramienta Artifact: primero `action: "read"` del enlace de arriba; después publica `file_path: buscador/pagina.html` con `url` igual al enlace y `files: {"ofertas.json": "/tmp/ofertas.json"}`. No cambies el diseño de la página.
6. Haz commit y push de `buscador/traducciones.json` a la rama (nunca subas `ofertas.json`).
7. Termina con un resumen breve en español: ofertas totales, ofertas en español, fuentes con error.
