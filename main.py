from agent.core.pipeline import run_analysis
from agent.core.report_builder import build_report
from agent.agents.clinical_agent import build_clinical_agent
from agent.core.cognitive_layer import build_cognitive_context


predictions = run_analysis()

print(predictions)

report = build_report(predictions)

cognitive_input = build_cognitive_context(report)

agent = build_clinical_agent()

response = agent.invoke(cognitive_input)