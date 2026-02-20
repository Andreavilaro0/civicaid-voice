# AGE Source Registry — Administracion General del Estado

> Research date: 2026-02-18
> Purpose: Document top 20+ official Spanish central government sources for CivicAid RAG system

---

## Summary Table

| # | Source | URL | Type | Priority | Coverage | Access |
|---|--------|-----|------|----------|----------|--------|
| 1 | SIA (Sistema de Informacion Administrativa) | https://administracion.gob.es/pag_Home/espanaAdmon/SIA.html | catalog | P0 | Master catalog of all public procedures | Crawl / structured HTML |
| 2 | PAG (Punto de Acceso General) | https://administracion.gob.es/ | portal | P0 | Citizen-facing portal, all procedures by topic | Crawl + sitemap |
| 3 | Carpeta Ciudadana | https://carpetaciudadana.gob.es/ | portal | P1 | Personal citizen folder (docs, appointments, notifications) | Auth-only (Clave) |
| 4 | Clave | https://clave.gob.es/ | identity | P1 | Digital identity system (PIN, permanente, certificado) | Info pages crawl |
| 5 | Sede Electronica del PAG | https://sede.administracion.gob.es/ | portal | P0 | Main government e-office, electronic registry | Crawl |
| 6 | BOE — Diario Oficial | https://www.boe.es/ | gazette | P0 | Official state gazette, all legislation | REST API + RSS |
| 7 | BOE — Legislacion Consolidada | https://www.boe.es/buscar/legislacion.php | search | P0 | Consolidated legislation search | REST API |
| 8 | BOE — Sumarios Diarios | https://www.boe.es/diario_boe/ | feed | P1 | Daily summaries of published acts | REST API + RSS |
| 9 | SEPE | https://sede.sepe.gob.es/ | sede electronica | P0 | Unemployment, job search, training | Crawl |
| 10 | Seguridad Social (TGSS/INSS) | https://sede.seg-social.gob.es/ | sede electronica | P0 | Pensions, SS numbers, benefits, IMV | Crawl |
| 11 | AEAT (Agencia Tributaria) | https://sede.agenciatributaria.gob.es/ | sede electronica | P0 | Taxes, fiscal procedures, certificates | Crawl + WSDL/SOAP |
| 12 | DGT | https://sede.dgt.gob.es/ | sede electronica | P1 | Driving licenses, vehicles, fines | Crawl |
| 13 | Extranjeria (Policia Nacional) | https://sede.policia.gob.es/portalCiudadano/_es/tramites_extranjeria.php | sede electronica | P0 | NIE, TIE, residency, work permits | Crawl |
| 14 | MUFACE | https://sede.muface.gob.es/ | sede electronica | P2 | Civil servant healthcare mutual | Crawl |
| 15 | IMSERSO | https://sede.imserso.gob.es/ | sede electronica | P1 | Elderly services, disability, dependency | Crawl |
| 16 | MIVAU (Min. Vivienda) | https://www.mivau.gob.es/ | portal + sede | P1 | Housing aid, bono alquiler joven, urban agenda | Crawl |
| 17 | Ministerio de Justicia | https://sede.mjusticia.gob.es/ | sede electronica | P1 | Criminal records, nationality, legal aid, civil registry | Crawl |
| 18 | INE | https://www.ine.es/ | API | P2 | National statistics, reference data | JSON API |
| 19 | Min. Inclusion — IMV | https://www.inclusion.gob.es/web/imv | portal | P0 | Ingreso Minimo Vital (minimum income) | Crawl |
| 20 | Catastro | https://www.sedecatastro.gob.es/ | sede electronica + API | P2 | Property registry, cadastral data | REST API + WMS/WFS |
| 21 | Portal de la Transparencia | https://transparencia.gob.es/ | portal | P2 | Public info access, institutional transparency | Crawl |
| 22 | Oficina de Asilo y Refugio | https://proteccion-asilo.interior.gob.es/ | portal | P1 | Asylum, international protection procedures | Crawl |
| 23 | Registro Civil | https://sede.mjusticia.gob.es/tramites | sede electronica | P1 | Birth, marriage, death certificates | Crawl (under MJusticia) |
| 24 | datos.gob.es | https://datos.gob.es/ | catalog | P1 | National open data catalog (CKAN-based) | CKAN API |
| 25 | Import@ss | https://portal.seg-social.gob.es/wps/portal/importass/importass/inicio | portal + app | P1 | TGSS digital portal: vida laboral, SS number, benefits | Auth-only |

