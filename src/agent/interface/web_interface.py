import gradio as gr
import numpy as np
import plotly.graph_objects as go
import time
import json

# Local imports
from agent.simulation.eeg_simulator import generate_time, generate_eeg_signal, add_anomaly
from agent.agents.clinical_agent import build_analysis_agent

# Initialize agent
agent = build_analysis_agent()

# Custom CSS
custom_css = """
.gradio-container { font-family: 'Inter', sans-serif; }
#title { text-align: center; color: #00FFCC; margin-bottom: 10px; }
"""

def analyze_eeg(show_reasoning, intensity):
    # 1️⃣ Generate simulated EEG
    t = generate_time()
    signal = generate_eeg_signal(t)
    signal = add_anomaly(signal, t, start_sec=2, duration_sec=1, intensity=intensity)

    # 2️⃣ Base Plotly figure
    base_fig = go.Figure()
    base_fig.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(10, 10, 10, 1)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title="Time (s)", showgrid=False, range=[t[0], t[-1]]),
        yaxis=dict(title="Amplitude", showgrid=True, gridcolor='#333333', range=[min(signal)-1, max(signal)+1]),
        margin=dict(l=40, r=40, t=40, b=40),
        height=400
    )

    # Yield empty state to reset outputs
    yield base_fig, "Processing...", "Processing...", "Processing..."

    # 3️⃣ Animate EEG scan
    chunk_size = len(t) // 20
    for i in range(chunk_size, len(t)+chunk_size, chunk_size):
        current_t = t[:i]
        current_signal = signal[:i]

        frame_fig = go.Figure(base_fig)
        frame_fig.add_trace(go.Scatter(
            x=current_t, y=current_signal,
            mode='lines',
            line=dict(color='#00FFCC', width=2),
            name="Simulated EEG"
        ))

        # Yield plot during animation
        yield frame_fig, "Scanning signal...", "Waiting for AI Agent...", "Waiting for AI Agent..."
        time.sleep(0.05)

    # 4️⃣ Add anomaly highlight (optional)
    # Example: highlight anomaly region
    frame_fig.add_vrect(
        x0=2, x1=3, fillcolor="red", opacity=0.2, line_width=0,
        annotation_text="Simulated Anomaly", annotation_position="top left"
    )

    # 5️⃣ Invoke agent
    report = {"signal_summary": f"Simulated EEG signal with potential anomalies (Intensity: {intensity})"}
    response_json = agent.invoke({"report": report})
    response = json.loads(response_json)

    eeg_analysis = response.get("eeg_analysis", "No analysis provided.")
    final_answer = response.get("final_answer", "No final answer provided.")

    # Structured reasoning
    reasoning_str = "Reasoning is hidden."
    if show_reasoning and response.get("should_explain"):
        reasoning = response.get("internal_reasoning", {})
        reasoning_str = "\n".join([
            f"**1️⃣ Signal Interpretation:** {reasoning.get('signal_interpretation', 'N/A')}",
            f"**2️⃣ Clinical Context:** {reasoning.get('clinical_context', 'N/A')}",
            f"**3️⃣ Possible Hypotheses:** {reasoning.get('possible_hypotheses', 'N/A')}",
            f"**4️⃣ Uncertainty Level:** {reasoning.get('uncertainty_level', 'N/A')}",
            f"**5️⃣ Suggested Next Tests:** {reasoning.get('suggested_next_tests', 'N/A')}",
            f"**6️⃣ Specialist Explanation:** {reasoning.get('specialist_explanation', 'N/A')}",
        ])

    # 6️⃣ Yield final stable plot + analysis
    yield frame_fig, eeg_analysis, final_answer, reasoning_str


# ===========================
# Gradio Blocks Layout
# ===========================
with gr.Blocks(theme=gr.themes.Monochrome(), css=custom_css) as demo:
    gr.Markdown("<h1 id='title'>🧠 NeuroCopilot: Simulated EEG Analysis MVP</h1>")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ Simulator Controls")
            intensity_slider = gr.Slider(minimum=0.5, maximum=5.0, value=1.0, step=0.5, label="Anomaly Intensity")
            reasoning_checkbox = gr.Checkbox(label="Show structured reasoning", value=True)
            run_btn = gr.Button("▶️ Run Analysis & Scan", variant="primary")

        with gr.Column(scale=3):
            plot_output = gr.Plot(label="Live EEG Scan")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🤖 Agent Analysis")
            eeg_analysis_output = gr.Textbox(label="EEG Analysis", lines=3, interactive=False)
            final_answer_output = gr.Textbox(label="Final Answer", lines=3, interactive=False)
            with gr.Accordion("🔍 Internal Reasoning (Structured)", open=False):
                reasoning_output = gr.Markdown("Run the analysis to see the agent's internal thought process.")

    run_btn.click(
        fn=analyze_eeg,
        inputs=[reasoning_checkbox, intensity_slider],
        outputs=[plot_output, eeg_analysis_output, final_answer_output, reasoning_output]
    )

if __name__ == "__main__":
    demo.launch()