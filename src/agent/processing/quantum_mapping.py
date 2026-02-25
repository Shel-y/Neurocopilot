import numpy as np

def quantum_feature_map(features):
    mapped = []

    for f in features:
        x, y, z = f

        q1 = np.cos(x)
        q2 = np.sin(y)
        q3 = np.cos(z)
        q4 = np.sin(x * y)

        mapped.append([q1, q2, q3, q4])

    return np.array(mapped)