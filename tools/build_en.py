#!/usr/bin/env python3
"""Genera en/index.html (versión en inglés) a partir de index.html.

Uso:  python3 tools/build_en.py
Si cambias un texto en index.html, agrega o ajusta su traducción en PARES.
El script avisa de cualquier texto que no encontró.
"""
import json, re, html, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
s = (ROOT / "index.html").read_text()

HEAD = [
 ('<html lang="es-SV">', '<html lang="en">'),
 ('<title>Administración de Airbnb en El Salvador | hōm Property Management</title>',
  '<title>Airbnb Property Management in El Salvador | hōm</title>'),
 ('content="Administramos tu casa o apartamento en Airbnb en San Salvador y la playa: anuncio, precios dinámicos, huéspedes y limpieza. 4.92★ en 479 reseñas. Análisis gratis."',
  'content="We manage your Airbnb house or apartment in San Salvador and on the beach: listing, dynamic pricing, guests and cleaning. 4.92★ across 479 reviews. Free analysis."'),
 ('<link rel="canonical" href="https://homlatam.com/">', '<link rel="canonical" href="https://homlatam.com/en/">'),
 ('<meta property="og:locale" content="es_SV">', '<meta property="og:locale" content="en_US">\n<meta property="og:locale:alternate" content="es_SV">'),
 ('<meta property="og:url" content="https://homlatam.com/">', '<meta property="og:url" content="https://homlatam.com/en/">'),
 ('content="hōm · Tu propiedad puede facturar hasta 3× más"', 'content="hōm · Your property could earn up to 3× more"'),
 ('content="Administración de Airbnb y renta vacacional en El Salvador. 479 reseñas · 4.92 ★. Análisis gratis de tu propiedad."',
  'content="Airbnb and vacation rental management in El Salvador. 479 reviews · 4.92 ★. Free analysis of your property."'),
 ('content="Piscina en la azotea con vista a San Salvador: Ponemos tu propiedad a trabajar en Airbnb"', 'content="Rooftop pool overlooking San Salvador: We put your property to work on Airbnb"'),
 ('<meta property="og:image" content="https://homlatam.com/img/og-image.jpg">', '<meta property="og:image" content="https://homlatam.com/img/og-image-en.jpg">'),
 ('<meta name="twitter:image" content="https://homlatam.com/img/og-image.jpg">', '<meta name="twitter:image" content="https://homlatam.com/img/og-image-en.jpg">'),
 ('content="hōm · Administración de Airbnb en El Salvador"', 'content="hōm · Airbnb Property Management in El Salvador"'),
 ('content="Tu propiedad puede facturar hasta 3× más. Análisis gratis."', 'content="Your property could earn up to 3× more. Free analysis."'),
]

