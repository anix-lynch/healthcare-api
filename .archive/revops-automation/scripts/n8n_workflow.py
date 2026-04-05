#!/usr/bin/env python3
"""
n8n Workflow Automation
Create, trigger, and monitor n8n workflows via API.
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Dict, Optional

sys.path.append(str(Path(__file__).parent.parent))

class N8nClient:
    """n8n API client for workflow automation."""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or os.getenv("N8N_BASE_URL", "http://localhost:5678")
        self.api_key = api_key or os.getenv("N8N_API_KEY")
        
        self.headers = {
            "Content-Type": "application/json"
        }
        
        if self.api_key:
            self.headers["X-N8N-API-KEY"] = self.api_key
    
    def create_workflow(self, workflow_data: Dict) -> Dict:
        """Create a new workflow in n8n."""
        url = f"{self.base_url}/api/v1/workflows"
        
        try:
            response = requests.post(url, json=workflow_data, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating workflow: {e}")
            return {}
    
    def get_workflow(self, workflow_id: str) -> Dict:
        """Get workflow details."""
        url = f"{self.base_url}/api/v1/workflows/{workflow_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting workflow {workflow_id}: {e}")
            return {}
    
    def trigger_webhook(self, webhook_path: str, data: Dict) -> Dict:
        """Trigger a webhook workflow."""
        url = f"{self.base_url}/webhook/{webhook_path}"
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error triggering webhook {webhook_path}: {e}")
            return {}
    
    def get_executions(self, workflow_id: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Get workflow executions."""
        url = f"{self.base_url}/api/v1/executions"
        params = {"limit": limit}
        
        if workflow_id:
            params["workflowId"] = workflow_id
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except requests.exceptions.RequestException as e:
            print(f"Error getting executions: {e}")
            return []
    
    def activate_workflow(self, workflow_id: str) -> bool:
        """Activate a workflow."""
        url = f"{self.base_url}/api/v1/workflows/{workflow_id}/activate"
        
        try:
            response = requests.post(url, headers=self.headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error activating workflow {workflow_id}: {e}")
            return False

def create_lead_enrichment_workflow() -> Dict:
    """Create a lead enrichment workflow template."""
    return {
        "name": "Lead Enrichment Pipeline",
        "nodes": [
            {
                "name": "Webhook Trigger",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "parameters": {
                    "path": "lead-enrichment",
                    "httpMethod": "POST"
                },
                "webhookId": "lead-enrichment-webhook"
            },
            {
                "name": "Clay Enrich",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 1,
                "parameters": {
                    "url": "https://api.clay.com/v1/enrichment/company",
                    "method": "POST",
                    "authentication": "genericCredentialType",
                    "genericAuthType": "httpHeaderAuth",
                    "sendBody": True,
                    "bodyParameters": {
                        "parameters": [
                            {
                                "name": "domain",
                                "value": "={{ $json.domain }}"
                            }
                        ]
                    }
                }
            },
            {
                "name": "Update HubSpot",
                "type": "n8n-nodes-base.hubspot",
                "typeVersion": 1,
                "parameters": {
                    "operation": "update",
                    "resource": "contact",
                    "contactId": "={{ $json.contactId }}",
                    "updateFields": {
                        "company_revenue": "={{ $json.revenue }}",
                        "num_employees": "={{ $json.employees }}"
                    }
                }
            }
        ],
        "connections": {
            "Webhook Trigger": {
                "main": [[{"node": "Clay Enrich"}]]
            },
            "Clay Enrich": {
                "main": [[{"node": "Update HubSpot"}]]
            }
        }
    }

def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage n8n workflows")
    parser.add_argument("--action", type=str, required=True,
                       choices=["create", "trigger", "list", "activate"],
                       help="Action to perform")
    parser.add_argument("--file", type=str, help="Workflow JSON file")
    parser.add_argument("--webhook", type=str, help="Webhook path")
    parser.add_argument("--data", type=str, help="JSON data for webhook")
    
    args = parser.parse_args()
    
    client = N8nClient()
    
    if args.action == "create":
        if args.file:
            with open(args.file, 'r') as f:
                workflow_data = json.load(f)
        else:
            # Create default lead enrichment workflow
            workflow_data = create_lead_enrichment_workflow()
        
        result = client.create_workflow(workflow_data)
        if result:
            print(f"✅ Workflow created: {result.get('id')}")
        else:
            print("❌ Failed to create workflow")
    
    elif args.action == "trigger":
        if not args.webhook:
            print("❌ --webhook required")
            return
        
        data = {}
        if args.data:
            data = json.loads(args.data)
        
        result = client.trigger_webhook(args.webhook, data)
        if result:
            print(f"✅ Webhook triggered: {args.webhook}")
        else:
            print(f"❌ Failed to trigger webhook")
    
    elif args.action == "list":
        executions = client.get_executions(limit=10)
        print(f"✅ Found {len(executions)} recent executions")
        for exec in executions[:5]:
            print(f"  - {exec.get('id')}: {exec.get('status')}")
    
    elif args.action == "activate":
        if not args.file:
            print("❌ --file required (workflow ID)")
            return
        
        # Assume file contains workflow ID
        workflow_id = args.file.strip()
        success = client.activate_workflow(workflow_id)
        if success:
            print(f"✅ Workflow {workflow_id} activated")
        else:
            print(f"❌ Failed to activate workflow")

if __name__ == "__main__":
    main()




