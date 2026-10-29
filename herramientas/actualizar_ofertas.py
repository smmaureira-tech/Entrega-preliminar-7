#!/usr/bin/env python3
"""Reúne ofertas de empleo remoto desde fuentes que las publican abiertamente
(API o RSS oficiales) y las guarda en un archivo ofertas.json para el buscador.

Uso:  python3 herramientas/actualizar_ofertas.py salida/ofertas.json [traducciones.json]

Las traducciones al español de los títulos se leen de traducciones.json (título -> español).
Los títulos sin traducción quedan listados en traducciones.json.faltan.txt.

Reglas que respeta:
- Solo usa canales oficiales (API pública o RSS) y respeta robots.txt.
- Guarda solo datos básicos (cargo, empresa, lugar, fecha y enlace) y enlaza a la oferta original.
- Hace pocas consultas, con pausas entre ellas. Remotive pide como máximo 4 consultas al día.
"""
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

UA = "TrabajoRemotoLatAm/1.0 (uso personal; buscador privado de ofertas)"
DIAS = 30  # solo ofertas publicadas en los últimos 30 días
AHORA = datetime.now(timezone.utc)
LIMITE = AHORA - timedelta(days=DIAS)


def get(url, kind="json"):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=40) as r:
        data = r.read()
    time.sleep(1.0)  # pausa de cortesía entre consultas
    return json.loads(data) if kind == "json" else data


