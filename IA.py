from random import choice
from UI import *

possible_moves = ["up", "down", "left", "right"]


def RandomIA():
    return choice(possible_moves)


def main(IA):
    init()
    while True:
        handle_win()
        handle_lose()
        move = IA()
        game.move(move)
        update()



if __name__ == '__main__':
    main(RandomIA)
    root.mainloop()
