from tkinter import *

from game import My2048

root = Tk()
root.title("2048")
WIDTH = HEIGHT = 500
root.geometry(f"{WIDTH}x{HEIGHT}")
root.config(bg="#FBC02D")

colors = {
    0: "#cdc1b4",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
    4096: "#3c3a32"
}
mycolors = {
    0: "#F9A825",
    2: "#FF8F00",
    4: "#F57F17",
    8: "#FF6F00",
    16: "#FFA000",
    32: "#E65100",
    64: "#FF7043",
    128: "#FF5722",
    256: "#D84315",
    512: "#F44336",
    1024: "#C62828",
    2048: "#BF360C"
}

game = My2048(size=4)
game.start()


def init():
    for i in range(game.size):
        for j in range(game.size):
            padding = 5
            frame = Frame(root,
                          width=(WIDTH - (2 * game.size * padding)) / game.size,
                          height=(HEIGHT - (
                                      2 * game.size * padding)) / game.size,
                          bg=mycolors[game.board[i][j]])
            frame.grid(row=i, column=j, padx=5, pady=5)
            if game.board[i][j] != 0:
                label = Label(frame, text=game.board[i][j],
                              font=("Arial", 40, "bold"),
                              bg=mycolors[game.board[i][j]], fg="#776e65")
                label.place(relx=0.5, rely=0.5, anchor=CENTER)


def on_key_press(event):
    pressed_key.set(event.keysym)


def handle_lose():
    if game.is_over():
        print("Game Over")
        print("Score:", game.score)
        maxx = 0
        for line in game.board:
            for elem in line:
                maxx = max(maxx, elem)
        print("Max:", maxx)
        game.reset()
        game.start()
        update()


def update():  # Bug at random moments
    for widget in root.winfo_children():
        if isinstance(widget, Frame) or isinstance(widget, Label):
            widget.destroy()
    for i in range(game.size):
        for j in range(game.size):
            padding = 5
            frame = Frame(root,
                          width=(WIDTH - (2 * game.size * padding)) / game.size,
                          height=(HEIGHT - (
                                      2 * game.size * padding)) / game.size,
                          bg=mycolors[game.board[i][j]])
            frame.grid(row=i, column=j, padx=5, pady=5)
            if game.board[i][j] != 0:
                label = Label(frame, text=game.board[i][j],
                              font=("Arial", 40, "bold"),
                              bg=mycolors[game.board[i][j]], fg="#776e65")
                label.place(relx=0.5, rely=0.5, anchor=CENTER)
    root.update()


def rollback():
    game.rollback()
    update()


def handle_win():  # TODO
    game.is_win()


pressed_key = StringVar()
# add rollback in menu
menubar = Menu(root)
menubar.add_command(label="Rollback", command=rollback)
root.config(menu=menubar)

root.bind("<Key>", on_key_press)


def main():
    init()
    while True:
        root.update()
        handle_lose()
        handle_win()
        root.wait_variable(pressed_key)
        game.move(pressed_key.get())
        pressed_key.set("")
        update()


if __name__ == "__main__":
    main()
    print("test")
    root.mainloop()
