import random
from copy import deepcopy
import numpy as np
import game
from UI import *
import tensorflow as tf
import os


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


def self_train_model(nbr_partie=10, nbr_epoch=10):
    dico = {0: 'Up', 1: 'Down', 2: 'Left', 3: 'Right'}
    for epoch in range(nbr_epoch):
        print("Epoch :", epoch)
        best_score = 0
        best_nbr_move = 0
        best_model = None
        best_tile = 0
        best_x_y = None
        for i in range(nbr_partie):
            print("Game :", i)
            model = build_model()
            model.build((None, game.size, game.size))
            if os.path.exists('self.h5'):
                model.load_weights('self.h5')
            # modify a bit the weights
            if i == 0:
                change = 0
            elif i <= nbr_partie * 0.8:
                change = 10
            else:
                change = 100
            for layer in model.layers:
                if layer.name == 'dense':
                    for i in range(len(layer.get_weights()[0])):
                        for j in range(len(layer.get_weights()[0][i])):
                            layer.get_weights()[0][i][j] += random.normalvariate(-change, change)
            game.start()
            all_x = []
            all_y = []
            while not game.is_over():
                root.update()
                handle_lose()
                handle_win()
                x = np.array([game.board])
                y = model.predict(x, verbose=0)[0]
                all_x.append(x)
                for move in sorted(enumerate(y), key=lambda a: a[1],
                                   reverse=True):
                    if game.can_move(dico[move[0]]):
                        game.move(dico[move[0]])
                        all_y.append(move[0])
                        break
                update()
                game.spawn_number()
            if (game.score >= best_score and
                game.nbr_move >= best_nbr_move and
                game.best_tile >= best_tile) \
                    or game.score >= best_score * 1.75 \
                    or game.nbr_move >= best_nbr_move * 1.25 \
                    or game.best_tile >= best_tile * 1.25:
                print("New best score:", game.score)
                print("New best nbr move:", game.nbr_move)
                print("New best tile:", game.best_tile)
                best_score = game.score
                best_nbr_move = game.nbr_move
                best_tile = game.best_tile
                best_model = model
                best_x_y = (deepcopy(all_x), deepcopy(all_y))
            game.reset()
        train_model(best_model, np.array(best_x_y[0]), np.array(best_x_y[1]))
        best_model.save_weights(f'self.h5')
        print("Saved best model\n")
        print("Best score:", best_score)
        print("Best nbr move:", best_nbr_move)
        print("Best tile:", best_tile)


if __name__ == "__main__":
    self_train_model(10, 1000)
    # humain_train_model("theostyle", nbr_coups=30, nbr_partie=1)
    # play_model("theostyle")
