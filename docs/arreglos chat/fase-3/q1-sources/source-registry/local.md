# Local Government Coverage Strategy

## Executive Summary

- Spain has **8,131 municipalities** -- pre-indexing all is infeasible. We adopt a tiered, incremental approach.
- **Tier 1 (P0):** 20 largest cities by population, manually curated with verified sede electronica URLs and procedure catalogs. Covers ~30% of Spain's population.
- **Tier 2 (P1):** Provincial capitals (52 provincias) plus cities ranked 21-50 by population. Semi-automated discovery via DIR3 + PAG directories.
- **Tier 3 (P2):** All municipalities above 50,000 inhabitants (~150 total). Automated crawl with human validation.
- **Tier 4 (deferred):** Remaining ~7,900 municipalities served via directory fallback (DIR3, INE registry, Diputaciones Provinciales).
- A **disambiguation strategy** ensures the bot asks the user's municipality only when the procedure is municipal-level, and falls back to provincial/CCAA sources for unknown municipalities.

---

## Tiered Coverage

### Tier 1: Top 20 Cities (P0) -- Manual Curation

These 20 cities represent approximately 30% of Spain's total population and an even higher share of the immigrant population. Each has been verified with real sede electronica URLs.

| # | City | Province | Pop. (approx) | Sede Electronica | Catalogo Tramites | Status |
|---|------|----------|---------------|------------------|-------------------|--------|
| 1 | Madrid | Madrid | 3,300,000 | https://sede.madrid.es/ | https://sede.madrid.es/portal/site/tramites | Verified |
| 2 | Barcelona | Barcelona | 1,660,000 | https://seuelectronica.ajuntament.barcelona.cat/es | https://seuelectronica.ajuntament.barcelona.cat/es/tramites-telematicos | Verified |
| 3 | Valencia | Valencia | 800,000 | https://sede.valencia.es/sede/ | https://sede.valencia.es/sede/menuContent.xhtml/PROCEDIMIENTOS?lang=1 | Verified |
| 4 | Sevilla | Sevilla | 685,000 | https://sede.sevilla.org/ | https://sede.sevilla.org/ (integrated) | Verified |
| 5 | Zaragoza | Zaragoza | 680,000 | https://www.zaragoza.es/sede/ | https://www.zaragoza.es/sede/portal/tramites-servicios/ | Verified |
| 6 | Malaga | Malaga | 580,000 | https://sede.malaga.eu/ | https://sede.malaga.eu/ (integrated) | Verified |
| 7 | Murcia | Murcia | 460,000 | https://sede.murcia.es/ | https://sede.murcia.es/ (integrated) | Verified |
| 8 | Palma | Illes Balears | 420,000 | https://seuelectronica.palma.cat/ | https://www.palma.es/es/gestiones-y-tramites | Verified |
| 9 | Las Palmas de Gran Canaria | Las Palmas | 380,000 | https://sedeelectronica.laspalmasgc.es/ | https://www.laspalmasgc.es/es/online/sede-electronica/catalogo-de-tramites/ | Verified |
| 10 | Bilbao | Bizkaia | 350,000 | https://www.bilbao.eus/eudala | https://www.bilbao.eus/eudala (integrated, e-Udala) | Verified |
| 11 | Alicante | Alicante | 340,000 | https://sedeelectronica.alicante.es/ | https://sedeelectronica.alicante.es/servicios.php | Verified |
| 12 | Cordoba | Cordoba | 325,000 | https://sede.cordoba.es/ | https://oficinavirtual.cordoba.es/catalogo-de-tramites-y-servicios | Verified |
| 13 | Valladolid | Valladolid | 300,000 | https://sede.valladolid.es/ | https://sede.valladolid.es/ (integrated) | Verified |
| 14 | Vigo | Pontevedra | 295,000 | https://sede.vigo.org/ | https://sede.vigo.org/ (integrated) | Verified |
| 15 | Gijon | Asturias | 270,000 | https://sedeelectronica.gijon.es/ | https://sedeelectronica.gijon.es/ (integrated) | Verified |
| 16 | L'Hospitalet de Llobregat | Barcelona | 265,000 | https://seuelectronica.l-h.cat/ | https://seuelectronica.l-h.cat/tramits/r/tramits_2.aspx?id=2 | Verified |
| 17 | Vitoria-Gasteiz | Araba/Alava | 255,000 | https://sedeelectronica.vitoria-gasteiz.org/ | https://sedeelectronica.vitoria-gasteiz.org/portal/es/tramites | Verified |
| 18 | A Coruna | A Coruna | 245,000 | https://sede.coruna.gal/ | https://sede.coruna.gal/sede/es/tramites-y-servicios-electronicos | Verified |
| 19 | Granada | Granada | 230,000 | https://sede.granada.org/ | https://www.granada.org/inicio.nsf/mn/s03 | Verified |
| 20 | Elche | Alicante | 230,000 | https://sede.elche.es/ | https://sede.elche.es/sta/CarpetaPublic/doEvent?APP_CODE=STA&PAGE_CODE=CATALOGO | Verified |

