from stable_baselines3 import PPO
import numpy as np

class Model():  
    def predict(self, env, obs):
        return PPO.load("snake_ppo_model_v2").predict(self.preprocess_observation(obs))
    
    def preprocess_observation(self, observation):
        return observation.astype(np.float32) / 10.0  # Normalize the observation values