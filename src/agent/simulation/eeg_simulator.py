import numpy as np

fs = 256

def generate_time():
    return np.linspace(0, 10, fs * 10)


def generate_eeg_signal(t):
    delta = np.sin(2 * np.pi * 2 * t)
    theta = 0.5 * np.sin(2 * np.pi * 6 * t)
    alpha = 0.8 * np.sin(2 * np.pi * 10 * t)
    beta = 0.3 * np.sin(2 * np.pi * 20 * t)

    noise = 0.2 * np.random.randn(len(t))

    return delta + theta + alpha + beta + noise


def add_anomaly(signal, t, start_sec, duration_sec, intensity):
    start = int(start_sec * fs)
    end = int((start_sec + duration_sec) * fs)

    anomaly = intensity * np.sin(2 * np.pi * 30 * t[start:end])
    signal[start:end] += anomaly

    return signal