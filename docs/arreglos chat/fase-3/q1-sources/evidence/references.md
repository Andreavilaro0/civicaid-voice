# Q1 References

> Sources consulted during Q1 research
> Date: 2026-02-18

## Legal Framework

| Reference | URL | Relevance |
|-----------|-----|-----------|
| Ley 39/2015 (Procedimiento Administrativo Comun) | https://www.boe.es/buscar/act.php?id=BOE-A-2015-10565 | Regulates all administrative procedures; Art. 21.4 mandates SIA |
| Ley 40/2015 (Regimen Juridico del Sector Publico) | https://www.boe.es/buscar/act.php?id=BOE-A-2015-10566 | Institutional framework for e-government |
| Ley 19/2013 (Transparencia) | https://www.boe.es/buscar/act.php?id=BOE-A-2013-12887 | Right of access to public information |
| Ley 27/2013 LRSAL (Racionalizacion y Sostenibilidad AALL) | https://www.boe.es/buscar/act.php?id=BOE-A-2013-13756 | Diputaciones must provide e-admin to municipalities <20k |
| RD 4/2010 (Esquema Nacional de Interoperabilidad) | https://www.boe.es/buscar/act.php?id=BOE-A-2010-1331 | Interoperability standards including DIR3 |

## Government Portals (Primary Sources)

| Source | URL | Accessed |
|--------|-----|----------|
| Punto de Acceso General (PAG) | https://administracion.gob.es/ | 2026-02-18 |
| SIA (Sistema de Informacion Administrativa) | https://administracion.gob.es/pag_Home/espanaAdmon/SIA.html | 2026-02-18 |
| BOE Open Data API | https://www.boe.es/datosabiertos/api/api.php | 2026-02-18 |
| datos.gob.es | https://datos.gob.es/ | 2026-02-18 |
| INE API | https://www.ine.es/dyngs/DataLab/manual.html?cid=45 | 2026-02-18 |
| DIR3 dataset | https://datos.gob.es/en/catalogo/e05188501-directorio-comun-de-unidades-organicas-y-oficinas-dir3 | 2026-02-18 |
| INE Municipal Registry | https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177031 | 2026-02-18 |
| PAG Municipal Portals | https://administracion.gob.es/pag_Home/atencionCiudadana/SedesElectronicas-y-Webs-Publicas/websPublicas/WP_EELL/WP_Ayuntamientos.html | 2026-02-18 |
| PAG Diputaciones | https://administracion.gob.es/pag_Home/atencionCiudadana/SedesElectronicas-y-Webs-Publicas/websPublicas/WP_EELL/WP_Diputaciones.html | 2026-02-18 |

## Sedes Electronicas (Verified)

### AGE (25 sources)
See `source-registry/age.md` for complete list with URLs.

### CCAA (19 communities)
See `source-registry/ccaa.md` for complete list with URLs.

### Municipal (Top 20 cities)
See `source-registry/local.md` for complete list with verified URLs.

## Technical References

| Reference | URL | Used in |
|-----------|-----|---------|
| trafilatura docs | https://trafilatura.readthedocs.io/ | extraction-spec.md |
| pdfplumber docs | https://github.com/jsvine/pdfplumber | extraction-spec.md |
| readability-lxml | https://github.com/buriy/python-readability | extraction-spec.md |
| langdetect | https://github.com/Mimino666/langdetect | normalization-schema.md |
| CKAN API docs | https://docs.ckan.org/en/latest/api/ | ingestion-playbook.md |
| BOE API PDF doc | https://www.boe.es/datosabiertos/documentos/APIsumarioBOE.pdf | age.md, ingestion-playbook.md |
| BOE Consolidated API doc | https://www.boe.es/datosabiertos/documentos/APIconsolidada.pdf | age.md |
| Catastro web services doc | https://www.catastro.meh.es/ws/webservices_libres.pdf | age.md |

## Statistics

| Metric | Value | Source |
|--------|-------|--------|
| Total municipalities in Spain | 8,131 | INE 2025 |
| Provinces | 50 + 2 autonomous cities | INE |
| CCAA | 17 + 2 autonomous cities | Constitution |
| AGE sources cataloged | 25 | This research |
| CCAA profiles completed | 19/19 | This research |
| Municipal URLs documented | 20/8,131 (Tier 1 seed cities; 0.25% of all municipalities) | This research |
