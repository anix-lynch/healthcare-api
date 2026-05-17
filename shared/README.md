# Layer 2 — Shared GenAI Patterns

> Seven brutal questions. Seven structured answers. One contract per pattern.

This folder is a standalone mirror of the `layer2-ai-application/shared/` slice
of [healthcare-genai-fullstack](https://github.com/anix-lynch/healthcare-genai-fullstack)
so the patterns are browseable without cloning the full monorepo.

---

## The 7 patterns

```
🔍 retrieval         (Rachel)         "what reminds me of?"
🚦 classify           (Traffic Light)  "how urgently should we panic?"
🔮 regress            (Crystal Ball)   "how bad will this become later?"
📖 generate           (Mad Lib)        "explain to humans"
🚨 anomaly            (Smoke Detector) "this case smells WRONG"
🗺️ cluster            (Treasure Map)   "what suffering tribe is this?"
👮 rank               (Police Lineup)  "which evidence should appear first?"
```

Each pattern folder has the same scaffold shape:

```
schema.py          Pydantic output contract (what every caller gets back)
baseline.py        honest orchestrator wrapping the engine into the contract
<engine>.py        the actual implementation (BM25 / cohort / k-means / etc.)
leakage_checks.py  (where applicable) fail-loud guard on future-data leakage
guardrails.py      (Rachel only) citation + cross-patient leak + score floor
eval.py            (where applicable) pattern-appropriate metric harness
README.md          tone + healthcare meaning + roadmap + sample output
__init__.py        public API
```

---

## What each pattern returns

```
🔍 Rachel        → RachelOutput          retrieved: list[Hit] with similarity + why_relevant
🚦 Traffic Light → TrafficLightOutput     tier (NOW/SOON/WAIT) + esi_tier 1-5 + escalate + red_flags
🔮 Crystal Ball  → CrystalBallOutput      LoS + readmission risk + mortality indicator + confidence
📖 Mad Lib       → MadLibOutput           chart_note + nurse_handoff + patient_explanation + citations
🚨 Smoke Detector → SmokeDetectorOutput   is_anomaly + score + outlier_reasons + clinical_review flag
🗺️ Treasure Map  → TreasureMapOutput      cluster_id + cluster_label + silhouette + neighbors
👮 Police Lineup → PoliceLineupOutput     ranked: list[RankedHit] with rerank_score + severity_signals
```

---

## Status snapshot (honest, not aspirational)

```
PATTERN          ENGINE                       SCHEMA  BASELINE  EVAL  GUARDS  README
─────────────────────────────────────────────────────────────────────────────────────
🔍 Rachel        BM25 + dense + identity     ✅      ✅        ✅    ✅      ✅
🚦 Traffic Light rule-based + LLM tier-router ✅      ✅        ✅    ✅      ✅
🔮 Crystal Ball  cohort + heuristics +        ✅      ✅        ✅    ✅      ✅
                 LightGBM (scaffold)
📖 Mad Lib        template + citation gate    ✅      ✅        —     —       ✅
🚨 Smoke Detector cohort z-score + rules       ✅      ✅        —     —       ✅
🗺️ Treasure Map   k-means + silhouette          ✅      ✅        —     —       ✅
👮 Police Lineup  heuristic rerank             ✅      ✅        —     —       ✅
```

`—` = uses shared/evaluation/ harness instead of pattern-local eval.py;
guardrails for non-retrieval patterns live in the central `guardrails/` folder.

---

## Cross-cutting

```
guardrails/         input + output runtime safety (PII redact, hallucination, citation, Llama Guard)
evaluation/         per-pattern eval functions used by Layer 3 governance baselines
```

---

## End-to-end (one ER case → 7 structured answers)

```python
case = {"cc": "chest pain", "hpi": "62yo M substernal pressure + diaphoresis + jaw radiation",
        "arrival": "ambulance",
        "vitals": {"bp_sys": 95, "hr": 122, "rr": 24, "spo2": 92, "temp_f": 99.1}}

from shared.retrieval  import retrieve
from shared.classify   import triage
from shared.regress    import predict_prognosis
from shared.generate   import generate_note
from shared.anomaly    import detect_smoke
from shared.cluster    import assign_cluster
from shared.rank       import lineup

rachel = retrieve("62yo M chest pain hypertension", query_case_id="CASE-104", k=10)
tl     = triage(case, case_id="CASE-104")
cb     = predict_prognosis(case, case_id="CASE-104", prior_visits=2)
ml     = generate_note(case, tl.model_dump(), case_id="CASE-104",
                       rachel_hits=[h.model_dump() for h in rachel.retrieved])
sd     = detect_smoke(case, case_id="CASE-104")
tm     = assign_cluster({"Medical Condition": "Hypertension", "Age": "62",
                         "Admission Type": "Emergency"}, case_id="CASE-104")
pl     = lineup("62yo M chest pain", [h.model_dump() for h in rachel.retrieved],
                case_id="CASE-104", top_k=3)
```

Verified end-to-end against the enriched 497-row corpus in
`data/raw/healthcare_dataset_enriched.csv`.

---

## Honest scope

```
✅ all 7 patterns scaffolded with Pydantic contracts
✅ leakage guards on classify + regress (label/future-knowledge protection)
✅ Rachel citation + cross-patient + score-floor guardrails
✅ identity bridge to Layer 1 patient_identity_map.json
✅ smoke-test pipeline runs end-to-end on holdout
❌ NOT a production hospital AI system
❌ NOT FDA-approved
❌ NOT clinically validated
❌ confidence caps stay LOW until L1 grows real telemetry
   (see ../L1_HARDENING.md for the L1 → L2 ceiling story)
```

---

## Cross-references

- L1 contract this layer consumes: `../dbt-project/models/staging/stg_healthcare.sql`
- L1 quality gate: `../scripts/checkpoint.py`
- L1 hardening roadmap: `../L1_HARDENING.md`
- Full 3-layer monorepo: https://github.com/anix-lynch/healthcare-genai-fullstack
