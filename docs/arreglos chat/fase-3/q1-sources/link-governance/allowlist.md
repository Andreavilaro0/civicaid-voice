# Domain Allowlist Policy

> **Scope:** Defines which domains Clara's RAG indexer may crawl, cite, and serve to users.
> **Owner:** Link Governance team
> **Last updated:** 2026-02-18

---

## Design Principles

1. **Government-only sources.** Clara cites official government information. Commercial advisory sites, forums, and aggregators are never cited.
2. **Tier-based trust.** Domains are classified into three trust tiers that determine crawl priority, check frequency, and citation weight.
3. **Allowlist-first.** Any domain not on the allowlist is rejected by default. New domains require manual review before inclusion.
4. **Subdomain inheritance.** If a root domain is allowed, all subdomains under it are auto-allowed unless explicitly blocked.

---

## Tier 1 -- Administracion General del Estado (AGE)

Always trusted. Highest crawl priority (P0/P1). These are the national-level government sources.

### Core ecosystem (*.gob.es)

| Domain | Entity | Notes |
|--------|--------|-------|
| `administracion.gob.es` | Portal de la Administracion | Central procedures catalogue |
| `sede.administracion.gob.es` | Sede electronica AGE | Electronic office, online filings |
| `boe.es` / `www.boe.es` | Boletin Oficial del Estado | Legislation, public domain content |
| `seg-social.es` / `sede.seg-social.gob.es` | Seguridad Social | IMV, pensions, affiliation |
| `sepe.es` / `sede.sepe.gob.es` | Servicio Publico de Empleo | Unemployment, job search |
| `agenciatributaria.es` / `agenciatributaria.gob.es` | Agencia Tributaria | Taxes, IRPF, NIF |
| `dgt.es` / `sede.dgt.gob.es` | Direccion General de Trafico | Driving, vehicle procedures |
| `inclusion.gob.es` | Ministerio de Inclusion | Migration, asylum, social services |
| `mites.gob.es` | Ministerio de Trabajo | Labor law, inspections |
| `mjusticia.gob.es` / `sede.mjusticia.gob.es` | Ministerio de Justicia | Criminal records, nationality, legal aid |
| `exteriores.gob.es` | Ministerio de Asuntos Exteriores | Consular, legalization |
| `mdsocialesa2030.gob.es` | Ministerio de Derechos Sociales | Social rights, dependency |
| `mitma.gob.es` | Ministerio de Transportes | Housing aid (ayuda alquiler) |
| `educacionyfp.gob.es` | Ministerio de Educacion | Scholarships, foreign title recognition |
| `mscbs.gob.es` / `sanidad.gob.es` | Ministerio de Sanidad | Health card, healthcare |
| `interior.gob.es` | Ministerio del Interior | NIE/TIE, asylum office |
| `policia.es` / `sede.policia.gob.es` | Policia Nacional | NIE appointments, documentation |
| `map.gob.es` | Ministerio de Administraciones Publicas | Admin reform portal |
| `060.es` | Punto de Acceso General | Citizen services portal |
| `carpetaciudadana.gob.es` | Carpeta Ciudadana | Personal admin dossier |
| `cl@ve` / `clave.gob.es` | Sistema Cl@ve | Digital identity |
| `iprem.es` | IPREM reference | (only if official) |

### Auto-allow rule

Any subdomain of `.gob.es` is auto-allowed:
```
*.gob.es -> ALLOW (Tier 1)
```

Exceptions can be added to the blocklist if a `.gob.es` subdomain serves non-authoritative content.

---

## Tier 2 -- Comunidades Autonomas (CCAA)

Trusted for regional procedures. Crawl priority P1.

| Domain pattern | CCAA | Notes |
|----------------|------|-------|
| `comunidad.madrid` / `sede.comunidad.madrid` | Madrid | |
| `web.gencat.cat` / `tramits.gencat.cat` | Cataluna | Prefer Spanish-language pages |
| `juntadeandalucia.es` / `ws089.juntadeandalucia.es` | Andalucia | |
| `gva.es` / `sede.gva.es` | Comunitat Valenciana | |
| `gobiernodecanarias.org` / `sede.gobiernodecanarias.org` | Canarias | |
| `euskadi.eus` / `sede.euskadi.eus` | Pais Vasco | |
| `xunta.gal` / `sede.xunta.gal` | Galicia | |
| `navarra.es` / `sede.navarra.es` | Navarra | |
| `aragon.es` / `sede.aragon.es` | Aragon | |
| `castillalamancha.es` / `sede.castillalamancha.es` | Castilla-La Mancha | |
| `jcyl.es` / `sede.jcyl.es` | Castilla y Leon | |
| `murciaregion.es` / `sede.carm.es` | Murcia | Also `carm.es` |
| `larioja.org` / `sede.larioja.org` | La Rioja | |
| `asturias.es` / `sede.asturias.es` | Asturias | |
| `cantabria.es` / `sede.cantabria.es` | Cantabria | |
| `caib.es` / `sede.caib.es` | Illes Balears | |
| `extremadura.es` / `sede.juntaex.es` | Extremadura | |
| `ceuta.es` | Ceuta | |
| `melilla.es` | Melilla | |

### Auto-allow rule for CCAA

Subdomains of the listed CCAA root domains are auto-allowed. Regional TLDs:
```
*.cat  -> ALLOW if root is in the CCAA list
*.eus  -> ALLOW if root is in the CCAA list
*.gal  -> ALLOW if root is in the CCAA list
```

