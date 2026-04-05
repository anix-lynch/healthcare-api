#!/usr/bin/env python3
"""
HubSpot CRM Automation
Sync data, update contacts, manage deals, trigger workflows.
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

class HubSpotClient:
    """HubSpot API client for CRM operations."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("HUBSPOT_API_KEY")
        if not self.api_key:
            raise ValueError("HUBSPOT_API_KEY environment variable required")
        
        self.base_url = "https://api.hubapi.com"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_contacts(self, limit: int = 100, properties: List[str] = None) -> List[Dict]:
        """Get contacts from HubSpot."""
        if properties is None:
            properties = ["email", "firstname", "lastname", "company", "phone"]
        
        url = f"{self.base_url}/crm/v3/objects/contacts"
        params = {
            "limit": limit,
            "properties": ",".join(properties)
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except requests.exceptions.RequestException as e:
            print(f"Error getting contacts: {e}")
            return []
    
    def create_contact(self, contact_data: Dict) -> Dict:
        """Create a new contact in HubSpot."""
        url = f"{self.base_url}/crm/v3/objects/contacts"
        payload = {
            "properties": contact_data
        }
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating contact: {e}")
            return {}
    
    def update_contact(self, contact_id: str, contact_data: Dict) -> Dict:
        """Update an existing contact."""
        url = f"{self.base_url}/crm/v3/objects/contacts/{contact_id}"
        payload = {
            "properties": contact_data
        }
        
        try:
            response = requests.patch(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating contact {contact_id}: {e}")
            return {}
    
    def update_lead_score(self, contact_id: str, score: int) -> Dict:
        """Update lead score for a contact."""
        return self.update_contact(contact_id, {"hs_lead_status": score})
    
    def get_deals(self, limit: int = 100) -> List[Dict]:
        """Get deals from HubSpot."""
        url = f"{self.base_url}/crm/v3/objects/deals"
        params = {"limit": limit}
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except requests.exceptions.RequestException as e:
            print(f"Error getting deals: {e}")
            return []
    
    def trigger_workflow(self, workflow_id: str, contact_id: str) -> bool:
        """Trigger a HubSpot workflow."""
        url = f"{self.base_url}/automation/v2/workflows/{workflow_id}/enrollments/contacts/{contact_id}"
        
        try:
            response = requests.post(url, headers=self.headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error triggering workflow {workflow_id}: {e}")
            return False
    
    def sync_from_enriched_data(self, enriched_data: List[Dict]) -> Dict:
        """Sync enriched data back to HubSpot."""
        results = {
            "created": 0,
            "updated": 0,
            "errors": 0
        }
        
        for lead in enriched_data:
            contact_data = {
                "email": lead.get("email") or lead.get("enriched_email"),
                "firstname": lead.get("first_name"),
                "lastname": lead.get("last_name"),
                "company": lead.get("company"),
                "phone": lead.get("phone"),
                "website": lead.get("company_domain"),
            }
            
            # Add custom properties if available
            if lead.get("company_revenue"):
                contact_data["annualrevenue"] = lead.get("company_revenue")
            if lead.get("company_employees"):
                contact_data["num_employees"] = lead.get("company_employees")
            if lead.get("company_industry"):
                contact_data["industry"] = lead.get("company_industry")
            
            # Try to update existing contact or create new
            email = contact_data.get("email")
            if email:
                # In production, check if contact exists first
                # For now, try to create (will fail if exists)
                result = self.create_contact(contact_data)
                if result:
                    results["created"] += 1
                else:
                    results["errors"] += 1
        
        return results

def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Sync data with HubSpot")
    parser.add_argument("--action", type=str, required=True,
                       choices=["get_contacts", "sync_enriched", "update_scores", "trigger_workflow"],
                       help="Action to perform")
    parser.add_argument("--input", type=str, help="Input file (for sync_enriched)")
    parser.add_argument("--workflow-id", type=str, help="Workflow ID (for trigger_workflow)")
    parser.add_argument("--contact-id", type=str, help="Contact ID (for trigger_workflow)")
    
    args = parser.parse_args()
    
    client = HubSpotClient()
    
    if args.action == "get_contacts":
        contacts = client.get_contacts(limit=100)
        print(f"✅ Retrieved {len(contacts)} contacts")
        for contact in contacts[:5]:  # Show first 5
            print(f"  - {contact.get('properties', {}).get('email', 'N/A')}")
    
    elif args.action == "sync_enriched":
        if not args.input:
            print("❌ --input required for sync_enriched")
            return
        
        import json
        with open(args.input, 'r') as f:
            enriched_data = json.load(f)
        
        results = client.sync_from_enriched_data(enriched_data)
        print(f"✅ Sync complete:")
        print(f"  - Created: {results['created']}")
        print(f"  - Updated: {results['updated']}")
        print(f"  - Errors: {results['errors']}")
    
    elif args.action == "trigger_workflow":
        if not args.workflow_id or not args.contact_id:
            print("❌ --workflow-id and --contact-id required")
            return
        
        success = client.trigger_workflow(args.workflow_id, args.contact_id)
        if success:
            print(f"✅ Workflow {args.workflow_id} triggered for contact {args.contact_id}")
        else:
            print(f"❌ Failed to trigger workflow")

if __name__ == "__main__":
    main()




