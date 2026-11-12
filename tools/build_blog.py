"""Genera el blog (blog/index.html y blog/<slug>/index.html) reutilizando estilos y scripts de index.html.
Para agregar un artículo: añade un dict a ARTICULOS y corre python3 tools/build_blog.py."""
import pathlib, json, html as H
R = pathlib.Path(__file__).resolve().parent.parent
src = (R/"index.html").read_text(encoding="utf-8")
def cut(a, b, s=src):
    i = s.index(a); j = s.index(b, i); return s[i:j]

CSS = """
.bwrap{max-width:760px;margin:0 auto;padding:72px 24px 40px}
.bwrap .eyebrow a{color:inherit}
.bwrap h1{font-size:clamp(2rem,4.6vw,3.1rem);line-height:1.08;margin:12px 0 16px}
.bmeta{color:var(--muted);font-size:15px;margin-bottom:28px}
.blead{font-size:1.25rem;line-height:1.55;margin-bottom:28px}
.bcover{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:14px;margin:6px 0 34px;display:block}
.art{font-size:1.1rem;line-height:1.7}
.art h2{font-size:1.65rem;line-height:1.2;margin:46px 0 12px}
.art h2 .n{color:var(--orange);margin-right:8px}
.art p{margin:0 0 16px}
.art ul{margin:0 0 18px 22px;padding:0}
.art li{margin:0 0 8px}
.art img{width:100%;border-radius:12px;margin:10px 0 6px;display:block;aspect-ratio:3/2;object-fit:cover}
.art figure{margin:0 0 22px}
.art figcaption{font-size:.9rem;color:var(--muted)}
.art .tip{background:#fff;border-left:4px solid var(--orange);padding:16px 20px;border-radius:0 12px 12px 0;margin:8px 0 22px}
.art .stat{background:var(--ink);color:#fff;border-radius:14px;padding:24px 26px;margin:24px 0}
.art .stat b{color:var(--orange);font-size:1.9rem;display:block;line-height:1.1;margin-bottom:6px}
.check{background:#fff;border:1px solid var(--line);border-radius:14px;padding:26px 28px;margin:40px 0}
.check h2{margin-top:0}
.check ul{list-style:none;margin:0}
.check li{padding-left:30px;position:relative}
.check li:before{content:"";position:absolute;left:0;top:.35em;width:16px;height:16px;border:2px solid var(--orange);border-radius:4px}
.bcta{background:var(--orange);color:#fff;border-radius:14px;padding:30px;margin:44px 0 10px}
.bcta h2{margin:0 0 10px;font-size:1.6rem;color:#fff}
.bcta p{margin:0 0 18px}
.bcta .btn{background:var(--ink);border-radius:10px}
.autor{display:flex;gap:18px;align-items:center;border-top:1px solid var(--line);padding-top:28px;margin-top:44px}
.autor .av{flex:0 0 72px;width:72px;height:72px;border-radius:50%;background:var(--ink);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:20px}
.autor b{font-size:1.1rem}
.autor p{margin:6px 0 0;color:var(--muted);line-height:1.6}
.autor a{color:var(--ink);text-decoration:underline}
.art h2{margin-top:40px}
.autor img.av{object-fit:cover;padding:0}
.bmeta{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.bmeta .mini{width:32px;height:32px;border-radius:50%;object-fit:cover}
.art .foto1 img{max-width:560px;width:100%;height:auto;margin:18px auto 8px;aspect-ratio:auto;border-radius:12px}
.art .foto1 figcaption{text-align:center}
.blist{display:grid;gap:22px;margin-top:30px}
.bcard{display:grid;grid-template-columns:1fr;gap:22px;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;color:inherit}
.bcard img{width:100%;height:100%;object-fit:cover;min-height:170px}
.bcard div{padding:24px 26px}
.bcard h2{font-size:1.4rem;line-height:1.2;margin:6px 0 8px}
.bcard p{color:var(--muted);margin:0}
@media(max-width:640px){.bcard{grid-template-columns:1fr}.bcard div{padding:0 20px 20px}.bwrap{padding:44px 16px 24px}.art{font-size:1.05rem}}
"""