#### Key Procedures per City (Tier 1)

For each Tier 1 city, the RAG system should index at minimum these five municipal-level procedures:

| Procedure | Description | Why critical |
|-----------|-------------|--------------|
| **Empadronamiento / Alta en Padron** | Municipal registration (census) | Required for all residents, prerequisite for many other procedures |
| **Certificado de empadronamiento** | Certificate of municipal registration | Needed for residency renewals, school enrollment, healthcare |
| **IBI (Impuesto sobre Bienes Inmuebles)** | Property tax | Affects all property owners/renters |
| **Tasa de basuras / residuos** | Waste collection tax | Universal municipal tax |
| **Licencias de actividad / apertura** | Business activity licenses | Needed by entrepreneurs and self-employed |

Additional procedures to consider for Phase 2 expansion:
- Licencia de obras (building permits)
- Bonificaciones y exenciones fiscales (tax exemptions)
- Tarjeta de transporte municipal (local transport card)
- Ayudas y subvenciones municipales (municipal grants)
- Registro de parejas de hecho (domestic partnership registry)

---

### Tier 2: Provincial Capitals + Cities 21-50 (P1) -- Semi-Automated

**Strategy:** Spain has 52 provincias (50 standard + Ceuta + Melilla). Many provincial capitals overlap with the top 20. After deduplication, approximately 40-45 additional cities need coverage.

**Approach:**
1. Use DIR3 directory to programmatically obtain the official sede electronica URL for each provincial capital.
2. Cross-reference with the PAG (Punto de Acceso General) municipal portal listing at: `https://administracion.gob.es/pag_Home/atencionCiudadana/SedesElectronicas-y-Webs-Publicas/websPublicas/WP_EELL/WP_Ayuntamientos.html`
3. Validate each URL with an automated HTTP check + manual spot-check.
4. Index the same five core procedures as Tier 1.

**Provincial capitals NOT in Tier 1 (sample -- not exhaustive):**

| Province | Capital | Est. Pop. |
|----------|---------|-----------|
| Almeria | Almeria | 200,000 |
| Badajoz | Badajoz | 150,000 |
| Burgos | Burgos | 175,000 |
| Caceres | Caceres | 96,000 |
| Cadiz | Cadiz | 115,000 |
| Castellon | Castellon de la Plana | 170,000 |
| Ciudad Real | Ciudad Real | 75,000 |
| Cuenca | Cuenca | 55,000 |
| Girona | Girona | 105,000 |
| Guadalajara | Guadalajara | 87,000 |
| Huelva | Huelva | 145,000 |
| Huesca | Huesca | 54,000 |
| Jaen | Jaen | 112,000 |
| Leon | Leon | 124,000 |
| Lleida | Lleida | 140,000 |
| Lugo | Lugo | 98,000 |
| Navarra | Pamplona | 205,000 |
| Ourense | Ourense | 105,000 |
| Palencia | Palencia | 78,000 |
| Cantabria | Santander | 172,000 |
| Salamanca | Salamanca | 145,000 |
| Segovia | Segovia | 52,000 |
| Soria | Soria | 40,000 |
| Tarragona | Tarragona | 135,000 |
| Teruel | Teruel | 36,000 |
| Toledo | Toledo | 85,000 |
| Zamora | Zamora | 60,000 |
| La Rioja | Logrono | 150,000 |
| Ceuta | Ceuta | 84,000 |
| Melilla | Melilla | 87,000 |

**Total estimated Tier 2 cities:** ~50 (after deduplication with Tier 1).

---

### Tier 3: Cities >50,000 inhabitants (P2) -- Automated with Validation

**Strategy:** According to INE data, approximately 150 municipalities in Spain have more than 50,000 inhabitants. After removing Tier 1 and Tier 2 cities, this leaves roughly 80-100 additional cities.

**Approach:**
1. Download the INE municipal population dataset.
2. Filter municipalities with population > 50,000.
3. For each, attempt to resolve the sede electronica URL using:
   - Pattern-based URL guessing: `sede.{municipio}.es`, `sedeelectronica.{municipio}.es`, `{municipio}.sedelectronica.es`
   - DIR3 lookup
   - PAG directory cross-reference
