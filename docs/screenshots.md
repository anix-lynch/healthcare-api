# Healthcare API — Visual Proof Screenshots

**Purpose:** Visual evidence for each portfolio claim in this repo.

**How these files are produced:** the API + dbt-fabric + ML pipeline are
re-runnable end-to-end; PNGs in `screenshots/` were captured from the
live Swagger UI, the live API stats response, and the Microsoft Fabric
workspace running the dbt-fabric build.

---

## 1. 55,500 Encounters + 6 Clinical Conditions

**Claim:** "End-to-end healthcare analytics workflow on 55,500 synthetic encounters across 6 clinical conditions."

**Screenshot:** [`screenshots/healthcare-da-api-stats.png`](../screenshots/healthcare-da-api-stats.png)

**Shows:**
- `total_encounters: 55500`
- 6 conditions in `clinical_conditions`: Arthritis (9308), Diabetes (9304), Hypertension (9245), Obesity (9231), Cancer (9227), Asthma (9185)

---

## 2. 11 GET Endpoints

**Claim:** "Productized data access with a FastAPI service exposing 11 GET endpoints."

**Screenshot:** [`screenshots/healthcare-da-fastapi-docs.png`](../screenshots/healthcare-da-fastapi-docs.png)

**Shows:** All 11 endpoints in Swagger UI:
1. `/` (root)
2. `/api/encounters`
3. `/api/encounters/{encounter_id}`
4. `/api/patients`
5. `/api/doctors`
6. `/api/hospitals`
7. `/api/conditions`
8. `/api/medications`
9. `/api/insurance`
10. `/api/stats`
11. `/api/search`

---

## 3. dbt Star Schema + 8 Marts + 3 Tests

**Claim:** "dbt star-schema warehouse with 8 core mart models plus 3 custom SQL quality checks."

**Reproduce locally:**

```bash
cd dbt-project && source ../.venv/bin/activate && dbt run --select fact_patient_encounters
# Expected: 1 of 1 OK created sql view model dbo.fact_patient_encounters
```

`fact_patient_encounters` builds in ~1s on Fabric Warehouse; 8 mart
models live in `dbt-project/models/marts/core/*.sql`, 3 quality tests
in `dbt-project/tests/`.

---

## 4. Power BI Semantic Model (TMDL) + Microsoft Fabric

**Claim:** "Code-first Power BI semantic model (TMDL/DAX) with table definitions, relationships, and reporting measures."

**Screenshots:**
- [`screenshots/healthcare-da-fabric-workspace.png`](../screenshots/healthcare-da-fabric-workspace.png) — Fabric workspace with Lakehouse
- [`screenshots/healthcare-da-fabric-lakehouse.png`](../screenshots/healthcare-da-fabric-lakehouse.png) — Lakehouse with `healthcare_encounters` table

**Source:**
- TMDL: [`powerbi-model/model.tmdl`](../powerbi-model/model.tmdl), [`powerbi-model/relationships.tmdl`](../powerbi-model/relationships.tmdl)

**Shows:**
- Lakehouse `HealthcareAnalytics` created via API
- Table `healthcare_encounters` (1,000 records, Delta format)
- Service principal authentication working

---

## 5. End-to-end Fabric Medallion (Lakehouse → Pipeline → Warehouse → Direct Lake)

See [`screenshots/fabric_april/`](../screenshots/fabric_april/) for the
four-phase Fabric proof:

| Phase | Screenshot | Narrative |
|---|---|---|
| F1 Lakehouse bronze | `lakehouse_files_explorer.png` | [`proof/fabric_april/bronze_onelake_upload.txt`](../proof/fabric_april/bronze_onelake_upload.txt) |
| F2 Data Factory pipeline | `data_factory_pipeline_run.png` | [`proof/fabric_april/f2_pipeline_run.txt`](../proof/fabric_april/f2_pipeline_run.txt) |
| F3 Warehouse SQL | `warehouse_sql_results.png` | [`proof/fabric_april/f3_warehouse_sql.txt`](../proof/fabric_april/f3_warehouse_sql.txt) |
| F4 Power BI Direct Lake | `powerbi_directlake_report.png` | [`proof/fabric_april/f4_directlake_report.txt`](../proof/fabric_april/f4_directlake_report.txt) |

---

## 6. XGBoost + MLflow

**Claim:** "XGBoost-based readmission model with MLflow metric logging."

**Reproduce locally:**

```bash
cd ml-pipeline/src && python3 train.py
# Expected: Model training complete; model saved to MLflow
```

Run output (synthetic data — values are illustrative, not clinical claims):

- Accuracy: 0.6641
- AUC-ROC: 0.5097
- Dataset: 55,500 records (44,400 train / 11,100 test)
- Top features: Gender (0.1504), Blood Type (0.1421), Billing Amount (0.1345)

---

## Notes on the data

The underlying dataset is **synthetic** (Kaggle-style patient encounter
generator). Use "synthetic" or "simulated" framing explicitly — these
are not real patient records and no clinical or cost-savings claims
should be derived from the model output.