def norm(s):
    s = unicodedata.normalize("NFD", str(s or "").lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


# --- Región ---------------------------------------------------------------
LATAM = {
    "argentina": "Argentina", "bolivia": "Bolivia", "brasil": "Brasil", "brazil": "Brasil",
    "chile": "Chile", "colombia": "Colombia", "costa rica": "Costa Rica", "cuba": "Cuba",
    "ecuador": "Ecuador", "el salvador": "El Salvador", "guatemala": "Guatemala",
    "honduras": "Honduras", "mexico": "México", "nicaragua": "Nicaragua", "panama": "Panamá",
    "paraguay": "Paraguay", "peru": "Perú", "puerto rico": "Puerto Rico",
    "dominican republic": "Rep. Dominicana", "republica dominicana": "Rep. Dominicana",
    "uruguay": "Uruguay", "venezuela": "Venezuela",
}
LATAM_ZONA = ["latam", "latin america", "latinoamerica", "america latina", "south america",
              "sudamerica", "central america", "americas", "lat am"]
MUNDO = ["anywhere in the world", "worldwide", "world wide", "global", "cualquier pais", "everywhere"]


def region(texto, paises=None):
    """Devuelve (abierta_a_latam, países_latam, etiqueta_lugar)."""
    t = norm(texto)
    encontrados = sorted({v for k, v in LATAM.items() if re.search(r"\b" + k + r"\b", t)})
    if paises is not None:  # lista explícita de países (Himalayas)
        if not paises:
            return True, [], "Cualquier país"
        lat = sorted({v for p in paises for k, v in LATAM.items() if re.search(r"\b" + k + r"\b", norm(p))})
        if not lat:
            return False, [], resumir(paises)
        return True, lat, resumir(paises)
    if encontrados or any(z in t for z in LATAM_ZONA):
        return True, encontrados, texto.strip() or "Latinoamérica"
    restringe = re.search(r"\b(only|usa|us|u\.s\.|united states|canada|europe|uk|emea|apac|asia|india|"
                          r"japan|australia|cet|time zone)\b", t)
    if not t.strip() or (any(m in t for m in MUNDO) and not restringe):
        return True, [], texto.strip() or "Cualquier país"
    return False, [], texto.strip()


def resumir(paises):
    if len(paises) <= 4:
        return ", ".join(paises)
    return f"{len(paises)} países"


# --- Área -----------------------------------------------------------------
AREAS = [
    ("Ventas", ["sales", "account executive", "account manager", "business development", "sdr", "bdr",
                "ventas", "comercial", "ejecutiv", "vendedor", "key account"]),
    ("Atención al cliente", ["customer support", "customer service", "customer success", "support",
                             "soporte", "atencion", "help desk", "helpdesk", "call center", "cx "]),
    ("Diseño UX/UI", ["design", "designer", "ux", "ui ", "disen", "grafic", "creative"]),
    ("Análisis de datos", ["data", "datos", "analyst", "analista", "analytics", "machine learning",
                           "bi ", "scientist", "ml ", "ai engineer"]),
    ("Marketing y contenido", ["marketing", "content", "contenido", "seo", "copywrit", "writer",
                               "redact", "social media", "community", "growth", "brand"]),
    ("Producto y proyectos", ["product manager", "product owner", "project manager", "program manager",
                              "scrum", "proyect", "producto", "operations", "operaciones"]),
    ("Recursos humanos", ["recruit", "talent", "people", "hr ", "human resources", "reclut",
                          "recursos humanos", "rrhh"]),
    ("Desarrollo web", ["developer", "engineer", "desarroll", "programad", "software", "frontend",
                        "front-end", "backend", "back-end", "full stack", "fullstack", "devops", "qa",
                        "programming", "web", "mobile", "ios", "android", "sre"]),
]


def areas(*textos):
    t = " " + norm(" ".join(str(x) for x in textos if x)) + " "
    hits = [a for a, ks in AREAS if any(k in t for k in ks)]
    return hits or ["Otras áreas"]


def oferta(fuente, titulo, empresa, url, fecha, lugar_txt, categoria="", paises=None, salario="", desc=""):
    if not url or not titulo or not fecha or fecha < LIMITE:
        return None
    lat, lat_paises, lugar = region(lugar_txt, paises)
    return {
        "idioma": idioma_texto(desc) if desc else idioma(titulo),
        "titulo": re.sub(r"\s+", " ", titulo).strip(),
        "empresa": (empresa or "").strip(),
        "url": url,
        "fecha": fecha.astimezone(timezone.utc).strftime("%Y-%m-%d"),
        "lugar": lugar,
        "latam": lat,
        "paises": lat_paises,
        "areas": areas(titulo, categoria),
        "categoria": categoria or "",
        "salario": salario,
        "fuente": fuente,
    }


# --- Fuentes --------------------------------------------------------------
def getonbrd():
    out = []
    cats = [c["id"] for c in get("https://www.getonbrd.com/api/v0/categories?per_page=100")["data"]]
    for cat in cats:
        page = 1
        while page <= 3:
            u = (f"https://www.getonbrd.com/api/v0/categories/{cat}/jobs?per_page=100&page={page}"
                 "&expand=%5B%22company%22%5D")
            d = get(u)
            for j in d["data"]:
                a = j["attributes"]
                if not a.get("remote"):
                    continue
                comp = ((a.get("company") or {}).get("data") or {}).get("attributes", {}).get("name", "")
                paises = [p for p in (a.get("countries") or []) if p and p != "Remote"]
                if a.get("remote_modality") == "fully_remote":
                    lugar = "Cualquier país"
                elif paises:
                    lugar = ", ".join(paises)
                else:  # remoto local: solo para quienes viven en ciertos países de la región
                    lugar = "Latinoamérica (solo algunos países; revisa la oferta)"
                sal = ""
                if a.get("min_salary") and a.get("max_salary"):
                    sal = f"USD {a['min_salary']:,}–{a['max_salary']:,} / mes".replace(",", ".")
                o = oferta("Get on Board", a.get("title"), comp, j.get("links", {}).get("public_url"),
                           datetime.fromtimestamp(a["published_at"], timezone.utc), lugar,
                           a.get("category_name", ""), salario=sal,
                           desc=(a.get("description") or "") + " " + (a.get("functions") or ""))
                if o:
                    out.append(o)
            if page >= d.get("meta", {}).get("total_pages", 1):
                break
            page += 1
    return out


def himalayas():
    out = []
    for pais, paginas in [("CL", 12), ("MX", 10), ("AR", 10), ("CO", 10), ("PE", 6), ("UY", 5), ("EC", 5),
                          ("CR", 5), ("GT", 3), ("DO", 3), ("VE", 3), ("BO", 3), ("PY", 3), ("PA", 3), ("BR", 3)]:
        for page in range(1, paginas + 1):
            d = get(f"https://himalayas.app/jobs/api/search?country={pais}&sort=recent&page={page}")
            for j in d.get("jobs", []):
                sal = ""
                if j.get("minSalary") and j.get("currency"):
                    per = {"year": "año", "month": "mes", "hour": "hora"}.get(j.get("salaryPeriod") or "", "")
                    sal = f"{j['currency']} {int(j['minSalary']):,}".replace(",", ".") + \
                          (f"–{int(j['maxSalary']):,}".replace(",", ".") if j.get("maxSalary") else "") + \
                          (f" / {per}" if per else "")
                o = oferta("Himalayas", j.get("title"), j.get("companyName"),
                           j.get("applicationLink") or j.get("guid"),
                           datetime.fromtimestamp(int(j["pubDate"]), timezone.utc), "",
                           " ".join(j.get("categories") or []), paises=j.get("locationRestrictions") or [],
                           salario=sal, desc=j.get("description") or j.get("excerpt") or "")
                if o:
                    out.append(o)
    return out


def weworkremotely():
    out = []
    root = ET.fromstring(get("https://weworkremotely.com/remote-jobs.rss", "xml"))
    for it in root.iter("item"):
        f = {c.tag: (c.text or "") for c in it}
        empresa, _, titulo = f.get("title", "").partition(": ")
        reg, pais_txt = f.get("region", ""), f.get("country", "")
        paises = [re.sub(r"[^\w .'-]", "", x).strip() for x in re.split(r",| and ", pais_txt) if x.strip()]
        paises = [x for x in paises if x]
        if "only" in reg.lower():
            o = oferta("We Work Remotely", titulo or f.get("title"), empresa if titulo else "", f.get("link"),
                       parsedate_to_datetime(f["pubDate"]), reg, f.get("category", ""), desc=f.get("description", ""))
        else:
            o = oferta("We Work Remotely", titulo or f.get("title"), empresa if titulo else "", f.get("link"),
                       parsedate_to_datetime(f["pubDate"]), "", f.get("category", ""), paises=paises,
                       desc=f.get("description", ""))
        if o:
            out.append(o)
    return out


def workingnomads():
    out = []
    for j in get("https://www.workingnomads.com/api/exposed_jobs/"):
        o = oferta("Working Nomads", j.get("title"), j.get("company_name"), j.get("url"),
                   datetime.fromisoformat(j["pub_date"]), j.get("location") or "", j.get("category_name", ""),
                   desc=j.get("description") or "")
        if o:
            out.append(o)
    return out


def remotive():
    out = []
    for j in get("https://remotive.com/api/remote-jobs")["jobs"]:
        o = oferta("Remotive", j.get("title"), j.get("company_name"), j.get("url"),
                   datetime.fromisoformat(j["publication_date"]).replace(tzinfo=timezone.utc),
                   j.get("candidate_required_location") or "", j.get("category", ""),
                   salario=j.get("salary") or "", desc=j.get("description") or "")
        if o:
            out.append(o)
    return out


# --- Idioma del título y traducción ------------------------------------------
PT = re.compile(r"(ç|ã|õ|ê|\b(sênior|júnior|pleno|vaga|para pessoas|desenvolvedor\w*|engenheir\w*|segurança|"
                r"analista de dados|atendimento|vendas|ção|ções)\b)", re.I)
ES = re.compile(r"(ñ|[áéíóú]|\b(de|para|con|en|del|y|las|los|ejecutiv\w*|analista|desarrollador\w*|"
                r"ingenier\w*|asistente|jefe|jefa|gerente|vendedor\w*|especialista|coordinador\w*|soporte|"
                r"ventas|programador\w*|docente|diseñador\w*|técnico\w*|líder|práctica)\b)", re.I)


def idioma(titulo):
    if PT.search(titulo):
        return "pt"
    if ES.search(titulo):
        return "es"
    return "en"


ES_W = set("de la que el en y los las para con una por del se su al lo como más trabajo experiencia empresa "
           "equipo buscamos conocimientos requisitos beneficios nuestro nuestra serás tendrás".split())
EN_W = set("the and to of a in for with you we our your is are will on as be this experience team".split())
PT_W = set("não você com uma vaga experiência nós são trabalho conhecimento".split())


def idioma_texto(texto):
    """Idioma de la descripción, contando palabras frecuentes de cada idioma."""
    t = re.sub(r"<[^>]+>", " ", texto or "")
    w = re.findall(r"[a-záéíóúñüãõçê]+", t.lower())[:500]
    es, en, pt = (sum(x in S for x in w) for S in (ES_W, EN_W, PT_W))
    if pt > es and pt > en:
        return "pt"
    return "es" if es > en else "en"


def traducir(ofertas, ruta):
    """Agrega titulo_es usando un diccionario de traducciones (titulo original -> español)."""
    try:
        with open(ruta, encoding="utf-8") as f:
            tr = json.load(f)
    except (OSError, ValueError):
        tr = {}
    faltan = []
    for o in ofertas:
        o.setdefault("idioma", idioma(o["titulo"]))
        if idioma(o["titulo"]) == "es":  # título ya en español
            continue
        if o["titulo"] in tr:
            o["titulo_es"] = tr[o["titulo"]]
        else:
            faltan.append(o["titulo"])
    return sorted(set(faltan))


def jobicy():
    out, cursor, vueltas = [], "", 0
    while vueltas < 5:
        u = "https://jobicy.com/api/v2/remote-jobs?count=100&geo=latam" + (f"&cursor={cursor}" if cursor else "")
        d = get(u)
        for j in d.get("jobs", []):
            sal = ""
            if j.get("salaryMin") and j.get("salaryCurrency"):
                sal = f"{j['salaryCurrency']} {int(j['salaryMin']):,}".replace(",", ".") + \
                      (f"–{int(j['salaryMax']):,}".replace(",", ".") if j.get("salaryMax") else "")
            o = oferta("Jobicy", j.get("jobTitle"), j.get("companyName"), j.get("url"),
                       datetime.fromisoformat(j["pubDate"].replace(" ", "T")).replace(tzinfo=timezone.utc)
                       if "+" not in j["pubDate"] else datetime.fromisoformat(j["pubDate"]),
                       j.get("jobGeo") or "", " ".join(j.get("jobIndustry") or []), salario=sal,
                       desc=j.get("jobDescription") or j.get("jobExcerpt") or "")
            if o:
                out.append(o)
        cursor, vueltas = d.get("nextCursor"), vueltas + 1
        if not d.get("hasMore") or not cursor:
            break
    return out


FUENTES = [
    ("Get on Board", "https://www.getonbrd.com", getonbrd),
    ("Himalayas", "https://himalayas.app", himalayas),
    ("We Work Remotely", "https://weworkremotely.com", weworkremotely),
    ("Working Nomads", "https://www.workingnomads.com", workingnomads),
    ("Remotive", "https://remotive.com", remotive),
    ("Jobicy", "https://jobicy.com", jobicy),
]
# Para no consultar de más una fuente (p. ej. Remotive pide máx. 4 consultas al día):
#   SALTAR=Remotive python3 ...  reutiliza las ofertas de esa fuente del archivo anterior.


def main():
    salida = sys.argv[1] if len(sys.argv) > 1 else "ofertas.json"
    todas, resumen = [], []
    import os
    saltar = {x.strip() for x in os.environ.get("SALTAR", "").split(",") if x.strip()}
    try:
        with open(salida, encoding="utf-8") as f:
            previas = json.load(f).get("ofertas", [])
    except (OSError, ValueError):
        previas = []
    for nombre, web, fn in FUENTES:
        try:
            if nombre in saltar:
                lista = [o for o in previas if o["fuente"] == nombre and o["fecha"] >= LIMITE.strftime("%Y-%m-%d")]
                for o in lista:
                    o.pop("titulo_es", None)
                estado = "ok"
            else:
                lista = fn()
                estado = "ok"
        except Exception as e:  # una fuente caída no detiene a las demás
            lista, estado = [], f"error: {e.__class__.__name__}"
        resumen.append({"nombre": nombre, "web": web, "ofertas": len(lista), "estado": estado})
        todas.extend(lista)
        print(f"{nombre}: {len(lista)} ofertas ({estado})", file=sys.stderr)
    vistos, unicas = set(), []
    for o in sorted(todas, key=lambda x: x["fecha"], reverse=True):
        k = o["url"].split("?")[0]
        if k not in vistos:
            vistos.add(k)
            unicas.append(o)
    rt = sys.argv[2] if len(sys.argv) > 2 else "traducciones.json"
    faltan = traducir(unicas, rt)
    if faltan:
        with open(rt + ".faltan.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(faltan))
        print(f"Títulos sin traducir: {len(faltan)} (lista en {rt}.faltan.txt)", file=sys.stderr)
    with open(salida, "w", encoding="utf-8") as f:
        json.dump({"generado": AHORA.strftime("%Y-%m-%dT%H:%M:%SZ"), "dias": DIAS,
                   "fuentes": resumen, "ofertas": unicas}, f, ensure_ascii=False, separators=(",", ":"))
    print(f"Total: {len(unicas)} ofertas únicas -> {salida}", file=sys.stderr)


if __name__ == "__main__":
    main()