---

## Detailed Source Profiles

### 1. SIA (Sistema de Informacion Administrativa)

- **URL:** https://administracion.gob.es/pag_Home/espanaAdmon/SIA.html
- **Technical URL:** https://administracionelectronica.gob.es/ctt/sia
- **Type:** Catalog / database
- **Priority:** P0 (essential)
- **Coverage:** Master catalog of ALL administrative procedures and services across the AGE and participating public administrations. Mandated by Article 21.4 of Law 39/2015.
- **Update frequency:** Continuously maintained by each ministry/organism; updated as procedures change.
- **Access method:** No public REST API discovered. Data is surfaced through the PAG portal (administracion.gob.es). Structured HTML crawl of procedure listings. Internal access via RED SARA network.
- **Notes:**
  - SIA is the authoritative source of truth for procedure metadata.
  - It feeds the PAG portal, so crawling PAG effectively captures SIA data.
  - Each procedure has a SIA code (useful for deduplication).
  - Regulated by Article 9 of the National Interoperability Framework.

### 2. PAG (Punto de Acceso General — administracion.gob.es)

- **URL:** https://administracion.gob.es/
- **Type:** Portal
- **Priority:** P0 (essential)
- **Coverage:** Single point of access for ALL public administrations (State, Regional, Local, EU). Procedures organized by topic. Links to all ministerial sedes electronicas. Includes procedure descriptions, requirements, deadlines, forms.
- **Update frequency:** Continuously updated as procedures change across agencies.
- **Access method:** Crawl with sitemap discovery. Try: `https://administracion.gob.es/sitemap.xml`. Structured HTML with consistent layout for procedure pages. Thematic navigation at `/pag_Home/Tramites.html`.
- **Notes:**
  - Managed by the General Directorate of Public Governance (Min. Transformacion Digital y Funcion Publica).
  - Includes a search engine for procedures.
  - Citizen-facing language (usually plain Spanish).
  - Has multilingual support (Catalan, Basque, Galician, Valencian, Spanish Sign Language).
  - Telephone channel: 060.

### 3. Carpeta Ciudadana (Mi Carpeta)

- **URL:** https://carpetaciudadana.gob.es/
- **More info:** https://masinformacioncarpeta.carpetaciudadana.gob.es/
- **Type:** Portal (authenticated)
- **Priority:** P1 (important)
- **Coverage:** Personal citizen folder aggregating: personal documents (DNI, passport, driving license expiry alerts), open administrative files, notifications, appointments, social benefits status, employment data, clinical history references.
- **Update frequency:** Real-time (pulls from multiple backend systems).
- **Access method:** Requires Clave authentication. NOT crawlable for content. Crawl the informational/help pages only for RAG (what it is, how to use it, what documents are available).
- **Notes:**
  - Mobile app available (iOS + Android).
  - Useful for RAG to explain WHAT citizens can find there, not to extract personal data.
  - Part of Espana Digital 2026 initiative.

### 4. Clave (Sistema de Identificacion Digital)

- **URL:** https://clave.gob.es/
- **Type:** Identity system (informational)
- **Priority:** P1 (important)
- **Coverage:** All information about digital identity methods: Clave PIN (one-time), Clave Permanente, electronic certificate (DNIe), and how to register.
- **Update frequency:** Infrequent (stable informational content).
- **Access method:** Crawl informational pages. Key sections: `/clave-pin`, `/clave-permanente`, `/registro`.
- **Notes:**
  - Nearly every sede electronica requires Clave. Understanding Clave is essential for guiding vulnerable users.
  - Registration requires in-person visit OR video call.
  - Clave PIN expires in 10 minutes.
  - Common pain point for vulnerable populations.

### 5. Sede Electronica del Punto de Acceso General

- **URL:** https://sede.administracion.gob.es/
- **Type:** Sede electronica (e-office)
- **Priority:** P0 (essential)
- **Coverage:** The main government e-office. Hosts the Registro Electronico General (REG-AGE) for submitting documents to any AGE body. Links to all ministerial electronic offices. Electronic notifications service.
- **Update frequency:** Continuously updated.
- **Access method:** Crawl. Key sections: `/PAG_Sede/ServiciosElectronicos/RegistroElectronicoGeneral.html`.
- **Notes:**
  - The REG-AGE is crucial: citizens can submit documents to ANY administration body through a single registry.
  - Requires electronic identification for transactions.

