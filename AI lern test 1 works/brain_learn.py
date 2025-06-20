from reversi import ReversiEnv
from brain import Brain

def train_and_save(total_timesteps=10000):
    env = ReversiEnv()
    brain = Brain(env)  # Will load existing if any
    brain.learn(total_timesteps=total_timesteps)  # Learn + auto save

if __name__ == "__main__":
    train_and_save()
