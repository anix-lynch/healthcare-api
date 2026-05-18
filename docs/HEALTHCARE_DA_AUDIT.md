# healthcare-da → healthcare-api migration audit

**Date:** 2026-05-18
**Source:** `anix-lynch/healthcare-da` (last push 2026-04-21 — archived after this migration)
**Target:** `anix-lynch/healthcare-api` (active L1 substrate)
**Rationale:** Cherry-pick recruiter-safe portfolio artifacts from the
stale `healthcare-da` repo into the active L1 substrate, then archive
`healthcare-da` to stop drift. All migrated content was scrubbed for
showroom-rule violations (no "interview / SLA roles / headhunter"
framing in public-facing files).

---

## Bucket assignments

### KEEP + MIGRATE (showroom-scrubbed)

| Source (healthcare-da) | Target (healthcare-api) | Notes |
|---|---|---|
| `screenshots/*.png` (4 files) | `screenshots/` | API stats, FastAPI docs, Fabric workspace, Fabric Lakehouse |
| `SCREENSHOTS.md` | `docs/screenshots.md` | Dropped "Interview Talking Points" section; reframed "interview-ready" → "portfolio proof" |
| `openapi_snapshot.json` | `docs/openapi_snapshot.json` | OpenAPI 3.1 schema for the 11-endpoint Healthcare API |
| `fabric_April20.md` | `docs/fabric_strategy.md` | Dropped Upwork job links + trial-billing operator notes; kept the Fabric architecture pattern (Lakehouse → Data Factory → Warehouse → Direct Lake) |
| `fabric_april/outputs/01_screenshots/*.png` (4 files) | `screenshots/fabric_april/` | Real Fabric UI proof: Lakehouse explorer, Data Factory pipeline run, Warehouse SQL results, Power BI Direct Lake report |
| `fabric_april/outputs/02_exports/fabric_pipeline_definition.json` | `proof/fabric_pipeline_definition.json` | Real pipeline body (not placeholder) |
| `fabric_april/outputs/03_proof/*.txt` (4 files) | `proof/fabric_april/` | Text proof narratives for F1-F4 phases |
| `dbt-project/profiles.yml` | (local-only) | Env-var-driven, but `healthcare-api/.gitignore` intentionally excludes `profiles.yml`. File was copied for local dbt-fabric runs; NOT committed to public repo. Anyone reproducing the dbt build should create their own `profiles.yml` from the dbt-fabric template + their own env vars. |

### SCRUB (do NOT migrate — showroom-rule violation)

| Source | Reason |
|---|---|
| `headhunter_ready/` (full folder) | Directory name itself violates showroom rule. Contents (pitch, proof, visuals, resume_context) duplicate what is already in `screenshots/` + `outputs/` + the resume layer that lives outside this repo. |
| `sla` (symlink) + `sla.md` + `sla_all_roles.md` | Resume bullets + "4 resume variants" framing. Belongs to the candidate's resume layer, not the L1 substrate. |
| `SPEC.md` | Structurally about "P9 interview lock" + "4 resume variants" — scrubbing would gut the document. Build-process metadata, not L1 deliverable. |
| `DASHBOARD.md` | Phase tracker with "interview-ready" framing + reference to `sla`/`SPEC.md`. Short, redundant once SPEC is dropped. |
| `.instructions.md` | Spec-Kit prompt with internal lane jargon ("Bchan runs 4 lanes"). Not for public repo. |
| `fabric_april/SLA.md`, `DASHBOARD.md`, `HANDOFF.md`, `README.md`, `PERPLEXITY_SLA_BRIEF.md` | Operator chatter (b-turn, Perplexity copilot brief). Architecture story preserved in the scrubbed `docs/fabric_strategy.md` + the screenshots themselves. |

### IGNORE (scratch / regeneratable / IDE-local)

| Source | Reason |
|---|---|
| `inputs/` (4 subdirs) | Scratch input snapshots; regeneratable from the raw CSV already in `data/raw/`. |
| `outputs/` (6 subdirs) | Proof outputs already represented by the migrated `screenshots/`. The JSON/MD proof files are timestamped scratch. |
| `.specify/` | Spec-Kit framework metadata (memory/scripts/templates). Build-tool internals. |
| `.vscode/` | Local IDE config. |
| `.github/agents/`, `.github/prompts/` | Spec-Kit agent prompts; build-time only. |
| `scripts/*` (8 files: `populate_proof_artifacts.sh`, `render_proof_screenshots.py`, `check_p4_semantic_model.sh`, `create_powerbi_dashboard.sh`, `add_visuals_to_report.py`, `upload_bronze_to_onelake.py`, `push_gitlab_full_github_showcase.sh`, `README_POWERBI_CLI.md`) | Proof-generation + GitLab-push automation; mostly one-shot. `upload_bronze_to_onelake.py` is worth a glance if Fabric work resumes, but is not L1 substrate code. |
| `fabric_april/inputs/` | Scratch inputs. |

---

## Verification

- All KEEP migrations land under `docs/`, `screenshots/`, `proof/`, or `dbt-project/` in `healthcare-api`.
- No source file was copied verbatim if it contained showroom-violation
  wording; markdown files were rewritten before commit.
- `healthcare-da` archived on GitHub immediately after migration to
  freeze the source state and prevent recruiter confusion.

## Cross-refs

- Showroom rule: `~/dev/SHOWROOM_RULE.md` (root `## Content Policy` + `## Name Boundary`)
- L1 substrate intent: `~/.claude/skills/northstar1/SKILL.md` § 4
- Pre-migration archive snapshot: `https://github.com/anix-lynch/healthcare-da` (read-only after this audit)
