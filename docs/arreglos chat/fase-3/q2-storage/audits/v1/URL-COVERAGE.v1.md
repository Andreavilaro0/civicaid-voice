# Q2 URL Coverage Audit (v1)

**Date:** 2026-02-19
**Auditor:** doc-auditor (automated)
**Method:** Extracted all URLs from Q2 docs (.md), src/core/rag/ (.py), and data/tramites/ (.json). Cross-referenced against `data/policy/allowlist.yaml`.

---

## Legend

| Status | Meaning |
|--------|---------|
| COVERED | Domain is in allowlist.yaml (tier 1, 2, or 3) |
| GOV_NOT_COVERED | Appears to be government but not explicitly in allowlist |
| NON_GOV_REF | Non-government reference URL |

---

## URLs Found

### data/tramites/ (JSON files)

| # | File | URL | Domain | Allowlist Status |
|---|------|-----|--------|-----------------|
| 1 | ayuda_alquiler.json | `https://www.mivau.gob.es/vivienda` | mivau.gob.es | **COVERED** (Tier 1 — Ministerio de Vivienda, allowlist line 101) |
| 2 | imv.json | `https://www.seg-social.es/wps/portal/wss/internet/Trabajadores/PrestacionesPensionesTrabajadores/65850d68-...` | seg-social.es | **COVERED** (Tier 1 — Seguridad Social, allowlist line 54) |
| 3 | justicia_gratuita.json | `https://www.mjusticia.gob.es/es/justicia-gratuita` | mjusticia.gob.es | **COVERED** (Tier 1 — Ministerio de Justicia, allowlist line 87) |
| 4 | prestacion_desempleo.json | `https://www.sepe.es/HomeSepe/Personas/Distribucion-Prestaciones/he-dejado-de-trabajar.html` | sepe.es | **COVERED** (Tier 1 — SEPE, allowlist line 62) |
| 5 | certificado_discapacidad.json | `https://www.comunidad.madrid/servicios/asuntos-sociales/valoracion-reconocimiento-discapacidad` | comunidad.madrid | **COVERED** (Tier 2 — Madrid CCAA, allowlist line 150) |
| 6 | empadronamiento.json | `https://www.madrid.es/portales/munimadrid/es/Inicio/El-Ayuntamiento/Empadronamiento` | madrid.es | **COVERED** (Tier 3 — Municipal Madrid, allowlist line 258) |
| 7 | nie_tie.json | `https://www.inclusion.gob.es/web/migraciones/nie` | inclusion.gob.es | **COVERED** (Tier 1 — Ministerio de Inclusion, allowlist line 79) |
| 8 | tarjeta_sanitaria.json | `https://www.comunidad.madrid/servicios/salud/tarjeta-sanitaria` | comunidad.madrid | **COVERED** (Tier 2 — Madrid CCAA, allowlist line 150) |

### docs/arreglos chat/fase-3/q2-storage/ (Markdown files)

| # | File | URL | Domain | Allowlist Status |
|---|------|-----|--------|-----------------|
| 9 | evidence/gates.md | `https://www.comunidad.madrid/servicios/asuntos-sociales/valoracion-reconocimiento-discapacidad` | comunidad.madrid | **COVERED** (Tier 2 — duplicate of #5) |

### src/core/rag/ (Python files)

No URLs found in any `.py` file in `src/core/rag/`.

---

## Summary

| Status | Count |
|--------|-------|
| COVERED | 9 (8 unique + 1 duplicate) |
| GOV_NOT_COVERED | 0 |
| NON_GOV_REF | 0 |

**All 8 unique government URLs are covered by the allowlist.**

| Tier | Count |
|------|-------|
| Tier 1 (AGE) | 5 (mivau.gob.es, seg-social.es, mjusticia.gob.es, sepe.es, inclusion.gob.es) |
| Tier 2 (CCAA) | 2 (comunidad.madrid x2) |
| Tier 3 (Municipal) | 1 (madrid.es) |

---

## Notes

- The Q2-CLOSING-REPORT.md contains a `postgresql://` connection string in the commands section (line 210) — this is a local dev connection, not a web URL.
- No non-government URLs were found anywhere in Q2 scope.
- All tramites `fuente_url` values point to allowlisted domains.

---

*Generated 2026-02-19 by doc-auditor v1*