### 6. BOE — Diario Oficial (Boletin Oficial del Estado)

- **URL:** https://www.boe.es/
- **API docs:** https://www.boe.es/datosabiertos/api/api.php
- **Type:** Official gazette + API
- **Priority:** P0 (essential)
- **Coverage:** ALL official state publications: laws, royal decrees, ministerial orders, resolutions, aid announcements, public employment offers, scholarships.
- **Update frequency:** Daily (published every day except Sundays).
- **Access method:**
  - **REST API** (preferred): `https://boe.es/datosabiertos/api/boe/sumario/[YYYYMMDD]` — returns XML with all provisions for a given date.
  - **RSS feeds:** https://www.boe.es/rss/ — multiple channels by section (Section I laws, Section III aid/scholarships, etc.).
  - **Consolidated legislation API:** `https://www.boe.es/datosabiertos/api/legislacion-consolidada` — search consolidated laws.
  - **PDF documentation:** https://www.boe.es/datosabiertos/documentos/APIsumarioBOE.pdf
  - Documents available in PDF, XML, and HTML formats.
- **Notes:**
  - The BOE API is the best-documented government API in Spain. Free, no auth required.
  - Rate limits: not explicitly documented but be respectful (< 1 req/sec recommended).
  - XML responses include metadata: publication date, section, department, title, PDF/XML/HTML URLs.
  - Essential for tracking new aid programs, regulatory changes affecting vulnerable populations.
  - Also includes BORME (commercial registry gazette) via separate API endpoint.

### 7. BOE — Legislacion Consolidada

- **URL:** https://www.boe.es/buscar/legislacion.php
- **API endpoint:** `https://www.boe.es/datosabiertos/api/legislacion-consolidada`
- **Type:** Search / API
- **Priority:** P0 (essential)
- **Coverage:** All consolidated (up-to-date) Spanish legislation. Includes the full text of laws with all amendments applied.
- **Update frequency:** Updated as amendments are published.
- **Access method:** REST API. PDF doc: https://www.boe.es/datosabiertos/documentos/APIconsolidada.pdf. Supports search by date range, department, topic.
- **Notes:**
  - Critical for RAG: always cite consolidated (current) version of laws, not original publication.
  - API FAQ: https://www.boe.es/datosabiertos/faq/consolidada.php
  - Returns XML with article-level granularity.

### 8. BOE — Sumarios Diarios (Daily Summaries)

- **URL:** https://www.boe.es/diario_boe/
- **RSS:** https://www.boe.es/rss/
- **Type:** Feed / API
- **Priority:** P1 (important)
- **Coverage:** Daily digest of everything published in the BOE, organized by section.
- **Update frequency:** Daily.
- **Access method:** RSS feeds (multiple channels by section). REST API for summaries by date. Useful for monitoring new aid programs, scholarship calls, regulatory changes.
- **Notes:**
  - Section III (Other provisions) is where most aid/scholarship announcements appear.
  - Section II.B contains public employment offers.
  - Ideal for a monitoring/alerting pipeline.

### 9. SEPE (Servicio Publico de Empleo Estatal)

- **URL (sede):** https://sede.sepe.gob.es/
- **URL (portal):** https://www.sepe.es/
- **Type:** Sede electronica
- **Priority:** P0 (essential)
- **Coverage:** Unemployment benefits (contributiva, asistencial, RAI, SED), job search services, training for employment, pre-solicitud online, appointment scheduling.
- **Update frequency:** Regularly updated; benefit amounts change annually.
- **Access method:** Crawl. Key procedure pages at `/portalSede/procedimientos-y-servicios/personas/proteccion-por-desempleo`. No public API found.
- **Notes:**
  - Extremely high-impact for vulnerable populations.
  - Pre-solicitud system allows starting benefit claims online.
  - Content structured by audience: personas (individuals) and empresas (companies).
  - Requires Clave or electronic certificate for transactional services.
  - Informational pages (what benefits exist, requirements, amounts) are publicly accessible and ideal for RAG.

### 10. Seguridad Social (TGSS / INSS)

