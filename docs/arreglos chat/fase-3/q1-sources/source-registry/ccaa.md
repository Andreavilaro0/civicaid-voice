# CCAA Source Registry — Comunidades Autonomas

> Research date: 2026-02-18
> Status: Complete — all 19 communities/cities profiled with verified URLs
> Author: Clara RAG Research Team
> Scope: 17 Comunidades Autonomas + 2 Ciudades Autonomas (Ceuta, Melilla)

---

## Executive Summary

Spain is organized into 17 Comunidades Autonomas (CCAA) and 2 Ciudades Autonomas (Ceuta and Melilla). Under the Spanish Constitution of 1978 and their respective Estatutos de Autonomia, the CCAA hold **exclusive or shared competence** over the areas most critical to Clara's users:

- **Healthcare (Sanidad):** Each CCAA manages its own public health service (e.g., SERMAS in Madrid, CatSalut in Catalunya, SAS in Andalucia). Tarjeta sanitaria issuance is a CCAA-level procedure.
- **Education (Educacion):** School enrollment (matriculacion), scholarships (becas), and vocational training are managed at CCAA level.
- **Social Services (Servicios Sociales):** Minimum income schemes (RMI/Renta de Insercion), dependency benefits (Ley de Dependencia implementation), and social emergency aid are CCAA responsibilities.
- **Housing (Vivienda):** Social housing registries, rental aid programs, and housing access plans are CCAA-managed.
- **Employment (Empleo):** Each CCAA has its own employment service (e.g., LABORA in Valencia, Lanbide in Euskadi, SAE in Andalucia) that complements the national SEPE.

For Clara, CCAA sources are **the most procedure-dense tier** of government. A vulnerable person in Spain interacts with their CCAA far more frequently than with the AGE (central government) for day-to-day needs like healthcare enrollment, school registration, or social aid applications.

**Key statistics (INE, January 2025):**
- Total population of Spain: 49,128,297
- Foreign nationals: 6,911,971 (14.1%)
- Highest foreign-born %: Illes Balears (27.65%), Catalunya (23.80%), Madrid (23.80%), Comunitat Valenciana (22.51%)
- Highest net external migration (2024): Catalunya (129,030), Madrid (113,964), Comunitat Valenciana (104,776)

---

## Summary Table

| # | CCAA | Sede Electronica | Catalogo de Tramites | Deteccion | Idiomas | Prioridad |
|---|------|-------------------|----------------------|-----------|---------|-----------|
| 1 | Comunidad de Madrid | https://sede.comunidad.madrid/ | https://sede.comunidad.madrid/buscador | Sitemap XML, manual | ES | P0 |
| 2 | Catalunya | https://web.gencat.cat/ca/seu-electronica/ | https://web.gencat.cat/ca/seu-electronica/tramits-i-serveis | API (Socrata/Open Data), sitemap | CA, ES | P0 |
| 3 | Andalucia | https://www.juntadeandalucia.es/servicios/sede.html | https://www.juntadeandalucia.es/servicios/sede/tramites/procedimientos.html | Sitemap, manual | ES | P0 |
| 4 | Comunitat Valenciana | https://sede.gva.es/es/ | https://www.gva.es/es/inicio/atencion_ciudadano/buscadores/tramites_servicios | Guia PROP (novedades), manual | ES, CA/VA | P0 |
| 5 | Canarias | https://sede.gobiernodecanarias.org/sede/ | Integrado en sede (934 proc.) | Manual | ES | P0 |
| 6 | Pais Vasco (Euskadi) | https://www.euskadi.eus/sede-electronica/ | https://www.euskadi.eus/sede-electronica/ (catalogo integrado) | datos.gob.es, manual | ES, EU | P1 |
| 7 | Castilla y Leon | https://www.tramitacastillayleon.jcyl.es/web/es/sede-electronica.html | https://www.tramitacastillayleon.jcyl.es/web/es/tramites-servicios/buscador-tramites-servicios.html | Sitemap, manual | ES | P1 |
| 8 | Castilla-La Mancha | https://www.jccm.es/ | https://www.jccm.es/tramites/buscador | Manual | ES | P1 |
| 9 | Galicia | https://sede.xunta.gal/es/portada | https://sede.xunta.gal/guia-de-procedementos-e-servizos | Sitemap, manual | GL, ES | P1 |
| 10 | Region de Murcia | https://sede.carm.es/ | https://www.carm.es/guiadeservicios | Manual | ES | P1 |
| 11 | Aragon | https://www.aragon.es/tramites/servicios-de-la-sede-electronica | https://www.aragon.es/tramites (~1300 servicios) | Manual | ES | P1 |
| 12 | Illes Balears | https://www.caib.es/seucaib/es/ | https://www.caib.es/seucaib/es/ (catalogo integrado) | Manual | CA, ES | P1 |
| 13 | Extremadura | https://tramites.juntaex.es/ | https://tramites.juntaex.es/sta/CarpetaPublic/doEvent?APP_CODE=STA&PAGE_CODE=CATALOGO | Manual | ES | P1 |
| 14 | Asturias | https://sede.asturias.es/ | https://sede.asturias.es/todos-los-servicios-y-tramites | Manual | ES | P2 |
| 15 | Navarra | https://www.navarra.es/es/tramites | https://www.navarra.es/es/tramites/buscador | Manual | ES, EU | P2 |
| 16 | Cantabria | https://sede.cantabria.es/sede/ | https://sede.cantabria.es/sede/catalogo-de-tramites (1253 proc.) | Manual | ES | P2 |
| 17 | La Rioja | https://web.larioja.org/sede-electronica | https://web.larioja.org/oficina-electronica/ | Manual | ES | P2 |
| 18 | Ceuta | https://sede.ceuta.es/ | Integrado en sede (494 proc., 479 online) | Manual | ES | P2 |
| 19 | Melilla | https://sede.melilla.es/ | https://sede.melilla.es/sta/CarpetaPublic/doEvent?APP_CODE=STA&PAGE_CODE=CATALOGO | Manual | ES | P2 |

