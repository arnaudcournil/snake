from snake_gym import SnakeEnv  # Assuming your environment is in a file named snake_env.py
#from snake_ppo import Model
from snake_minimin import Model

width = 10
height = 10
max_depth = 10

meanScore = 0
bestScore = 0
nbEssais = 1

env = SnakeEnv(width, height)
model = Model()

while bestScore < width * height:
    obs = env.reset()
    while True:
        action, _ = model.predict(env, obs)
        obs, reward, done, _ = env.step(action)
        nb_pommes = len(env.snake)
        bestScore = max(bestScore, nb_pommes)
        env.render()
        print("Score:", nb_pommes, "Best score:", bestScore, "Essai:", nbEssais, "Mean score:", meanScore)
        if done:
            meanScore = (meanScore * (nbEssais - 1) + nb_pommes) / nbEssais
            nbEssais += 1
            if nb_pommes == width * height:
                print("Victoire !")
            else:
                print("Défaite !")
            break

env.close()