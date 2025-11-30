# Instructions for Kilo Code

## ✅ Setup Status

### Healthcare API
- **GitHub Repository:** https://github.com/anix-lynch/healthcare-api
- **Status:** ✅ Deployed and ready
- **Endpoints:** `/api/encounters`, `/api/patients`, `/api/doctors`, `/api/hospitals`, `/api/stats`, etc.
- **Documentation:** See `api/README.md` in this project
- **Usage:** All 3 projects (dbt, Power BI, ML) can consume data from the API instead of CSV

### Microsoft Fabric
- **Workspace:** HealthcareAnalytics ✅
- **Workspace ID:** `577de43f-21b4-479e-99b6-ea78f32e5216`
- **URL:** https://app.fabric.microsoft.com/groups/577de43f-21b4-479e-99b6-ea78f32e5216
- **Credentials:** `~/.config/secrets/fabric.env`
- **Access:** Azure CLI authentication working
- **Note:** No official Fabric MCP server - use REST API with Azure CLI tokens

---

## 🎯 Mission

Build a production-grade Healthcare Analytics Platform using **ONE unified dataset** as the foundation for all 3 projects:

**Dataset Options:**
1. **Local CSV:** `/Users/anixlynch/dev/healthcare-analytics/data/raw/healthcare_dataset.csv`
2. **REST API (Recommended):** Healthcare API is deployed on GitHub at `https://github.com/anix-lynch/healthcare-api`
   - API endpoints: `/api/encounters`, `/api/patients`, `/api/stats`, etc.
   - No authentication required
   - Perfect for dbt, Power BI, and ML pipelines
   - See `api/README.md` for full documentation

---

## 📋 Project Overview

### Project 1: Data Warehouse (dbt + Fabric SQL)
- Transform 55,500 patient records into star schema
- 1 fact table + 8 dimension tables
- Staging → Intermediate → Marts pipeline
- 15+ data quality tests
- **Timeline:** Weeks 1-2

### Project 2: Semantic Model (TMDL + DAX)
- Code-first Power BI model
- Advanced DAX measures (30-day readmission rate, ALOS, cost per day)
- Calculation groups for time intelligence
- Row-Level Security for HIPAA
- **Timeline:** Weeks 3-4

### Project 3: ML Pipeline (Python + MLflow)
- XGBoost readmission risk predictor
- Feature engineering from warehouse
- MLflow experiment tracking
- REST API deployment
- **Timeline:** Weeks 5-7

---

## 🏗️ Architecture Reference

**Read these files first:**
1. `UNIFIED_ARCHITECTURE.md` - Complete technical spec
2. `PROJECT_SPEC.md` - Original project requirements

