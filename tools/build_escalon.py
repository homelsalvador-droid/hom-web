"""Genera escalon/index.html reutilizando estilos, formulario y scripts de index.html."""
import re, pathlib, json
R = pathlib.Path(__file__).resolve().parent.parent
src = (R/"index.html").read_text(encoding="utf-8")
def cut(a, b, s=src):
    i = s.index(a); j = s.index(b, i); return s[i:j]

style = cut("<style>", "</style>").replace("url(img/","url(../img/") + """
.zstats{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:28px}
.zstats div{background:#fff;border:1px solid var(--line,#e4ddd0);border-radius:14px;padding:22px}
.zstats b{display:block;font-size:2rem;line-height:1.1}
.zstats span{color:var(--muted,#6f6863);font-size:.95rem}
.zcmp{margin-top:28px;display:grid;gap:14px;max-width:760px}
.zbar{display:grid;grid-template-columns:200px 1fr;align-items:center;gap:14px}
.zbar i{display:block;height:34px;border-radius:8px;background:#e4ddd0;position:relative}
.zbar i.o{background:var(--orange,#ec5028)}
.zbar i em{position:absolute;right:10px;top:50%;transform:translateY(-50%);font-style:normal;font-weight:700;font-size:.95rem;color:#181413}
.zbar i.o em{color:#fff}
.zsrc{color:var(--muted,#6f6863);font-size:.85rem;margin-top:14px}
.ztab{overflow-x:auto;margin-top:22px}
.ztab table{border-collapse:collapse;width:100%;min-width:560px;background:#fff;border:1px solid var(--line,#e4ddd0);border-radius:14px;overflow:hidden}
.ztab th,.ztab td{padding:12px 16px;text-align:left;border-bottom:1px solid var(--line,#e4ddd0)}
.ztab th{font-size:.85rem;color:var(--muted,#6f6863);font-weight:600}
.ztab tr.us td{background:#181413;color:#fff;font-weight:700}
.ztab tr.us td:last-child{color:var(--orange,#ec5028)}
.zfair{margin-top:22px;background:#fff;border-left:4px solid var(--orange,#ec5028);padding:18px 22px;border-radius:0 12px 12px 0;max-width:820px;font-size:1.05rem}
.zhero{padding:80px 96px 20px;max-width:1100px}
@media(max-width:1100px){.zfair{margin-top:22px;background:#fff;border-left:4px solid var(--orange,#ec5028);padding:18px 22px;border-radius:0 12px 12px 0;max-width:820px;font-size:1.05rem}
.zhero{padding-left:32px;padding-right:32px}}\n@media(max-width:760px){.zfair{margin-top:22px;background:#fff;border-left:4px solid var(--orange,#ec5028);padding:18px 22px;border-radius:0 12px 12px 0;max-width:820px;font-size:1.05rem}
.zhero{padding:48px 16px 0}.zhero h1{font-size:34px}}
.zhero h1{font-size:clamp(2rem,5vw,3.4rem);line-height:1.05;margin:10px 0 18px}
.zhero p{font-size:1.15rem;max-width:640px}
.zhero .ctas{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}
@media(max-width:760px){.zstats{grid-template-columns:1fr 1fr}.zbar{grid-template-columns:1fr}}
</style>"""

cases = cut('<div class="cgrid">', '<figure class="testi">').replace("url(img/", "url(../img/")
faq_end = src.index("</section>", src.index('id="preguntas"'))
faq = src[src.index('<section style="padding-top:0" id="preguntas">'):faq_end] + "</section>"
final = cut('<div class="final" id="contacto">', "<footer>").replace('data-form="Propietario interesado"', 'data-form="Propietario interesado (Escalón)"').replace('placeholder="Colonia, ciudad o playa"', 'value="Colonia Escalón, San Salvador"')
okdlg = cut('<dialog class="okpop" id="ok-dialog">', "</dialog>") + "</dialog>"
footer = cut("<footer>", "</footer>") + "</footer>"
footer = footer.replace('src="img/', 'src="../img/')
mainjs = cut("<script>\n/* === EDITA AQUÍ", "/* animación: contadores")
mainjs = mainjs.replace('document.getElementById("open-ref").addEventListener("click",()=>refDlg.showModal());\nrefDlg.addEventListener("click",e=>{if(e.target===refDlg)refDlg.close()});\n', "")
mainjs = mainjs.replace('const refDlg=document.getElementById("ref-dialog"),', 'const refDlg={open:false},')
mainjs += 'document.getElementById("yr").textContent=new Date().getFullYear();\n</script>'
mapjs = cut("function initMap(){", "</script>").replace('"vendor/leaflet/leaflet.js"', '"../vendor/leaflet/leaflet.js"')
mapjs = re.sub(r'\s*// Etiquetas por zona\n.*?\n', "\n", mapjs)
mapjs = mapjs.replace(".setView([SITIOS[i][2],SITIOS[i][3]],15)", ".setView([SITIOS[i][2],SITIOS[i][3]],16)")
gtag = cut('<script async src="https://www.googletagmanager.com', '<script type="application/ld+json">')