4. Automated HTTP validation + content check (look for keywords: "tramites", "catalogo", "sede electronica").
5. Human review of failed resolutions.

**Common sede electronica URL patterns observed:**

| Pattern | Examples | Frequency |
|---------|----------|-----------|
| `sede.{city}.es` | sede.madrid.es, sede.murcia.es, sede.valencia.es | Very common |
| `sedeelectronica.{city}.es` | sedeelectronica.alicante.es, sedeelectronica.gijon.es | Common |
| `seuelectronica.{city}.cat` | seuelectronica.ajuntament.barcelona.cat, seuelectronica.palma.cat | Catalan cities |
| `{city}.sedelectronica.es` | (used by smaller municipalities via shared platform) | Common for small towns |
| `{city}.sedipualba.es` | palma.sedipualba.es | SedipAlba platform users |
| `sede.{city}.org` | sede.vigo.org, sede.sevilla.org | Less common |

---

### Tier 4: Remaining Municipalities (Deferred) -- Directory Fallback

**Strategy:** The remaining ~7,900 municipalities (mostly under 20,000 inhabitants) will NOT be individually indexed. Instead, the system uses directory-based fallback.

**Approach:**
1. When a user names a municipality not in Tiers 1-3, the system:
   - Confirms the municipality exists via the INE code registry.
   - Attempts to find the sede electronica URL via DIR3.
   - If found, provides the URL directly to the user.
   - If not found, redirects to the corresponding Diputacion Provincial or CCAA sede electronica.
2. Many small municipalities share platforms provided by their Diputacion Provincial (e.g., `{municipio}.sedelectronica.es` hosted by the Diputacion).

---

## Official Directories (Fallback Infrastructure)

These directories form the backbone of the fallback system for municipalities not in Tiers 1-3.

### 1. DIR3 -- Directorio Comun de Unidades Organicas y Oficinas

- **URL:** https://administracionelectronica.gob.es/ctt/dir3
- **Dataset (datos.gob.es):** https://datos.gob.es/en/catalogo/e05188501-directorio-comun-de-unidades-organicas-y-oficinas-dir3
- **What it provides:** Unified inventory of ALL organizational units, public bodies, and registration offices across all levels of Spanish public administration (AGE, CCAA, EELL).
- **Update frequency:** Approximately monthly.
- **Use case:** Programmatic lookup of any municipality's official sede electronica and registration offices. Each unit has a unique DIR3 code.
- **Format:** Available as downloadable dataset (XML, CSV).

### 2. INE Municipal Registry (Relacion de Municipios y Codigos)

- **URL:** https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177031&menu=ultiDatos&idp=1254734710990
- **Description page:** https://www.ine.es/daco/daco42/codmun/codmun00i.htm
- **Dataset (datos.gob.es):** https://datos.gob.es/en/catalogo/ea0010587-relacion-de-municipios-y-sus-codigos-por-provincias
- **What it provides:** Complete list of all 8,131 municipalities with their INE codes (5 digits: 2 province + 3 municipality), province, and CCAA.
- **Update frequency:** Annual (reference date: January 1st each year).
- **Use case:** Validate that a municipality exists, get its province/CCAA, and use the INE code to look up further information.
- **Format:** PC-Axis, Excel, CSV.

### 3. PAG -- Punto de Acceso General (Municipal Portals Listing)

- **URL (Ayuntamientos):** https://administracion.gob.es/pag_Home/atencionCiudadana/SedesElectronicas-y-Webs-Publicas/websPublicas/WP_EELL/WP_Ayuntamientos.html
- **URL (Diputaciones):** https://administracion.gob.es/pag_Home/atencionCiudadana/SedesElectronicas-y-Webs-Publicas/websPublicas/WP_EELL/WP_Diputaciones.html
- **URL (Federaciones):** https://administracion.gob.es/pag_Home/atencionCiudadana/SedesElectronicas-y-Webs-Publicas/websPublicas/WP_EELL/WP_Federaciones.html
- **What it provides:** Browsable directory of municipal websites and sedes electronicas maintained by the Spanish government.
- **Use case:** Manual or semi-automated lookup of municipal web portals. Not as structured as DIR3 but more user-friendly.

### 4. FEMP -- Federacion Espanola de Municipios y Provincias

- **URL:** https://www.femp.es/
- **What it provides:** Association of 7,412 local entities. Provides best-practice guides, templates, and coordination resources. Not a direct directory of sedes electronicas, but useful for understanding municipal service patterns.
- **Use case:** Reference for standard municipal procedures and inter-municipal coordination.