ARTICULOS = [{
 "slug": "miedo-a-invertir-en-bienes-raices-el-salvador",
 "titulo": "El miedo a invertir en bienes raíces en El Salvador (y cómo lo perdí)",
 "seo_title": "El miedo a invertir en bienes raíces en El Salvador | Christian Leonés",
 "desc": "Pasé años viendo los bienes raíces desde afuera. Esta es la historia de cómo hice los números, descarté decenas de propiedades y compré mi primer apartamento para Airbnb.",
 "fecha": "2026-11-12", "fecha_txt": "12 de noviembre de 2026", "lectura": "5 min",
 "portada": "caso-1.jpg",
 "lead": "Desde hace mucho quería escribir. En la universidad era de las cosas que más disfrutaba, y siempre pensé que podría hacerlo como hobby. Fui un chico inquieto, no el mejor del colegio, pero siempre andaba vendiendo alguna idea: cuadros con dibujos animados cuando era pequeño, camisas de fútbol, pulseras, entradas para conciertos, cargadores inalámbricos y hasta un negocio de <i>meat boxes</i> para cocinar con amigos. ¡Vaya que me emocionaba esa idea!</p><p class=\"blead\">Hoy miro atrás y me cuesta creer que ya pasaron casi cinco años desde que me aventuré en este negocio. Me cambió la vida y se volvió algo más grande que yo: recuerdos de huéspedes, un servicio para otros inversionistas y un ingreso estable para familias enteras. Por eso quiero aclararlo desde el principio: esto no es un discurso para venderte nada. Soy Christian Leonés, escribiendo desde mi experiencia, un joven (al menos en ese entonces) que siempre quiso crear algo para los demás.",
 "cuerpo": """
<h2>El miedo de invertir mal</h2>
<p>No nos mintamos: muchos queremos entrar en los bienes raíces, pero eso no quita que da mucho miedo. Son años de trabajo y de privarnos de experiencias con la esperanza de un mejor futuro, de dejar un legado y de que nuestros hijos tengan más oportunidades. Toda esa presión se convierte en miedo a invertir mal. ¿Cómo me aseguro de que mi idea no va a fracasar y me voy a quedar pagando una hipoteca por 30 años? ¿Qué pasa si pierdo mi empleo y ya no puedo pagarla? Son preguntas que todos nos hacemos.</p>
<p>Pasé muchos años viendo el negocio de bienes raíces desde afuera, sin animarme nunca a entrar. En 2022 tenía un empleo corporativo bueno y estable, y empecé a buscar en qué invertir, porque siempre he creído que el dinero tiene que estar en movimiento.</p>
<h2>No empecé pensando en Airbnb</h2>
<p>No creas que mi primera idea fue Airbnb. Al contrario: yo quería algo más pasivo.</p>
<p>Creo firmemente que la educación es lo primero, así que me puse a investigar distintas inversiones, con sus pros y sus contras. Aunque ya tenía la espinita de intentar algo en bienes raíces, no era mi primera opción.</p>

<h2>Los números que no cuadraban</h2>
<p>Cuando, con un poco de ayuda, logré juntar un buen ahorro, decidí investigar si alguna propiedad podía ser rentable para mí.</p>
<p>Vi muchísimos videos de inversionistas inmobiliarios en España. Allá el negocio es muy rentable porque las tasas de interés son mucho más bajas: con una buena investigación podías comprar una casa, adecuarla y alquilarla por más de lo que pagabas de hipoteca. Y mejor todavía, te quedaba un pequeño flujo de efectivo cada mes.</p>
<p>Me emocioné mucho. Pensé que ese era el camino.</p>
<p>Analicé el mercado durante meses para encontrar una buena propiedad. Me memoricé el costo promedio por metro cuadrado en San Salvador, Apopa, Soyapango, Antiguo Cuscatlán y hasta Zaragoza. Aun así, no encontraba ninguna propiedad cuyo alquiler pagara la hipoteca. Ni de cerca.</p>

<h2>La idea que llegó desde Andorra</h2>
<p>Hasta que abrí la mente y entendí que tenía que buscar otra alternativa.</p>
<p>Por casualidad, en uno de los cientos de videos que vi, me topé con un chico, quizás menor que yo, que tenía unos apartamentos en Andorra. Se los alquilaba a gente que llegaba a hacer deportes de nieve durante el invierno. Vi sus números y cuadraban: era un negocio que le dejaba flujo de efectivo.</p>
<p>Empecé a planteármelo para El Salvador. Los números aquí estaban apretados, pero eran mejores que los de un alquiler tradicional.</p>

<h2>Las madrugadas en Marketplace</h2>
<p>Ahora sí me puse serio. Vi muchas opciones, hablé con muchos realtors y no encontré nada que me convenciera.</p>
<p>Pasé meses buscando, precalificándome, haciendo números sobre cada propiedad. Madrugaba revisando Marketplace por si salía algo nuevo, para escribir rápido y poder hacer una oferta antes que nadie.</p>
<p>Hasta que una madrugada la encontré: un apartamento que estaba alquilado de forma tradicional y cuyo dueño lo quería vender. Esta vez los números sí daban.</p>

<h2>La propiedad que no pude ver</h2>
<p>Le escribí, hablamos y acordamos una visita. Pero había un problema: el inquilino no se quería ir. Quería comprarla él, así que no me dejó entrar a verla.</p>
<p>Fue una gran desilusión. Era otra propiedad más, de las muchas que había visto, que no iba a poder concretar.</p>
<p>Unos días después, el realtor me dijo: "Oye, el dueño tiene otro apartamento igual, solo que en un piso más arriba, en la misma torre".</p>
<p>Fui a verlo, todavía con el inquilino adentro. Era más caro, eso sí, pero me pareció una buena opción.</p>
<p>Investigué los precios de la zona, el precio de lanzamiento de ese mismo apartamento y los años que habían pasado, e hice una oferta. Para no aburrirte con el proceso paso a paso (que te cuento en otro artículo), compré la propiedad.</p>
<figure class="foto1"><img src="../../img/blog/primer-apartamento.jpg" alt="Sala vacía con ventanales y vista a San Salvador: la primera foto del primer apartamento de Christian Leonés" width="1100" height="1173" loading="lazy"><figcaption>La primera foto que le tomé a mi apartamento, todavía vacío. De aquí nació hōm.</figcaption></figure>
<p>Y ahí empezaba lo realmente difícil. ¿Qué haría que mi apartamento funcionara en Airbnb? ¿Qué buscaban los huéspedes? ¿Qué comprar y qué no? ¿Cuánto presupuesto tenía? Eso es otra historia.</p>

<h2>Lo que quiero que te lleves</h2>
<p>Una inversión en bienes raíces hay que tomarla como eso: una inversión.</p>
<p>Hay que hacer los números. No compres porque tu tía, tu primo o tu hermano que vive en otro país te dicen que es buena inversión. No todas las propiedades lo son.</p>
<p>Pierde el miedo a hacer los números, y pierde también el miedo a descartar las opciones que no dan, aunque ya te imagines viviendo en ellas. La casa de tus sueños no necesariamente es una buena inversión.</p>
"""},
{
 "borrador": True,
 "slug": "que-necesita-tu-apartamento-para-airbnb",
 "titulo": "Qué necesita un apartamento para funcionar en Airbnb: lo que aprendí empezando",
 "seo_title": "Qué necesita tu apartamento para Airbnb en El Salvador | Christian Leonés",
 "desc": "Si estás pensando en poner tu apartamento en Airbnb en El Salvador, esto es lo que de verdad importa (y en qué no gastar), contado desde mi experiencia.",
 "fecha": "2026-11-12", "fecha_txt": "12 de noviembre de 2026", "lectura": "6 min",
 "portada": "caso-1.jpg",
 "lead": "En 2022 tenía un apartamento de dos habitaciones en la Masferrer alquilado en $750 al mes. Decidí probar con Airbnb sin saber muy bien lo que estaba haciendo. Ese primer año facturó $29,036. No fue suerte, pero tampoco fue genialidad: fueron muchos ajustes pequeños, casi todos aprendidos leyendo reseñas. Si estás pensando en empezar, esto es lo que me hubiera gustado que alguien me dijera.",
 "cuerpo": """
<h2>Empieza por la cama, no por la sala</h2>
<p>Cuando uno amuebla un apartamento piensa en la sala, porque es lo que se ve. Pero el huésped no escribe en su reseña sobre tu sofá. Escribe sobre cómo durmió.</p>
<p>Si vas a invertir en algo, que sea en buenos colchones. Después, sábanas blancas (dos juegos por cama, para que siempre haya uno limpio), cuatro almohadas por cama y cortinas que de verdad oscurezcan el cuarto. Aquí amanece temprano y nadie de vacaciones quiere despertarse a las 5:30.</p>

<h2>El internet es parte del producto</h2>
<p>Hoy mucha gente viaja y trabaja al mismo tiempo. Para ellos el internet no es un extra: es la razón por la que eligen tu anuncio o el de al lado. Yo no bajaría de 100 Mbps, y pondría la velocidad en el título.</p>
<p>Revisa también que la señal llegue bien a todos los cuartos y que haya una mesa donde alguien pueda sentarse con su computadora sin terminar con dolor de espalda.</p>

<h2>Con este calor, el aire acondicionado no es opcional</h2>
<p>Puede sonar obvio, pero lo veo seguido: apartamentos bonitos sin aire en las habitaciones. En San Salvador, y más en la playa, eso se paga con reseñas de tres estrellas. Si solo puedes poner aire en un lugar, que sea donde se duerme.</p>

<h2>Una cocina para quedarse una semana</h2>
<p>Las reservas largas son las que hacen que los números cierren: menos limpiezas, menos entradas y salidas, menos desgaste. Y nadie se queda una semana donde no puede ni hacerse un huevo.</p>
<p>No necesitas una cocina de chef. Necesitas cuchillos que corten, un par de sartenes decentes, cafetera, licuadora, vajilla para el doble de personas que caben y lo básico de despensa: sal, aceite, azúcar y café.</p>

<h2>Que nadie tenga que esperarte para entrar</h2>
<p>Muchos vuelos llegan de noche. Si tu huésped depende de que alguien le entregue una llave, su estadía empieza con una espera, y tú vas a terminar manejando a medianoche.</p>
<p>Una cerradura con código o una caja de llaves, más unas instrucciones claras con fotos (cómo entrar al edificio, dónde parquear, cuál es la puerta), te resuelven el problema. Y avísale a la seguridad del edificio quién llega: se evita más de un mal rato.</p>

<h2>Decora para las fotos, no para ti</h2>
<p>Tu apartamento no compite en persona, compite en una pantalla del tamaño de tu mano. La gente decide en un segundo si le da clic o sigue bajando.</p>
<p>No hace falta remodelar ni comprar muebles caros. Lo que funciona es algo coherente: colores neutros, dos o tres acentos, plantas, luz cálida y nada de fotos familiares ni adornos personales. Muebles resistentes y fáciles de limpiar le ganan a los delicados, siempre.</p>
<p>Y luego, fotos profesionales. Fue de las mejores inversiones que hice al principio. La diferencia entre fotos de celular y fotos bien hechas se nota en las reservas desde la primera semana.</p>

<h2>Lo pequeño es lo que termina en las reseñas</h2>
<p>Café de bienvenida. Agua fría en la refri. Una secadora de pelo, una plancha y ganchos suficientes. Champú y papel higiénico de buena calidad, con repuestos donde se vean. Una guía corta con el WiFi, las reglas y los lugares que tú recomendarías.</p>
<p>Ninguna de estas cosas cuesta mucho, pero son las que hacen que alguien escriba "se notaba que pensaron en todo".</p>

<h2>Dónde no gastaría</h2>
<p>Televisores enormes, decoración cara y muebles de diseñador. Se ven bien, pero no suben la tarifa tanto como uno cree. Ese dinero rinde más en colchones, aire acondicionado, internet y fotos.</p>

<h2>Si apenas estás empezando</h2>
<p>No tienes que tener todo perfecto el primer día. Empieza con lo básico, lee cada reseña con atención (incluso las buenas, porque ahí también hay pistas) y mejora un poco cada mes. Así fue como empecé yo.</p>
<p>Si te ayuda, este es el resumen:</p>
<ul>
<li>Buenos colchones, sábanas blancas y cortinas que oscurezcan</li>
<li>Internet de 100 Mbps o más y un lugar para trabajar</li>
<li>Aire acondicionado en los cuartos</li>
<li>Una cocina con lo necesario para quedarse una semana</li>
<li>Entrada sin depender de nadie</li>
<li>Decoración sencilla y fotos profesionales</li>
<li>Detalles de bienvenida y una guía de la casa</li>
</ul>
"""},
]

