from copy import deepcopy

import numpy as np
from time import sleep
import game
from UI import *
import tensorflow as tf

x = list()
y = list()


def get_playstyle(nbr_coups=100):
    init()
    x = list()
    y = list()
    for _ in range(nbr_coups):
        root.update()
        handle_lose()
        handle_win()
        root.wait_variable(pressed_key)
        x.append(deepcopy(game.board))
        game.move(pressed_key.get())
        y.append(pressed_key.get())
        pressed_key.set("")
        update()
    game.reset()
    return x, y


def build_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(4, activation='softmax')
    ])
    model.compile(optimizer='sgd',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model


def train_model(model, x_train, y_train):
    model.fit(x_train, y_train, epochs=50, batch_size=32)


def play_model(name: str):
    dico = {0: 'Up', 1: 'Down', 2: 'Left', 3: 'Right'}
    model = build_model()
    model.build((None, 4, 4))
    model.load_weights(f'{name}.h5')
    game.start()
    while True:
        root.update()
        handle_lose()
        handle_win()
        x = np.array([game.board])
        y = model.predict(x, verbose=0)[0]
        for move in sorted(enumerate(y), key=lambda a: a[1], reverse=True):
            if game.can_move(dico[move[0]]):
                game.move(dico[move[0]])
                break
        update()
        game.spawn_number()


def humain_train_model(name: str, nbr_coups=100, nbr_partie=3):
    dico = {'Up': 0, 'Down': 1, 'Left': 2, 'Right': 3}
    x, y = [], []
    for i in range(nbr_partie):
        a, b = get_playstyle(nbr_coups)
        x.extend(a)
        y.extend(b)
    model = build_model()
    model.build((None, game.size, game.size))
    train_model(model, x, [dico[i] for i in y])
    model.save_weights(f'{name}.h5')


def self_train_model(nbr_partie=20, style=None):  # Pas ouf
    dico = {0: 'Up', 1: 'Down', 2: 'Left', 3: 'Right'}
    model = build_model()
    model.build((None, game.size, game.size))
    if style is not None:
        model.load_weights(f'{style}.h5')
    init()
    for _ in range(nbr_partie):
        boards = list()
        moves = list()
        game.reset()
        while not game.is_over():
            root.update()
            handle_lose()
            handle_win()
            boards.append(deepcopy(game.board))
            for move in sorted(enumerate(
                    model.predict(np.array([game.board]), verbose=0)[0]),
                               key=lambda a: a[1],
                               reverse=True):
                if game.can_move(dico[move[0]]):
                    game.move(dico[move[0]])
                    moves.append(move[0])
                    break
            game.spawn_number()
            update()
        model.fit(np.array(boards), np.array(moves), epochs=len(boards),
                  batch_size=32)
    model.save_weights("self.h5")


if __name__ == "__main__":
    # self_train_model(style="theostyle")
    # humain_train_model("theostyle", nbr_coups=30, nbr_partie=1)
    play_model("theostyle")