- **URL (sede):** https://sede.seg-social.gob.es/
- **URL (portal):** https://www.seg-social.es/
- **URL (Import@ss):** https://portal.seg-social.gob.es/wps/portal/importass/importass/inicio
- **URL (prestaciones):** https://prestaciones.seg-social.es/
- **Type:** Sede electronica + portal
- **Priority:** P0 (essential)
- **Coverage:** Social Security numbers, vida laboral (work history), pensions (contributivas, no contributivas), maternity/paternity benefits, temporary disability, IMV processing, dependency benefits.
- **Update frequency:** Continuously. Pension amounts updated annually (revalorizacion).
- **Access method:** Crawl informational pages. Transactional pages require auth. Import@ss portal requires SMS or Clave authentication.
- **Notes:**
  - Two main bodies: INSS (benefits/pensions management) and TGSS (contributions/economic management).
  - Import@ss app (launched Sept 2024) is the modern digital portal, 1M+ installs.
  - Import@ss allows access WITHOUT digital certificate (via SMS verification).
  - Non-contributory pensions (PNC) are critical for vulnerable populations.
  - Phone: 901 16 65 65.

### 11. AEAT (Agencia Tributaria)

- **URL (sede):** https://sede.agenciatributaria.gob.es/
- **URL (portal):** https://www.agenciatributaria.es/
- **Type:** Sede electronica + SOAP/REST APIs
- **Priority:** P0 (essential)
- **Coverage:** All tax procedures: income tax (IRPF), VAT (IVA), tax certificates, fiscal residency, Renta campaign, tax debts, payment plans.
- **Update frequency:** Continuously; major updates during Renta campaign (April-June).
- **Access method:** Crawl informational pages. AEAT has extensive WSDL/SOAP web services (SII - Suministro Inmediato de Informacion) primarily for businesses. REST API services available since April 2024. Technical docs at sede.agenciatributaria.gob.es. Requires digital certificate for most web services.
- **Notes:**
  - WSDL documentation: https://sede.agenciatributaria.gob.es/Sede/iva/suministro-inmediato-informacion/informacion-tecnica/wsdl-servicios-web.html
  - Mutual TLS required for API access.
  - For RAG: focus on informational content about tax obligations, deadlines, deductions for vulnerable groups.
  - Renta Web (income tax filing tool) is heavily used; guiding users through it is high value.
  - Phone: 901 33 55 33.

### 12. DGT (Direccion General de Trafico)

- **URL (sede):** https://sede.dgt.gob.es/
- **URL (portal):** https://www.dgt.es/
- **Type:** Sede electronica
- **Priority:** P1 (important)
- **Coverage:** Driving licenses (obtaining, renewing, points), vehicle registration, transfers, fines payment, ITV (vehicle inspection) info, international driving permits.
- **Update frequency:** Stable procedural content; fine/fee amounts updated periodically.
- **Access method:** Crawl. Key sections: `/es/vehiculos/`, `/es/conductores/`, `/es/otros-tramites/`. Procedure list at `/es/`.
- **Notes:**
  - Access via Clave, digital certificate, or SMS verification.
  - Useful for immigrants needing to exchange foreign driving licenses.
  - DEV (Direccion Electronica Vial) is the electronic address for traffic notifications.

### 13. Extranjeria (Policia Nacional Sede Electronica)

- **URL:** https://sede.policia.gob.es/portalCiudadano/_es/tramites_extranjeria.php
- **URL (appointments):** https://icp.administracionelectronica.gob.es/icpplus/index.html
- **URL (MISM portal):** https://expinterweb.inclusion.gob.es/
- **URL (Asilo):** https://proteccion-asilo.interior.gob.es/
- **Type:** Sede electronica
- **Priority:** P0 (essential)
- **Coverage:** ALL immigration procedures: NIE assignment, TIE (residence card), initial and renewal residence permits, work permits, family reunification, EU family residence cards, long-term residence.
- **Update frequency:** Procedure requirements change with regulatory updates.
- **Access method:** Crawl. Procedure pages are well-structured at Policia Nacional sede. Appointment system (ICP Plus) is separate. Status consultation available at sede.policia.gob.es.
- **Notes:**
  - CRITICAL for vulnerable populations (immigrants, asylum seekers).
  - Appointment system (cita previa extranjeria) is notoriously difficult — slots fill instantly.
  - Status tracking: enter NIE + application date + birth year.
  - Content split between Policia Nacional (card issuance) and Min. Inclusion (authorization).
  - Delegaciones de Gobierno handle extranjeria at provincial level.

### 14. MUFACE (Mutualidad General de Funcionarios Civiles del Estado)