AUTOR = """<div class="autor"><img class="av" src="../../img/blog/christian-leones.jpg" alt="Christian Leonés" width="72" height="72"><div><b>Christian Leonés</b><p>Si estás considerando invertir en bienes raíces, <a class="wa" data-msg="Hola Christian, leí tu blog y estoy considerando invertir en bienes raíces.">escríbeme por WhatsApp</a> y compartimos experiencias.</p></div></div>"""

exec(open(pathlib.Path(__file__).with_name("blog_en.py"), encoding="utf-8").read())  # EN, AUTOR_EN

def piezas(fuente):
    t = (R/fuente).read_text(encoding="utf-8")
    c = lambda a, b: cut(a, b, t)
    js = c("<script>\n/* === EDITA AQUÍ", "/* animación: contadores")
    js = js.replace('document.getElementById("open-ref").addEventListener("click",()=>refDlg.showModal());\nrefDlg.addEventListener("click",e=>{if(e.target===refDlg)refDlg.close()});\n', "")
    js = js.replace('const refDlg=document.getElementById("ref-dialog"),', 'const refDlg={open:false},')
    js += 'document.getElementById("yr").textContent=new Date().getFullYear();\n</script>'
    return {"gtag": c('<script async src="https://www.googletagmanager.com', '<script type="application/ld+json">'),
            "style": c("<style>", "</style>").replace("url(img/", "url(UP/img/").replace("url(../img/", "url(UP/img/") + CSS + "</style>",
            "okdlg": c('<dialog class="okpop" id="ok-dialog">', "</dialog>") + "</dialog>",
            "footer": c("<footer>", "</footer>").replace('src="img/', 'src="UP/img/').replace('src="../img/', 'src="UP/img/') + "</footer>",
            "js": js}

