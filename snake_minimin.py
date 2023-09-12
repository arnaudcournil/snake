class Model():
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height

    def predict(self, env, obs):
        return self.get_best_move(env.snake, env.apple)
    
    def get_possible_moves(self, snake):
        moves = (snake[0][0] + 1, snake[0][1]), (snake[0][0] - 1, snake[0][1]), (snake[0][0], snake[0][1] + 1), (snake[0][0], snake[0][1] - 1)
        for move in moves:
            if move not in snake and 0 <= move[0] < self.width and 0 <= move[1] < self.height:
                yield move

    def miniminEscape(self, snake, apple, depth = 10, nb_moves = 1, min_act = 1000, min_score = 100, malus = 0, onborder = False):
        if snake[0][0] == 0 or snake[0][0] == self.width - 1 or snake[0][1] == 0 or snake[0][1] == self.height - 1:
            if not onborder and not (abs(snake[0][0] - apple[0]) + abs(snake[0][1] - apple[1]) <= 1 and (apple[0] == 0 or apple[0] == self.width - 1 or apple[1] == 0 or apple[1] == self.height - 1)):
                malus += 1
            onborder = True
        else:
            onborder = False

        if snake[0][0] == apple[0] and snake[0][1] == apple[1]:
            min_score = min(min_score, nb_moves)
        if depth == 0:
            return min_score + malus
        canEscape = False
        for move in self.get_possible_moves(snake):
            canEscape = True
            snake_copy = snake.copy()
            snake_copy.insert(0, move)
            snake_copy.pop()
            next_depth = depth - 1
            min_act = min(min_act, self.miniminEscape(snake_copy, apple, next_depth, nb_moves + 1, min_act, min_score, malus, onborder))
        if not canEscape:
            return 1000
        return min_act + malus

    def sort_moves(self, snake, apple):
        moves = (snake[0][0] - 1, snake[0][1]), (snake[0][0] + 1, snake[0][1]), (snake[0][0], snake[0][1] - 1), (snake[0][0], snake[0][1] + 1)
        moves_dict = {}
        for move in moves:
            if move not in snake and 0 <= move[0] < self.width and 0 <= move[1] < self.height:
                moves_dict[move] = abs(apple[0] - move[0]) + abs(apple[1] - move[1])
        sorted_moves = sorted(moves_dict, key=moves_dict.get, reverse=False)
        return dict(zip(sorted_moves, [moves.index(move) for move in sorted_moves]))

    def get_best_move(self, snake, apple, depth = 10):
        min_act = 1001
        best_move = None
        for move, key in self.sort_moves(snake, apple).items():
            snake_copy = snake.copy()
            snake_copy.insert(0, move)
            snake_copy.pop()
            move_score = self.miniminEscape(snake_copy, apple, depth)
            if move_score < min_act:
                min_act = move_score
                best_move = key
        return best_move, min_act