- **URL (sede):** https://sede.muface.gob.es/
- **URL (alt sede):** https://muface.sede.gob.es/
- **URL (portal):** https://muface.es/
- **Type:** Sede electronica
- **Priority:** P2 (nice-to-have)
- **Coverage:** Civil servant healthcare: medical provider selection, reimbursements, prescriptions, dental coverage, temporary disability for civil servants.
- **Update frequency:** Periodic; provider lists updated annually during "cambio de entidad" period.
- **Access method:** Crawl informational pages. Procedures list at https://muface.sede.gob.es/procedimientos. Transactional pages require Clave/cert.
- **Notes:**
  - Relevant only for civil servants and their families.
  - Lower priority for vulnerable populations unless they are dependents of civil servants.
  - Available 24/7/365.

### 15. IMSERSO (Instituto de Mayores y Servicios Sociales)

- **URL (sede):** https://sede.imserso.gob.es/
- **URL (portal):** https://imserso.es/
- **Type:** Sede electronica
- **Priority:** P1 (important)
- **Coverage:** Elderly services, disability recognition (grado de discapacidad), dependency assessment, non-contributory pensions (PNC), social and economic benefits for disabled persons (PSPD), travel programs for elderly, thermal tourism.
- **Update frequency:** Programs updated annually; PNC amounts revalorized yearly.
- **Access method:** Crawl. Key sections: `/procedimientos-servicios/dependencia-discapacidad`, `/procedimientos-servicios/prestaciones`. Requires Clave for transactional services.
- **Notes:**
  - IMSERSO manages Ceuta and Melilla directly; in rest of Spain, CCAA manage dependency/disability.
  - Annual income certificates for PNC and PSPD downloadable from sede.
  - Disability recognition (>= 33%) unlocks many benefits across administrations.
  - Very relevant for elderly and disabled vulnerable populations.

### 16. MIVAU (Ministerio de Vivienda y Agenda Urbana)

- **URL (sede):** https://mivau.sede.gob.es/
- **URL (portal):** https://www.mivau.gob.es/
- **URL (bono alquiler):** https://www.mivau.gob.es/vivienda/bono-alquiler-joven
- **Type:** Portal + sede electronica
- **Priority:** P1 (important)
- **Coverage:** Housing policy, Bono Alquiler Joven (250 EUR/month for under-35), Plan Estatal de Vivienda 2022-2025, housing aid programs, urban agenda.
- **Update frequency:** Program-dependent; major updates with new housing plans.
- **Access method:** Crawl. Sede created March 2025 (BOE-A-2025-5411). Previously under Min. Transportes (sede.transportes.gob.es).
- **Notes:**
  - IMPORTANT: Bono Alquiler Joven is managed by CCAA, not directly by MIVAU. MIVAU sets the framework; each autonomous community runs its own application process.
  - Requirements: 18-35 years, income < 3x IPREM, rent <= 600 EUR/month.
  - Ministry restructured: housing separated from transport in 2024-2025.
  - For RAG: document the national framework AND link to CCAA-specific application portals.

### 17. Ministerio de Justicia

- **URL (sede):** https://sede.mjusticia.gob.es/
- **URL (portal):** https://www.mjusticia.gob.es/
- **URL (Carpeta Justicia):** https://www.administraciondejusticia.gob.es/carpeta-justicia
- **Type:** Sede electronica
- **Priority:** P1 (important)
- **Coverage:** Criminal records certificates (antecedentes penales), nationality by residence, civil registry (birth/marriage/death certificates), legal aid (asistencia juridica gratuita), apostille, powers of attorney.
- **Update frequency:** Stable procedural content; nationality processing times vary.
- **Access method:** Crawl. Key procedure pages at `/tramites`. Certificates (antecedentes penales) can be obtained with Clave or certificate. Birth certs from 1996+, marriage certs from 1989+ available online.
- **Notes:**
  - Criminal records certificate is required for many immigration procedures.
  - Nationality by residence: one of the most complex and slow procedures (2+ years).
  - Asistencia juridica gratuita: critical for vulnerable populations — free legal representation if income < threshold.
  - Registro Civil is accessed through this same sede electronica.

### 18. INE (Instituto Nacional de Estadistica)

