import json
import os
from typing import Optional

# Use real LLM (Ollama) by default; set USE_MOCK_LLM=1 to use mock for tests
USE_MOCK = os.getenv("USE_MOCK_LLM", "0") == "1"

OllamaLLM = None
if not USE_MOCK:
    try:
        from langchain_ollama import OllamaLLM
    except Exception:
        OllamaLLM = None


class _MockLLM:
    def invoke(self, prompt: str) -> str:
        # Return a simple, valid JSON response for tests and fallback cases
        response = {
            "eeg_analysis": "Simulated analysis (mock).",
            "internal_reasoning": {
                "signal_interpretation": "Mock interpretation.",
                "clinical_context": "Simulated context.",
                "possible_hypotheses": "Mock hypotheses.",
                "uncertainty_level": "low",
                "suggested_next_tests": "Simulated next tests.",
                "specialist_explanation": "Mock specialist explanation."
            },
            "should_explain": True,
            "final_answer": "This is a mock final answer."
        }
        return json.dumps(response)


def build_analysis_agent(llm: Optional[object] = None):
    # Allow injection of a real or mock LLM (useful for tests)
    if llm is None:
        if USE_MOCK:
            llm = _MockLLM()
        else:
            if OllamaLLM is not None:
                try:
                    llm = OllamaLLM(model="mistral")
                except Exception:
                    llm = _MockLLM()
            else:
                llm = _MockLLM()

    class Agent:
        def invoke(self, data):
            report = data.get("report", {})
            return think(str(report), llm)

    return Agent()


# Backwards-compatible alias used in other modules/tests
def build_clinical_agent(llm: Optional[object] = None):
    return build_analysis_agent(llm=llm)


def think(user_input: str, llm_instance: object):
    # If using the internal MockLLM, avoid importing langchain prompt machinery
    if isinstance(llm_instance, _MockLLM):
        prompt = user_input
    else:
        # Import prompt template lazily to avoid heavy imports at module load time
        from agent.prompts.reasoning_prompt import reasoning_prompt
        prompt = reasoning_prompt.format(input=user_input)

    raw_response = llm_instance.invoke(prompt)

    try:
        result = json.loads(raw_response)
    except Exception:
        return json.dumps({"final_answer": raw_response})

    if result.get("should_explain"):
        result["final_answer"] += "\n\n🧠 Internal reasoning available."

    return json.dumps(result)