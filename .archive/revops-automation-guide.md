# RevOps Automation Guide: n8n, Make, HubSpot, Clay & More

## What RevOps Teams Actually Use

RevOps professionals care about **workflow automation**, **CRM orchestration**, and **data enrichment pipelines**. Here's what they want to see automated:

### Core RevOps Tools Stack

1. **Workflow Automation**
   - **n8n** - Self-hosted workflow automation (open source)
   - **Make (Integromat)** - Cloud workflow automation
   - **Zapier** - Simple workflow automation

2. **CRM & Sales**
   - **HubSpot** - CRM, marketing automation, sales
   - **Salesforce** - Enterprise CRM
   - **Pipedrive** - Sales CRM

3. **Data Enrichment**
   - **Clay** - AI-powered data enrichment & lead gen
   - **Apollo** - B2B contact database
   - **Clearbit** - Data enrichment API
   - **ZoomInfo** - B2B contact data

4. **Attribution & Analytics**
   - **Revenue.io** - Revenue attribution
   - **HubSpot Attribution** - Multi-touch attribution
   - **Segment** - Customer data platform

5. **Sales Enablement**
   - **Outreach** - Sales engagement
   - **Salesloft** - Sales engagement platform
   - **Gong** - Revenue intelligence

---

## RevOps Automation Opportunities

### ✅ **Fully Automatable (90-100%)**

#### 1. **Lead Enrichment Pipeline**
- **Tools:** Clay + HubSpot + n8n/Make
- **Automation:**
  - Auto-enrich leads from forms/imports
  - Company data lookup (revenue, employees, industry)
  - Contact data enrichment (email, phone, LinkedIn)
  - Technographic data (tech stack detection)
- **CLI/Cursor Approach:**
  ```bash
  # Enrich leads via Clay API
  python scripts/enrich_leads.py --source hubspot --enrichment clay,clearbit
  ```

#### 2. **Lead Scoring & Routing**
- **Tools:** HubSpot Workflows + n8n
- **Automation:**
  - Automated lead scoring based on behavior
  - Lead routing to correct sales rep
  - Territory assignment
  - Account-based routing
- **CLI/Cursor Approach:**
  ```bash
  # Update lead scores
  python scripts/update_lead_scores.py --source hubspot --rules config/scoring_rules.yaml
  ```

#### 3. **Data Sync & Hygiene**
- **Tools:** n8n + HubSpot + Salesforce
- **Automation:**
  - Bi-directional sync between systems
  - Duplicate detection & merging
  - Data validation & cleaning
  - Field mapping automation
- **CLI/Cursor Approach:**
  ```bash
  # Sync data between systems
  python scripts/sync_crm_data.py --source hubspot --target salesforce --mode bidirectional
  ```

#### 4. **Attribution Tracking**
- **Tools:** HubSpot + Segment + n8n
- **Automation:**
  - Multi-touch attribution calculation
  - Campaign performance tracking
  - Revenue attribution by channel
  - Automated reporting
- **CLI/Cursor Approach:**
  ```bash
  # Calculate attribution
  python scripts/calculate_attribution.py --model multi_touch --period 30d
  ```

#### 5. **Sales Activity Automation**
- **Tools:** Outreach/Salesloft + HubSpot + n8n
- **Automation:**
  - Automated sequence triggers
  - Email open/click tracking
  - Meeting booking automation
  - Follow-up task creation
- **CLI/Cursor Approach:**
  ```bash
  # Trigger sales sequences
  python scripts/trigger_sequences.py --platform outreach --trigger stage_change
  ```

### ⚠️ **Partially Automatable (50-70%)**

#### 6. **Account-Based Marketing (ABM)**
- **Automation Level:** 60%
- **What's Automated:**
  - Target account identification
  - Account scoring
  - Personalized content delivery
- **Human Input Needed:**
  - Strategic account selection
  - Custom messaging

#### 7. **Revenue Forecasting**
- **Automation Level:** 70%
- **What's Automated:**
  - Pipeline analysis
  - Win probability calculation
  - Forecast generation
- **Human Input Needed:**
  - Deal review & adjustments
  - Strategic input

---

## RevOps Automation Framework

### Architecture

```
┌─────────────────┐
│   Data Sources  │
│ (Forms, APIs,   │
│  Imports)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  n8n / Make     │ ◄── Workflow Orchestration
│  Workflows      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Clay / Clearbit│ ◄── Data Enrichment
│  Enrichment     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  HubSpot / SF   │ ◄── CRM Storage
│  CRM            │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Analytics &    │
│  Reporting      │
└─────────────────┘
```

### Key Workflows to Automate

1. **Lead Enrichment Workflow**
   - Trigger: New lead in HubSpot
   - Enrich with Clay (company data, technographics)
   - Enrich with Clearbit (contact data)
   - Update HubSpot with enriched data
   - Auto-assign lead score

2. **Attribution Workflow**
   - Track all touchpoints (email, ads, web)
   - Calculate multi-touch attribution
   - Update HubSpot deal with attribution data
   - Generate attribution reports

3. **Data Sync Workflow**
   - Monitor HubSpot for changes
   - Sync to Salesforce (or vice versa)
   - Handle conflicts & duplicates
   - Log sync activity

4. **Sales Sequence Workflow**
   - Trigger on lead stage change
   - Start Outreach/Salesloft sequence
   - Track engagement
   - Update HubSpot based on activity

---

## Tools Comparison: n8n vs Make vs Zapier

