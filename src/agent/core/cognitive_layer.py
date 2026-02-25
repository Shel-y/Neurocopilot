"""
Cognitive Layer

Adds internal reasoning scaffolding before calling the LLM.
This simulates structured clinical thinking without exposing
chain-of-thought to the final user.
"""


def build_cognitive_context(report: dict) -> dict:
    """
    Enriches report with reasoning metadata.

    Complexity: O(1)
    """

    anomalies = report["anomalies_detected"]
    total = report["total_windows"]

    anomaly_ratio = anomalies / total if total > 0 else 0

    # uncertainty heuristic (simple MVP logic)
    if anomaly_ratio < 0.1:
        uncertainty = "High"
    elif anomaly_ratio < 0.3:
        uncertainty = "Moderate"
    else:
        uncertainty = "Low"

    enriched_report = {
        "report": report,
        "anomaly_ratio": anomaly_ratio,
        "suggested_uncertainty": uncertainty,
    }

    return enriched_report