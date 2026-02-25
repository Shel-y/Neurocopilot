from agent.core.report_builder import build_report
import numpy as np


def test_report_creation():
    fake_predictions = np.array([1, 1, -1, 1])

    report = build_report(fake_predictions)

    assert "total_windows" in report
    assert "anomalies_detected" in report