- **URL:** https://www.ine.es/
- **API docs:** https://www.ine.es/dyngs/DataLab/manual.html?cid=45
- **API endpoint:** https://servicios.ine.es/wstempus/js/ES/
- **Type:** Statistical API
- **Priority:** P2 (nice-to-have)
- **Coverage:** All national statistics: CPI/IPC, population, unemployment rates, IPREM, SMI (minimum wage), poverty thresholds, demographic data.
- **Update frequency:** Varies by indicator (monthly CPI, quarterly GDP, annual census).
- **Access method:** JSON REST API. No auth required. Example: `https://servicios.ine.es/wstempus/js/ES/OPERACIONES_DISPONIBLES` lists all available datasets. URL definition docs: https://www.ine.es/dyngs/DataLab/manual.html?cid=47
- **Notes:**
  - Three data sources: Tempus3 database, PC-Axis files, tpx files.
  - Useful for RAG reference data: IPREM values (used as threshold for many aid programs), SMI, poverty lines.
  - Not directly user-facing for procedures, but essential for contextual data.
  - Free, well-documented, no rate limits documented.

### 19. Ministerio de Inclusion — Ingreso Minimo Vital (IMV)

- **URL (info):** https://www.inclusion.gob.es/web/imv
- **URL (sede solicitud):** https://sede.inclusion.gob.es/w/solicitud-imv
- **URL (simulador):** https://imv.seg-social.es/
- **Type:** Portal + sede electronica
- **Priority:** P0 (essential)
- **Coverage:** Ingreso Minimo Vital — Spain's minimum income guarantee. Application, requirements, amounts, compatible situations, complemento de ayuda a la infancia.
- **Update frequency:** Amounts updated annually. Eligibility rules updated periodically.
- **Access method:** Crawl informational pages. Application via sede.inclusion.gob.es (requires Clave/cert) OR via sede.seg-social.gob.es without certificate (INSS service).
- **Notes:**
  - THE most relevant benefit for vulnerable populations.
  - Can be requested without digital certificate through INSS phone channel or in-person.
  - Managed jointly by Min. Inclusion and Seguridad Social (INSS processes applications).
  - Complemento de Ayuda a la Infancia: additional amount for families with children.
  - Income thresholds vary by family composition.
  - Processing time: several months typically.

### 20. Catastro (Direccion General del Catastro)