LANG = {
 "es": {"src": "index.html", "html": "es-SV", "locale": "es_SV", "home": "/", "blog": "/blog/",
        "links": '<a href="/#como">Cómo funciona</a><a href="/#propiedades">Propiedades</a><a href="/#planes">Planes</a><a href="/blog/">Blog</a>',
        "cta": '<a class="btn wa" data-msg="Hola, quiero mi análisis gratis de ingresos para mi propiedad.">Análisis gratis</a>',
        "eyebrow": "Mi historia", "por": "Por", "ld": "es-SV"},
 "en": {"src": "en/index.html", "html": "en", "locale": "en_US", "home": "/en/", "blog": "/en/blog/",
        "links": '<a href="/en/#como">How it works</a><a href="/en/#propiedades">Properties</a><a href="/en/#planes">Plans</a><a href="/en/blog/">Blog</a>',
        "cta": '<a class="btn wa" data-msg="Hi, I would like my free income analysis for my property.">Free analysis</a>',
        "eyebrow": "My story", "por": "By", "ld": "en"},
}
for k in LANG: LANG[k]["p"] = piezas(LANG[k]["src"])

def page(lang, up, title, desc, url, body, ld, alt_es, alt_en, og_img="https://homlatam.com/img/og-image.jpg", og_type="article"):
    L = LANG[lang]; P = L["p"]; f = lambda x: x.replace("UP/", up)
    otro = alt_en if lang == "es" else alt_es
    sw = '<a class="lang" href="%s" hreflang="%s" lang="%s">%s</a>' % (otro, "en" if lang == "es" else "es", "en" if lang == "es" else "es", "EN" if lang == "es" else "ES")
    return f"""<!doctype html>
<html lang="{L['html']}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{H.escape(title)}</title>
<meta name="description" content="{H.escape(desc)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#181413">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="es" href="https://homlatam.com{alt_es}">
<link rel="alternate" hreflang="en" href="https://homlatam.com{alt_en}">
<link rel="alternate" hreflang="x-default" href="https://homlatam.com{alt_es}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="{L['locale']}">
<meta property="og:site_name" content="hōm Property Management">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{H.escape(title)}">
<meta property="og:description" content="{H.escape(desc)}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{up}img/favicon.png">
{P['gtag']}<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{f(P['style'])}
</head><body>
<noscript><img height="1" width="1" style="display:none" alt="" src="https://www.facebook.com/tr?id=4369760116620796&amp;ev=PageView&amp;noscript=1"></noscript>
<nav>
  <a href="{L['home']}"><img src="{up}img/logo-claro-sm.png" alt="hōm property management" width="140" height="38"></a>
  <div class="links">{L['links']}</div>
  <div class="nav-r">{sw}{L['cta']}</div>
</nav>
{body}
{P['okdlg']}
{f(P['footer'])}
{P['js']}
</body></html>
"""

