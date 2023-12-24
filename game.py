from copy import deepcopy
from math import ceil
from random import randint


def create_mat(size):
    return [[0 for _ in range(size)] for _ in range(size)]


class My2048:
    def __init__(self, size):
        self.size = size
        self.board = create_mat(self.size)
        self.last_matrice = deepcopy(self.board)
        self.start()
        self.won = False
        self.score = 0

    def __str__(self):
        res = ""
        for y in range(self.size):
            for x in range(self.size):
                res += str(self.get_elem(x, y)) + " "
            res += "\n"
        return res

    def change_elem(self, x, y, val):
        self.board[y][x] = val

    def get_elem(self, x, y):
        return self.board[y][x]

    def spawn_number(self):
        x, y = randint(0, self.size - 1), randint(0, self.size - 1)
        while self.get_elem(x, y) != 0:
            x, y = randint(0, self.size - 1), randint(0, self.size - 1)
        self.change_elem(x, y, 2)

    def start(self):
        for _ in range(ceil(self.size ** 0.5)):
            self.spawn_number()

    def move(self, d):
        d = d.lower()
        if d == "up":
            self.moveUp()
        elif d == "down":
            self.moveDown()
        elif d == "left":
            self.moveLeft()
        elif d == "right":
            self.moveRight()
        else:
            raise ValueError("d must be in {Up, Down, Left, Right}")
        if self.last_matrice != self.board:
            self.spawn_number()
            self.last_matrice = deepcopy(self.board)

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
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 2048:
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

    for move in ["Down", "Left", "Up", "Right"]:
        game.move(move)
        print(game)
        print("Score:", game.score)
        print("")
