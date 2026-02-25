import numpy as np

def extract_features(signal, window_size):
    features = []

    for i in range(0, len(signal) - window_size, window_size):
        window = signal[i:i+window_size]

        mean = np.mean(window)
        std = np.std(window)
        energy = np.sum(window**2)

        features.append([mean, std, energy])

    return np.array(features)