ARTICULOS = [a for a in ARTICULOS if not a.get("borrador")]  # los borradores no se publican
publicados = {"es": [], "en": []}
for a in ARTICULOS:
    e = EN.get(a["slug"])
    alt_es = "/blog/" + a["slug"] + "/"; alt_en = ("/en/blog/" + e["slug"] + "/") if e else "/en/blog/"
    versiones = [("es", a, "../../", AUTOR, alt_es)] + ([("en", dict(a, **e), "../../../", AUTOR_EN, alt_en)] if e else [])
    for lang, x, up, autor, path in versiones:
        L = LANG[lang]; url = "https://homlatam.com" + path
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "BlogPosting", "headline": x["titulo"], "description": x["desc"], "datePublished": x["fecha"], "dateModified": x["fecha"],
             "inLanguage": L["ld"], "mainEntityOfPage": url, "image": "https://homlatam.com/img/" + x["portada"],
             "author": {"@type": "Person", "name": "Christian Leonés", "url": "https://homlatam.com" + L["blog"]},
             "publisher": {"@type": "Organization", "name": "hōm Property Management", "logo": {"@type": "ImageObject", "url": "https://homlatam.com/img/logo-oscuro.png"}}},
            {"@type": "BreadcrumbList", "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "hōm", "item": "https://homlatam.com" + L["home"]},
             {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://homlatam.com" + L["blog"]},
             {"@type": "ListItem", "position": 3, "name": x["titulo"], "item": url}]}]}
        cuerpo = x["cuerpo"] if lang == "en" else x["cuerpo"]
        body = f"""<main class="bwrap">
  <div class="eyebrow"><a href="{L['blog']}">Blog</a> · {L['eyebrow']}</div>
  <h1>{x["titulo"]}</h1>
  <div class="bmeta"><img class="mini" src="{up}img/blog/christian-leones.jpg" alt="" width="32" height="32">{L['por']} Christian Leonés · {x["fecha_txt"]} · {x["lectura"]}{' de lectura' if lang == 'es' else ''}</div>
  <p class="blead">{x["lead"]}</p>
  <article class="art">{cuerpo}
  {autor}
  </article>
</main>"""
        out = R/path.strip("/")/"index.html"; out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(lang, up, x["seo_title"], x["desc"], url, body, ld, alt_es, alt_en, "https://homlatam.com/img/" + x["portada"]), encoding="utf-8")
        publicados[lang].append((path, x))

