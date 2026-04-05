#!/usr/bin/env python3
"""
Wasted Spend Detection Automation
Identifies underperforming campaigns and suggests optimizations.
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict

sys.path.append(str(Path(__file__).parent.parent))

class WastedSpendDetector:
    """Detect wasted ad spend and optimization opportunities."""
    
    def __init__(self, roas_threshold: float = 2.0, cac_threshold: float = 50.0):
        self.roas_threshold = roas_threshold
        self.cac_threshold = cac_threshold
    
    def analyze_campaign(self, campaign_data: Dict) -> Dict:
        """Analyze individual campaign performance."""
        spend = campaign_data.get("spend", 0)
        revenue = campaign_data.get("revenue", 0)
        conversions = campaign_data.get("conversions", 0)
        
        roas = revenue / spend if spend > 0 else 0
        cac = spend / conversions if conversions > 0 else float('inf')
        
        is_wasted = roas < self.roas_threshold or cac > self.cac_threshold
        
        return {
            "campaign_id": campaign_data.get("id"),
            "campaign_name": campaign_data.get("name"),
            "spend": spend,
            "revenue": revenue,
            "roas": roas,
            "cac": cac,
            "conversions": conversions,
            "is_wasted": is_wasted,
            "wasted_amount": spend if is_wasted else 0,
            "recommendation": self._get_recommendation(roas, cac, conversions)
        }
    
    def _get_recommendation(self, roas: float, cac: float, conversions: int) -> str:
        """Generate optimization recommendation."""
        if roas < self.roas_threshold and conversions > 0:
            return "PAUSE - Low ROAS"
        elif cac > self.cac_threshold:
            return "OPTIMIZE - High CAC"
        elif conversions == 0 and roas == 0:
            return "PAUSE - No conversions"
        else:
            return "SCALE - Performing well"
    
    def find_wasted_spend(self, campaigns: List[Dict]) -> Dict:
        """Find all wasted spend across campaigns."""
        results = {
            "total_campaigns": len(campaigns),
            "wasted_campaigns": [],
            "total_wasted_spend": 0,
            "potential_savings": 0,
            "scaling_opportunities": []
        }
        
        for campaign in campaigns:
            analysis = self.analyze_campaign(campaign)
            
            if analysis["is_wasted"]:
                results["wasted_campaigns"].append(analysis)
                results["total_wasted_spend"] += analysis["wasted_amount"]
            elif analysis["recommendation"] == "SCALE - Performing well":
                results["scaling_opportunities"].append(analysis)
        
        results["potential_savings"] = results["total_wasted_spend"]
        
        return results
    
    def generate_report(self, results: Dict) -> str:
        """Generate wasted spend report."""
        report_path = Path(__file__).parent.parent / "reports" / f"wasted_spend_{datetime.now().strftime('%Y%m%d')}.md"
        
        report = f"""# Wasted Spend Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- **Total Campaigns Analyzed:** {results['total_campaigns']}
- **Wasted Campaigns:** {len(results['wasted_campaigns'])}
- **Total Wasted Spend:** ${results['total_wasted_spend']:,.2f}
- **Potential Savings:** ${results['potential_savings']:,.2f}

## Wasted Campaigns

| Campaign | Spend | ROAS | CAC | Recommendation |
|----------|-------|------|-----|----------------|
"""
        
        for campaign in results["wasted_campaigns"]:
            report += f"| {campaign['campaign_name']} | ${campaign['spend']:,.2f} | {campaign['roas']:.2f} | ${campaign['cac']:.2f} | {campaign['recommendation']} |\n"
        
        if results["scaling_opportunities"]:
            report += "\n## Scaling Opportunities\n\n"
            report += "| Campaign | Spend | ROAS | CAC | Recommendation |\n"
            report += "|----------|-------|------|-----|----------------|\n"
            
            for campaign in results["scaling_opportunities"][:10]:  # Top 10
                report += f"| {campaign['campaign_name']} | ${campaign['spend']:,.2f} | {campaign['roas']:.2f} | ${campaign['cac']:.2f} | {campaign['recommendation']} |\n"
        
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report)
        
        print(f"✅ Wasted spend report saved to: {report_path}")
        return str(report_path)

def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Find wasted ad spend")
    parser.add_argument("--threshold", type=float, default=0.5, help="ROAS threshold")
    parser.add_argument("--auto-pause", action="store_true", help="Automatically pause wasted campaigns")
    
    args = parser.parse_args()
    
    # TODO: Pull actual campaign data from APIs
    # Example campaign data structure
    sample_campaigns = [
        {"id": "1", "name": "Campaign A", "spend": 1000, "revenue": 1500, "conversions": 20},
        {"id": "2", "name": "Campaign B", "spend": 2000, "revenue": 3000, "conversions": 40},
        {"id": "3", "name": "Campaign C", "spend": 500, "revenue": 400, "conversions": 5},
    ]
    
    detector = WastedSpendDetector(roas_threshold=args.threshold)
    results = detector.find_wasted_spend(sample_campaigns)
    
    report_path = detector.generate_report(results)
    
    if args.auto_pause:
        print("⚠️  Auto-pause not implemented - would pause campaigns here")
        # TODO: Implement API calls to pause campaigns
    
    print(f"✅ Analysis complete! Report: {report_path}")

if __name__ == "__main__":
    main()