**Key Design Principles:**
- **Single source of truth:** Healthcare API (deployed on GitHub: https://github.com/anix-lynch/healthcare-api)
- **Alternative:** Local CSV at `data/raw/healthcare_dataset.csv`
- Reusable features for all ML models
- Extensible for future AI (embeddings, RAG, knowledge graphs)
- 100% CLI/API - zero GUI

**Important:** The Healthcare REST API is available on GitHub and can be used by all 3 projects (dbt, Power BI, ML) instead of parsing CSV files. See `api/README.md` for API documentation.

---

## 🚀 Phase 1: Data Warehouse (START HERE)

### Step 1: Fabric Workspace Setup ✅ COMPLETE!

**Fabric Workspace Already Configured:**
- **Workspace Name:** HealthcareAnalytics
- **Workspace ID:** `577de43f-21b4-479e-99b6-ea78f32e5216`
- **URL:** https://app.fabric.microsoft.com/groups/577de43f-21b4-479e-99b6-ea78f32e5216
- **Credentials:** Saved in `~/.config/secrets/fabric.env`

**Access Fabric via:**
- **Azure CLI:** `az account get-access-token --resource https://analysis.windows.net/powerbi/api`
- **REST API Helper:** `./scripts/fabric_api_helper.sh list_workspaces`
- **Direct API:** Use workspace ID in all Fabric API calls

**Note:** No official Fabric MCP server exists yet, but you can use REST API calls with Azure CLI authentication for all operations.

### Step 2: Create dbt Project

```bash
cd /Users/anixlynch/dev/healthcare-analytics
mkdir dbt-project && cd dbt-project
dbt init healthcare_analytics
```

**Project Location:** `/Users/anixlynch/dev/healthcare-analytics/`

**Configure `profiles.yml` for Fabric:**
```yaml
healthcare_analytics:
  target: dev
  outputs:
    dev:
      type: fabric
      driver: ODBC Driver 18 for SQL Server
      server: <fabric-sql-endpoint>
      database: healthcare_dw
      schema: dbt_dev
      authentication: CLI
      threads: 4
```

### Step 3: Build Staging Models

**File:** `models/staging/stg_healthcare.sql`

**Data Source Options:**

**Option A: Use Healthcare API (Recommended)**
- API URL: `http://localhost:8000/api/encounters?limit=55500` (if running locally)
- Or use GitHub API when deployed
- Fetch via Python/pandas in dbt, or use external table connector

**Option B: Use Local CSV**
- File: `data/raw/healthcare_dataset.csv`
- Direct file read in dbt

**Requirements:**
- Clean column names (remove spaces, standardize)
- Type cast dates (Date of Admission, Discharge Date)
- Generate surrogate key: `encounter_id = hash(Name + Date of Admission)`
- Hash PII: `patient_name_hash = SHA256(Name)`
- No business logic yet!

**Validation:**
- `dbt run --models stg_healthcare`
- Expect 55,500 rows

### Step 4: Build Intermediate Models

**File:** `models/intermediate/int_encounters_enriched.sql`

**Requirements:**
- Calculate `length_of_stay_days = discharge_date - admission_date`
- Calculate `cost_per_day = billing_amount / length_of_stay_days`
- Flag `is_emergency = (admission_type = 'Emergency')`
- Derive `age_group` (0-17, 18-30, 31-50, 51-70, 70+)
- Derive `season` from admission date

**File:** `models/intermediate/int_readmissions.sql`

**Requirements:**
- Window function: `LAG(admission_date) OVER (PARTITION BY patient_name_hash ORDER BY admission_date)`
- Calculate `days_since_last_admission`
- Flag `is_readmission = (days_since_last_admission <= 30)`
- Calculate `previous_admission_count` per patient

### Step 5: Build Dimension Tables

**Files:**
- `models/marts/core/dim_patient.sql`
- `models/marts/core/dim_date.sql` (use dbt_utils date spine)
- `models/marts/core/dim_doctor.sql`
- `models/marts/core/dim_hospital.sql`
- `models/marts/core/dim_diagnosis.sql`
- `models/marts/core/dim_medication.sql`
- `models/marts/core/dim_insurance.sql`

**Key Requirements:**
- Each dimension has surrogate key (`*_key`)
- `dim_patient`: Type 2 SCD (track changes over time)
- `dim_date`: Standard date dimension (365 days × 6 years = 2,190 rows)
- Denormalize aggregates (e.g., `doctor_avg_los`, `hospital_bed_count`)

### Step 6: Build Fact Table

**File:** `models/marts/core/fact_patient_encounters.sql`

**Requirements:**
- Grain: 1 row per patient encounter
- All foreign keys to dimensions
- All measures (billing_amount, length_of_stay_days, cost_per_day)
- All flags (is_emergency, is_readmission)
- Incremental materialization (for performance)

**Validation:**
- `dbt run --models fact_patient_encounters`
- Expect 55,500 rows
- All FK relationships valid

### Step 7: Add Data Quality Tests

**File:** `models/schema.yml`

**Required Tests:**
```yaml
models:
  - name: fact_patient_encounters
    columns:
      - name: encounter_key
        tests:
          - unique
          - not_null
      - name: patient_key
        tests:
          - not_null
          - relationships:
              to: ref('dim_patient')
              field: patient_key
      - name: length_of_stay_days
        tests:
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 365
      - name: billing_amount
        tests:
          - not_null
```

**Custom Tests:**
- `tests/assert_discharge_after_admission.sql`
- `tests/assert_no_negative_los.sql`
- `tests/assert_valid_readmission_logic.sql`

**Validation:**
- `dbt test`
- Expect 0 failures

### Step 8: Generate Documentation

```bash
dbt docs generate
dbt docs serve
```

**Deliverables:**
- Star schema ERD (export as PNG)
- Data lineage graph
- Column-level documentation

---

## 🎯 Phase 2: Semantic Model (After dbt Complete)

### Step 1: Create TMDL Structure

```bash
cd /Users/anixlynch/dev/serpAPI/healthcare-analytics
mkdir powerbi-model
cd powerbi-model
```

**Create base `model.bim` file:**
- Connect to Fabric SQL Warehouse
- Import all tables from `dbt_dev` schema
- Define relationships

### Step 2: Define Relationships

**File:** `relationships.tmdl`

**Required Relationships:**
- `fact_patient_encounters[patient_key]` → `dim_patient[patient_key]` (Many-to-One)
- `fact_patient_encounters[admission_date_key]` → `dim_date[date_key]` (Many-to-One, ACTIVE)
- `fact_patient_encounters[discharge_date_key]` → `dim_date[date_key]` (Many-to-One, INACTIVE)
- `fact_patient_encounters[doctor_key]` → `dim_doctor[doctor_key]` (Many-to-One)
- `fact_patient_encounters[hospital_key]` → `dim_hospital[hospital_key]` (Many-to-One)
- `fact_patient_encounters[diagnosis_key]` → `dim_diagnosis[diagnosis_key]` (Many-to-One)
- `fact_patient_encounters[medication_key]` → `dim_medication[medication_key]` (Many-to-One)
- `fact_patient_encounters[insurance_key]` → `dim_insurance[insurance_key]` (Many-to-One)

### Step 3: Create DAX Measures

**File:** `measures/clinical_metrics.tmdl`

**Required Measures:**
```dax
// Core Metrics
Total Encounters = COUNT(fact_patient_encounters[encounter_key])
Total Patients = DISTINCTCOUNT(fact_patient_encounters[patient_key])
Avg Length of Stay = AVERAGE(fact_patient_encounters[length_of_stay_days])
Total Billing = SUM(fact_patient_encounters[billing_amount])

// Clinical KPIs
Readmission Rate 30d = 
DIVIDE(
    CALCULATE([Total Encounters], fact_patient_encounters[is_readmission] = TRUE),
    [Total Encounters]
)

Emergency Admission Rate = 
DIVIDE(
    CALCULATE([Total Encounters], fact_patient_encounters[is_emergency] = TRUE),
    [Total Encounters]
)

// Financial KPIs
Cost per Patient Day = DIVIDE([Total Billing], SUM(fact_patient_encounters[length_of_stay_days]))
Avg Cost per Encounter = DIVIDE([Total Billing], [Total Encounters])

// Operational KPIs
Bed Occupancy % = 
VAR TotalBedDays = SUM(dim_hospital[bed_count]) * [Days in Period]
VAR OccupiedBedDays = SUM(fact_patient_encounters[length_of_stay_days])
RETURN DIVIDE(OccupiedBedDays, TotalBedDays)
```

### Step 4: Create Calculation Groups

**File:** `calculation_groups/time_intelligence.tmdl`

**Required Calculation Items:**
- Current Period
- Prior Period
- Year to Date
- Prior Year to Date
- YoY % Change
- MoM % Change

### Step 5: Implement RLS

**File:** `roles.tmdl`

**Required Roles:**
```dax
// Doctor Role - can only see their own patients
Role: Doctor
Table: fact_patient_encounters
Filter: [doctor_key] = LOOKUPVALUE(dim_doctor[doctor_key], dim_doctor[doctor_name], USERNAME())

// Hospital Admin Role - can only see their facility
Role: HospitalAdmin
Table: fact_patient_encounters
Filter: [hospital_key] IN VALUES(user_hospital_access[hospital_key])
```

### Step 6: Deploy to Fabric

```bash
# Use Fabric API to deploy TMDL
curl -X POST https://api.fabric.microsoft.com/v1/workspaces/$WORKSPACE_ID/semanticModels \
  -H "Authorization: Bearer $TOKEN" \
  -F "model=@model.bim"
```

---

## 🎯 Phase 3: ML Pipeline (After Semantic Model Complete)

### Step 1: Feature Engineering

**File:** `ml-pipeline/features/patient_features.py`

**Requirements:**
- Extract features from `fact_patient_encounters` table
- Demographic features: age, gender, blood_type
- Clinical features: medical_condition, medication, test_result, previous_admission_count
- Operational features: admission_type, length_of_stay_days, season
- Financial features: billing_amount, insurance_type
- One-hot encode categorical variables
- Scale numeric features

### Step 2: Train Model

**File:** `ml-pipeline/notebooks/03_model_training.ipynb`

**Requirements:**
- Load features from warehouse
- Split: 70% train, 15% validation, 15% test
- Handle class imbalance (SMOTE or class_weight)
- Train XGBoost classifier
- Hyperparameter tuning (GridSearchCV or Optuna)
- Log everything to MLflow

**Target Metrics:**
- AUC-ROC > 0.85
- Precision @ 80% Recall > 0.70
- F1 Score > 0.75

### Step 3: Model Evaluation

**File:** `ml-pipeline/notebooks/04_model_evaluation.ipynb`

**Requirements:**
- Confusion matrix
- ROC curve
- Precision-Recall curve
- Feature importance (SHAP values)
- Calibration plot
- Business impact calculation ($8.3M savings)

### Step 4: Deploy Model

**File:** `ml-pipeline/src/deploy.py`

**Requirements:**
- Register model in MLflow Model Registry
- Tag as "production"
- Deploy to Fabric ML endpoint
- Create REST API wrapper
- Test endpoint with sample data

### Step 5: Batch Scoring

**File:** `ml-pipeline/notebooks/05_batch_scoring.ipynb`

**Requirements:**
- Score all recent discharges (last 7 days)
- Write predictions back to warehouse
- Create alert for high-risk patients (score > 0.7)
- Schedule daily run

---

## 📊 Deliverables Checklist

### dbt Project
- [ ] All models build successfully (`dbt run`)
- [ ] All tests pass (`dbt test`)
- [ ] Documentation generated (`dbt docs generate`)
- [ ] ERD diagram exported
- [ ] Data lineage graph exported

### TMDL Project
- [ ] Model deploys to Fabric
- [ ] All DAX measures calculate correctly
- [ ] Calculation groups work
- [ ] RLS tested and validated
- [ ] Relationships diagram exported

### ML Project
- [ ] Model achieves AUC-ROC > 0.85
- [ ] MLflow experiments tracked
- [ ] Model deployed to Fabric
- [ ] REST API functional
- [ ] Batch scoring pipeline working

### Documentation
- [ ] GitHub README with screenshots
- [ ] BUSINESS_IMPACT.md with ROI calculation
- [ ] HIPAA_COMPLIANCE.md with security notes
- [ ] API_DOCUMENTATION.md with endpoints

---

## 🚀 CLI Commands Reference

### dbt
```bash
# Run all models
dbt run

# Run specific model
dbt run --models stg_healthcare

# Run tests
dbt test

# Generate docs
dbt docs generate && dbt docs serve

# Compile SQL (debug)
dbt compile --models fact_patient_encounters
```

### Fabric API
```bash
# Get access token
TOKEN=$(az account get-access-token --resource https://analysis.windows.net/powerbi/api --query accessToken -o tsv)

# List workspaces
curl -H "Authorization: Bearer $TOKEN" https://api.powerbi.com/v1.0/myorg/groups

# Deploy TMDL
curl -X POST https://api.fabric.microsoft.com/v1/workspaces/$WORKSPACE_ID/semanticModels \
  -H "Authorization: Bearer $TOKEN" \
  -F "model=@model.bim"
```

### MLflow
```bash
# Start MLflow UI
mlflow ui --port 5000

# Log experiment
mlflow run . --experiment-name readmission_prediction

# Register model
mlflow models register --model-uri runs:/<run_id>/model --name readmission_predictor

# Serve model
mlflow models serve --model-uri models:/readmission_predictor/production --port 8080
```

---

## 🎯 Success Criteria

**Technical:**
- ✅ All dbt models build (0 errors)
- ✅ All dbt tests pass (0 failures)
- ✅ TMDL deploys to Fabric (0 errors)
- ✅ ML model AUC-ROC > 0.85
- ✅ API latency < 200ms

**Business:**
- ✅ Readmission rate calculated correctly
- ✅ Cost savings quantified ($8.3M)
- ✅ ROI calculated (740%)

**Portfolio:**
- ✅ GitHub repo polished
- ✅ README has screenshots
- ✅ Blog post written
- ✅ LinkedIn post published
- ✅ Resume updated with metrics

---

## 🔥 Key Principles

1. **Single Source of Truth:** Use Healthcare API (GitHub: https://github.com/anix-lynch/healthcare-api) or local CSV
2. **CLI Only:** No GUI clicking - all via CLI/API
3. **Reusable Features:** Build once, use everywhere
4. **Future-Proof:** Design for AI/RAG extensions
5. **Business Impact:** Always quantify ROI
6. **Fabric Ready:** Workspace ID `577de43f-21b4-479e-99b6-ea78f32e5216` is configured

---

## 📞 When Stuck

**Check these files:**
1. `UNIFIED_ARCHITECTURE.md` - Complete technical spec
2. `PROJECT_SPEC.md` - Original requirements
3. dbt docs: https://docs.getdbt.com
4. Fabric API docs: https://learn.microsoft.com/fabric
5. MLflow docs: https://mlflow.org/docs/latest

**Common Issues:**
- Fabric connection: Check `profiles.yml` and token
- dbt tests failing: Check `schema.yml` and custom tests
- ML model underperforming: Check class imbalance, feature engineering
- TMDL deployment error: Validate relationships, check DAX syntax

---

---

## 🚀 Quick Start Summary

**You have everything you need:**

1. ✅ **Healthcare API** - Deployed on GitHub (https://github.com/anix-lynch/healthcare-api)
   - Use API endpoints instead of CSV parsing
   - All endpoints documented in `api/README.md`

2. ✅ **Fabric Workspace** - HealthcareAnalytics (ID: `577de43f-21b4-479e-99b6-ea78f32e5216`)
   - Ready for dbt, TMDL, and ML deployment
   - Access via Azure CLI: `az account get-access-token --resource https://analysis.windows.net/powerbi/api`

3. ✅ **Dataset** - 55,500 patient encounters
   - Available via API or local CSV: `data/raw/healthcare_dataset.csv`

**Start with Phase 1 (Data Warehouse) and work 100% CLI/API!**

**LET'S BUILD! 🚀**