| Feature | n8n | Make | Zapier |
|---------|-----|------|--------|
| **Cost** | Free (self-hosted) | $9-299/mo | $20-599/mo |
| **Complexity** | High | Medium | Low |
| **API Access** | Full REST API | Limited | Limited |
| **CLI Support** | ✅ Yes | ❌ No | ❌ No |
| **Custom Nodes** | ✅ Yes | ⚠️ Limited | ❌ No |
| **Best For** | Technical teams | Business users | Non-technical |

**RevOps Recommendation:** **n8n** for technical teams (CLI-friendly, API-first), **Make** for business users.

---

## HubSpot Automation via CLI/API

### HubSpot API Capabilities

```python
# HubSpot API - Fully automatable via CLI
- Contacts API - CRUD operations
- Companies API - Account management
- Deals API - Pipeline management
- Engagements API - Activity tracking
- Workflows API - Automation triggers
- Properties API - Custom fields
- Lists API - Segmentation
- Analytics API - Reporting
```

### Example: Automated Lead Enrichment

```bash
# 1. Get new leads from HubSpot
python scripts/hubspot_get_leads.py --status new

# 2. Enrich with Clay
python scripts/clay_enrich.py --leads leads.json --output enriched.json

# 3. Update HubSpot with enriched data
python scripts/hubspot_update_leads.py --data enriched.json

# 4. Trigger workflow
python scripts/hubspot_trigger_workflow.py --workflow lead_enrichment_complete
```

---

## Clay Automation

Clay is **the** RevOps tool for data enrichment. It's API-first and CLI-friendly.

### Clay Use Cases

1. **Lead Enrichment**
   - Company data (revenue, employees, industry)
   - Contact data (email, phone, LinkedIn)
   - Technographic data (tech stack)

2. **Prospecting**
   - Find contacts at target companies
   - Email finding & verification
   - Social profile enrichment

3. **Data Enrichment Pipelines**
   - Bulk enrichment workflows
   - Real-time enrichment via API
   - Custom enrichment logic

### Clay + CLI Integration

```bash
# Enrich leads via Clay API
python scripts/clay_enrich.py \
  --input leads.csv \
  --enrichments company_data,contact_data,technographics \
  --output enriched_leads.csv

# Clay table operations
python scripts/clay_table.py \
  --action sync \
  --source hubspot \
  --target clay_table_id
```

---

## n8n Workflow Automation

n8n is **perfect** for RevOps because it's:
- Self-hosted (data stays in your control)
- API-first (CLI-friendly)
- Open source (customizable)
- Powerful (complex workflows)

### n8n + CLI Integration

```bash
# Create workflow via CLI
python scripts/n8n_create_workflow.py \
  --file workflows/lead_enrichment.json

# Trigger workflow
curl -X POST http://n8n.local:5678/webhook/lead-enrichment \
  -H "Content-Type: application/json" \
  -d '{"lead_id": "12345"}'

# Monitor workflow execution
python scripts/n8n_monitor.py --workflow lead_enrichment --status active
```

### Example n8n Workflow: Lead Enrichment

```json
{
  "name": "Lead Enrichment Pipeline",
  "nodes": [
    {
      "name": "HubSpot Trigger",
      "type": "n8n-nodes-base.hubspotTrigger",
      "parameters": {
        "event": "contact.created"
      }
    },
    {
      "name": "Clay Enrich",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.clay.com/v1/enrich",
        "method": "POST"
      }
    },
    {
      "name": "Update HubSpot",
      "type": "n8n-nodes-base.hubspot",
      "parameters": {
        "operation": "update",
        "resource": "contact"
      }
    }
  ]
}
```

---

## Make (Integromat) Automation

Make is great for business users but less CLI-friendly than n8n.

### Make Scenarios (Workflows)

- **Lead Enrichment:** HubSpot → Clay → HubSpot
- **Data Sync:** HubSpot ↔ Salesforce
- **Attribution:** Multiple sources → HubSpot Attribution
- **Sales Sequences:** HubSpot → Outreach → HubSpot

### Make + API Integration

```bash
# Trigger Make scenario via webhook
curl -X POST https://hook.integromat.com/your-scenario-id \
  -H "Content-Type: application/json" \
  -d '{"trigger": "new_lead", "data": {...}}'
```

---

## Complete RevOps Automation Stack

### Recommended Setup

1. **Workflow Engine:** n8n (self-hosted, CLI-friendly)
2. **CRM:** HubSpot (API-first, powerful)
3. **Data Enrichment:** Clay (best-in-class)
4. **Attribution:** HubSpot Attribution + custom scripts
5. **Sales Engagement:** Outreach/Salesloft (API integrations)

### Automation Coverage

| RevOps Task | Automation Level | Tools |
|-------------|------------------|-------|
| Lead Enrichment | 95% | Clay + HubSpot + n8n |
| Lead Scoring | 90% | HubSpot Workflows |
| Data Sync | 95% | n8n + HubSpot API |
| Attribution | 85% | HubSpot + Custom scripts |
| Sales Sequences | 90% | Outreach + HubSpot |
| Revenue Forecasting | 70% | HubSpot + Python |
| Account-Based Marketing | 60% | Clay + HubSpot + n8n |

---

## Time Savings

- **Manual RevOps:** ~15 hours/week
- **Automated RevOps:** ~3 hours/week
- **Savings:** 80% (624 hours/year)

---

## Getting Started

1. **Set up n8n** (self-hosted or cloud)
2. **Get HubSpot API key**
3. **Get Clay API key**
4. **Build workflows** (n8n or Make)
5. **Automate everything** via CLI/API

---

**Bottom Line:** RevOps teams want to see **n8n workflows**, **Clay enrichment**, **HubSpot automation**, and **API-first integrations**. This is 80-90% automatable with the right tools.




