"""
Builds structured clinical reports from model predictions.
"""


def build_report(predictions):
    """
    Convert anomaly predictions into a structured report
    usable by the clinical agent.
    """

    report = {
        "total_windows": len(predictions),
        "anomalies_detected": int((predictions == -1).sum())
    }

    return report