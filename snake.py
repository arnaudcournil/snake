import numpy as np
import os

width = 10
height = 10
max_depth = 10

meanScore = 0
bestScore = 0
nbEssais = 1

def print_board(apple, snake):
    os.system("cls")
    board = np.zeros((width, height), dtype=int)
    board[apple[0], apple[1]] = -1
    board[snake[0][0], snake[0][1]] = 2
    for x, y in snake[1:]:
        board[x, y] = 1
    print("##" * (width + 2) + "#")
    for y in range(height):
        for x in range(width):
            if x == 0:
                print("##", end="")
            if board[x, y] == 0:
                print("  ", end="")
            elif board[x, y] == -1:
                print(" o", end="")
            elif board[x, y] == 1:
                print(" x", end="")
            elif board[x, y] == 2:
                print(" X", end="")
            if x == width - 1:
                print(" ##", end="")
        print()
    print("##" * (width + 2) + "#")

def get_possible_moves(snake):
    moves = (snake[0][0] + 1, snake[0][1]), (snake[0][0] - 1, snake[0][1]), (snake[0][0], snake[0][1] + 1), (snake[0][0], snake[0][1] - 1)
    for move in moves:
        if move not in snake and 0 <= move[0] < width and 0 <= move[1] < height:
            yield move

def miniminEscape(snake, apple, depth = 10, nb_moves = 1, min_act = 1000, min_score = 100, malus = 0, onborder = False):
    if snake[0][0] == 0 or snake[0][0] == width - 1 or snake[0][1] == 0 or snake[0][1] == height - 1:
        if not onborder and not (abs(snake[0][0] - apple[0]) + abs(snake[0][1] - apple[1]) <= 1 and (apple[0] == 0 or apple[0] == width - 1 or apple[1] == 0 or apple[1] == height - 1)):
            malus += 1
        onborder = True
    else:
        onborder = False

    if snake[0][0] == apple[0] and snake[0][1] == apple[1]:
        min_score = min(min_score, nb_moves)
    if depth == 0:
        return min_score + malus
    canEscape = False
    for move in get_possible_moves(snake):
        canEscape = True
        snake_copy = snake.copy()
        snake_copy.insert(0, move)
        snake_copy.pop()
        next_depth = depth - 1
        min_act = min(min_act, miniminEscape(snake_copy, apple, next_depth, nb_moves + 1, min_act, min_score, malus, onborder))
    if not canEscape:
        return 1000
    return min_act + malus

def sort_moves(snake, apple):
    moves = (snake[0][0] + 1, snake[0][1]), (snake[0][0] - 1, snake[0][1]), (snake[0][0], snake[0][1] + 1), (snake[0][0], snake[0][1] - 1)
    moves_dict = {}
    for move in moves:
        if move not in snake and 0 <= move[0] < width and 0 <= move[1] < height:
            moves_dict[move] = abs(apple[0] - move[0]) + abs(apple[1] - move[1])
    return sorted(moves_dict, key=moves_dict.get, reverse=False)

def get_best_move(snake, apple, depth = 10):
    min_act = 1001
    best_move = None
    for move in sort_moves(snake, apple):
        snake_copy = snake.copy()
        snake_copy.insert(0, move)
        snake_copy.pop()
        move_score = miniminEscape(snake_copy, apple, depth)
        if move_score < min_act:
            min_act = move_score
            best_move = move
    return best_move, min_act

while bestScore < width * height:
    nb_pommes = 3
    snake = [(0, 2), (0, 1), (0, 0)]
    apple = np.array([np.random.randint(0, width), np.random.randint(0, height)], dtype=int)
    while list(apple) in snake:
        apple[0] = np.random.randint(0, width)
        apple[1] = np.random.randint(0, height)
    print_board(apple, snake)
    print("First move")
    print("Score:", nb_pommes, "Best score:", bestScore, "Essai:", nbEssais, "Mean score:", meanScore)
    while True:
        move, nb_moves = get_best_move(snake, apple, max_depth)
        if nb_moves == 1001:   
            meanScore = (meanScore * (nbEssais - 1) + nb_pommes) / nbEssais
            if nb_pommes >= width * height:
                print_board(apple, snake)
                print(nb_moves)
                print("Score:", nb_pommes, "Best score:", bestScore, "Essai:", nbEssais, "Mean score:", meanScore)
                print("Good Job ! You won !")
            else:
                print("Game over")
                nbEssais += 1
            break
        snake.insert(0, move)
        if snake[0][0] != apple[0] or snake[0][1] != apple[1]:
            snake.pop()
        print_board(apple, snake)
        print(nb_moves)
        print("Score:", nb_pommes, "Best score:", bestScore, "Essai:", nbEssais, "Mean score:", meanScore)
        if snake[0][0] == apple[0] and snake[0][1] == apple[1]:
            nb_pommes += 1
            apple[0] = np.random.randint(0, width)
            apple[1] = np.random.randint(0, height)
            while list(apple) in snake:
                apple[0] = np.random.randint(0, width)
                apple[1] = np.random.randint(0, height)
            bestScore = max(bestScore, nb_pommes)