URL = "https://homlatam.com/escalon/"
ld = {"@context": "https://schema.org", "@graph": [
  {"@type": "Service", "name": "Administración de Airbnb en Colonia Escalón", "serviceType": "Administración de renta vacacional",
   "provider": {"@id": "https://homlatam.com/#negocio", "@type": "LocalBusiness", "name": "hōm Property Management", "url": "https://homlatam.com/", "telephone": "+50379281377"},
   "areaServed": {"@type": "Place", "name": "Colonia Escalón, San Salvador"}, "url": URL},
  {"@type": "BreadcrumbList", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "hōm", "item": "https://homlatam.com/"},
   {"@type": "ListItem", "position": 2, "name": "Colonia Escalón", "item": URL}]}]}

html = f"""<!doctype html>
<html lang="es-SV"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Administración de Airbnb en Colonia Escalón | hōm</title>
<meta name="description" content="Administramos tu apartamento en Airbnb en la Colonia Escalón. Un Airbnb promedio en la Escalón factura entre $10,000 y $17,000 al año; nuestros apartamentos en la zona facturan más de $28,000. Análisis gratis.">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#181413">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_SV">
<meta property="og:site_name" content="hōm Property Management">
<meta property="og:url" content="{URL}">
<meta property="og:title" content="Administración de Airbnb en Colonia Escalón · hōm">
<meta property="og:description" content="Tu apartamento en Escalón puede facturar más de $28,000 al año en Airbnb. Análisis gratis.">
<meta property="og:image" content="https://homlatam.com/img/og-image.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../img/favicon.png">
{gtag}<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{style}
<link rel="stylesheet" href="../vendor/leaflet/leaflet.css" media="print" onload="this.media='all'"></head><body>
<noscript><img height="1" width="1" style="display:none" alt="" src="https://www.facebook.com/tr?id=4369760116620796&amp;ev=PageView&amp;noscript=1"></noscript>

<nav>
  <a href="/"><img src="../img/logo-claro-sm.png" alt="hōm property management" width="140" height="38"></a>
  <div class="links"><a href="/#como">Cómo funciona</a><a href="#mercado">Mercado</a><a href="#resultados">Resultados</a><a href="/#planes">Planes</a></div>
  <div class="nav-r"><a class="btn wa" data-msg="Hola, tengo una propiedad en la Escalón y quiero mi análisis gratis.">Análisis gratis</a></div>
</nav>

<header class="zhero">
  <div class="eyebrow">Colonia Escalón · San Salvador</div>
  <h1>Administración de Airbnb en la Colonia Escalón<span class="dot">.</span></h1>
  <p>Ya gestionamos apartamentos en Vistas de Masferrer, Panorama Tower y Condominio 105. Nuestros apartamentos en la zona facturan más de <b>$28,000 al año</b>, 1.7 veces el promedio de Escalón Alta y casi el doble del promedio de Escalón Media.</p>
  <div class="ctas"><a class="btn wa" data-msg="Hola, tengo una propiedad en la Escalón y quiero mi análisis gratis.">Quiero mi análisis gratis →</a><a class="btn ghost" href="#mercado">Ver datos de la zona</a></div>
</header>

<section id="mercado">
  <div class="head">
    <div class="eyebrow">El mercado en la Escalón</div>
    <h2>Cuánto factura un Airbnb en la Escalón<span class="dot">.</span></h2>
    <p>Datos de AirDNA de los últimos 12 meses. La demanda es alta y estable; la diferencia la hace cómo se gestiona cada anuncio.</p>
  </div>
  <div class="zstats">
    <div><b>836</b><span>Airbnbs activos en la Escalón y Masferrer Norte</span></div>
    <div><b>60%</b><span>ocupación promedio en la zona; nosotros, 68–82%</span></div>
    <div><b>$51–81</b><span>tarifa promedio por noche, según la sub-zona</span></div>
    <div><b>$10–17k</b><span>facturación anual promedio por anuncio</span></div>
  </div>
  <div class="ztab"><table>
    <thead><tr><th>Sub-zona</th><th>Anuncios activos / calificación</th><th>Tarifa por noche</th><th>Ocupación</th><th>Facturación anual</th></tr></thead>
    <tbody>
      <tr><td>Escalón Alta</td><td>152</td><td>$81</td><td>60%</td><td>$16,648</td></tr>
      <tr><td>Escalón Media</td><td>255</td><td>$75</td><td>60%</td><td>$15,445</td></tr>
      <tr><td>Escalón Baja</td><td>122</td><td>$51</td><td>59%</td><td>$10,406</td></tr>
      <tr><td>Masferrer Norte</td><td>307</td><td>$75</td><td>59%</td><td>$15,177</td></tr>
      <tr><td>Masferrer Norte, solo 2 hab.</td><td>112</td><td>$76</td><td>62%</td><td>$16,434</td></tr>
      <tr class="us"><td>Masferrer 705 (2 hab.), gestionado por hōm</td><td>4.9 ★</td><td>$100</td><td>68%</td><td>$23,000</td></tr>
      <tr class="us"><td>Panorama A209, gestionado por hōm*</td><td>4.9 ★</td><td>$104</td><td>82%</td><td>$23,300</td></tr>
      <tr class="us"><td>Panorama 306, gestionado por hōm</td><td>4.9 ★</td><td>$105</td><td>72%</td><td>$27,000</td></tr>
    </tbody>
  </table></div>
  <p class="zfair"><b>La comparación más justa:</b> un apartamento promedio de 2 habitaciones en Masferrer Norte factura <b>$16,434</b> al año. Masferrer 705, también de 2 habitaciones y en la misma zona, factura <b>$23,000</b> con hōm según la misma medición de AirDNA: <b style="color:var(--orange,#ec5028)">40% más</b>, con una tarifa por noche 31% más alta y más ocupación.</p>
  <div class="zcmp" role="img" aria-label="Comparación de facturación anual: promedio de Escalón Alta, la sub-zona más alta, $16,648; Panorama 306 con hōm $28,200; Masferrer 705 con hōm $29,036">
    <div class="zbar"><span>Promedio Escalón Alta</span><i style="width:57%"><em>$16,648</em></i></div>
    <div class="zbar"><span>Panorama 306 con hōm</span><i class="o" style="width:97%"><em>$28,200</em></i></div>
    <div class="zbar"><span>Masferrer 705 con hōm</span><i class="o" style="width:100%"><em>$29,036</em></i></div>
  </div>
  <p class="zsrc">Fuente del promedio: AirDNA, sub-mercados Escalón Alta, Media, Baja y Masferrer Norte, últimos 12 meses a noviembre de 2026. Las filas de hōm usan la misma medición de AirDNA. *Panorama A209 estuvo disponible 273 de los últimos 365 días. las barras muestran la facturación del primer año de cada propiedad según nuestros reportes.</p>
</section>

<section class="cases" id="resultados">
  <div class="head">
    <div class="eyebrow">Resultados en la Escalón</div>
    <h2>Antes y después de hōm<span class="dot">.</span></h2>
  </div>
  {cases}
</section>

<section style="padding-top:0" id="mapa">
  <div class="head">
    <div class="eyebrow">Dónde operamos</div>
    <h2>Ya tenemos equipo en tu edificio o a pocas cuadras<span class="dot">.</span></h2>
  </div>
  <div class="map-wrap">
    <div id="map" role="img" aria-label="Mapa de edificios gestionados por hōm en la Colonia Escalón"></div>
    <ul class="map-list">
      <li data-i="0"><b>Vistas de Masferrer</b><span>Colonia Escalón</span></li>
      <li data-i="1"><b>Panorama Tower</b><span>Colonia Escalón</span></li>
      <li data-i="2"><b>Condominio 105</b><span>Colonia Escalón</span></li>
    </ul>
  </div>
  <p class="map-note">Ubicaciones aproximadas.</p>
</section>

{okdlg}

{faq}

{final}
{footer}

<a class="wa-float wa" data-msg="Hola, tengo una propiedad en la Escalón y quiero información.">WhatsApp</a>

{mainjs}

<script>
const SITIOS=[
  ["Vistas de Masferrer","Colonia Escalón",13.7128,-89.2445],
  ["Panorama Tower","Colonia Escalón",13.7062,-89.2398],
  ["Condominio 105","Colonia Escalón",13.7018,-89.2472]
];
{mapjs}</script>
</body></html>
"""
(R/"escalon"/"index.html").write_text(html, encoding="utf-8")
print("ok", len(html))