---

## Detailed Profiles

### P0 — High Priority

---

### 1. Comunidad de Madrid

- **Sede Electronica:** https://sede.comunidad.madrid/
- **Catalogo de tramites:** https://sede.comunidad.madrid/buscador
- **Guia de tramitacion:** https://sede.comunidad.madrid/guia-tramitacion-electronica
- **Formato:** HTML (fichas de tramites), PDF (formularios descargables)
- **Deteccion de cambios:** Sitemap XML disponible en https://www.comunidad.madrid/sitemap; no se ha identificado RSS especifico para tramites ni API publica de catalogo
- **Idiomas:** ES
- **Notas:**
  - El Ayuntamiento de Madrid tiene su propia sede en https://sede.madrid.es/ (nivel local, no CCAA)
  - Portal de datos abiertos del Ayuntamiento: https://datos.madrid.es/ (pero es nivel municipal)
  - La Comunidad esta desarrollando una plataforma para municipios menores de 20.000 habitantes
  - Procedimientos clave: empadronamiento (municipal), tarjeta sanitaria, becas educacion, vivienda

---

### 2. Catalunya

- **Sede Electronica (Seu Electronica):** https://web.gencat.cat/ca/seu-electronica/
- **Catalogo de tramites (Tramits i Serveis):** https://web.gencat.cat/ca/seu-electronica/tramits-i-serveis
- **Portal de tramites:** https://tramits.gencat.cat/
- **Oficina Virtual:** https://ovt.gencat.cat/carpetaciutadana360
- **Formato:** HTML (fichas detalladas), PDF (formularios)
- **Deteccion de cambios:**
  - **API Open Data:** Dataset en datos.gob.es — https://datos.gob.es/en/catalogo/a09002970-tramites-de-la-generalitat-de-catalunya
  - Plataforma Socrata: https://analisi.transparenciacatalunya.cat/ con API REST
  - Portal de datos abiertos: https://administraciodigital.gencat.cat/ca/dades/dades-obertes/inici/
  - Catalogo de procedimientos en Govern Obert: https://governobert.gencat.cat/es/transparencia/Organitzacio-i-normativa/cataleg-de-serveis/cataleg-de-procediments/
- **Idiomas:** CA (catalan, principal), ES (castellano)
- **Notas:**
  - Mas de 1.400 tramites catalogados
  - Consorci AOC (Administracio Oberta de Catalunya): https://www.aoc.cat/ — plataforma compartida para administraciones locales catalanas
  - Mejor infraestructura de datos abiertos entre las CCAA para deteccion automatizada
  - Procedimientos clave: tramits d'estrangeria, targeta sanitaria (CatSalut), empadronament, educacio

---

### 3. Andalucia

- **Sede Electronica General:** https://www.juntadeandalucia.es/servicios/sede.html
- **Acceso a tramites:** https://www.juntadeandalucia.es/servicios/sede/tramites.html
- **Catalogo de Procedimientos y Servicios:** https://www.juntadeandalucia.es/servicios/sede/tramites/procedimientos.html
- **Portal de servicios:** https://www.juntadeandalucia.es/servicios.html
- **Formato:** HTML (fichas), PDF (formularios)
- **Deteccion de cambios:** Sitemap probable; no se ha identificado RSS ni API publica especifica para el catalogo de tramites
- **Idiomas:** ES
- **Notas:**
  - Incluye Carpeta Ciudadana, notificaciones electronicas, plataforma de pagos
  - Presentacion Electronica General: https://www.juntadeandalucia.es/servicios/tramites/presentacion-documentos/peg.html
  - Procedimientos clave: tarjeta sanitaria SAS, educacion, vivienda, empleo SAE

---

### 4. Comunitat Valenciana

- **Sede Electronica:** https://sede.gva.es/es/
- **Buscador de tramites y servicios (Guia PROP):** https://www.gva.es/es/inicio/atencion_ciudadano/buscadores/tramites_servicios
- **Portal Guia PROP:** https://www.gva.es/es/inicio/atencion_ciudadano/buscadores
- **Novedades en tramites:** https://www.gva.es/es/web/atencio_ciutadania/inicio/atencion_ciudadano/novedades/nov_tram_serv
- **Transparencia — tramites:** https://gvaoberta.gva.es/es/tramites
- **Formato:** HTML (fichas detalladas por procedimiento con id_proc), PDF
- **Deteccion de cambios:**
  - Pagina de novedades de tramites y servicios (ultimos 10 dias) — puede servir como fuente de polling
  - No se ha identificado RSS ni API publica especifica
