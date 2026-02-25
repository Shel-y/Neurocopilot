from sklearn.ensemble import IsolationForest

def train_detector(features):
    model = IsolationForest(contamination=0.1)
    model.fit(features)
    return model


def detect_anomalies(model, features):
    return model.predict(features)