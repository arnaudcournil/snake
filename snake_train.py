import gym
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from snake_gym import SnakeEnv  # Assuming your environment is in a file named snake_env.py
import random
from snake_ppo import Model

# Create a function to preprocess observations
def preprocess_observation(observation):
    return observation.astype(np.float32) / 10.0  # Normalize the observation values

# Create a SnakeEnv instance
env = SnakeEnv(width=10, height=10)

# Wrap the environment in a DummyVecEnv
dummyEnv = DummyVecEnv([lambda: env])

# Preprocess the environment observation space

bestMeanScore = 0
while True:
    learning_rate = float(3) / (10 ** random.randint(3, 6))
    model = PPO.load("snake_ppo_model_v2", env=dummyEnv, learning_rate = learning_rate, verbose = 1) # PPO("MlpPolicy", dummyEnv, verbose=1)
    test_model = Model()
    distance = 0
    meanScore = 0
    #bestScore = 0
    nbEssais = 1
    while nbEssais < 100:
        obs = env.reset()
        while True:
            action, _ = test_model.predict(env, obs)
            obs, reward, done, _ = env.step(action)
            nb_pommes = len(env.snake)
            #bestScore = max(bestScore, nb_pommes)
            distance += 1
            #env.render()
            #print("Score:", nb_pommes, "Best score:", bestScore, "Essai:", nbEssais, "Mean score:", meanScore)
            if done:
                meanScore = (meanScore * (nbEssais - 1) + nb_pommes) / nbEssais
                nbEssais += 1
                if nbEssais % 10 == 0:
                    print(nbEssais, meanScore)
                break
    print(meanScore, bestMeanScore)
    if meanScore > bestMeanScore:
        bestMeanScore = meanScore
        # Save the trained model
        model.save("snake_ppo_model_v2")
        
    # Create and train the PPO agent
    model.learn(total_timesteps=int(1e5), progress_bar=True)  # You can adjust the number of timesteps
    



# Load the trained model
# loaded_model = PPO.load("snake_ppo_model")

# Test the trained model
obs = env.reset()
while True:
    action, _ = model.predict(preprocess_observation(obs))
    obs, reward, done, _ = env.step(action)
    env.render()
    if done:
        break

env.close()
