#!/usr/bin/env python3
"""
Clay Data Enrichment Automation
Enriches leads/contacts with company data, contact info, and technographics.
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional

sys.path.append(str(Path(__file__).parent.parent))

class ClayEnricher:
    """Enrich leads using Clay API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("CLAY_API_KEY")
        if not self.api_key:
            raise ValueError("CLAY_API_KEY environment variable required")
        
        self.base_url = "https://api.clay.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def enrich_company(self, domain: str) -> Dict:
        """
        Enrich company data from domain.
        Returns: revenue, employees, industry, location, etc.
        """
        url = f"{self.base_url}/enrichment/company"
        payload = {"domain": domain}
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error enriching company {domain}: {e}")
            return {}
    
    def enrich_contact(self, email: Optional[str] = None, 
                      first_name: Optional[str] = None,
                      last_name: Optional[str] = None,
                      company: Optional[str] = None) -> Dict:
        """
        Enrich contact data.
        Returns: email, phone, LinkedIn, job title, etc.
        """
        url = f"{self.base_url}/enrichment/contact"
        payload = {}
        
        if email:
            payload["email"] = email
        if first_name:
            payload["first_name"] = first_name
        if last_name:
            payload["last_name"] = last_name
        if company:
            payload["company"] = company
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error enriching contact: {e}")
            return {}
    
    def get_technographics(self, domain: str) -> Dict:
        """
        Get technographic data (tech stack) for a company.
        Returns: technologies used, categories, etc.
        """
        url = f"{self.base_url}/technographics"
        params = {"domain": domain}
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting technographics for {domain}: {e}")
            return {}
    
    def bulk_enrich(self, leads: List[Dict], enrichments: List[str] = None) -> List[Dict]:
        """
        Bulk enrich multiple leads.
        enrichments: ['company_data', 'contact_data', 'technographics']
        """
        if enrichments is None:
            enrichments = ['company_data', 'contact_data']
        
        enriched_leads = []
        
        for lead in leads:
            enriched = lead.copy()
            
            # Extract domain from email or company field
            domain = None
            if lead.get("email"):
                domain = lead["email"].split("@")[1] if "@" in lead.get("email", "") else None
            elif lead.get("company_domain"):
                domain = lead["company_domain"]
            elif lead.get("company"):
                # Try to extract domain from company name (simplified)
                domain = lead["company"].lower().replace(" ", "") + ".com"
            
            if 'company_data' in enrichments and domain:
                company_data = self.enrich_company(domain)
                enriched.update({
                    "company_revenue": company_data.get("revenue"),
                    "company_employees": company_data.get("employees"),
                    "company_industry": company_data.get("industry"),
                    "company_location": company_data.get("location"),
                })
            
            if 'contact_data' in enrichments:
                contact_data = self.enrich_contact(
                    email=lead.get("email"),
                    first_name=lead.get("first_name"),
                    last_name=lead.get("last_name"),
                    company=lead.get("company")
                )
                enriched.update({
                    "enriched_email": contact_data.get("email"),
                    "phone": contact_data.get("phone"),
                    "linkedin_url": contact_data.get("linkedin_url"),
                    "job_title": contact_data.get("job_title"),
                })
            
            if 'technographics' in enrichments and domain:
                tech_data = self.get_technographics(domain)
                enriched["technologies"] = tech_data.get("technologies", [])
            
            enriched_leads.append(enriched)
        
        return enriched_leads

def main():
    """Main execution."""
    import argparse
    import csv
    
    parser = argparse.ArgumentParser(description="Enrich leads using Clay API")
    parser.add_argument("--input", type=str, required=True, help="Input CSV file")
    parser.add_argument("--output", type=str, help="Output CSV file")
    parser.add_argument("--enrichments", type=str, default="company_data,contact_data",
                       help="Comma-separated: company_data,contact_data,technographics")
    
    args = parser.parse_args()
    
    # Parse enrichments
    enrichments = [e.strip() for e in args.enrichments.split(",")]
    
    # Read input CSV
    leads = []
    with open(args.input, 'r') as f:
        reader = csv.DictReader(f)
        leads = list(reader)
    
    print(f"📊 Enriching {len(leads)} leads with Clay...")
    
    # Enrich leads
    enricher = ClayEnricher()
    enriched_leads = enricher.bulk_enrich(leads, enrichments)
    
    # Write output
    output_file = args.output or args.input.replace(".csv", "_enriched.csv")
    
    if enriched_leads:
        fieldnames = enriched_leads[0].keys()
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(enriched_leads)
        
        print(f"✅ Enriched {len(enriched_leads)} leads")
        print(f"✅ Saved to: {output_file}")
    else:
        print("❌ No leads enriched")

if __name__ == "__main__":
    main()