Other `.es` subdomains are allowed only if the root is explicitly listed above.

---

## Tier 3 -- Municipal (Validated per Seed List)

Trusted only for local procedures relevant to Clara's coverage areas. Crawl priority P2. Each domain must be individually validated before inclusion.

### Initial seed list (major cities)

| Domain | Municipality | Notes |
|--------|-------------|-------|
| `madrid.es` / `sede.madrid.es` | Madrid | Empadronamiento, social services |
| `barcelona.cat` / `ajuntament.barcelona.cat` / `sede.barcelona.cat` | Barcelona | |
| `sevilla.org` / `sede.sevilla.org` | Sevilla | |
| `valencia.es` / `sede.valencia.es` | Valencia | |
| `zaragoza.es` / `sede.zaragoza.es` | Zaragoza | |
| `malaga.eu` / `sede.malaga.eu` | Malaga | |
| `bilbao.eus` / `sede.bilbao.eus` | Bilbao | |
| `alicante.es` | Alicante | |
| `cordoba.es` | Cordoba | |
| `valladolid.es` | Valladolid | |
| `laspalmasgc.es` | Las Palmas | |
| `santacruzdetenerife.es` | Santa Cruz | |

### Expansion rules

- New municipalities are added only when a specific tramite in the KB references that municipality.
- Each new domain must be verified manually (check WHOIS, check it resolves to the actual ayuntamiento).
- Do not bulk-add all 8,000+ Spanish municipalities. Add on-demand.

---

## Blocked Domains

The following categories are **always rejected**, regardless of content quality:

| Category | Examples | Reason |
|----------|----------|--------|
| Commercial gestoria/asesoria | `loentiendo.com`, `tramitalia.com`, `emigralia.es`, `parainmigrantes.info` | Commercial, may have outdated/biased info |
| SEO content farms | `rankia.com`, `asesorias.com`, `supercontable.com` | SEO-optimized, not authoritative |
| Forums and Q&A | `forocoches.com`, `burbuja.info`, Reddit, Quora | User-generated, unverified |
| Social media | `twitter.com`, `facebook.com`, `instagram.com`, `tiktok.com` | Not authoritative sources |
| Wikipedia | `es.wikipedia.org` | Useful reference but not a primary source |
| News outlets | `elpais.com`, `elmundo.es`, `20minutos.es` | Journalism, not primary source |
| Unofficial aggregators | `tramitesygestiones.com`, `extranjeria.info` | Appear official but are not |
| Legal databases (commercial) | `noticias.juridicas.com`, `vlex.es` | Commercial interpretation of law |
| AI-generated content sites | Various | Cannot verify accuracy |

### Explicit blocklist patterns

```
# Reject any domain not on the allowlist
DEFAULT: REJECT

# Explicit blocks (even if they match a pattern)
*.wordpress.com     -> BLOCK
*.blogspot.com      -> BLOCK
*.medium.com        -> BLOCK
*.notion.site       -> BLOCK  (public Notion pages)
```

---

## Domain Review Process

### Adding a new domain

1. **Request:** Any team member can request a new domain via the backlog.
2. **Validation checklist:**
   - [ ] Domain resolves to an official government entity
   - [ ] WHOIS registrant is a government body (or `.gob.es`)
   - [ ] The site contains specific procedure information (not just a homepage)
   - [ ] SSL certificate is valid
   - [ ] robots.txt allows crawling
   - [ ] Content is in Spanish (or has Spanish version)
3. **Approval:** Requires review by at least one other team member.
4. **Documentation:** Add to this allowlist with tier, notes, and date added.

### Removing a domain

1. Domain consistently returns errors (dead for 30+ days).
2. Domain is discovered to serve non-authoritative content.
3. Domain merges with another (update the allowlist to point to the new domain).

---

## Implementation Notes

### For the RAG indexer

```python
# Pseudocode for allowlist check
def is_allowed(url: str) -> bool:
    domain = extract_domain(url)

    # Check explicit blocklist first
    if domain in BLOCKLIST or matches_block_pattern(domain):
        return False

    # Check tier 1: *.gob.es auto-allow
    if domain.endswith(".gob.es"):
        return True

    # Check tiers 1-3: explicit allowlist
    if domain in ALLOWLIST or parent_domain(domain) in ALLOWLIST:
        return True

    # Default: reject
    return False
```

### For Clara's citation behavior

- When citing a source, always prefer the most specific (deepest) informative link.
- If only a homepage is available, cite it but flag it for the team to find a deeper link.
- Never cite a blocked domain even if a user shares it.
- If a user shares a link from a blocked domain, Clara should acknowledge the question but answer from official sources only.

---

## Appendix: Domains Already in Clara's KB

These domains are already cited in `data/tramites/*.json` and are confirmed Tier 1:

| KB File | `fuente_url` domain | Status |
|---------|---------------------|--------|
| `imv.json` | `seg-social.es` | Tier 1 |
| `prestacion_desempleo.json` | `sepe.es` | Tier 1 |
| `empadronamiento.json` | TBD (municipal) | Tier 3 |
| `tarjeta_sanitaria.json` | TBD (CCAA/AGE) | Tier 1/2 |
| `nie_tie.json` | `inclusion.gob.es` or `policia.es` | Tier 1 |
| `ayuda_alquiler.json` | `mitma.gob.es` | Tier 1 |
| `certificado_discapacidad.json` | CCAA-specific | Tier 2 |
| `justicia_gratuita.json` | `mjusticia.gob.es` | Tier 1 |
