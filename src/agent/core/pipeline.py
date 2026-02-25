from agent.simulation.eeg_simulator import (
    generate_time,
    generate_eeg_signal,
    add_anomaly,
    fs
)

from agent.processing.features import extract_features
from agent.processing.quantum_mapping import quantum_feature_map
from agent.models.anomaly_detector import (
    train_detector,
    detect_anomalies
)

from agent.config.settings import *


def run_analysis():

    t = generate_time()
    signal = generate_eeg_signal(t)

    signal = add_anomaly(
        signal,
        t,
        ANOMALY_TIME,
        ANOMALY_DURATION,
        ANOMALY_INTENSITY
    )

    window_size = int(fs * WINDOW_SECONDS)

    features = extract_features(signal, window_size)

    q_features = quantum_feature_map(features)

    model = train_detector(q_features)

    predictions = detect_anomalies(model, q_features)

    return predictions