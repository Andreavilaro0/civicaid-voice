# URL Canonicalization Policy

> **Scope:** Rules for normalizing and deduplicating URLs across Clara's source registry and link health system.
> **Owner:** Link Governance team
> **Last updated:** 2026-02-18

---

## Why Canonicalize

Government websites are inconsistent. The same page might be reachable via:
- `http://www.sepe.es/HomeSepe/Personas/` and `https://sepe.es/HomeSepe/Personas`
- `https://sede.seg-social.gob.es/page?lang=es&utm_source=google` and `https://sede.seg-social.gob.es/page?lang=es`

Without canonicalization, the system would store duplicates, waste crawl budget, and potentially cite stale versions of the same page. Every URL entering the system must pass through canonicalization before storage.

---

## Canonicalization Rules

### Rule 1: Protocol -- Always HTTPS

Strip `http://` and normalize to `https://`.

```
http://www.boe.es/buscar/   ->  https://www.boe.es/buscar/
```

**Exception:** If a government site genuinely does not support HTTPS (rare), store as HTTP and flag for manual review.

### Rule 2: Trailing Slashes -- Remove

Normalize to no trailing slash for consistency.

```
https://sepe.es/HomeSepe/Personas/  ->  https://sepe.es/HomeSepe/Personas
https://boe.es/                     ->  https://boe.es
```

**Exception:** If removing the trailing slash causes a redirect to a different page, keep the trailing slash and note it.

### Rule 3: Query Parameters -- Strip Tracking Params

Remove known tracking and analytics parameters. Preserve parameters that affect page content.

**Always strip:**

| Parameter pattern | Source |
|-------------------|--------|
| `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content` | Google Analytics |
| `fbclid` | Facebook |
| `gclid`, `gad_source` | Google Ads |
| `ref`, `source`, `origin` | Generic referral |
| `mc_cid`, `mc_eid` | Mailchimp |
| `_ga`, `_gl` | Google Analytics cross-domain |
| `hsCtaTracking` | HubSpot |
| `mkt_tok` | Marketo |

**Always preserve:**

| Parameter pattern | Reason |
|-------------------|--------|
| `lang`, `idioma`, `locale` | Language selection (content changes) |
| `id`, `codigo`, `expediente` | Resource identifier |
| `page`, `pagina`, `p` | Pagination (see Rule 9) |
| `tipo`, `category`, `seccion` | Content filtering |

```
# Strip tracking
https://sepe.es/page?utm_source=twitter&lang=es  ->  https://sepe.es/page?lang=es

# Preserve content params
https://boe.es/buscar?id=BOE-A-2023-12345  ->  https://boe.es/buscar?id=BOE-A-2023-12345
```

**When uncertain:** Preserve the parameter and log it for manual review.

### Rule 4: Fragments/Anchors -- Strip from Stored URL

Remove `#fragment` from the canonical URL. Log the fragment separately for reference (it may indicate a specific section of a long page).

```
https://inclusion.gob.es/extranjeria#requisitos  ->  https://inclusion.gob.es/extranjeria
                                                      (logged: fragment=#requisitos)
```

### Rule 5: www vs non-www -- Follow the Domain's Canonical Form

Each domain has a preferred form. Normalize to whichever the domain itself uses (follow redirects to determine this).

| Domain | Canonical form | Notes |
|--------|---------------|-------|
| `boe.es` | `www.boe.es` | Redirects to www |
| `sepe.es` | `www.sepe.es` | Redirects to www |
| `seg-social.es` | `www.seg-social.es` | Redirects to www |
| `agenciatributaria.es` | `sede.agenciatributaria.gob.es` | Redirects to sede subdomain |
| `comunidad.madrid` | `www.comunidad.madrid` | Check redirect behavior |

**Discovery method:** Issue a HEAD request to `http://example.es` and follow all redirects. The final domain is the canonical form. Cache this mapping per domain.

### Rule 6: Case -- Lowercase Domain, Preserve Path Case