- **Idiomas:** ES, CA/VA (valenciano)
- **Notas:**
  - Los tramites tienen URL con patron predecible: https://www.gva.es/es/inicio/procedimientos?id_proc=XXXXX
  - Carpeta Ciudadana disponible via sede.gva.es
  - Red de oficinas PROP para atencion presencial
  - Procedimientos clave: tarjeta sanitaria SIP, educacion, vivienda, empleo LABORA

---

### 5. Canarias

- **Sede Electronica:** https://sede.gobiernodecanarias.org/sede/
- **Catalogo de tramites:** Integrado en la sede electronica (934 procedimientos catalogados)
- **Portal general:** https://www.gobiernodecanarias.org/
- **Formato:** HTML (fichas de procedimiento), PDF
- **Deteccion de cambios:** Manual; la sede tiene buscador con multiples criterios de busqueda
- **Idiomas:** ES
- **Notas:**
  - La sede integra todos los departamentos del Gobierno de Canarias excepto la Agencia Tributaria Canaria y el Servicio Canario de Empleo
  - Cabildo de Gran Canaria tiene sede propia: https://sede.grancanaria.com/
  - Procedimientos clave: tarjeta sanitaria SCS, educacion, vivienda, REF canario

---

### P1 — Medium Priority

---

### 6. Pais Vasco (Euskadi)

- **Sede Electronica:** https://www.euskadi.eus/sede-electronica/
- **Catalogo de tramites:** Integrado en la sede — https://www.euskadi.eus/sede-electronica/ (busqueda por catalogo)
- **Portal general:** https://www.euskadi.eus/inicio/
- **Mi Carpeta:** https://www.euskadi.eus/mi-carpeta/web01-sede/es/
- **Formato:** HTML (fichas), PDF
- **Deteccion de cambios:**
  - Dataset en datos.gob.es con anuncios del tablon de la sede electronica (ultimos 90 dias)
  - Manual para catalogo general
- **Idiomas:** ES, EU (euskera)
- **Notas:**
  - Servicio de atencion Zuzenean (telefono 012)
  - Sistema de identificacion via Izenpe (certificado digital propio del Pais Vasco)
  - Procedimientos clave: Osakidetza (sanidad), educacion, vivienda, Lanbide (empleo)

---

### 7. Castilla y Leon

- **Sede Electronica:** https://www.tramitacastillayleon.jcyl.es/web/es/sede-electronica.html
- **Buscador de tramites:** https://www.tramitacastillayleon.jcyl.es/web/es/tramites-servicios/buscador-tramites-servicios.html
- **Tramites y servicios:** https://www.tramitacastillayleon.jcyl.es/web/es/tramites-servicios.html
- **Formato:** HTML (fichas organizadas por materia y tipo), PDF
- **Deteccion de cambios:** Manual; organizacion por categorias (Educacion, Sanidad, Servicios Sociales, etc.)
- **Idiomas:** ES
- **Notas:**
  - Categorias principales: Educacion, Sanidad, Servicios Sociales y mayores, Ayudas/becas/subvenciones, Inscripcion en registros
  - Catalogo de simplificacion documental disponible
  - Procedimientos clave: SACYL (sanidad), educacion, servicios sociales, empleo ECYL

---

### 8. Castilla-La Mancha

- **Sede Electronica:** https://www.jccm.es/
- **Buscador de tramites:** https://www.jccm.es/tramites/buscador
- **Tramites:** https://www.jccm.es/tramites
- **Tu Carpeta:** https://www.jccm.es/index.php/tu-carpeta
- **Formato:** HTML, PDF
- **Deteccion de cambios:** Manual
- **Idiomas:** ES
- **Notas:**
  - Registro electronico: https://www.jccm.es/servicios/registro-electronico
  - Catalogo publicado y actualizado con todos los procedimientos de la JCCM
  - Procedimientos clave: SESCAM (sanidad), educacion, vivienda, empleo SEPECAM

---

### 9. Galicia

- **Sede Electronica:** https://sede.xunta.gal/es/portada
- **Guia de procedementos e servizos:** https://sede.xunta.gal/guia-de-procedementos-e-servizos
- **Catalogo de sistemas dixitais:** https://www.xunta.gal/es/catalogo-sistemas-dixitais
- **Formato:** HTML (fichas con filtros por tipo de usuario), PDF (formularios genericos)
- **Deteccion de cambios:** Sitemap probable; la sede fue renovada recientemente con mejor buscador y sugerencias automaticas
- **Idiomas:** GL (gallego, principal), ES
- **Notas:**
  - Filtros por tipo de usuario: ciudadanos, empresas/profesionales, entidades locales, asociaciones/ONG
  - Modelos de formularios genericos: https://sede.xunta.gal/es/tramites-e-servizos/modelos-xenericos
  - Sistema Chave365 para identificacion digital
  - Procedimientos clave: SERGAS (sanidad), educacion, vivienda, empleo

