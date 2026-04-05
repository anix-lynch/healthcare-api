#!/usr/bin/env python3
"""
Budget Forecasting Automation
Predictive models for budget allocation and CAC/ROAS targets.
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import json

sys.path.append(str(Path(__file__).parent.parent))

class BudgetForecaster:
    """Forecast budget allocation and performance metrics."""
    
    def __init__(self):
        pass
    
    def forecast_roas(self, historical_data: list, days_ahead: int = 30) -> dict:
        """
        Forecast ROAS using simple trend analysis.
        In production, use Prophet, ARIMA, or XGBoost.
        """
        # Simplified forecasting (replace with actual ML model)
        if not historical_data:
            return {"forecast": 3.0, "confidence": "low"}
        
        # Simple average (replace with proper time series model)
        avg_roas = sum(d.get("roas", 0) for d in historical_data) / len(historical_data)
        
        return {
            "forecast": avg_roas,
            "confidence": "medium",
            "forecast_date": (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        }
    
    def forecast_cac(self, historical_data: list, days_ahead: int = 30) -> dict:
        """Forecast CAC."""
        if not historical_data:
            return {"forecast": 50.0, "confidence": "low"}
        
        avg_cac = sum(d.get("cac", 0) for d in historical_data) / len(historical_data)
        
        return {
            "forecast": avg_cac,
            "confidence": "medium",
            "forecast_date": (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        }
    
    def optimize_budget_allocation(self, platforms: dict, total_budget: float) -> dict:
        """
        Optimize budget allocation across platforms based on performance.
        """
        # Calculate efficiency scores
        platform_scores = {}
        for platform, data in platforms.items():
            roas = data.get("roas", 0)
            cac = data.get("cac", 0)
            # Simple efficiency score (higher ROAS, lower CAC = better)
            efficiency = roas / (cac / 100) if cac > 0 else 0
            platform_scores[platform] = efficiency
        
        # Allocate budget proportionally to efficiency
        total_score = sum(platform_scores.values())
        allocation = {}
        
        for platform, score in platform_scores.items():
            if total_score > 0:
                allocation[platform] = {
                    "budget": (score / total_score) * total_budget,
                    "percentage": (score / total_score) * 100,
                    "efficiency_score": score
                }
            else:
                allocation[platform] = {
                    "budget": total_budget / len(platforms),
                    "percentage": 100 / len(platforms),
                    "efficiency_score": 0
                }
        
        return allocation
    
    def generate_scenarios(self, base_budget: float, scenarios: int = 3) -> list:
        """Generate multiple budget scenarios."""
        scenario_list = []
        
        for i in range(scenarios):
            multiplier = 0.8 + (i * 0.2)  # 80%, 100%, 120%
            budget = base_budget * multiplier
            
            scenario_list.append({
                "scenario": f"Scenario {i+1}",
                "budget": budget,
                "multiplier": multiplier,
                "expected_revenue": budget * 3.0,  # Assume 3x ROAS
                "expected_cac": 45.0
            })
        
        return scenario_list
    
    def generate_forecast_report(self, horizon_days: int = 30, scenarios: int = 3) -> str:
        """Generate comprehensive forecast report."""
        # TODO: Pull actual historical data
        historical_data = [
            {"date": "2024-01-01", "roas": 3.2, "cac": 45},
            {"date": "2024-01-02", "roas": 3.5, "cac": 42},
            {"date": "2024-01-03", "roas": 3.1, "cac": 48},
        ]
        
        roas_forecast = self.forecast_roas(historical_data, horizon_days)
        cac_forecast = self.forecast_cac(historical_data, horizon_days)
        
        # Budget allocation optimization
        platforms = {
            "Meta": {"roas": 3.2, "cac": 45},
            "Google": {"roas": 3.5, "cac": 42}
        }
        allocation = self.optimize_budget_allocation(platforms, 10000)
        
        # Generate scenarios
        scenario_list = self.generate_scenarios(10000, scenarios)
        
        report_path = Path(__file__).parent.parent / "reports" / f"forecast_{datetime.now().strftime('%Y%m%d')}.md"
        
        report = f"""# Budget Forecast Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Forecast Horizon: {horizon_days} days

## Performance Forecasts

### ROAS Forecast
- **Forecasted ROAS:** {roas_forecast['forecast']:.2f}
- **Confidence:** {roas_forecast['confidence']}
- **Forecast Date:** {roas_forecast['forecast_date']}

### CAC Forecast
- **Forecasted CAC:** ${cac_forecast['forecast']:.2f}
- **Confidence:** {cac_forecast['confidence']}
- **Forecast Date:** {cac_forecast['forecast_date']}

## Optimized Budget Allocation

| Platform | Budget | Percentage | Efficiency Score |
|----------|--------|------------|------------------|
"""
        
        for platform, data in allocation.items():
            report += f"| {platform} | ${data['budget']:,.2f} | {data['percentage']:.1f}% | {data['efficiency_score']:.2f} |\n"
        
        report += "\n## Budget Scenarios\n\n"
        report += "| Scenario | Budget | Expected Revenue | Expected CAC |\n"
        report += "|----------|--------|------------------|--------------|\n"
        
        for scenario in scenario_list:
            report += f"| {scenario['scenario']} | ${scenario['budget']:,.2f} | ${scenario['expected_revenue']:,.2f} | ${scenario['expected_cac']:.2f} |\n"
        
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report)
        
        print(f"✅ Forecast report saved to: {report_path}")
        return str(report_path)

def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate budget forecasts")
    parser.add_argument("--horizon", type=str, default="30d", help="Forecast horizon (e.g., 30d)")
    parser.add_argument("--scenarios", type=int, default=3, help="Number of scenarios to generate")
    
    args = parser.parse_args()
    
    horizon_days = int(args.horizon.replace("d", ""))
    
    forecaster = BudgetForecaster()
    report_path = forecaster.generate_forecast_report(horizon_days, args.scenarios)
    
    print(f"✅ Forecasting complete! Report: {report_path}")

if __name__ == "__main__":
    main()




