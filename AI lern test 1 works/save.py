import os
import pickle

def save_experience(data, file="models/experience.pkl"):
    os.makedirs("models", exist_ok=True)
    with open(file, "wb") as f:
        pickle.dump(data, f)

def load_experience(file="models/experience.pkl"):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return pickle.load(f)
    return None
