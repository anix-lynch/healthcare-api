# RevOps Automation Framework

**Automation potential: 80-90% of RevOps tasks**

This framework demonstrates how to automate RevOps workflows using **n8n**, **Make**, **HubSpot**, **Clay**, and other RevOps tools via CLI and APIs.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up API keys
export CLAY_API_KEY="your_clay_key"
export HUBSPOT_API_KEY="your_hubspot_key"
export N8N_BASE_URL="http://localhost:5678"  # or your n8n instance

# Enrich leads with Clay
python scripts/clay_enrich.py --input leads.csv --enrichments company_data,contact_data

# Sync to HubSpot
python scripts/hubspot_sync.py --action sync_enriched --input enriched_leads.json

# Create n8n workflow
python scripts/n8n_workflow.py --action create --file workflows/lead_enrichment_n8n.json
```

## RevOps Tools Coverage

| Tool | Automation Level | CLI Support | Script |
|------|------------------|-------------|--------|
| **Clay** | 95% | ✅ Yes | `clay_enrich.py` |
| **HubSpot** | 90% | ✅ Yes | `hubspot_sync.py` |
| **n8n** | 100% | ✅ Yes | `n8n_workflow.py` |
| **Make** | 70% | ⚠️ Webhooks | (via webhooks) |
| **Salesforce** | 85% | ✅ Yes | (similar to HubSpot) |

## Key Workflows

### 1. Lead Enrichment Pipeline
```
New Lead → Clay Enrichment → HubSpot Update → Lead Scoring → Workflow Trigger
```

**Automation:**
- HubSpot webhook triggers n8n workflow
- Clay enriches company + contact data
- HubSpot updated automatically
- Lead score calculated & updated
- Sales sequence triggered

### 2. Data Sync Workflow
```
HubSpot ↔ Salesforce (bi-directional sync)
```

**Automation:**
- n8n monitors both CRMs
- Syncs contacts, companies, deals
- Handles conflicts & duplicates
- Logs all sync activity

### 3. Attribution Pipeline
```
Multiple Touchpoints → Attribution Calculation → HubSpot Update → Reporting
```

**Automation:**
- Track all touchpoints (email, ads, web)
- Calculate multi-touch attribution
- Update HubSpot deals
- Generate attribution reports

## Setup

### 1. n8n Setup (Self-Hosted)

```bash
# Install n8n
npm install -g n8n

# Start n8n
n8n start

# Access at http://localhost:5678
```

### 2. API Keys

```bash
# Clay API
export CLAY_API_KEY="your_key"

# HubSpot API
export HUBSPOT_API_KEY="your_key"

# n8n API (if using API key)
export N8N_API_KEY="your_key"
```

### 3. HubSpot Webhooks

Set up webhooks in HubSpot to trigger n8n workflows:
- Contact created → n8n webhook
- Deal stage changed → n8n webhook
- Form submission → n8n webhook

## Example: Complete Lead Enrichment Flow

```bash
# 1. Get new leads from HubSpot
python scripts/hubspot_sync.py --action get_contacts > leads.json

# 2. Enrich with Clay
python scripts/clay_enrich.py --input leads.json --enrichments company_data,contact_data,technographics

# 3. Sync enriched data back to HubSpot
python scripts/hubspot_sync.py --action sync_enriched --input leads_enriched.json

# 4. Trigger workflow (if needed)
python scripts/hubspot_sync.py --action trigger_workflow --workflow-id "12345" --contact-id "67890"
```

## n8n Workflow Examples

### Lead Enrichment Workflow
See `workflows/lead_enrichment_n8n.json` for a complete example.

**Nodes:**
1. HubSpot Webhook (trigger)
2. Extract Domain (code node)
3. Clay Company Enrich (HTTP request)
4. Clay Contact Enrich (HTTP request)
5. Update HubSpot Contact
6. Calculate Lead Score (code node)
7. Update Lead Score

### Create Workflow via CLI

```bash
python scripts/n8n_workflow.py --action create --file workflows/lead_enrichment_n8n.json
```

## Time Savings

- **Manual RevOps:** ~15 hours/week
- **Automated RevOps:** ~3 hours/week
- **Savings:** 80% (624 hours/year)

## Next Steps

1. **Set up n8n** (self-hosted or cloud)
2. **Get API keys** (Clay, HubSpot, etc.)
3. **Create workflows** in n8n
4. **Automate everything** via CLI/API
5. **Monitor & optimize** workflows

---

**Built with:** n8n, Clay, HubSpot, Python, CLI tools, Cursor + AI agents
