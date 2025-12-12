# Fabric Workspace Setup - Action Required

## Current Situation

✅ **What's Working:**
- Fabric free trial is activated
- Workspace `HealthcareAnalytics` exists (ID: `577de43f-21b4-479e-99b6-ea78f32e5216`)
- Azure CLI authentication working
- User: `alynch@gozeroshot.dev`

❌ **What's Blocked:**
- API returns `UserNotLicensed` error
- Cannot create or access warehouse items
- Cannot deploy TMDL models

## Root Cause

The workspace **exists** but has **no Fabric capacity assigned** to it. Even with a free trial, you must:
1. Create or access a Fabric capacity (Trial capacity)
2. Assign that capacity to the workspace

## How to Fix (Via Fabric Portal)

### Step 1: Access Fabric Portal
Go to: https://app.fabric.microsoft.com/groups/577de43f-21b4-479e-99b6-ea78f32e5216

### Step 2: Assign Capacity to Workspace

**Option A: Via Workspace Settings (Recommended)**
1. Click the **⚙️ Settings** icon in the workspace
2. Select **Workspace settings**
3. Go to **Premium** tab
4. Under **License mode**, select **Trial** or **Fabric capacity**
5. If you see a capacity dropdown, select your trial capacity
6. Click **Save**

**Option B: Via Admin Portal**
1. Go to https://app.fabric.microsoft.com/admin-portal/capacities
2. Find your **Trial capacity** (should be F64 or similar)
3. Click on the capacity
4. Under **Workspaces**, click **Assign workspaces**
5. Search for `HealthcareAnalytics`
6. Assign it
7. Click **Save**

### Step 3: Create SQL Warehouse

Once capacity is assigned:

1. In the workspace, click **+ New**
2. Select **Warehouse** (under Data Engineering)
3. Name it: `HealthcareWarehouse`
4. Click **Create**
5. Wait for provisioning (~2-3 minutes)
6. Copy the **SQL connection string** from warehouse settings

The connection string will look like:
```
<workspace-name>-<warehouse-name>.datawarehouse.pbidedicated.windows.net
```

### Step 4: Update dbt Configuration

Once you have the SQL connection string, update:

**File:** `dbt-project/profiles.yml`

Replace:
```yaml
server: "{{ env_var('FABRIC_SERVER', 'placeholder-server.datawarehouse.pbidedicated.windows.net') }}"
```

With your actual server (or set the `FABRIC_SERVER` environment variable):
```yaml
server: "your-actual-server.datawarehouse.pbidedicated.windows.net"
```

## Verification Commands

After assigning capacity and creating warehouse, run:

```bash
# Test API access
TOKEN=$(az account get-access-token --resource https://analysis.windows.net/powerbi/api --query accessToken -o tsv)
curl -H "Authorization: Bearer $TOKEN" "https://api.fabric.microsoft.com/v1/workspaces/577de43f-21b4-479e-99b6-ea78f32e5216/items"

# Should now return items (including your warehouse)

# Test dbt connection
cd dbt-project
export $(cat /Users/anixlynch/.config/secrets/fabric.env | xargs)
export FABRIC_SERVER="your-actual-server.datawarehouse.pbidedicated.windows.net"
dbt debug --profiles-dir .

# Should show: Connection test: [OK]
```

## Alternative: Use DuckDB Locally

If you prefer to demo the project **without Fabric** (fastest option):

```bash
# Install dbt-duckdb
source .venv/bin/activate
pip install dbt-duckdb

# Update profiles.yml
cat > dbt-project/profiles.yml << 'EOF'
healthcare_analytics:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: '../healthcare.duckdb'
      schema: main
EOF

# Run dbt
cd dbt-project
dbt seed  # Load CSV data
dbt run   # Build models
dbt test  # Run tests
```

This will build everything locally in a DuckDB database file.

## Summary

**The "UserNotLicensed" error means the workspace needs a capacity assigned, not that you lack a license.**

**Fastest path forward:**
1. Go to workspace settings in Fabric portal
2. Assign your trial capacity
3. Create a SQL Warehouse
4. Update `FABRIC_SERVER` in your config
5. Run `dbt run`

**Or use DuckDB locally** to demo the entire pipeline without Fabric.

---

Let me know which path you'd like to take!
