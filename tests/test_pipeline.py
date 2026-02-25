from agent.core.pipeline import run_analysis


def test_pipeline_runs():
    predictions = run_analysis()

    assert predictions is not None
    assert len(predictions) > 0