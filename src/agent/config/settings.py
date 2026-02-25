"""
Global configuration for Neurocopilot.
Centralizes parameters to avoid magic numbers.
"""

# EEG PARAMETERS
SAMPLE_RATE = 256
WINDOW_SECONDS = 0.5

# SIMULATION
ANOMALY_TIME = 4
ANOMALY_DURATION = 1
ANOMALY_INTENSITY = 2

# MODEL
RANDOM_STATE = 42

# AGENT
MODEL_NAME = "local"