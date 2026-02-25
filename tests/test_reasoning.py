from agent.agents.clinical_agent import build_clinical_agent


def test_agent_reasoning_structure():

    agent = build_clinical_agent()

    report = "Simulated EEG shows alpha wave asymmetry and occasional theta bursts."

    response = agent.invoke({"report": report})

    assert response is not None
    assert isinstance(response, str)