---

### 10. Region de Murcia

- **Sede Electronica:** https://sede.carm.es/
- **Guia de servicios:** https://www.carm.es/guiadeservicios
- **Realizar un tramite:** https://sede.carm.es/web/pagina?IDCONTENIDO=40288&IDTIPO=100&RASTRO=c$m
- **Registro y guia de procedimientos (buscador avanzado):** https://agenciatributaria.carm.es/web/guest/guiaprocedimiento
- **Formato:** HTML (fichas con formularios electronicos), PDF
- **Deteccion de cambios:** Manual; sede operativa 24/7
- **Idiomas:** ES
- **Notas:**
  - Identificacion via certificados digitales/DNIe y progresivamente Cl@ve
  - Procedimientos clave: SMS (sanidad), educacion, vivienda, empleo SEF

---

### 11. Aragon

- **Sede Electronica:** https://www.aragon.es/tramites/servicios-de-la-sede-electronica
- **Catalogo de tramites:** https://www.aragon.es/tramites
- **Herramientas digitales — catalogo:** https://www.aragon.es/es/w/herramientas-digitales-catalogo-de-servicios-y-procedimientos
- **Guia rapida de ayuda:** https://www.aragon.es/tramites/guia-rapida-de-ayuda-al-ciudadano
- **Formato:** HTML (fichas), PDF
- **Deteccion de cambios:** Manual; el catalogo alimenta directamente la sede electronica
- **Idiomas:** ES
- **Notas:**
  - Aproximadamente 1.300 servicios activos catalogados
  - Registro Electronico General de Aragon disponible
  - Procedimientos clave: Salud Aragon, educacion, vivienda, INAEM (empleo)

---

### 12. Illes Balears

- **Sede Electronica (Seu Electronica):** https://www.caib.es/seucaib/es/ (ES) / https://seuelectronica.caib.es/ (CA)
- **Catalogo de tramites:** Integrado en la sede electronica, con filtros por unidad administrativa
- **Portal general:** https://caib.es/webgoib/es/quieres-hacer-tus-tramites-de-forma-telematica
- **Formato:** HTML, PDF
- **Deteccion de cambios:** Manual
- **Idiomas:** CA (catalan/balear), ES
- **Notas:**
  - Soporte tecnico para tramitacion: https://www.illesbalears.cat/sites/suporttecnic/es/introduccio-17235/
  - Carpeta Ciudadana disponible
  - Procedimientos clave: IB-Salut (sanidad), educacion, vivienda, empleo SOIB

---

### 13. Extremadura

- **Sede Electronica:** https://tramites.juntaex.es/
- **Catalogo de tramites:** https://tramites.juntaex.es/sta/CarpetaPublic/doEvent?APP_CODE=STA&PAGE_CODE=CATALOGO
- **Portal de tramites:** https://www.juntaex.es/tramites
- **Ayuda:** https://www.juntaex.es/tramites/ayuda
- **Formato:** HTML, PDF
- **Deteccion de cambios:** Manual
- **Idiomas:** ES
- **Notas:**
  - Sistema STA (Servicios Telematicos Avanzados) para gestion de tramites
  - Soporte: soporte.sede@juntaex.es / Tel. 924336975
  - Organizacion por temas y subtemas con buscador
  - Procedimientos clave: SES (sanidad), educacion, vivienda, empleo SEXPE

---

### P2 — Lower Priority

---

### 14. Asturias (Principado de)

- **Sede Electronica:** https://sede.asturias.es/
- **miPrincipado (sede principal):** https://miprincipado.asturias.es/
- **Todos los servicios y tramites:** https://sede.asturias.es/todos-los-servicios-y-tramites
- **Consultar mis tramites:** https://miprincipado.asturias.es/consultar-tramites
- **Formato:** HTML, PDF
- **Deteccion de cambios:** Manual
- **Idiomas:** ES
- **Notas:**
  - Doble portal: sede.asturias.es y miprincipado.asturias.es
  - Solicitud generica disponible para tramites sin procedimiento especifico
  - Procedimientos clave: SESPA (sanidad), educacion, vivienda, empleo

---

### 15. Navarra (Comunidad Foral de)

- **Sede Electronica / Tramites:** https://www.navarra.es/es/tramites
- **Buscador de tramites:** https://www.navarra.es/es/tramites/buscador
- **Registro General Electronico:** https://www.navarra.es/es/tramites/on/-/line/registro-general-electronico
- **Formato:** HTML (fichas), PDF
- **Deteccion de cambios:** Manual
- **Idiomas:** ES, EU (euskera, en zona vascofona)
- **Notas:**
  - Categorias: autorizaciones/licencias, ayudas/subvenciones, certificados/registros, empleo publico, impuestos/pagos, inscripcion a cursos, prestaciones/servicios
  - Hacienda Foral de Navarra con sistema tributario propio
  - Procedimientos clave: Osasunbidea/SNS-O (sanidad), educacion, vivienda, empleo SNE

---

### 16. Cantabria

