# Microsoft Fabric strategy — end-to-end medallion on this L1 substrate

This doc explains the **Fabric build pattern** used in this repo:
Lakehouse → Data Factory pipeline → Warehouse SQL → Power BI Direct
Lake. The pattern is intentionally minimal so it ports cleanly to any
healthcare analytics workload and is a faithful match for what most
real Fabric engagements ask for.

---

## Repo snapshot

Already in this repo:

- `api/` — FastAPI service over the 55,500-row dataset
- `dbt-project/` — transformation logic targeting Fabric Warehouse
- `ml-pipeline/` — XGBoost + MLflow
- `powerbi-model/` — TMDL semantic model
- `data/raw/` — raw healthcare CSV

What this doc adds: a visible **Fabric** wiring story, so the same
business logic that runs locally also runs (and is screenshotted) in
a real Fabric workspace.

---

## Wire-up sequence

```
data/raw/healthcare_dataset.csv
        │
        ▼
Fabric Lakehouse (bronze)         ← OneLake upload
        │
        ▼
Data Factory pipeline             ← bronze → silver → gold (medallion)
        │
        ▼
Fabric Warehouse (SQL endpoint)   ← T-SQL queryable
        │
        ▼
Power BI report (Direct Lake)     ← semantic model bound to Lakehouse
```

## Free Fabric features used

### Priority 1 — minimum viable buyer-visible proof

1. **Lakehouse** — load raw CSVs (bronze); every Fabric job asks for this.
2. **Data Factory pipeline** — bronze → silver → gold medallion flow.
3. **Warehouse / SQL endpoint** — T-SQL for reporting (pairs with Lakehouse).
4. **Power BI Direct Lake** — semantic model → Lakehouse in Direct Lake mode (strong differentiator vs Import mode).

### Priority 2 — nice-to-have

- **Notebooks (PySpark)** — bring the MLflow story into Fabric where relevant.
- **Dataflows Gen2** — simpler ETL alternative to ADF for smaller demos.

### Skip

- Eventstreams / KQL (real-time — burns capacity for a demo).
- Fabric Copilot at scale (needs higher SKU).

---

## Execution order

Workspace: `HealthcareAnalytics`.

1. Create **Lakehouse** in the workspace.
2. Load **healthcare raw** data (bronze) — see `scripts/upload_bronze_to_onelake.py` pattern (referenced from `proof/fabric_april/bronze_onelake_upload.txt`).
3. Build **pipeline** (medallion path: bronze → silver → gold).
4. Connect **Power BI** to semantic model in **Direct Lake** mode against the Lakehouse / Warehouse.

Each step has a screenshot in `screenshots/fabric_april/` and a
narrative proof file in `proof/fabric_april/`.

---

## Why Direct Lake over Import

Direct Lake means the Power BI report reads Parquet files in the
Lakehouse **without** importing them into the dataset cache. Refreshes
are effectively instant; the storage footprint is the Lakehouse, not a
duplicated PBIX. For a buyer who already runs on Fabric, this is the
modern default and removes a whole class of refresh-failure incidents.

---

## See also

- `docs/screenshots.md` — visual proof index for the four-phase Fabric build
- `proof/fabric_april/` — narrative proof texts for each phase
- `dbt-project/profiles.yml` — dbt-fabric connection (env-var driven)
