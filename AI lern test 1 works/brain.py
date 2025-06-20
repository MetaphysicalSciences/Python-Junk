from stable_baselines3 import PPO
import os

class Brain:
    def __init__(self, env, model_path="models/reversi_ai"):
        self.model_path = model_path
        if os.path.exists(model_path + ".zip"):
            print("Loading existing model...")
            self.model = PPO.load(model_path, env=env)
        else:
            print("Creating new model...")
            self.model = PPO("MlpPolicy", env, verbose=1)

    def predict(self, obs):
        action, _ = self.model.predict(obs, deterministic=True)
        return action

    def learn(self, total_timesteps=5000):
        self.model.learn(total_timesteps=total_timesteps)
        self.save()  # Auto save after training

    def save(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        self.model.save(self.model_path)
        print(f"Model saved to {self.model_path}")

    def load(self):
        if os.path.exists(self.model_path + ".zip"):
            self.model = PPO.load(self.model_path)
            print("Model loaded")
        else:
            print("No saved model to load")