- **Sede Electronica:** https://sede.cantabria.es/sede/
- **Catalogo de tramites:** https://sede.cantabria.es/sede/catalogo-de-tramites
- **Portal general:** https://www.cantabria.es/sede-electronica
- **Formato:** HTML, PDF
- **Deteccion de cambios:** Manual
- **Idiomas:** ES
- **Notas:**
  - 1.253 procedimientos catalogados
  - Identificacion via Cl@ve, certificados electronicos y DNIe
  - Tablon electronico de anuncios: https://sede.cantabria.es/sede/tablon-electronico-de-anuncios
  - Procedimientos clave: SCS (sanidad), educacion, vivienda, empleo EMCAN

---

### 17. La Rioja

- **Sede Electronica:** https://web.larioja.org/sede-electronica
- **Oficina Electronica (tramites):** https://web.larioja.org/oficina-electronica/
- **Tramites:** https://web.larioja.org/oficinaelectronica
- **Formato:** HTML, PDF
- **Deteccion de cambios:** Manual; pagina de "ultimos dias" para tramites con plazo proximo — https://web.larioja.org/oficina-electronica/ultimos-dias
- **Idiomas:** ES
- **Notas:**
  - Instancia general electronica disponible
  - Pagina de "ultimos dias" util para detectar tramites con plazos proximos a vencer
  - Procedimientos clave: SERIS (sanidad), educacion, vivienda, empleo

---

### 18. Ceuta (Ciudad Autonoma)

- **Sede Electronica:** https://sede.ceuta.es/
- **Catalogo de procedimientos:** Integrado en la sede (seccion Tramites, busqueda por tema)
- **Portal general:** https://www.ceuta.es/
- **Formato:** HTML (fichas de procedimiento), PDF (formularios)
- **Deteccion de cambios:** Manual
- **Idiomas:** ES
- **Notas:**
  - 494 procedimientos catalogados, de los cuales 479 pueden iniciarse online
  - Verificacion de documentos electronicos disponible
  - Certificados online para descarga/impresion
  - Ciudad con alta densidad de inmigracion — tramites de extranjeria son criticos
  - Procedimientos clave: sanidad (INGESA), educacion, empadronamiento, extranjeria

---

### 19. Melilla (Ciudad Autonoma)

- **Sede Electronica:** https://sede.melilla.es/
- **Catalogo de procedimientos:** https://sede.melilla.es/sta/CarpetaPublic/doEvent?APP_CODE=STA&PAGE_CODE=CATALOGO
- **Tramites destacados:** https://sede.melilla.es/sta/CarpetaPublic/doEvent?APP_CODE=STA&PAGE_CODE=PTS2_TRAMDESTACADOS
- **Carpeta Ciudadana:** https://sede.melilla.es/sta/CarpetaPublic/doEvent?APP_CODE=STA&PAGE_CODE=PTS2_MICARPETACIUDADANA
- **Formato:** HTML, PDF
- **Deteccion de cambios:** Manual
- **Idiomas:** ES
- **Notas:**
  - Sistema STA similar al de Extremadura
  - Tramites tributarios con seccion separada
  - Ciudad con alta densidad de inmigracion — tramites de extranjeria son criticos
  - Procedimientos clave: sanidad (INGESA), educacion, empadronamiento, extranjeria

---

## Detection Methods Summary

| Metodo | CCAA que lo soportan | Notas |
|--------|----------------------|-------|
| API / Open Data | Catalunya (Socrata API en datos.gob.es) | Mejor opcion para deteccion automatizada |
| Sitemap XML | Madrid, Andalucia, Galicia (probable), Castilla y Leon (probable) | Requiere polling periodico y diff |
| Feed de novedades | Comunitat Valenciana (pagina novedades ultimos 10 dias), La Rioja (ultimos dias) | Scraping de pagina de novedades |
| Dataset datos.gob.es | Catalunya, Pais Vasco (tablon de anuncios) | Acceso via API CKAN de datos.gob.es |
| Manual / Scraping | Todas (fallback) | Requiere scraping periodico del catalogo |

---

## Key Gaps Identified

1. **APIs publicas de catalogo:** Solo Catalunya ofrece un dataset estructurado de tramites via API. El resto requiere scraping.
2. **RSS feeds:** Ninguna CCAA ofrece RSS dedicado para nuevos tramites o cambios en procedimientos.
3. **Formatos estandarizados:** No hay formato comun entre CCAA. Cada una tiene su propia estructura de fichas.
4. **Idiomas:** Las comunidades bilingues (Catalunya, Euskadi, Galicia, Baleares, Valencia, Navarra zona vascofona) requieren procesamiento multilingue.
5. **Ceuta y Melilla:** Especial atencion por alta densidad migratoria pero infraestructura digital mas limitada; sanidad gestionada por INGESA (nivel estatal).

---

## Recommendations for CivicAid Integration

### Phase 1 — Quick wins
- **Catalunya:** Usar API Socrata/datos.gob.es para ingesta automatizada de tramites
- **Madrid, Andalucia:** Scraping de catalogo con deteccion via sitemap
- **Comunitat Valenciana:** Scraping + pagina de novedades como trigger de actualizacion

