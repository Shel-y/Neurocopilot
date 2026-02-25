"""
Visualization utilities.
Kept independent from processing logic.
"""

import matplotlib.pyplot as plt


def plot_signal(time, signal, title="EEG Signal"):
    plt.figure(figsize=(10, 4))
    plt.plot(time, signal)
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.show()


def plot_predictions(predictions):
    plt.figure(figsize=(10, 3))
    plt.plot(predictions, marker="o")
    plt.title("Anomaly Detection")
    plt.show()