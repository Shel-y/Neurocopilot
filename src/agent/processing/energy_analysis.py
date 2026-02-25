import numpy as np

def sliding_window_energy(signal, window_size):
    energies = []

    for i in range(0, len(signal) - window_size):
        window = signal[i:i+window_size]
        energy = np.sum(window**2)
        energies.append(energy)

    return np.array(energies)