### Phase 2 — Expansion
- **Pais Vasco, Galicia, Castilla y Leon:** Scraping de sedes electronicas con buen catalogo estructurado
- **Canarias, Murcia, Aragon:** Sedes con catalogos amplios (934, guia de servicios, 1300 servicios)
- **Cantabria:** 1.253 procedimientos catalogados

### Phase 3 — Coverage complete
- **Resto de P1 y P2:** Completar con scraping de las sedes restantes
- **Ceuta y Melilla:** Priorizar tramites de extranjeria por perfil migratorio

### Cross-cutting
- Implementar scraper generico para plataforma STA (usada por Extremadura y Melilla)
- Manejar multilingue para CA, EU, GL en comunidades bilingues
- Usar datos.gob.es como fuente centralizada cuando haya datasets disponibles

---

## Common CCAA-Level Procedures

These are the procedures most relevant to Clara's target users (vulnerable populations, immigrants) that are managed at the CCAA level across all 17+2 territories:

### 1. Tarjeta Sanitaria (Healthcare Card)

| Aspecto | Detalle |
|---------|---------|
| Que es | Documento que acredita el derecho a asistencia sanitaria publica |
| Quien lo gestiona | El servicio de salud de cada CCAA (SERMAS, CatSalut, SAS, etc.) |
| Requisitos comunes | Empadronamiento + alta en Seguridad Social (o documento DASE para irregulares) |
| Variaciones | Cada CCAA tiene su propio nombre y proceso: TSI en Madrid, TIS en Andalucia, CIP en Catalunya, SIP en Valencia |
| Relevancia Clara | ALTA — es el primer tramite que necesita cualquier persona para acceder a sanidad |

### 2. Renta Minima de Insercion (RMI) / Renta de Garantia

| Aspecto | Detalle |
|---------|---------|
| Que es | Prestacion economica para personas en situacion de exclusion social o pobreza extrema |
| Quien lo gestiona | Servicios Sociales de cada CCAA |
| Variaciones | Nombres distintos: RMI (Madrid), Renta Garantizada (Catalunya), RGI (Euskadi), Renta Valenciana de Inclusion, Renta del Pueblo (Andalucia propuesta 2025) |
| Complementariedad | Complementa o se solapa con el IMV estatal (gestionado por INSS) |
| Relevancia Clara | ALTA — prestacion critica para personas sin ingresos |

### 3. Becas y Ayudas Educativas

| Aspecto | Detalle |
|---------|---------|
| Que es | Ayudas para comedor, transporte, material escolar, matricula |
| Quien lo gestiona | Consejeria de Educacion de cada CCAA |
| Variaciones | Convocatorias, plazos y requisitos distintos en cada CCAA |
| Relevancia Clara | MEDIA-ALTA — familias con hijos en edad escolar |

### 4. Prestaciones de Dependencia

| Aspecto | Detalle |
|---------|---------|
| Que es | Valoracion y prestaciones para personas dependientes (Ley 39/2006) |
| Quien lo gestiona | Servicios Sociales de cada CCAA (valoracion, PIA, prestaciones) |
| Variaciones | Tiempos de resolucion y prestaciones complementarias varian mucho entre CCAA |
| Relevancia Clara | MEDIA — personas mayores o con discapacidad |

### 5. Vivienda Social y Ayudas al Alquiler

| Aspecto | Detalle |
|---------|---------|
| Que es | Registro de demandantes de vivienda social, ayudas al alquiler, planes de vivienda |
| Quien lo gestiona | Consejeria de Vivienda de cada CCAA |
| Variaciones | Requisitos de ingresos, plazos de convocatoria y cuantias distintas |
| Relevancia Clara | ALTA — el acceso a vivienda es critico para poblaciones vulnerables |

### 6. Empadronamiento (Nivel Municipal pero con Impacto CCAA)

| Aspecto | Detalle |
|---------|---------|
| Que es | Inscripcion en el padron municipal — requisito previo para la mayoria de tramites CCAA |
| Quien lo gestiona | Ayuntamientos (nivel local), pero es prerequisito para tramites CCAA |
| Relevancia Clara | ALTA — sin empadronamiento no se puede acceder a sanidad, educacion ni ayudas |

---

## Shared Infrastructure Patterns Across CCAA

### Plataformas de Sede Electronica

| Patron | CCAA que lo usan | Notas |
|--------|-----------------|-------|
| Plataforma STA (Servicios Telematicos Avanzados) | Extremadura, Melilla | URLs con patron APP_CODE=STA — posible scraper reutilizable |
| Carpeta Ciudadana integrada | Madrid, Catalunya, Andalucia, Valencia, Euskadi, Galicia, Canarias, Illes Balears, Asturias, Cantabria, Ceuta, Melilla | Espacio personal del ciudadano para seguimiento de expedientes |
| Registro Electronico General | Todas las CCAA | Requisito legal (Ley 39/2015), todas deben tenerlo |
| Cl@ve como sistema de identificacion | Todas las CCAA (progresivamente) | Ademas de certificado digital y DNIe |

### Sistemas de Identificacion

