import json
import os
import traceback

# Ensure tests use mock LLM (don't require Ollama running)
os.environ["USE_MOCK_LLM"] = "1"

from agent.agents.clinical_agent import build_analysis_agent, build_clinical_agent, _MockLLM
from tests.test_agent import EEGReport


def run_test_agent_response():
    try:
        agent = build_analysis_agent(llm=_MockLLM())
        report = EEGReport(total_windows=10, anomalies_detected=2, channels=["Fp1", "Fp2"])
        response = agent.invoke({"report": report.model_dump()})
        data = json.loads(response)
        ok = all(k in data for k in ("eeg_analysis", "internal_reasoning", "final_answer"))
        print("test_agent_response:", "PASS" if ok else f"FAIL - keys missing: {list(data.keys())}")
    except Exception as e:
        print("test_agent_response: ERROR")
        traceback.print_exc()


def run_test_reasoning_structure():
    try:
        agent = build_clinical_agent(llm=_MockLLM())
        report = "Simulated EEG shows alpha wave asymmetry and occasional theta bursts."
        response = agent.invoke({"report": report})
        print("test_agent_reasoning_structure:", "PASS" if isinstance(response, str) and response else "FAIL")
    except Exception:
        print("test_agent_reasoning_structure: ERROR")
        traceback.print_exc()


if __name__ == '__main__':
    run_test_agent_response()
    run_test_reasoning_structure()