- **URL (sede):** https://www.sedecatastro.gob.es/
- **URL (portal):** https://www.catastro.hacienda.gob.es/
- **Type:** Sede electronica + REST API + WMS/WFS
- **Priority:** P2 (nice-to-have)
- **Coverage:** Property registry: cadastral references, property values, building data, mapping, ownership queries.
- **Update frequency:** Continuously updated as property changes are registered.
- **Access method:**
  - **Free web services:** SOAP/XML services documented at https://www.catastro.meh.es/ws/webservices_libres.pdf (v2.6). Includes: query by cadastral reference, query by address, query by coordinates.
  - **INSPIRE services:** WMS/WFS/ATOM for geospatial data.
  - **Bulk download:** Alphanumeric data in CAT format via datos.gob.es.
  - **R package:** CatastRo (https://ropenspain.github.io/CatastRo/).
- **Notes:**
  - Cadastral reference is needed for property-related tax procedures.
  - Non-protected data is freely available. Protected data (ownership) requires auth.
  - Lower priority for vulnerable populations unless dealing with property/housing issues.

### 21. Portal de la Transparencia

- **URL:** https://transparencia.gob.es/
- **Type:** Portal
- **Priority:** P2 (nice-to-have)
- **Coverage:** Government transparency: organizational info, institutional data, right of access to public information (derecho de acceso), budgets, contracts, subsidies granted.
- **Update frequency:** Continuously updated.
- **Access method:** Crawl. Right of access requests require Clave authentication. Informational pages are public. Solicitud at `/derecho-acceso/solicite-informacion-publica`.
- **Notes:**
  - Governed by Ley 19/2013 de Transparencia.
  - Right of access: any person can request public information from AGE.
  - Consejo de Transparencia (independent body) at https://consejodetransparencia.es/.
  - Moderate relevance for RAG; useful for explaining citizens' rights to information.

### 22. Oficina de Asilo y Refugio (OAR)

- **URL (portal):** https://proteccion-asilo.interior.gob.es/
- **URL (MIR sede):** https://sede.mir.gob.es/
- **URL (Interior):** https://www.interior.gob.es/opencms/es/servicios-al-ciudadano/tramites-y-gestiones/oficina-de-asilo-y-refugio/
- **Type:** Portal + sede electronica
- **Priority:** P1 (important)
- **Coverage:** International protection: asylum applications, refugee status, subsidiary protection, statelessness, procedure steps, applicant rights, legal framework.
- **Update frequency:** Informational content relatively stable; processing times and regulatory changes periodic.
- **Access method:** Crawl. Key sections at proteccion-asilo.interior.gob.es: `/proteccion-internacional/tramitacion-de-la-solicitud/`, `/proteccion-internacional/normativa-basica-reguladora/`.
- **Notes:**
  - OAR is under the Ministry of Interior.
  - Asylum seekers are among the most vulnerable populations.
  - Application is in-person (police station or border); cannot be done online.
  - After application: "tarjeta roja" (red card) issued as temporary documentation.
  - Processing times: 6 months to several years.
  - UNHCR Spain resource: https://help.unhcr.org/spain/

### 23. Registro Civil

- **URL (birth cert):** https://sede.mjusticia.gob.es/tramites/certificado-nacimiento
- **URL (marriage cert):** https://sede.mjusticia.gob.es/tramites/certificado-matrimonio
- **URL (info):** https://www.mjusticia.gob.es/es/ciudadania/estado-civil/registro-civil
- **Type:** Sede electronica (under Min. Justicia)
- **Priority:** P1 (important)
- **Coverage:** Civil registry certificates: birth, marriage, death. Also: name changes, civil status modifications.
- **Update frequency:** Stable procedures.
- **Access method:** Crawl via sede.mjusticia.gob.es. Certificate requests online with Clave/certificate. Digital records: births from 1996+, marriages from 1989+.
- **Notes:**
  - Part of the Ministerio de Justicia sede electronica (shared infrastructure).
  - Physical Registro Civil offices are transitioning to new digital system (LRC - Ley del Registro Civil).
  - Certificates needed for many other procedures (nationality, marriage, inheritance).
  - FAQ at https://sede.mjusticia.gob.es/informacion-ayuda/faq-registro-civil.

### 24. datos.gob.es (Portal Nacional de Datos Abiertos)

- **URL:** https://datos.gob.es/
- **API endpoint:** https://datos.gob.es/apidata/catalog/dataset
- **GitHub:** https://github.com/datosgobes
- **Type:** Open data catalog (CKAN-based)
- **Priority:** P1 (important)
- **Coverage:** National open data catalog aggregating datasets from all Spanish administrations. Includes: employment data, geographic data, health data, transport, budgets, statistical data.
- **Update frequency:** Continuously as publishers add/update datasets.
- **Access method:** CKAN REST API. Default format: JSON. Supports: JSON, XML, RDF, TTL, CSV. Endpoint: `https://datos.gob.es/apidata/catalog/dataset`. Filtering by theme, publisher, format.
- **Notes:**
  - Built on CKAN + Drupal.
  - Useful for finding specific datasets that can enrich RAG answers (e.g., lists of SEPE offices, social services locations).
  - No auth required for API.
  - Can be searched by theme (empleo, educacion, salud, etc.).

### 25. Import@ss (Portal Digital de la Seguridad Social)

- **URL:** https://portal.seg-social.gob.es/wps/portal/importass/importass/inicio
- **App:** iOS (App Store) + Android (Google Play) — "Importass Seguridad Social"
- **Type:** Portal + mobile app
- **Priority:** P1 (important)
- **Coverage:** Modern digital interface for TGSS services: Social Security number lookup/request, vida laboral download, contribution history, home employment registration, self-employment management, contact/address updates, benefit tracking.
- **Update frequency:** Continuously updated; app launched September 2024.
- **Access method:** Requires authentication. Accessible via SMS verification (no digital certificate needed — key advantage for vulnerable users). NOT crawlable for personal data; crawl informational/help pages.
- **Notes:**
  - 1.2M+ installs as of May 2025.
  - Major advantage: SMS-based auth (no need for Clave or digital certificate).
  - For RAG: document what users can do through Import@ss and how to access it.
  - Represents the modern direction of Spanish e-government (mobile-first).

---

## Appendix A: Priority Classification Criteria

| Priority | Criteria | Count |
|----------|----------|-------|
| **P0 (Essential)** | Directly serves high-impact procedures for vulnerable populations (employment, income, immigration, housing, social security). Must be in RAG from day 1. | 8 |
| **P1 (Important)** | Important supporting sources, frequently needed but not the first line of support. Should be in RAG within first quarter. | 10 |
| **P2 (Nice-to-have)** | Reference data, niche audiences, or low-frequency needs. Can be added later. | 5 |

### P0 Sources (8):
1. SIA, 2. PAG, 5. Sede PAG, 6. BOE Diario, 7. BOE Legislacion, 9. SEPE, 10. Seguridad Social, 11. AEAT, 13. Extranjeria, 19. IMV

### P1 Sources (10):
3. Carpeta Ciudadana, 4. Clave, 8. BOE Sumarios, 12. DGT, 15. IMSERSO, 16. MIVAU, 17. Min. Justicia, 22. Asilo y Refugio, 23. Registro Civil, 24. datos.gob.es, 25. Import@ss

### P2 Sources (5):
14. MUFACE, 18. INE, 20. Catastro, 21. Portal Transparencia

---

## Appendix B: Access Method Summary

| Access Method | Sources | Notes |
|---------------|---------|-------|
| **REST API (no auth)** | BOE (6,7,8), INE (18), datos.gob.es (24) | Best for automated ingestion. Structured data. |
| **SOAP/WSDL** | AEAT (11), Catastro (20) | Business-oriented; requires certificates for most. |
| **RSS feeds** | BOE (6,8) | Good for monitoring new publications. |
| **Crawl (public pages)** | PAG (2), Sede PAG (5), SEPE (9), Seg. Social (10), DGT (12), Extranjeria (13), MUFACE (14), IMSERSO (15), MIVAU (16), Min. Justicia (17), IMV (19), Transparencia (21), Asilo (22), Registro Civil (23) | Main method for most sources. Respect robots.txt. |
| **Auth-only** | Carpeta Ciudadana (3), Import@ss (25) | Cannot extract personal data; crawl help/info pages only. |
| **Informational crawl** | Clave (4), SIA (1) | Static content about how systems work. |

---

## Appendix C: Key URLs Quick Reference

```
# Core Infrastructure
https://administracion.gob.es/                              # PAG
https://sede.administracion.gob.es/                         # Sede PAG
https://carpetaciudadana.gob.es/                            # Carpeta Ciudadana
https://clave.gob.es/                                       # Clave

# BOE (APIs)
https://www.boe.es/datosabiertos/api/api.php                # API docs
https://boe.es/datosabiertos/api/boe/sumario/YYYYMMDD       # Daily summary
https://www.boe.es/datosabiertos/api/legislacion-consolidada # Consolidated law
https://www.boe.es/rss/                                     # RSS feeds

# High-Impact Sedes Electronicas
https://sede.sepe.gob.es/                                   # SEPE (employment)
https://sede.seg-social.gob.es/                             # Seguridad Social
https://sede.agenciatributaria.gob.es/                      # AEAT (taxes)
https://sede.policia.gob.es/portalCiudadano/                # Extranjeria
https://sede.inclusion.gob.es/                              # Min. Inclusion
https://sede.mjusticia.gob.es/                              # Min. Justicia
https://sede.imserso.gob.es/                                # IMSERSO
https://sede.dgt.gob.es/                                    # DGT (traffic)
https://mivau.sede.gob.es/                                  # MIVAU (housing)

# Data APIs
https://servicios.ine.es/wstempus/js/ES/                    # INE JSON API
https://datos.gob.es/apidata/catalog/dataset                # datos.gob.es CKAN API
https://www.sedecatastro.gob.es/                            # Catastro

# Other
https://transparencia.gob.es/                               # Transparencia
https://proteccion-asilo.interior.gob.es/                   # Asilo y Refugio
https://portal.seg-social.gob.es/wps/portal/importass/      # Import@ss
```

---

## Appendix D: Ingestion Recommendations

1. **Start with BOE API** — structured, documented, no auth. Set up daily monitoring for Section III (aid/scholarships).
2. **Crawl PAG procedure pages** — highest coverage of procedures in citizen-friendly language.
3. **Crawl SEPE + Seg. Social + Extranjeria informational pages** — the three most impactful domains for vulnerable users.
4. **Add IMV content** — Ingreso Minimo Vital is the single most requested benefit.
5. **Use INE API for reference data** — IPREM, SMI thresholds used in eligibility calculations.
6. **Monitor BOE RSS** — detect new aid programs and regulatory changes automatically.
7. **Respect robots.txt** — all .gob.es sites should be crawled respectfully (1-2 sec delay between requests).
8. **Handle Clave-gated content** — extract ONLY publicly available informational pages. Never attempt to bypass authentication.