PARES = [
 # nav
 ('<a class="lang" href="/en/" hreflang="en" lang="en" title="English version">EN</a>',
  '<a class="lang" href="/" hreflang="es" lang="es" title="Versión en español">ES</a>'),
 ('<a href="#como">Cómo funciona</a><a href="#propiedades">Propiedades</a><a href="#nosotros">Nosotros</a><a href="#planes">Planes</a>',
  '<a href="#como">How it works</a><a href="#propiedades">Properties</a><a href="#nosotros">About us</a><a href="#planes">Plans</a>'),
 ('>Análisis gratis</a>', '>Free analysis</a>'),
 # hero
 ('Administración de Airbnb · El Salvador', 'Airbnb property management · El Salvador'),
 ('<h1>Tu propiedad puede facturar hasta <span class="hl"><span class="n3">3</span>× más</span><span class="dot">.</span></h1>',
  '<h1>Your property could earn up to <span class="hl"><span class="n3">3</span>× more</span><span class="dot">.</span></h1>'),
 ('Gestionamos tu casa o apartamento en Airbnb de principio a fin: anuncio, precios, huéspedes, limpieza y mantenimiento. Airbnb te paga directo a tu cuenta y tú recibes un reporte claro cada mes.',
  'We manage your Airbnb house or apartment from start to finish: listing, pricing, guests, cleaning and maintenance. Airbnb pays you directly and you get a clear report every month.'),
 ('>Quiero mi análisis gratis →</a><a class="btn ghost" href="#resultados">Ver resultados</a>',
  '>Get my free analysis →</a><a class="btn ghost" href="#resultados">See results</a>'),
 ('Respuesta por WhatsApp en menos de 24 horas · Sin permanencia · ', 'WhatsApp reply within 24 hours · No lock-in · '),
 ('>Nuestro perfil en Airbnb</a>', '>Our Airbnb profile</a>'),
 ('aria-label="Sala con vista al volcán de San Salvador"', 'aria-label="Living room with a view of the San Salvador volcano"'),
 ('<span>calificación promedio</span>', '<span>average rating</span>'),
 ('<span>reseñas de huéspedes</span>', '<span>guest reviews</span>'),
 ('reseñas verificadas en Airbnb · ', 'verified Airbnb reviews · '),
 ('>ver perfil →</a>', '>see profile →</a>'),
 ('lo que factura el promedio de San Salvador', 'what the average San Salvador listing earns'),
 ('meses de permanencia obligatoria', 'months of mandatory commitment'),
 # como funciona
 ('<div class="eyebrow">Cómo funciona</div>', '<div class="eyebrow">How it works</div>'),
 ('Así ponemos tu propiedad a trabajar en Airbnb<span class="dot">.</span>', 'How we put your property to work on Airbnb<span class="dot">.</span>'),
 ('<h3>Analizamos tu propiedad y te decimos cuánto puede facturar</h3>', '<h3>We analyze your property and tell you how much it can earn</h3>'),
 ('<h3>Te recomendamos mejoras de diseño, amenidades y operación</h3>', '<h3>We recommend design, amenity and operations upgrades</h3>'),
 ('<h3>Hacemos fotos profesionales y la publicamos en Airbnb</h3>', '<h3>We shoot professional photos and list it on Airbnb</h3>'),
 ('<h3>Gestionamos todo y Airbnb te paga directo a ti</h3>', '<h3>We manage everything and Airbnb pays you directly</h3>'),
 ('aria-roledescription="carrusel" aria-label="Fotos de propiedades"', 'aria-roledescription="carousel" aria-label="Property photos"'),
 ('aria-label="Foto anterior"', 'aria-label="Previous photo"'),
 ('aria-label="Foto siguiente"', 'aria-label="Next photo"'),
 ('b.setAttribute("aria-label","Foto "+(k+1))', 'b.setAttribute("aria-label","Photo "+(k+1))'),
 # vs
 ('Renta corta vs. renta tradicional', 'Short-term vs. long-term rental'),
 ('¿Airbnb o alquiler mensual? Te lo decimos claro', 'Airbnb or a monthly lease? We tell you straight'),
 ('Las dos opciones tienen ventajas. Esto es lo que cambia para ti como propietario.', 'Both options have advantages. Here is what changes for you as an owner.'),
 ('<div class="h us">Renta corta con hōm</div><div class="h">Renta tradicional</div>', '<div class="h us">Short-term with hōm</div><div class="h">Long-term lease</div>'),
 ('Ingreso al año (apto. 2 hab., según zona)', 'Yearly income (2-bed apt., by area)'),
 ('Estabilidad del ingreso', 'Income stability'), ('Varía por temporada', 'Varies by season'), ('Fijo cada mes', 'Fixed every month'),
 ('Usar la propiedad cuando quieras', 'Use the property whenever you want'), ('Sí, bloqueas fechas', 'Yes, just block the dates'), ('No, durante el contrato', 'No, not during the lease'),
 ('Estado de la propiedad', 'Property condition'), ('Revisada después de cada huésped', 'Inspected after every guest'), ('La ves al final del contrato', 'You see it when the lease ends'),
 ('Riesgo de impago o inquilino difícil', 'Risk of non-payment or a difficult tenant'), ('Pago anticipado por Airbnb', 'Paid in advance through Airbnb'), ('Desalojo lento y costoso', 'Slow, costly eviction'),
 ('Ajustar el precio', 'Price adjustments'), ('Cada día, según demanda', 'Daily, based on demand'), ('Una vez al año', 'Once a year'),
 ('Desgaste y gastos de servicios', 'Wear and utility costs'), ('Mayor; se cubre con el ingreso', 'Higher; covered by the income'), ('<div class="y">Menor</div>', '<div class="y">Lower</div>'),
 ('Tu tiempo', 'Your time'), ('Cero: lo hacemos todo', 'Zero: we do it all'), ('Poco, salvo problemas', 'Little, unless there are problems'),
 ('<h3>Ventajas de la renta corta</h3>', '<h3>Advantages of short-term rental</h3>'),
 ('<b>Hasta 2 a 3 veces más ingreso</b><span>Cobras por noche y ajustas el precio a la demanda.</span>', '<b>Up to 2 to 3 times more income</b><span>You charge per night and adjust the price to demand.</span>'),
 ('<b>Flexibilidad total</b><span>Puedes usar tu propiedad en vacaciones o venderla sin esperar a que termine un contrato.</span>', '<b>Total flexibility</b><span>Use your property on vacation, or sell it without waiting for a lease to end.</span>'),
 ('<b>Propiedad siempre cuidada</b><span>Limpieza e inspección después de cada estancia.</span>', '<b>Always well kept</b><span>Cleaning and inspection after every stay.</span>'),
 ('<b>Menos riesgo de impago</b><span>El huésped paga antes de llegar.</span>', '<b>Less risk of non-payment</b><span>Guests pay before they arrive.</span>'),
 ('<h3>Desventajas, y cómo las manejamos</h3>', '<h3>Disadvantages, and how we handle them</h3>'),
 ('<b>Ingreso variable</b><span>Precios dinámicos y estrategia de estancias largas en temporada baja.</span>', '<b>Variable income</b><span>Dynamic pricing and a long-stay strategy in the low season.</span>'),
 ('<b>Más desgaste</b><span>Mantenimiento preventivo y reposición incluidos en el plan Completo.</span>', '<b>More wear</b><span>Preventive maintenance and restocking included in the Complete plan.</span>'),
 ('<b>Reglas y permisos</b><span>Mantenemos tu anuncio al día con las políticas de Airbnb y el reglamento de tu condominio.</span>', '<b>Rules and permits</b><span>We keep your listing compliant with Airbnb policies and your building rules.</span>'),
 ('<b>Pagas servicios y comisión</b><span>Aun así, el ingreso neto suele superar al de la renta tradicional.</span>', '<b>You pay utilities and commission</b><span>Even so, net income usually beats a long-term lease.</span>'),
 ('<b>Somos honestos:</b> si tu propiedad rinde más en renta tradicional, te lo diremos en el análisis gratis.', '<b>We are honest:</b> if your property does better as a long-term rental, we will tell you in the free analysis.'),
 ('>Comparar mi propiedad</a>', '>Compare my property</a>'),
 # galeria
 ('<div class="eyebrow">Nuestras propiedades</div>', '<div class="eyebrow">Our properties</div>'),
 ('Así se ven las propiedades que gestionamos', 'This is what the properties we manage look like'),
 ('alt="Vista del volcán de San Salvador al atardecer desde un apartamento gestionado por hōm"', 'alt="San Salvador volcano at sunset seen from an apartment managed by hōm"'),
 ('alt="Sala con vista al volcán en apartamento de Avitat, Antiguo Cuscatlán"', 'alt="Living room with volcano view in an Avitat apartment, Antiguo Cuscatlán"'),
 ('alt="Sala decorada de apartamento de renta vacacional en San Salvador"', 'alt="Decorated living room of a vacation rental apartment in San Salvador"'),
 ('alt="Piscina infinita en la azotea de un edificio en San Salvador"', 'alt="Rooftop infinity pool of a building in San Salvador"'),
 ('alt="Sala y cocina abierta de apartamento en Panorama Tower, Colonia Escalón"', 'alt="Living room and open kitchen in a Panorama Tower apartment, Colonia Escalón"'),
 ('alt="Terraza con vista a la ciudad en apartamento de renta vacacional"', 'alt="Terrace with city view in a vacation rental apartment"'),
 ('alt="Sala con vista en apartamento de Lomas de San Francisco"', 'alt="Living room with a view in a Lomas de San Francisco apartment"'),
 ('alt="Cocina equipada con barra en apartamento de Airbnb"', 'alt="Equipped kitchen with breakfast bar in an Airbnb apartment"'),
 ('alt="Balcón con vista a San Salvador y el volcán"', 'alt="Balcony overlooking San Salvador and the volcano"'),
 # mapa
 ('<div class="eyebrow">Dónde estamos</div>', '<div class="eyebrow">Where we are</div>'),
 ('Ya operamos en los mejores edificios de San Salvador y la costa', 'We already operate in the best buildings in San Salvador and on the coast'),
 ('Si tu propiedad está en uno de estos edificios o cerca, ya tenemos equipo en la zona.', 'If your property is in one of these buildings or nearby, we already have a team in the area.'),
 ('aria-label="Mapa de propiedades gestionadas por hōm"', 'aria-label="Map of properties managed by hōm"'),
 ('<p class="map-note">Ubicaciones aproximadas. · <a href="/escalon/" style="text-decoration:underline">¿Tienes propiedad en la Escalón? Mira los datos de la zona →</a></p>', '<p class="map-note">Approximate locations. · <a href="/escalon/" hreflang="es" style="text-decoration:underline">Own property in Colonia Escalón? See the area data (in Spanish) →</a></p>'),
 # resultados
 ('<div class="eyebrow">Resultados reales</div>', '<div class="eyebrow">Real results</div>'),
 ('Antes y después de hōm', 'Before and after hōm'),
 ('aria-label="Apartamento de 2 habitaciones en Vistas de Masferrer, San Salvador"', 'aria-label="2-bedroom apartment in Vistas de Masferrer, San Salvador"'),
 ('<h3>Apartamento 2 hab. · Masferrer 705</h3>', '<h3>2-bed apartment · Masferrer 705</h3>'),
 ('<small>Tradicional</small><b>$9,000/año</b>', '<small>Long-term</small><b>$9,000/yr</b>'),
 ('<small>Con hōm, año 1</small><b>$29,036/año</b>', '<small>With hōm, year 1</small><b>$29,036/yr</b>'),
 ('3.2× más ingreso.</b> En 2022 se alquilaba en $750 al mes; en su primer año en renta corta facturó $29,036.', '3.2× more income.</b> In 2022 it rented for $750 a month; in its first year as a short-term rental it earned $29,036.'),
 ('aria-label="Apartamento de 3 habitaciones en Panorama Tower, San Salvador"', 'aria-label="3-bedroom apartment in Panorama Tower, San Salvador"'),
 ('<h3>Apartamento 3 hab. · Panorama 306</h3>', '<h3>3-bed apartment · Panorama 306</h3>'),
 ('<small>Tradicional*</small><b>$14,400/año</b>', '<small>Long-term*</small><b>$14,400/yr</b>'),
 ('<small>Con hōm, año 1</small><b>$28,200/año</b>', '<small>With hōm, year 1</small><b>$28,200/yr</b>'),
 ('Casi 2× más ingreso.</b> Nació como Airbnb. *Estimado de mercado: $1,200 al mes en alquiler tradicional.', 'Almost 2× more income.</b> It started as an Airbnb. *Market estimate: $1,200 a month as a long-term rental.'),
 ('“En noviembre de 2024 le entregué a hōm mi propiedad, amueblada con piezas de alta gama. Mi mayor preocupación era el cuidado, y la verdad es que tanto los muebles como la casa se han mantenido en perfecto estado gracias al mantenimiento constante. Los resultados han superado lo que esperaba: este año la propiedad va encaminada a generar alrededor de $30,000. Y lo mejor es la flexibilidad, porque cuando vengo a El Salvador bloqueamos las fechas y la disfruto como mi casa.”',
  '“In November 2024 I handed my property to hōm, furnished with high-end pieces. My biggest concern was how it would be cared for, and honestly both the furniture and the house have stayed in perfect condition thanks to constant maintenance. The results have beaten my expectations: this year the property is on track to generate around $30,000. And the best part is the flexibility: when I come to El Salvador we block the dates and I enjoy it as my home.”'),
 ('<b>Alejandro Acuña</b> · Propietario · Administración en Airbnb desde 2024', '<b>Alejandro Acuña</b> · Owner · Airbnb management since 2024'),
 # nosotros
 ('aria-label="Apartamento gestionado por hōm"', 'aria-label="Apartment managed by hōm"'),
 ('<div class="eyebrow">Sobre nosotros</div>', '<div class="eyebrow">About us</div>'),
 ('Somos anfitriones antes que administradores', 'We were hosts before we were managers'),
 ('Llevamos 4 años recibiendo huéspedes en El Salvador. Empezamos con nuestras propias propiedades, aprendimos qué hace que un huésped deje cinco estrellas y qué números hacen rentable una propiedad, y hoy aplicamos ese mismo estándar a cada propiedad que gestionamos.',
  'We have been hosting guests in El Salvador for 4 years. We started with our own properties, learned what makes a guest leave five stars and which numbers make a property profitable, and today we apply that same standard to every property we manage.'),
 ('<span>años como anfitriones</span>', '<span>years as hosts</span>'),
 ('<span>huéspedes recibidos</span>', '<span>guests hosted</span>'),
 ('<span>en 479 reseñas</span>', '<span>across 479 reviews</span>'),
 ('<h3>Expertos en números</h3><p>Decidimos con datos: precios, ocupación y rentabilidad medidos cada mes, para que tu propiedad rinda lo máximo.</p>',
  '<h3>Numbers experts</h3><p>We decide with data: pricing, occupancy and profitability measured every month so your property performs at its best.</p>'),
 ('<h3>Equipo entrenado</h3><p>Limpieza, mantenimiento y atención al huésped con personal formado para renta vacacional, no improvisado.</p>',
  '<h3>Trained team</h3><p>Cleaning, maintenance and guest care by staff trained for vacation rentals, not improvised.</p>'),
 ('<h3>Ojo al detalle</h3><p>Revisamos cada propiedad después de cada estancia: amenidades, blancos, decoración y funcionamiento.</p>',
  '<h3>Eye for detail</h3><p>We check every property after every stay: amenities, linens, decor and everything working.</p>'),
 ('<h3>Trato cercano</h3><p>Hablas directo con nosotros por WhatsApp. Sin call centers ni respuestas automáticas.</p>',
  '<h3>Personal service</h3><p>You talk to us directly on WhatsApp. No call centers, no automated replies.</p>'),
 ('>Ver nuestro perfil y reseñas en Airbnb →</a>', '>See our Airbnb profile and reviews →</a>'),
 ('Síguenos: <a', 'Follow us: <a'),
 # planes
 ('<div class="eyebrow">Planes</div>', '<div class="eyebrow">Plans</div>'),
 ('Solo ganamos si tú ganas', 'We only earn when you earn'),
 ('Cobramos un porcentaje de lo reservado. Sin cuota fija, sin permanencia.', 'We charge a percentage of bookings. No fixed fee, no lock-in.'),
 ('data-z="ciudad" type="button">Ciudad</button><button data-z="playa" type="button">Playa</button>', 'data-z="ciudad" type="button">City</button><button data-z="playa" type="button">Beach</button>'),
 ('<h3>Básico</h3><div class="desc">Lo esencial para que tu propiedad rente bien.</div>', '<h3>Basic</h3><div class="desc">The essentials for your property to rent well.</div>'),
 ('<div class="per">de cada reserva</div>', '<div class="per">of each booking</div>'),
 ('<li>Anuncio optimizado</li><li>Precios dinámicos</li><li>Mensajes con huéspedes 24/7</li><li>Coordinación de limpiezas</li><li>Reporte mensual</li><li>30% de descuento en sesión de fotos</li>',
  '<li>Optimized listing</li><li>Dynamic pricing</li><li>24/7 guest messaging</li><li>Cleaning coordination</li><li>Monthly report</li><li>30% off the photo shoot</li>'),
 ('<li class="no">Coordinación de mantenimiento</li><li class="no">Entrega de suministros</li><li class="no">Asesoría de interiores y operativa</li>',
  '<li class="no">Maintenance coordination</li><li class="no">Supply delivery</li><li class="no">Interior and operations advice</li>'),
 ('data-msg="Hola, me interesa el plan Básico.">Elegir Básico</a>', 'data-msg="Hi, I am interested in the Basic plan.">Choose Basic</a>'),
 ('<div class="tag">El más elegido</div>', '<div class="tag">Most popular</div>'),
 ('<h3>Completo</h3><div class="desc">Nos encargamos de todo. Tú solo recibes.</div>', '<h3>Complete</h3><div class="desc">We handle everything. You just get paid.</div>'),
 ('<li>Todo lo del plan Básico</li><li>Coordinación de mantenimiento</li><li>Entrega de suministros y amenidades</li><li>Asesoría de interiores y operativa</li>',
  '<li>Everything in Basic</li><li>Maintenance coordination</li><li>Supply and amenity delivery</li><li>Interior and operations advice</li>'),
 ('<li>Sesión de fotos profesional gratis</li><li>60 días con comisión reducida</li>', '<li>Free professional photo shoot</li><li>60 days at a reduced commission</li>'),
 ('Coordinamos mantenimientos y amenidades; su costo lo cubre el propietario.', 'We coordinate maintenance and amenities; the owner covers their cost.'),
 ('data-msg="Hola, me interesa el plan Completo.">Quiero el plan Completo</a>', 'data-msg="Hi, I am interested in the Complete plan.">I want the Complete plan</a>'),
 ('<div class="desc">Todo incluido: tú no pagas gastos de operación.</div>', '<div class="desc">All-inclusive: you pay no operating costs.</div>'),
 ('<li>Todo lo del plan Completo</li><li>Pagamos el equipo de limpieza</li><li>Pagamos insumos y amenidades</li><li>Pagamos los mantenimientos</li>',
  '<li>Everything in Complete</li><li>We pay the cleaning team</li><li>We pay supplies and amenities</li><li>We pay for maintenance</li>'),
 ('<li>Atención prioritaria al propietario</li><li>Gestor dedicado</li>', '<li>Priority owner support</li><li>Dedicated manager</li>'),
 ('Los gastos incluidos tienen un monto máximo mensual, definido según la propiedad.', 'Included costs have a monthly cap, set according to the property.'),
 ('data-msg="Hola, me interesa el plan Premium.">Elegir Premium</a>', 'data-msg="Hi, I am interested in the Premium plan.">Choose Premium</a>'),
 ('<b>Sin permanencia:</b> te vas con 30 días de aviso', '<b>No lock-in:</b> leave with 30 days notice'),
 ('<b>Sin cuota fija:</b> si no hay reservas, no cobramos', '<b>No fixed fee:</b> no bookings, no charge'),
 ('<b>Transparencia total:</b> Airbnb te paga directo, nunca tocamos tu dinero', '<b>Full transparency:</b> Airbnb pays you directly, we never touch your money'),
 # renta fija
 ('<div class="eyebrow">Otra modalidad · Rent to rent</div>', '<div class="eyebrow">Another option · Rent to rent</div>'),
 ('¿Prefieres un ingreso fijo? Nosotros te rentamos tu propiedad', 'Prefer a fixed income? We rent your property from you'),
 ('Tú nos alquilas tu propiedad con un contrato a largo plazo. Nosotros la amueblamos, la equipamos y la ponemos a trabajar en renta vacacional. Tú recibes una renta fija cada mes, haya o no reservas.',
  'You lease your property to us on a long-term contract. We furnish it, equip it and put it to work as a vacation rental. You receive a fixed rent every month, with or without bookings.'),
 ('data-msg="Hola, me interesa la modalidad rent to rent para mi propiedad.">Evaluar mi propiedad para rent to rent →</a>', 'data-msg="Hi, I am interested in rent to rent for my property.">Evaluate my property for rent to rent →</a>'),
 ('<b>Ingreso fijo</b><span>Una renta mensual garantizada por contrato, sin depender de la temporada.</span>', '<b>Fixed income</b><span>A monthly rent guaranteed by contract, regardless of the season.</span>'),
 ('<b>Nosotros amueblamos</b><span>Invertimos en muebles, equipamiento y decoración para que la propiedad esté lista para huéspedes.</span>', '<b>We furnish it</b><span>We invest in furniture, equipment and decor so the property is guest-ready.</span>'),
 ('<b>Contratos largos</b><span>Acuerdos de varios años, con estabilidad para ti y para nosotros.</span>', '<b>Long contracts</b><span>Multi-year agreements, with stability for you and for us.</span>'),
 ('<b>Cero gestión</b><span>Nos encargamos de todo: huéspedes, limpieza, mantenimiento y gastos de operación.</span>', '<b>Zero hassle</b><span>We handle everything: guests, cleaning, maintenance and operating costs.</span>'),
 ('alt="Héctor Pleites, propietario en renta fija con hōm"', 'alt="Héctor Pleites, owner on a fixed-rent contract with hōm"'),
 ('“Hace más de dos años firmé con hōm un contrato de tres años por mi apartamento. Ellos se encargaron de amueblarlo y ponerlo a punto para trabajarlo, sin que yo tuviera que invertir ni coordinar nada. Desde entonces todos los pagos han llegado puntuales, y nunca me han pedido ayuda con nada. Para mí es un ingreso fijo, seguro y totalmente estable. Me olvido del apartamento y sé que está bien cuidado.”',
  '“More than two years ago I signed a three-year contract with hōm for my apartment. They furnished it and got it ready to operate without me having to invest or coordinate anything. Since then every payment has arrived on time, and they have never needed my help with anything. For me it is a fixed, secure and completely stable income. I don’t have to think about the apartment and I know it is well cared for.”'),
 ('<b>Héctor Pleites</b> · Propietario en renta fija desde hace más de 2 años', '<b>Héctor Pleites</b> · Fixed-rent owner for over 2 years'),
 ('alt="Jorge Cáceres, propietario en Avitat Joy"', 'alt="Jorge Cáceres, owner at Avitat Joy"'),
 ('“Empecé con hōm alquilándoles mi apartamento en Avitat Joy con un contrato de dos años. Fue una experiencia tan buena que, al terminar, no quise volver a la renta tradicional. Decidimos que hōm se quedara administrando la propiedad en Airbnb. Ya llevamos casi un año así. Conozco las dos modalidades y en ambas he tenido la misma tranquilidad y el mismo cuidado de mi propiedad.”',
  '“I started with hōm by leasing them my apartment at Avitat Joy on a two-year contract. It went so well that when it ended I didn’t want to go back to a long-term lease. We decided hōm would keep managing the property on Airbnb, and we are almost a year into that now. I know both options, and with both I have had the same peace of mind and the same care for my property.”'),
 ('<b>Jorge Cáceres</b> · Propietario en Avitat Joy · Primero renta fija, hoy administración', '<b>Jorge Cáceres</b> · Owner at Avitat Joy · First fixed rent, now management'),
 ('Esta modalidad depende del potencial de cada propiedad: zona, vista, tamaño y amenidades del edificio. Lo evaluamos en el análisis gratis.',
  'This option depends on each property’s potential: area, view, size and building amenities. We evaluate it in the free analysis.'),
 # realtors
 ('<div class="eyebrow">Programa de referidos</div>', '<div class="eyebrow">Referral program</div>'),
 ('¿Eres realtor? Conéctanos una propiedad y gana $500', 'Are you a realtor? Connect us with a property and earn $500'),
 ('Si tienes clientes que compran para invertir o propietarios que no saben qué hacer con su propiedad, preséntanos. Por cada propiedad que firme con hōm, te pagamos <b>$500</b> después de su primer mes completo de gestión.',
  'If you have clients buying to invest, or owners who don’t know what to do with their property, introduce us. For every property that signs with hōm, we pay you <b>$500</b> after its first full month under management.'),
 ('>Quiero referir una propiedad →</button>', '>Refer a property →</button>'),
 ('<b>Nos presentas</b><span>Llenas el formulario con tus datos y los de la propiedad.</span>', '<b>You introduce us</b><span>Fill out the form with your details and the property’s.</span>'),
 ('<b>Nosotros evaluamos</b><span>Hacemos el análisis gratis y le presentamos la propuesta al propietario.</span>', '<b>We evaluate</b><span>We run the free analysis and present the proposal to the owner.</span>'),
 ('<b>Tú cobras</b><span>Al completarse el primer mes de gestión de la propiedad, recibes $500.</span>', '<b>You get paid</b><span>Once the property completes its first month under management, you receive $500.</span>'),
 # dialogo realtor
 ('aria-label="Cerrar"', 'aria-label="Close"'),
 ('<h3>Referir una propiedad</h3>', '<h3>Refer a property</h3>'),
 ('Te contactamos pronto. Si el propietario firma con hōm, ganas $500 al completarse su primer mes de gestión.', 'We will contact you soon. If the owner signs with hōm, you earn $500 once their first month under management is complete.'),
 ('data-form="Referido de realtor"', 'data-form="Realtor referral (EN)"'),
 ('<label>Tu nombre<input', '<label>Your name<input'),
 ('<label>Tu teléfono / WhatsApp<input', '<label>Your phone / WhatsApp<input'),
 ('<span>Tu correo <small>(opcional)</small></span>', '<span>Your email <small>(optional)</small></span>'),
 ('<label>Tipo<select name="Tipo de propiedad"><option>Apartamento</option><option>Casa</option><option>Casa de playa</option><option>Otro</option></select>',
  '<label>Type<select name="Tipo de propiedad"><option>Apartment</option><option>House</option><option>Beach house</option><option>Other</option></select>'),
 ('<span>Nombre del propietario <small>(opcional)</small></span>', '<span>Owner’s name <small>(optional)</small></span>'),
 ('<label class="full">¿El propietario ya sabe de hōm?<select name="Propietario informado"><option>Sí, ya le hablé de hōm</option><option>Todavía no</option></select>',
  '<label class="full">Does the owner know about hōm?<select name="Propietario informado"><option>Yes, I told them about hōm</option><option>Not yet</option></select>'),
 ('<span>Comentarios <small>(opcional)</small></span>', '<span>Comments <small>(optional)</small></span>'),
 ('placeholder="Estado de la propiedad, si está amueblada, si hoy se renta, etc."', 'placeholder="Condition, whether it is furnished, whether it is rented today, etc."'),
 ('>Enviar referido →</button>', '>Send referral →</button>'),
 # preguntas
 ('<div class="eyebrow">Preguntas frecuentes</div>', '<div class="eyebrow">FAQ</div>'),
 ('Lo que nos preguntan los propietarios', 'What owners ask us'),
 ('¿Qué tengo que hacer yo como propietario? <span>+</span></summary><p>Nada. Nosotros manejamos la gestión completa. Durante el mes pagamos los gastos del día a día de tu propiedad (insumos, reparaciones menores y lo que haga falta para operar). A fin de mes te enviamos el reporte con la conciliación de esos gastos y te hacemos un solo cobro. Ese es el único contacto que necesitas tener con nosotros.',
  'What do I have to do as an owner? <span>+</span></summary><p>Nothing. We handle the full management. During the month we pay your property’s day-to-day costs (supplies, minor repairs and whatever it takes to operate). At the end of the month we send you a report reconciling those costs and charge you once. That is the only contact you need to have with us.'),
 ('¿Puedo seguir usando mi propiedad algunos fines de semana? <span>+</span></summary><p>Sí. Nos avisas con anticipación y bloqueamos esas fechas en el calendario.',
  'Can I still use my property on some weekends? <span>+</span></summary><p>Yes. Let us know in advance and we block those dates on the calendar.'),
 ('¿Quién paga la limpieza? <span>+</span></summary><p>La limpieza se cobra al huésped en cada reserva como tarifa de limpieza. Nosotros la coordinamos y revisamos que la propiedad quede lista.',
  'Who pays for cleaning? <span>+</span></summary><p>Cleaning is charged to the guest on each booking as a cleaning fee. We coordinate it and check that the property is ready.'),
 ('¿Cómo y cuándo recibo mi dinero? <span>+</span></summary><p>Airbnb te deposita directamente en tu cuenta bancaria. Por transparencia, nosotros nunca recibimos ni manejamos tu dinero. Para ahorrar en costos de transferencia, te recomendamos configurar en tu cuenta un monto mínimo para recibir los pagos, en lugar de una transferencia por cada reserva.',
  'How and when do I get paid? <span>+</span></summary><p>Airbnb deposits directly into your bank account. For transparency, we never receive or handle your money. To save on transfer fees, we recommend setting a minimum payout threshold in your account instead of a transfer for every booking.'),
 ('Vivo fuera del país, ¿cómo funciona? <span>+</span></summary><p>Muchos de nuestros propietarios viven en Estados Unidos. Todo se maneja por WhatsApp y videollamada, y recibes el reporte mensual donde estés.',
  'I live abroad. How does it work? <span>+</span></summary><p>Many of our owners live in the United States. Everything is handled over WhatsApp and video call, and you get the monthly report wherever you are.'),
 # final
 ('<h2>Descubre cuánto puede facturar tu propiedad</h2>', '<h2>Find out how much your property can earn</h2>'),
 ('Análisis gratis y sin compromiso. Déjanos tus datos y te contactamos, o escríbenos directo.', 'Free, no-commitment analysis. Leave your details and we will contact you, or message us directly.'),
 ('<div class="or">¿Prefieres WhatsApp?</div>', '<div class="or">Prefer WhatsApp?</div>'),
 ('data-msg="Hola, quiero saber cuánto puede facturar mi propiedad.">Escribir por WhatsApp →</a>', 'data-msg="Hi, I would like to know how much my property can earn.">Message us on WhatsApp →</a>'),
 ('Aceptamos solo 3 propiedades nuevas al mes para cuidar la calidad.', 'We take on only 3 new properties a month to protect quality.'),
 ('data-form="Propietario interesado"', 'data-form="Interested owner (EN)"'),
 ('<label>Nombre<input name="Nombre"', '<label>Name<input name="Nombre"'),
 ('<label>Teléfono / WhatsApp<input name="Teléfono"', '<label>Phone / WhatsApp<input name="Teléfono"'),
 ('<label class="full">Correo<input', '<label class="full">Email<input'),
 ('<label class="full">Hoy la propiedad está<select name="Situación actual"><option>Vacía</option><option>En renta tradicional</option><option>Ya en Airbnb</option><option>En construcción / por entregar</option></select>',
  '<label class="full">The property is currently<select name="Situación actual"><option>Empty</option><option>On a long-term lease</option><option>Already on Airbnb</option><option>Under construction / not yet delivered</option></select>'),
 ('<label class="full">Me interesa<select name="Servicio de interés"><option>Administración en Airbnb (comisión)</option><option>Renta fija (ustedes me rentan la propiedad)</option><option>No sé, quiero que me asesoren</option></select>',
  '<label class="full">I am interested in<select name="Servicio de interés"><option>Airbnb management (commission)</option><option>Fixed rent (you lease my property)</option><option>Not sure, I would like advice</option></select>'),
 ('<span>Mensaje <small>(opcional)</small></span>', '<span>Message <small>(optional)</small></span>'),
 ('>Quiero mi análisis gratis →</button>', '>Get my free analysis →</button>'),
 # footer / flotante
 ('data-msg="Hola, quiero información sobre la gestión de mi propiedad."', 'data-msg="Hi, I would like information about managing my property."'),
 ('<a class="wa" data-msg="Hola">WhatsApp</a>', '<a class="wa" data-msg="Hi">WhatsApp</a>'),
 # scripts
 ('btn.textContent="Enviando...";', 'btn.textContent="Sending...";'),
 ('<h3>¡Formulario enviado!</h3>', '<h3>Form sent!</h3>'),
 ('<p>Gracias. Recibimos tus datos y te contactaremos pronto.</p>', '<p>Thank you. We received your details and will contact you soon.</p>'),
 ('onclick="this.closest(\'dialog\').close()">Cerrar</button>', 'onclick="this.closest(\'dialog\').close()">Close</button>'),
 ("'No se pudo enviar el formulario. <a", "'The form could not be sent. <a"),
 ('" target="_blank" rel="noopener" style="text-decoration:underline">Envíanos tus datos por WhatsApp</a>.\'', '" target="_blank" rel="noopener" style="text-decoration:underline">Send us your details on WhatsApp</a>.\''),
 ('encodeURIComponent("Hola, quiero información.\\n"', 'encodeURIComponent("Hi, I would like information.\\n"'),
 ('data-msg="Hola, quiero comparar si me conviene más Airbnb o renta tradicional."', 'data-msg="Hi, I would like to compare whether Airbnb or a long-term lease is better for me."'),
]

