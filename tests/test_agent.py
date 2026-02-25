import json
from agent.agents.clinical_agent import build_analysis_agent
from pydantic import BaseModel
from typing import List

class EEGReport(BaseModel):
    total_windows: int
    anomalies_detected: int
    channels: List[str] = []

def test_agent_response():
    agent = build_analysis_agent()
    report = EEGReport(total_windows=10, anomalies_detected=2, channels=["Fp1", "Fp2"])
    response = agent.invoke({"report": report.dict()})
    
    data = json.loads(response)
    assert "eeg_analysis" in data
    assert "internal_reasoning" in data
    assert "final_answer" in data