### 5. Diputaciones Provinciales

- **Directory:** https://administracion.gob.es/pag_Home/atencionCiudadana/SedesElectronicas-y-Webs-Publicas/websPublicas/WP_EELL/WP_Diputaciones.html
- **What they provide:** Provincial governments that serve as the digital backbone for municipalities under 20,000 inhabitants (per Ley 27/2013 LRSAL). They often host shared sede electronica platforms for their smaller municipalities.
- **Use case:** When a user's municipality is too small to have its own sede, redirect to the corresponding Diputacion. The Diputacion's platform often allows selecting the specific municipality within the province.
- **Key role:** By law, Diputaciones must provide e-administration services to municipalities under 20,000 inhabitants.

### 6. Registro de Entidades Locales (REL)

- **Maintained by:** Ministerio de Politica Territorial
- **What it provides:** Official registry of all local entities (municipalities, mancomunidades, comarcas, etc.) with their official names as recognized by the State.
- **Use case:** Authoritative source for municipality names, useful for disambiguation and name normalization.

---

## Disambiguation Strategy

### When to Ask for Municipality

The bot should ask the user's municipality **only when the procedure is municipal-level**. Many procedures are handled at AGE or CCAA level and do not require knowing the municipality.

**Decision tree:**

```
User asks about a procedure
  |
  +--> Is it an AGE-level procedure? (e.g., NIE, TIE, asilo)
  |      YES --> Do NOT ask municipality. Route to AGE sources.
  |
  +--> Is it a CCAA-level procedure? (e.g., tarjeta sanitaria, educacion)
  |      YES --> Ask for CCAA (if not already known). Do NOT ask municipality.
  |
  +--> Is it a municipal-level procedure? (e.g., empadronamiento, IBI, basuras)
         YES --> Ask for municipality.
```

### Municipal-Level Procedures (require municipality disambiguation)

- Empadronamiento / alta en padron
- Certificado de empadronamiento
- IBI (Impuesto sobre Bienes Inmuebles)
- Tasa de basuras / residuos solidos urbanos
- Licencia de apertura / actividad
- Licencia de obras
- Plusvalia municipal
- ORA / zona azul (parking)
- Bonificaciones fiscales municipales
- Registro de parejas de hecho (some CCAA, some municipal)

### How to Ask

**Primary question (Spanish):**
> "Para ayudarte con este tramite, necesito saber en que municipio resides. Cual es tu municipio?"

**Follow-up if ambiguous:**
> "Hay varios municipios con ese nombre. Puedes indicarme la provincia?"

**Follow-up if municipality not in our system:**
> "No tenemos informacion especifica de tu municipio, pero puedo orientarte. Te proporciono el enlace a la sede electronica de tu ayuntamiento o de tu Diputacion Provincial para que puedas realizar el tramite."

### Fallback Chain

```
1. User provides municipality name
   |
   +--> Found in Tier 1-3? --> Provide specific procedure info from indexed data
   |
   +--> NOT found in Tier 1-3?
         |
         +--> Look up in DIR3/INE registry
         |     |
         |     +--> Sede electronica URL found? --> Provide URL + generic procedure guidance
         |     |
         |     +--> No sede URL? --> Provide Diputacion Provincial URL + generic guidance
         |
         +--> Municipality not recognized?
               |
               +--> Ask user to verify spelling / provide province
               +--> Suggest: administracion.gob.es or 060 phone line
```

### Name Disambiguation Cases

Some municipality names are shared across provinces:

| Name | Provinces |
|------|-----------|
| Aguilar | Cordoba, Huesca, Murcia |
| Santiago | A Coruna, others |
| Villanueva | Many (50+ municipalities start with "Villanueva") |

**Strategy:** When the municipality name is ambiguous, always ask for the province. Maintain a lookup table of ambiguous names.

---

## Incremental Rollout Plan

### Phase 1: Tier 1 -- Top 20 Cities (Q1-Q2 2026)

**Scope:** 20 cities, ~5 procedures each = ~100 procedure pages indexed.

**Tasks:**
1. Manually verify all 20 sede electronica URLs (done -- see table above).
2. For each city, locate and index the five core procedure pages (empadronamiento, certificado, IBI, basuras, licencias).
3. Extract structured data: requirements, documents needed, online vs. in-person, fees, deadlines.
4. Build per-city allowlist of crawlable URLs (see link governance document).
5. Validate RAG retrieval quality with test queries.

**Success criteria:**
- 20/20 cities indexed with at least 3 procedures each.
- RAG correctly retrieves municipal info for 90%+ of test queries about these cities.