# textos que se repiten en varios lugares: se reemplazan todos
TODOS = [
 ('data-msg="Hola, quiero mi análisis gratis de ingresos para mi propiedad."', 'data-msg="Hi, I would like my free income analysis for my property."'),
 ('<span>calificación promedio</span>', '<span>average rating</span>'),
 ('>Ubicación de la propiedad<input', '>Property location<input'),
 ('placeholder="Colonia, ciudad o playa"', 'placeholder="Neighborhood, city or beach"'),
 ('<legend>Cantidad de cuartos</legend>', '<legend>Bedrooms</legend>'),
 ('value="Estudio" required><span>Estudio</span>', 'value="Studio" required><span>Studio</span>'),
 ('value="4 o más"><span>4 o más</span>', 'value="4+"><span>4 or more</span>'),
]

faltan = []
for a, b in HEAD:
    if a not in s: faltan.append(a)
    s = s.replace(a, b, 1)
for a, b in TODOS:
    if a not in s: faltan.append(a)
    s = s.replace(a, b)
for a, b in PARES:
    if a not in s and b not in s: faltan.append(a)
    s = s.replace(a, b, 1)

# rutas relativas: la página vive en /en/
s = re.sub(r'(src|href)="(img|vendor)/', r'\1="../\2/', s)
s = s.replace('url(img/', 'url(../img/')
s = s.replace('sc.src="vendor/', 'sc.src="../vendor/')

