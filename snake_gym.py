import gym
from gym import spaces
import numpy as np
import os

class SnakeEnv(gym.Env):
    def __init__(self, width=10, height=10):
        super(SnakeEnv, self).__init__()

        self.width = width
        self.height = height

        self.snake = [(0, 2), (0, 1), (0, 0)]  # Initial position of the snake
        self.apple = np.array([np.random.randint(0, width), np.random.randint(0, height)], dtype=int)   # Initial position of the food
        self.direction = (0, 1)  # Initial direction of the snake

        self.action_space = spaces.Discrete(4)  # Four possible actions: 0=up, 1=down, 2=left, 3=right
        self.observation_space = spaces.Box(low=0, high=1, shape=((self.height * 2 - 1) * 3, self.width * 2 - 1), dtype=np.uint8)

    def reset(self):
        self.snake = [(0, 2), (0, 1), (0, 0)]
        self.apple = self._generate_apple()
        self.direction = (0, 1)
        return self._get_observation()

    def step(self, action):
        # Update snake direction based on action
        if action == 0 and self.direction != (1, 0):  # Left
            self.direction = (-1, 0)
        elif action == 1 and self.direction != (-1, 0):  # Right
            self.direction = (1, 0)
        elif action == 2 and self.direction != (0, 1):   # Up
            self.direction = (0, -1)
        elif action == 3 and self.direction != (0, -1):  # Down
            self.direction = (0, 1)

        # Move snake
        new_position = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])

        # Check if snake hits wall or itself
        if self._is_collision(new_position) or not (0 <= new_position[0] < self.height) or not (0 <= new_position[1] < self.width):
            reward = -5
            done = True
        else:
            self.snake = [new_position] + self.snake
            if new_position[0] == self.apple[0] and new_position[1] == self.apple[1]:
                reward = 2
                self.apple = self._generate_apple()
            else:
                reward = 0 #1
                self.snake = self.snake[:-1]
            done = False

        if (action == 0 and self.direction == (1, 0)) or (action == 1 and self.direction == (-1, 0)) or (action == 2 and self.direction == (0, 1)) or (action == 3 and self.direction == (0, -1)):
            reward -= -1

        return self._get_observation(), reward, done, {}

    def _generate_apple(self):
        apple = np.array([np.random.randint(0, self.width), np.random.randint(0, self.height)], dtype=int)
        while list(apple) in self.snake:
            apple = np.array([np.random.randint(0, self.width), np.random.randint(0, self.height)], dtype=int)
        return apple

    def _is_collision(self, position):
        return position in self.snake

    def _get_observation(self):
        observation = np.zeros(((self.height * 2 - 1) * 3, (self.width * 2 - 1)), dtype=np.uint8)
        # First observation : snake in all map
        """
            observation[self.snake[0][0]][self.snake[0][1]] = 2
            for body_part in self.snake[1:]:
                observation[body_part[0]][body_part[1]] = 1
        """
        observation[self.height -1][self.width -1] = 3 # Head
        for body_part in self.snake[1:-1]:
            observation[body_part[0] - self.snake[0][0] + self.height -1][body_part[1] - self.snake[0][1] + self.width -1] = 2 # Body
        observation[self.snake[-1][0] - self.snake[0][0] + self.height -1][self.snake[-1][1] - self.snake[0][1] + self.width -1] = 1 # Tail

        # Second observation layer: apple in all map
        observation[self.apple[0] - self.snake[0][0] + self.height * 2 -1][self.apple[1] - self.snake[0][1] + self.width -1] = 1

        # Third observation layer: bordures centered
        for x in range(self.width * 2 - 1):
            for y in range(self.height * 2 - 1):
                if y < self.height - self.snake[0][0] -1 or y > 2 * self.height - self.snake[0][0] -1 or x < self.width - self.snake[0][1] -1 or x > 2 * self.width - self.snake[0][1] -1:
                    observation[(self.height * 2 - 1) * 2 + y][x] = 1
        
        return observation

    def render(self, mode='human'):
        os.system("cls")
        print("##" * (self.width + 2) + "#")
        for y in range(self.height):
            for x in range(self.width):
                if x == 0:
                    print("##", end="")                    
                if [self.apple[0], self.apple[1]] == [x, y]:
                    print(" o", end="")
                elif [self.snake[0][0], self.snake[0][1]] == [x, y]:
                    print(" X", end="")
                elif (x, y) in self.snake:
                    print(" x", end="")
                else:
                    print("  ", end="")
                if x == self.width - 1:
                    print(" ##", end="")
            print()
        print("##" * (self.width + 2) + "#")

    def close(self):
        pass