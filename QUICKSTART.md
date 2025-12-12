# Healthcare Analytics - Quick Start

## ✅ What's Working Now

### 1. REST API
```bash
./scripts/start_api.sh
# → http://localhost:8000/docs
```

### 2. ML Model Training
```bash
source .venv/bin/activate
cd ml-pipeline/src
python train.py
# ✅ Successfully trained on 55,500 patients
# ✅ Accuracy: 66.41%, AUC: 0.51
```

### 3. View MLflow Results
```bash
source .venv/bin/activate
mlflow ui
# → http://localhost:5000
```

## ⏳ Waiting on Fabric

### Fix Fabric Capacity (5 min)
1. Go to: https://app.fabric.microsoft.com/groups/577de43f-21b4-479e-99b6-ea78f32e5216
2. Settings → Workspace settings → Premium
3. Assign Trial capacity
4. Create Warehouse: `HealthcareWarehouse`
5. Copy connection string

### Then Deploy dbt (5 min)
```bash
cd dbt-project
export FABRIC_SERVER="your-warehouse.datawarehouse.pbidedicated.windows.net"
export $(cat /Users/anixlynch/.config/secrets/fabric.env | xargs)
dbt run
dbt test
```

## 📚 Documentation
- `docs/BUILD_COMPLETE.md` - Full summary
- `docs/FABRIC_SETUP_FIX.md` - Capacity fix guide
- `docs/CURRENT_STATUS.md` - Detailed status

## 🎯 Status
- **Code:** 100% complete
- **Tested:** ML ✅, API ✅, dbt ⏳ (waiting on Fabric)
- **Deployed:** 50% (API + ML working, dbt + TMDL waiting on capacity)