# datos estructurados en inglés (FAQ desde el propio HTML)
strip = lambda x: html.unescape(re.sub('<[^>]+>', '', x)).strip()
faqs = re.findall(r'<details class="q"><summary>(.*?) <span>\+</span></summary><p>(.*?)</p></details>', s)
m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
ld = json.loads(m.group(1))
for node in ld["@graph"]:
    if node["@type"] == "LocalBusiness":
        node["description"] = "Airbnb and vacation rental property management in San Salvador and the coast of El Salvador."
        node["url"] = "https://homlatam.com/en/"
        node["knowsAbout"] = ["Airbnb management", "Vacation rentals", "Property management", "Rent to rent"]
    if node["@type"] == "FAQPage":
        node["mainEntity"] = [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faqs]
s = s[:m.start(1)] + json.dumps(ld, ensure_ascii=False) + s[m.end(1):]

# avisa si queda español visible
restos = [w for w in ["Propietario", "Nosotros", "Análisis", "año", "reseñas", "Escríbenos", "¿"] if w in re.sub(r'name="[^"]*"', '', s.split("<body>",1)[1].split("<script>",1)[0])]

out = ROOT / "en" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(s)
print("OK ->", out)
if faltan:
    print("\nNO ENCONTRADOS (revisa la traducción):")
    for f in faltan: print(" -", f[:110])
if restos: print("\nPosible español restante:", restos)
sys.exit(1 if faltan else 0)
