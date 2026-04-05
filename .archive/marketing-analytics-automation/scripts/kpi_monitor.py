#!/usr/bin/env python3
"""
KPI Monitoring Automation
Tracks key metrics: CAC, ROAS, MER, LTV, AOV, CTR, CVR, CPM
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

sys.path.append(str(Path(__file__).parent.parent))

class KPIMonitor:
    """Monitor and track marketing KPIs."""
    
    def __init__(self):
        self.kpis = {
            "cac": {"name": "Customer Acquisition Cost", "threshold": 50, "direction": "lower"},
            "roas": {"name": "Return on Ad Spend", "threshold": 3.0, "direction": "higher"},
            "mer": {"name": "Marketing Efficiency Ratio", "threshold": 3.0, "direction": "higher"},
            "ltv": {"name": "Lifetime Value", "threshold": 200, "direction": "higher"},
            "aov": {"name": "Average Order Value", "threshold": 75, "direction": "higher"},
            "ctr": {"name": "Click-Through Rate", "threshold": 0.02, "direction": "higher"},
            "cvr": {"name": "Conversion Rate", "threshold": 0.03, "direction": "higher"},
            "cpm": {"name": "Cost Per Mille", "threshold": 15, "direction": "lower"},
        }
    
    def calculate_cac(self, spend: float, conversions: int) -> float:
        """Calculate Customer Acquisition Cost."""
        return spend / conversions if conversions > 0 else 0
    
    def calculate_roas(self, revenue: float, spend: float) -> float:
        """Calculate Return on Ad Spend."""
        return revenue / spend if spend > 0 else 0
    
    def calculate_mer(self, total_revenue: float, marketing_spend: float) -> float:
        """Calculate Marketing Efficiency Ratio."""
        return total_revenue / marketing_spend if marketing_spend > 0 else 0
    
    def check_thresholds(self, current_values: Dict[str, float]) -> List[Dict]:
        """Check if KPIs are within acceptable thresholds."""
        alerts = []
        
        for kpi_key, kpi_config in self.kpis.items():
            current_value = current_values.get(kpi_key, 0)
            threshold = kpi_config["threshold"]
            direction = kpi_config["direction"]
            
            is_alert = False
            if direction == "lower" and current_value > threshold:
                is_alert = True
            elif direction == "higher" and current_value < threshold:
                is_alert = True
            
            if is_alert:
                alerts.append({
                    "kpi": kpi_key,
                    "name": kpi_config["name"],
                    "current": current_value,
                    "threshold": threshold,
                    "status": "⚠️ ALERT"
                })
        
        return alerts
    
    def generate_kpi_report(self, period_days: int = 7) -> str:
        """Generate KPI monitoring report."""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=period_days)
        
        # TODO: Pull actual data from APIs/data warehouse
        # This is a placeholder structure
        current_values = {
            "cac": 45.0,
            "roas": 3.5,
            "mer": 3.2,
            "ltv": 250,
            "aov": 85,
            "ctr": 0.025,
            "cvr": 0.035,
            "cpm": 12
        }
        
        alerts = self.check_thresholds(current_values)
        
        report_path = Path(__file__).parent.parent / "reports" / f"kpi_report_{datetime.now().strftime('%Y%m%d')}.md"
        
        report = f"""# KPI Monitoring Report
Period: {start_date} to {end_date}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Current KPI Values

| KPI | Value | Threshold | Status |
|-----|-------|-----------|--------|
"""
        
        for kpi_key, kpi_config in self.kpis.items():
            value = current_values.get(kpi_key, 0)
            threshold = kpi_config["threshold"]
            direction = kpi_config["direction"]
            
            if direction == "lower":
                status = "✅" if value <= threshold else "⚠️"
            else:
                status = "✅" if value >= threshold else "⚠️"
            
            report += f"| {kpi_config['name']} ({kpi_key.upper()}) | {value:.2f} | {threshold} | {status} |\n"
        
        if alerts:
            report += "\n## ⚠️ Alerts\n\n"
            for alert in alerts:
                report += f"- **{alert['name']}:** {alert['current']:.2f} (Threshold: {alert['threshold']})\n"
        
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report)
        
        print(f"✅ KPI report saved to: {report_path}")
        return str(report_path)

def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Monitor marketing KPIs")
    parser.add_argument("--metrics", type=str, default="all", help="Comma-separated list of metrics")
    parser.add_argument("--period", type=str, default="7d", help="Time period (e.g., 7d, 30d)")
    
    args = parser.parse_args()
    
    # Parse period
    period_days = int(args.period.replace("d", ""))
    
    monitor = KPIMonitor()
    report_path = monitor.generate_kpi_report(period_days=period_days)
    
    print(f"✅ KPI monitoring complete! Report: {report_path}")

if __name__ == "__main__":
    main()