- Domain: always lowercase (`SEPE.ES` -> `sepe.es`)
- Path: preserve original case. Many government CMS platforms use case-sensitive paths.

```
https://SEPE.ES/HomeSepe/Personas  ->  https://sepe.es/HomeSepe/Personas
```

### Rule 7: Redirects -- Store Final URL

When a URL redirects (301, 302, 303, 307, 308), follow the full redirect chain and store the **final destination** as the canonical URL. Also store the redirect chain for debugging.

```
Original:  https://seg-social.es/imv
Chain:     -> 301 https://www.seg-social.es/imv
           -> 302 https://www.seg-social.es/wps/portal/wss/internet/Trabajadores/...
Canonical: https://www.seg-social.es/wps/portal/wss/internet/Trabajadores/...
```

**Limits:**
- Maximum redirect depth: 5 hops. If exceeded, store the original URL and flag for manual review.
- If a redirect leaves the allowlist (e.g., redirects to a commercial site), reject the URL.

### Rule 8: Session Parameters -- Strip

Remove server-side session identifiers that make URLs unique per user/session.

**Always strip:**
- `JSESSIONID`
- `PHPSESSID`
- `sid`
- `session_id`
- `ASPSESSIONID*`
- `cfid`, `cftoken`
- Any parameter matching pattern `^[A-Za-z]*session[A-Za-z]*$` (case-insensitive)

```
https://sede.example.gob.es/tramite;jsessionid=ABC123?id=456
  ->  https://sede.example.gob.es/tramite?id=456
```

### Rule 9: Pagination -- Store Base URL, Annotate

For paginated content, store the base URL (page 1 / no page param) as the canonical URL. Record pagination metadata separately.

```
Canonical: https://boe.es/buscar?tipo=leyes
Metadata:  { paginated: true, total_pages: 12, page_param: "p" }
```

**Rationale:** Clara should cite the starting point of a paginated list, not page 7 of 12.

### Rule 10: Language Variants -- Prefer Spanish, Note Others

For bilingual/multilingual government sites (common in Cataluna, Pais Vasco, Galicia, Comunitat Valenciana):

