def build_value_report(metrics: dict) -> dict:
    monthly = metrics.get('time_saved',0)*40 + metrics.get('risk_reduced',0)*20
    justified = 1200 if monthly>=1200 else 1000 if monthly>=1000 else 800 if monthly>=800 else 0
    return {**metrics, 'estimated_monthly_value': monthly, 'pilot_justified': justified, 'honesty_notes': ['Missing UI/RGPD/multi-client checks may lower confidence.']}