| Sistema | Disponibilidad |
|---------|---------------|
| Cl@ve (PIN, Permanente, Movil) | Universal — todas las CCAA lo aceptan |
| Certificado digital FNMT | Universal |
| DNIe (DNI electronico) | Universal |
| Izenpe | Pais Vasco (certificado digital propio) |
| Chave365 | Galicia (sistema propio de la Xunta) |
| idCAT | Catalunya (certificado digital propio de la Generalitat) |

### Patrones de URL

| CCAA | Patron de URL de tramites | Ejemplo |
|------|--------------------------|---------|
| Comunitat Valenciana | `gva.es/es/inicio/procedimientos?id_proc=XXXXX` | Predecible, facil de rastrear |
| Catalunya | `tramits.gencat.cat/es/tramits/XXXXX` | Catalogo dedicado |
| Castilla-La Mancha | `jccm.es/tramites/XXXXXXX` | IDs numericos |
| Canarias | `sede.gobiernodecanarias.org/sede/tramites/XXXX` | IDs numericos |
| Resto | Variados, generalmente con parametros en query string | Requiere analisis individual |

### Servicios Sanitarios por CCAA

| CCAA | Servicio de Salud | Tarjeta |
|------|-------------------|---------|
| Andalucia | SAS (Servicio Andaluz de Salud) | TIS |
| Aragon | Salud Aragon | TSI |
| Asturias | SESPA | TSI |
| Illes Balears | IB-Salut | TSI |
| Canarias | SCS (Servicio Canario de Salud) | TSI |
| Cantabria | SCS (Servicio Cantabro de Salud) | TSI |
| Castilla-La Mancha | SESCAM | TSI |
| Castilla y Leon | SACYL | TSI |
| Catalunya | CatSalut (Servei Catala de la Salut) | CIP |
| Comunitat Valenciana | Conselleria de Sanitat | SIP |
| Extremadura | SES (Servicio Extremeno de Salud) | TSI |
| Galicia | SERGAS (Servizo Galego de Saude) | TSI |
| Madrid | SERMAS | TSI |
| Murcia | SMS (Servicio Murciano de Salud) | TSI |
| Navarra | Osasunbidea / SNS-O | TIS |
| Pais Vasco | Osakidetza | TIS |
| La Rioja | SERIS | TSI |
| Ceuta | INGESA (gestion estatal) | TSI |
| Melilla | INGESA (gestion estatal) | TSI |

### Servicios de Empleo por CCAA