1. **Prefer the Spanish (`es`, `cas`, `castellano`) version** as the canonical URL.
2. **Record the existence of other language versions** in metadata.
3. If French is available (relevant for Clara's French-speaking users), record the French URL as an alternate.

```
Canonical: https://web.gencat.cat/es/tramits/tramit-12345
Alternates:
  - ca: https://web.gencat.cat/ca/tramits/tramit-12345
  - en: https://web.gencat.cat/en/tramits/tramit-12345

Canonical: https://euskadi.eus/tramite/es/12345
Alternates:
  - eu: https://euskadi.eus/tramite/eu/12345
```

**If no Spanish version exists:** Store the available version and flag for manual translation/review.

---

## Informative Link vs Home Page

This distinction is critical for Clara's citation quality.

### Definition

| Type | Description | Example |
|------|-------------|---------|
| **Informative link** | Points to a SPECIFIC procedure, requirement page, or information document | `https://www.sepe.es/HomeSepe/Personas/Distribucion-Prestaciones/he-dejado-de-trabajar.html` |
| **Home page** | Root or landing page of a government entity with no specific content | `https://www.sepe.es` |
| **Section page** | An intermediate navigation page | `https://www.sepe.es/HomeSepe/Personas` |

### Citation rules

1. **Clara must cite informative links, never home pages.**
2. If only a home page or section page exists for a given topic, Clara should:
   - Cite it with a qualifier: "Puedes consultar mas informacion en la web del SEPE (sepe.es)"
   - Flag the gap internally so the team can find a deeper link
3. **Exception:** When a government entity has no deeper link for a specific topic, the home page is acceptable as a last resort.

### Classification heuristics

A URL is likely a **home page** if:
- Path is `/` or empty
- Path is a single segment (e.g., `/inicio`, `/home`, `/es`)
- Path depth < 2 segments

A URL is likely an **informative link** if:
- Path depth >= 2 segments
- URL contains identifiers (numeric IDs, slugs like `prestacion-desempleo`)
- URL points to a PDF or specific document
- Page title contains a procedure name

### How this applies to the KB

Every `fuente_url` in `data/tramites/*.json` should be an informative link, not a home page. During source registry validation, check each URL against these heuristics and flag any that appear to be home pages.

---

## Canonicalization Pipeline

### Order of operations

When a URL enters the system, apply the rules in this sequence:

```
1. Parse URL into components (scheme, domain, path, query, fragment)
2. Normalize protocol to HTTPS (Rule 1)
3. Lowercase domain (Rule 6)
4. Strip session parameters from path and query (Rule 8)
5. Strip tracking parameters from query (Rule 3)
6. Strip fragment (Rule 4, log it)
7. Remove trailing slash (Rule 2)
8. Follow redirects to get final URL (Rule 7)
9. Apply www normalization using cached domain mappings (Rule 5)
10. Determine language variant preference (Rule 10)
11. Annotate pagination metadata (Rule 9)
12. Classify as informative link vs home page
13. Store canonical URL + metadata
```

### Pseudocode

```python
def canonicalize(raw_url: str) -> CanonicalURL:
    parsed = urlparse(raw_url)

    # Step 1-2: HTTPS
    scheme = "https"

    # Step 3: lowercase domain
    domain = parsed.hostname.lower()

    # Step 4: strip session params from path
    path = strip_session_from_path(parsed.path)

    # Step 5: strip tracking + session from query
    query_params = parse_qs(parsed.query)
    query_params = {k: v for k, v in query_params.items()
                    if k not in TRACKING_PARAMS and k not in SESSION_PARAMS}

    # Step 6: log fragment
    fragment_note = parsed.fragment if parsed.fragment else None

    # Step 7: remove trailing slash
    path = path.rstrip("/") or "/"

    # Rebuild URL
    canonical = urlunparse((scheme, domain, path, "", urlencode(query_params), ""))

    # Step 8: follow redirects
    final_url, redirect_chain = follow_redirects(canonical, max_hops=5)

    # Step 9: www normalization
    final_url = apply_www_mapping(final_url)

    # Step 10-12: metadata
    lang_variants = detect_language_variants(final_url)
    pagination = detect_pagination(final_url, query_params)
    link_type = classify_link_type(final_url)

    return CanonicalURL(
        url=final_url,
        original=raw_url,
        redirect_chain=redirect_chain,
        fragment_note=fragment_note,
        lang_variants=lang_variants,
        pagination=pagination,
        link_type=link_type,  # "informative" | "homepage" | "section"
    )
```

---

## Edge Cases

### BOE URLs

BOE has a specific URL structure that must be preserved:
```
https://www.boe.es/buscar/act.php?id=BOE-A-2023-12345
https://www.boe.es/diario_boe/txt.php?id=BOE-A-2023-12345
```
The `id` parameter is always content-critical. Never strip it.

### Sede electronica URLs

Many `sede.*.gob.es` sites use Java-based CMS platforms with complex path structures:
```
https://sede.seg-social.gob.es/wps/portal/wss/internet/Trabajadores/PrestacionesPensionesTrabajadores/65850d68-...
```
These UUID-like path segments are content identifiers. Preserve them exactly.

### URL shorteners

Government agencies sometimes use `bit.ly`, `goo.gl`, or custom shorteners. Policy:
1. Resolve the shortener to the final URL.
2. If the final URL is on the allowlist, store the resolved URL (never the shortened form).
3. If the final URL is not on the allowlist, reject it.

### Broken encoding

Some government sites serve URLs with incorrect encoding (e.g., raw spaces, non-UTF8 characters). Normalize to proper percent-encoding:
```
https://example.gob.es/tramite con espacios  ->  https://example.gob.es/tramite%20con%20espacios
```