IDX = {"es": ("Blog de Christian Leonés", "Empezar en Airbnb en El Salvador", "Lo que he aprendido invirtiendo en bienes raíces y administrando apartamentos en San Salvador y la costa, para quien está pensando en empezar.", "Blog: invertir en bienes raíces y Airbnb en El Salvador | Christian Leonés", "Historias y aprendizajes de Christian Leonés para quien quiere invertir en bienes raíces y Airbnb en El Salvador."),
       "en": ("Christian Leonés's blog", "Getting started with Airbnb in El Salvador", "What I have learned investing in real estate and managing apartments in San Salvador and on the coast, for anyone thinking about getting started.", "Blog: real estate and Airbnb in El Salvador | Christian Leonés", "Stories and lessons from Christian Leonés for anyone who wants to invest in real estate and Airbnb in El Salvador.")}
for lang in ("es", "en"):
    L = LANG[lang]; eb, h1, lead, t, d = IDX[lang]; up = "../" if lang == "es" else "../../"
    cards = "\n".join(f"""  <a class="bcard" href="{p}"><div><div class="bmeta" style="margin:0">{x['fecha_txt']} · {x['lectura']}</div><h2>{x['titulo']}</h2><p>{x['desc']}</p></div></a>""" for p, x in sorted(publicados[lang], key=lambda z: z[1]["fecha"], reverse=True))
    ld = {"@context": "https://schema.org", "@type": "Blog", "name": eb, "url": "https://homlatam.com" + L["blog"], "inLanguage": L["ld"],
          "author": {"@type": "Person", "name": "Christian Leonés"}}
    body = f"""<main class="bwrap">
  <div class="eyebrow">{eb}</div>
  <h1>{h1}<span class="dot">.</span></h1>
  <p class="blead">{lead}</p>
  <div class="blist">
{cards}
  </div>
</main>"""
    out = R/L["blog"].strip("/")/"index.html"; out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(lang, up, t, d, "https://homlatam.com" + L["blog"], body, ld, "/blog/", "/en/blog/", og_type="website"), encoding="utf-8")
print("ok", len(ARTICULOS), "artículo(s);", len(publicados["en"]), "en inglés")
