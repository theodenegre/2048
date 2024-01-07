from copy import deepcopy
from math import ceil, log2
from random import randint, choice


def create_mat(size):
    return [[0 for _ in range(size)] for _ in range(size)]


class My2048:
    def __init__(self, size):
        self.won = False
        self.score = 0
        self.nbr_move = 0
        self.best_tile = 0
        self.size = size
        self.board = create_mat(self.size)
        self.last_matrice = deepcopy(self.board)
        self.start()

    def __str__(self):
        res = ""
        for y in range(self.size):
            for x in range(self.size):
                res += str(self.get_elem(x, y)) + " "
            res += "\n"
        return res

    def reset(self):
        self.board = create_mat(self.size)
        self.last_matrice = deepcopy(self.board)
        self.score = 0
        self.nbr_move = 0
        self.best_tile = 0
        self.start()

    def change_elem(self, x, y, val):
        self.board[y][x] = val

    def get_elem(self, x, y):
        return self.board[y][x]

    def spawn_number(self, fixedRandom=True):
        empty = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    empty.append((i, j))
        if len(empty) == 0:
            return
        if not fixedRandom:
            to_spawn = 2
            if randint(0, 9) == 0:  # 10% chance to spawn a 4
                to_spawn = 4
            x, y = choice(empty)
            self.change_elem(x, y, to_spawn)
        else:
            x, y = empty[(empty[self.size % len(empty)][0] * 2 + empty[int(log2(self.best_tile + 1)) % len(empty)][1] * 3) % len(empty)]
            to_spawn = 2
            if empty[0][0] % 2 and empty[-1][0] % 5:
                to_spawn = 4
            self.board[x][y] = to_spawn


    def start(self):
        for _ in range(ceil(self.size ** 0.5)):
            self.spawn_number()

    def move(self, d):
        temp = deepcopy(self.board)
        d = d.lower()
        dic = {"up": self.moveUp,
               "down": self.moveDown,
               "left": self.moveLeft,
               "right": self.moveRight}
        if d in dic:
            dic[d]()
            if temp != self.board:
                self.spawn_number()
                self.last_matrice = deepcopy(temp)
                self.nbr_move += 1
        else:
            raise ValueError("d must be in {Up, Down, Left, Right}")

    def moveUp(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    k = i - 1
                    while k >= 0 and self.board[k][j] == 0:
                        k -= 1
                    if k >= 0 and self.board[k][j] == self.board[i][j]:
                        self.board[k][j] *= 2
                        self.board[i][j] = 0
                        self.score += self.board[k][j]
                        self.best_tile = max(self.best_tile, self.board[k][j])
                    elif k + 1 != i:
                        self.board[k + 1][j] = self.board[i][j]
                        self.board[i][j] = 0

    def transpose(self):
        for i in range(self.size):
            for j in range(i, self.size):
                self.board[i][j], self.board[j][i] = self.board[j][i], \
                    self.board[i][j]

    def reverseLR(self):
        for ligne in self.board:
            ligne.reverse()

    def reverseUD(self):
        self.transpose()
        self.reverseLR()
        self.transpose()

    def moveDown(self):
        self.reverseUD()
        self.moveUp()
        self.reverseUD()

    def moveLeft(self):
        self.transpose()
        self.moveUp()
        self.transpose()

    def moveRight(self):
        self.reverseLR()
        self.moveLeft()
        self.reverseLR()

    def is_over(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0 or \
                        (i > 0 and self.board[i][j] == self.board[i - 1][j]) or \
                        (j > 0 and self.board[i][j] == self.board[i][j - 1]):
                    return False
        return True

    def is_win(self):
        if self.won:
            return True
        for line in self.board:
            if 2048 in line:
                self.won = True
                print("You won!")
                return True

    def rollback(self):
        self.board = deepcopy(self.last_matrice)
        self.last_matrice = deepcopy(self.board)

    def can_move(self, d):
        temp = deepcopy(self.board)
        d = d.lower()
        dic = {"up": self.moveUp,
               "down": self.moveDown,
               "left": self.moveLeft,
               "right": self.moveRight}
        if d in dic:
            dic[d]()
        else:
            raise ValueError("d must be in {Up, Down, Left, Right}")
        if temp != self.board:
            self.last_matrice = deepcopy(temp)
            return True
        return False


if __name__ == "__main__":
    game = My2048(4)
    game.board = \
        [[2, 2, 0, 0],
         [4, 0, 0, 0],
         [0, 0, 0, 0],
         [2, 0, 2, 0]]
    print(game)

    # for move in ["Down", "Left", "Up", "Right"]:
    #     game.move(move)
    #     print(game)
    #     print("Score:", game.score)
    #     print("")
    game.move("left")
    print(game)