**Effort:** ~40 hours manual curation.

### Phase 2: Tier 2 -- Provincial Capitals (Q2-Q3 2026)

**Scope:** ~50 additional cities, ~5 procedures each = ~250 procedure pages.

**Tasks:**
1. Download DIR3 dataset and extract provincial capital sede electronica URLs.
2. Cross-reference with PAG directory.
3. Automated HTTP validation of all URLs.
4. Semi-automated extraction of core procedure pages (using patterns learned from Tier 1).
5. Human review of extraction results (spot-check 20% of cities).
6. Add to RAG index with city-level metadata.

**Success criteria:**
- 45/50 cities indexed successfully (90%).
- Average 4+ procedures per city.

**Effort:** ~60 hours (20 automated + 40 human review).

### Phase 3: Tier 3 -- Cities >50k (Q3-Q4 2026)

**Scope:** ~100 additional cities, ~3-5 procedures each = ~300-500 procedure pages.

**Tasks:**
1. Download INE population dataset, filter >50k.
2. Remove already-indexed cities (Tiers 1-2).
3. Attempt automated sede electronica URL resolution using known URL patterns.
4. For unresolved cities, fall back to DIR3 lookup.
5. Automated crawl + extraction using templates from Phase 2.
6. Automated quality check (content length, keyword presence, language detection).
7. Human review of flagged issues only (~10% of cities).

**Success criteria:**
- 80/100 cities indexed successfully (80%).
- Average 3+ procedures per city.

**Effort:** ~40 hours (30 automated + 10 human review).

### Phase 4: Tier 4 -- Rest (Ongoing, from Q4 2026)

**Scope:** ~7,900 municipalities. NO individual indexing.

**Tasks:**
1. Load INE municipal registry into the system as a lookup table (municipality name --> province --> CCAA).
2. Load DIR3 sede electronica URLs as a fallback directory.
3. Map each province to its Diputacion Provincial sede electronica URL.
4. Implement the disambiguation and fallback chain described above.
5. Monitor user queries to identify high-demand municipalities not yet in Tiers 1-3 and prioritize them for future indexing.

**Success criteria:**
- System correctly identifies 95%+ of municipality names.
- System provides a valid fallback URL (Diputacion or CCAA) for 100% of recognized municipalities.
- Top 10 most-queried non-indexed municipalities are promoted to Tier 3 each quarter.

**Effort:** ~20 hours initial setup, ~5 hours/quarter maintenance.

---

## Technical Notes

### URL Stability

Municipal sede electronica URLs are generally stable, but some risks exist:
- Platform migrations (e.g., Granada migrated from sedeelectronica.granada.org to sede.granada.org).
- Domain changes (e.g., some cities use `.es`, others `.eu`, `.cat`, `.gal`, `.eus`).
- Shared platform updates (sedelectronica.es, sedipualba.es).

**Mitigation:** Quarterly URL health checks via automated HTTP HEAD requests. Alert on 404/redirect changes.

### Language Considerations

Some municipalities serve content in co-official languages:
- **Catalan:** Barcelona, L'Hospitalet, Palma, Girona, Lleida, Tarragona (domain: `.cat`)
- **Basque:** Bilbao, Vitoria-Gasteiz, San Sebastian (domain: `.eus`)
- **Galician:** Vigo, A Coruna, Lugo, Ourense, Santiago (domain: `.gal`)
- **Valencian:** Valencia, Alicante, Elche, Castellon

The RAG system should index the Spanish (Castellano) version of procedure pages when available, and note the availability of co-official language versions.

### Data Freshness

Municipal procedures change infrequently (annually at most for tax rates, rarely for core procedures like empadronamiento). A **quarterly re-crawl** of Tier 1 cities and **semi-annual re-crawl** of Tiers 2-3 should be sufficient.

---

## Appendix: Population and Immigrant Density Considerations

Cities with high immigrant populations should be prioritized within each tier, as these users are the primary audience for CivicAid Voice. Key indicators:
- **Percentage of foreign-born residents** (INE Padron data).
- **Absolute number of foreign residents.**
- **Diversity of origin countries** (affects language needs).

Top cities by foreign-born population percentage (approximate):
1. Torrevieja (Alicante) -- ~40%
2. Benidorm (Alicante) -- ~35%
3. Fuengirola (Malaga) -- ~33%
4. Roquetas de Mar (Almeria) -- ~30%
5. Marbella (Malaga) -- ~28%

These cities, while not in the top 20 by total population, should be considered for early Tier 3 promotion due to their high relevance to CivicAid Voice users.
