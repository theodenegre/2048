from tkinter import *

from game import My2048

root = Tk()
root.title("2048")
WIDTH = 780
HEIGHT = 780
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)
root.config(bg="#faf8ef")

colors = {
    0   : "#cdc1b4",
    2   : "#eee4da",
    4   : "#ede0c8",
    8   : "#f2b179",
    16  : "#f59563",
    32  : "#f67c5f",
    64  : "#f65e3b",
    128 : "#edcf72",
    256 : "#edcc61",
    512 : "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
    4096: "#3c3a32"
}

game = My2048(size=4)
game.start()


def init():
    for i in range(game.size):
        for j in range(game.size):
            padding = 5
            frame = Frame(root,
                          width=(WIDTH - (2 * game.size * padding)) / game.size,
                          height=(HEIGHT - (2 * game.size * padding)) / game.size,
                          bg=colors[game.board[i][j]])
            frame.grid(row=i, column=j, padx=5, pady=5)
            label = Label(frame, text=game.board[i][j],
                          font=("Arial", 40, "bold"),
                          bg=colors[game.board[i][j]], fg="#776e65")
            label.place(relx=0.5, rely=0.5, anchor=CENTER)


def on_key_press(event):
    pressed_key.set(event.keysym)


def handle_lose():
    if game.is_over():
        print("Game Over")
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
                          height=(HEIGHT - (2 * game.size * padding)) / game.size,
                          bg=colors[game.board[i][j]])
            frame.grid(row=i, column=j, padx=5, pady=5)
            label = Label(frame, text=game.board[i][j],
                          font=("Arial", 40, "bold"),
                          bg=colors[game.board[i][j]], fg="#776e65")
            label.place(relx=0.5, rely=0.5, anchor=CENTER)
    root.update()


def rollback():
    game.rollback()
    update()


def handle_win():
    if game.is_win():
        print("You win")


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