| CCAA | Servicio de Empleo |
|------|-------------------|
| Andalucia | SAE (Servicio Andaluz de Empleo) |
| Aragon | INAEM |
| Asturias | SEPEPA |
| Illes Balears | SOIB |
| Canarias | SCE (Servicio Canario de Empleo) |
| Cantabria | EMCAN |
| Castilla-La Mancha | SEPECAM |
| Castilla y Leon | ECYL |
| Catalunya | SOC (Servei d'Ocupacio de Catalunya) |
| Comunitat Valenciana | LABORA |
| Extremadura | SEXPE |
| Galicia | Emprego Xunta |
| Madrid | Comunidad de Madrid - Empleo |
| Murcia | SEF |
| Navarra | SNE (Servicio Navarro de Empleo) |
| Pais Vasco | Lanbide |
| La Rioja | Empleo La Rioja |
| Ceuta | SEPE (gestion estatal directa) |
| Melilla | SEPE (gestion estatal directa) |

---

## Language Considerations for the RAG System

### Co-official Languages by CCAA

| CCAA | Lengua co-oficial | Codigo ISO | Impacto en RAG |
|------|-------------------|------------|----------------|
| Catalunya | Catalan (Catala) | ca | Portal principal en catalan; version castellana disponible pero contenido puede diferir |
| Catalunya (Val d'Aran) | Aranes (Occitan) | oc | Muy minoritario; solo relevante para Val d'Aran |
| Illes Balears | Catalan (variante balear) | ca | Portal bilingue; sede en catalan por defecto |
| Comunitat Valenciana | Valenciano (Catalan) | ca | Portal bilingue; muchos tramites solo en castellano |
| Galicia | Gallego (Galego) | gl | Sede principal en gallego; version castellana completa |
| Pais Vasco | Euskera (Vasco) | eu | Portal bilingue completo |
| Navarra | Euskera (zona vascofona) | eu | Solo en municipios de la zona vascofona; la mayoria del portal es solo en castellano |

### Estrategia de Idioma para Clara

1. **Ingesta:** Ingestar siempre la version en castellano (ES) cuando exista, ya que Clara responde en espanol y frances. Para CCAA bilingues, priorizar URLs con `/es/` o parametro `langId=es_ES`.
2. **Fallback a co-oficial:** Si un tramite solo existe en lengua co-oficial (raro pero posible en Catalunya o Galicia), ingestar igualmente y usar el LLM para traducir al responder.
3. **Deteccion de idioma en URLs:**
   - Catalunya: `/ca/` (catalan) vs `/es/` (castellano)
   - Galicia: sin prefijo (gallego por defecto) vs `/es/` (castellano)
   - Euskadi: `/eu/` (euskera) vs `/es/` (castellano)
   - Valencia: sin distincion clara en URL; parametro `langId`
   - Baleares: `/ca/` vs `/es/`
4. **Nombres de tramites:** Almacenar tanto el nombre en castellano como en lengua co-oficial para mejorar la busqueda. Ejemplo: "Tarjeta Sanitaria" / "Targeta Sanitaria" (CA) / "Txartel Sanitarioa" (EU).

---

## Priority Ranking — Population and Immigrant Density

### Tier P0 — Critical Priority (5 CCAA)

Criterio: >15% poblacion extranjera O >100,000 saldo migratorio exterior en 2024

| # | CCAA | Poblacion total | % Extranjeros | Saldo migratorio 2024 | Justificacion |
|---|------|----------------|---------------|----------------------|---------------|
| 1 | Comunidad de Madrid | ~7,000,000 | 16.7% | 113,964 | Capital, mayor concentracion de servicios, 2o saldo migratorio |
| 2 | Catalunya | ~8,000,000 | 18.7% | 129,030 | Mayor saldo migratorio de Espana, infraestructura digital avanzada |
| 3 | Andalucia | ~8,600,000 | ~11% | ~60,000 | CCAA mas poblada, alto volumen absoluto de extranjeros |
| 4 | Comunitat Valenciana | ~5,200,000 | 19.3% | 104,776 | 3er saldo migratorio, alto % extranjeros |
| 5 | Canarias | ~2,300,000 | ~16% | ~30,000 | Alta proporcion turistica y migratoria, isla con problematica especifica |

### Tier P1 — Medium Priority (8 CCAA)

Criterio: poblacion significativa O % extranjeros relevante O importancia estrategica

| # | CCAA | Poblacion total | % Extranjeros | Justificacion |
|---|------|----------------|---------------|---------------|
| 6 | Pais Vasco | ~2,200,000 | ~10% | Economia fuerte, sistema propio (concierto economico), creciente inmigracion |
| 7 | Castilla y Leon | ~2,400,000 | ~8% | Gran extension territorial, poblacion rural dispersa |
| 8 | Castilla-La Mancha | ~2,100,000 | ~12% | % extranjeros significativo en zonas agricolas |
| 9 | Galicia | ~2,700,000 | ~6% | Poblacion significativa, idioma co-oficial |
| 10 | Region de Murcia | ~1,500,000 | ~17% | Alto % de extranjeros (sector agricola) |
| 11 | Aragon | ~1,350,000 | ~14% | % extranjeros elevado |
| 12 | Illes Balears | ~1,200,000 | ~22% | Mayor % de poblacion nacida en extranjero (27.65%) |
| 13 | Extremadura | ~1,060,000 | ~5% | Baja inmigracion pero poblacion vulnerable significativa |

### Tier P2 — Lower Priority (6 CCAA + ciudades)

Criterio: menor poblacion O menor % de inmigracion O cobertura por fuentes AGE

| # | CCAA | Poblacion total | % Extranjeros | Justificacion |
|---|------|----------------|---------------|---------------|
| 14 | Asturias | ~1,010,000 | ~7% | Poblacion menor, envejecida |
| 15 | Navarra | ~670,000 | ~13% | Pequena pero con % extranjeros notable |
| 16 | Cantabria | ~585,000 | ~8% | Poblacion pequena |
| 17 | La Rioja | ~320,000 | ~16% | Muy pequena pero alto % extranjeros |
| 18 | Ceuta | ~84,000 | Especial | Ciudad fronteriza con Marruecos — alta densidad migratoria, sanidad gestionada por INGESA |
| 19 | Melilla | ~87,000 | Especial | Ciudad fronteriza con Marruecos — alta densidad migratoria, sanidad gestionada por INGESA |

> **Nota sobre Ceuta y Melilla:** Aunque estan en Tier P2 por poblacion, su relevancia para Clara es desproporcionadamente alta por la concentracion de poblacion migrante y la complejidad de sus tramites de extranjeria. Considerar elevar a P1 para tramites especificos de frontera.

### Resumen de Prioridades por Numero de Procedimientos

| CCAA | Procedimientos catalogados (aprox.) | Tier |
|------|-------------------------------------|------|
| Aragon | ~1,300 | P1 |
| Cantabria | ~1,253 | P2 |
| Catalunya | ~1,400+ | P0 |
| Canarias | ~934 | P0 |
| Ceuta | ~494 | P2 |
| Resto | No publicado / variable | — |

---

## Data Sources and References

- INE — Estadistica Continua de Poblacion, enero 2025: https://www.ine.es/dyngs/Prensa/ECP4T24.htm
- INE — Estadistica de Migraciones y Cambios de Residencia, 2024: https://www.ine.es/dyngs/Prensa/EMCR2024.htm
- datos.gob.es — Catalogo de procedimientos por CCAA: https://datos.gob.es/
- Sedes electronicas de cada CCAA (URLs verificadas febrero 2026)

---

*Documento generado para el proyecto Clara (CivicAid Voice) — Fase 3, Q1 Sources*
*Ultima actualizacion: 2026-02-18*
