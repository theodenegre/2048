from random import choice
from UI import *

possible_moves = ["up", "down", "left", "right"]


def RandomIA():
    move = choice(possible_moves)
    if game.can_move(move):
        game.move(move)
        game.spawn_number()
        return


def firstStrart():
    for elem in possible_moves:
        if game.can_move(elem):
            game.move(elem)
            game.spawn_number()
            return


def heuristic():
    board = game.board
    size = game.size
    score = 0
    for i in range(size):
        for j in range(size):
            score += board[i][j]
            if i > 0:
                score -= abs(board[i][j] - board[i - 1][j])
            if i < size - 1:
                score -= abs(board[i][j] - board[i + 1][j])
            if j > 0:
                score -= abs(board[i][j] - board[i][j - 1])
            if j < size - 1:
                score -= abs(board[i][j] - board[i][j + 1])
    return score


def minimax(depth=8, maximizingPlayer=False):
    if depth == 0 or game.is_over():
        return heuristic()
    if maximizingPlayer:
        maxEval = -float("inf")
        for move in possible_moves:
            if game.can_move(move):
                game.move(move)
                eval = minimax(depth - 1, False)
                maxEval = max(maxEval, eval)
        return maxEval
    else:
        minEval = float("inf")
        for move in possible_moves:
            if game.can_move(move):
                game.move(move)
                eval = minimax(depth - 1, True)
                minEval = min(minEval, eval)
        return minEval


def minimaxIA():
    bestMove = ""
    bestScore = -float("inf")
    for move in possible_moves:
        if game.can_move(move):
            game.move(move)
            score = minimax(8, False)
            if score > bestScore:
                bestScore = score
                bestMove = move
    game.move(bestMove)


def main(IA):
    init()
    while True:
        handle_win()
        handle_lose()
        IA()
        update()



if __name__ == '__main__':
    main(minimaxIA)
    root.mainloop()
