from keyboard import is_pressed
from random import randint
from time import time
import os


def clear():
    os.system('cls')


class Timer:
    def __init__(self, length, start=time()):
        self.length = length
        self.start = start

    def elapsed(self):
        return True if time() > self.start + self.length else False

    def reset(self, st=None):
        if st is None:
            st = time()
        self.start = st


class Piece:
    p = [[[1]],
         [[1]],
         [[1]],
         [[1]]]
    P = [[[1, 0], [1, 0]],
         [[0, 0], [1, 1]],
         [[0, 1], [0, 1]],
         [[1, 1], [0, 0]]]

    L = [[[0, 1, 0], [0, 1, 0], [0, 1, 1]],
         [[0, 0, 1], [1, 1, 1], [0, 0, 0]],
         [[1, 1, 0], [0, 1, 0], [0, 1, 0]],
         [[0, 0, 0], [1, 1, 1], [1, 0, 0]]]
    J = [[[0, 1, 0], [0, 1, 0], [1, 1, 0]],
         [[0, 0, 0], [1, 1, 1], [0, 0, 1]],
         [[0, 1, 1], [0, 1, 0], [0, 1, 0]],
         [[1, 0, 0], [1, 1, 1], [0, 0, 0]]]
    S = [[[0, 1, 1], [1, 1, 0], [0, 0, 0]],
         [[1, 0, 0], [1, 1, 0], [0, 1, 0]],
         [[0, 0, 0], [0, 1, 1], [1, 1, 0]],
         [[0, 1, 0], [0, 1, 1], [0, 0, 1]]]
    Z = [[[1, 1, 0], [0, 1, 1], [0, 0, 0]],
         [[0, 1, 0], [1, 1, 0], [1, 0, 0]],
         [[0, 0, 0], [1, 1, 0], [0, 1, 1]],
         [[0, 0, 1], [0, 1, 1], [0, 1, 0]]]
    T = [[[0, 0, 0], [1, 1, 1], [0, 1, 0]],
         [[0, 1, 0], [0, 1, 1], [0, 1, 0]],
         [[0, 1, 0], [1, 1, 1], [0, 0, 0]],
         [[0, 1, 0], [1, 1, 0], [0, 1, 0]]]

    O = [[[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
         [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
         [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
         [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]]
    I = [[[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]],
         [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]],
         [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]],
         [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]]

    def __init__(self, tipo, SIZE_X=10, SIZE_Y=20):
        self.SIZE_X = SIZE_X
        self.SIZE_Y = SIZE_Y
        self.nome = tipo
        self.tipo = 'Piece.' + tipo
        self.posizione = 0
        self.y = 0  # dall'alto
        self.x = self.SIZE_X//2-2  # da sinistra

    def ruota_sx(self):
        self.posizione += 1
        if self.posizione > 3:
            self.posizione = 0

    def ruota_dx(self):
        self.posizione -= 1
        if self.posizione < 0:
            self.posizione = 3

    def move_dx(self):
        self.x += 1

    def move_sx(self):
        self.x -= 1

    def move_down(self):
        self.y += 1

    def move_up(self):
        self.y -= 1

    def get(self):
        pezzo = eval(self.tipo)[self.posizione]
        griglia_ = []
        for y in range(self.SIZE_Y):
            t = []
            if y < self.y or y > self.y + len(pezzo) - 1:
                t = [0 for _ in range(self.SIZE_X)]
            else:
                for x in range(self.SIZE_X):
                    if x < self.x or x > self.x + len(pezzo[y - self.y]) - 1:
                        t.append(0)
                    else:
                        t.append(1 if pezzo[y - self.y][x - self.x] else 0)
            griglia_.append(t)
        return griglia_

    def copy(self):
        new_piece = Piece(self.nome, self.SIZE_X, self.SIZE_Y)
        new_piece.posizione = self.posizione
        new_piece.y = self.y
        new_piece.x = self.x
        return new_piece

    __call__ = get


class Game:
    @staticmethod
    def random():
        index = ['L', 'J', 'I', 'O', 'T', 'S', 'Z']  # tirare fuori se serve
        return index[randint(0, 6)]

    def __init__(self, SIZE_X=10, SIZE_Y=20):
        self.SIZE_X = SIZE_X
        self.SIZE_Y = SIZE_Y
        self.griglia = [[0 for _ in range(SIZE_X)] for __ in range(SIZE_Y)]
        self.pezzo = Piece(Game.random(), self.SIZE_X, self.SIZE_Y)
        self.next = Piece(Game.random(), self.SIZE_X, self.SIZE_Y)
        self.timer_pezzi = Timer(0.5)
        self.timer_refresh = Timer(0.02)
        self.timer_tasti = Timer(0.07)
        self.lines = 0
        self.points = 0
        self.level = 1

    def can_move_down(self):
        if 1 in self.pezzo.get()[self.SIZE_Y - 1]:
            return False
        self.pezzo.move_down()
        for y in range(self.SIZE_Y):
            for x in range(self.SIZE_X):
                if self.pezzo.get()[y][x] and self.griglia[y][x]:
                    self.pezzo.move_up()
                    return False
        self.pezzo.move_up()
        return True

    def can_move_right(self):
        if 1 in [x[self.SIZE_X-1] for x in self.pezzo.get()]:
            return False
        self.pezzo.move_dx()
        for y in range(self.SIZE_Y):
            for x in range(self.SIZE_X):
                if self.pezzo.get()[y][x] and self.griglia[y][x]:
                    self.pezzo.move_sx()
                    return False
        self.pezzo.move_sx()
        return True

    def can_move_lef(self):
        if 1 in [x[0] for x in self.pezzo.get()]:
            return False
        self.pezzo.move_sx()
        for y in range(self.SIZE_Y):
            for x in range(self.SIZE_X):
                if self.pezzo.get()[y][x] and self.griglia[y][x]:
                    self.pezzo.move_dx()
                    return False
        self.pezzo.move_dx()
        return True

    def can_rotate_right(self):
        a = sum(self.pezzo.get(), []).count(1)
        self.pezzo.ruota_dx()
        for y in range(self.SIZE_Y):
            for x in range(self.SIZE_X):
                if self.pezzo.get()[y][x] and self.griglia[y][x]:
                    self.pezzo.ruota_sx()
                    return False
        b = sum(self.pezzo.get(), []).count(1)
        self.pezzo.ruota_sx()
        if b < a:
            return False
        return True

    def can_rotate_left(self):
        a = sum(self.pezzo.get(), []).count(1)
        self.pezzo.ruota_sx()
        for y in range(self.SIZE_Y):
            for x in range(self.SIZE_X):
                if self.pezzo.get()[y][x] and self.griglia[y][x]:
                    self.pezzo.ruota_dx()
                    return False
        b = sum(self.pezzo.get(), []).count(1)
        self.pezzo.ruota_dx()
        if b < a:
            return False
        return True

    def lock(self):
        griglia = []
        lines = 0
        for y in range(self.SIZE_Y):
            riga = []
            for x in range(self.SIZE_X):
                riga.append(1 if self.griglia[y][x] or self.pezzo.get()[y][x] else 0)
            griglia.append(riga)
        while [1 for x in range(self.SIZE_X)] in griglia:
            griglia.remove([1 for x in range(self.SIZE_X)])
            lines += 1
        while len(griglia) < self.SIZE_Y:
            griglia = [[0 for x in range(self.SIZE_X)]] + griglia
        self.griglia = griglia
        self.pezzo = self.next.copy()
        self.next = Piece(Game.random(), self.SIZE_X, self.SIZE_Y)
        self.lines += lines
        self.points += int(400 * (lines**2 / 4) * self.level)
        # TODO: aggiornare livello, e in caso il timer

    def move_down(self):
        if self.can_move_down():
            self.pezzo.move_down()
        else:
            self.lock()

    def move_right(self):
        if self.can_move_right():
            self.pezzo.move_dx()

    def move_left(self):
        if self.can_move_lef():
            self.pezzo.move_sx()

    def ruota_dx(self):
        if self.can_rotate_right():
            self.pezzo.ruota_dx()

    def ruota_sx(self):
        if self.can_rotate_left():
            self.pezzo.ruota_sx()

    def genera_frame(self):
        clear()
        for y in range(self.SIZE_Y):
            print('|', end='')
            for x in range(self.SIZE_X):
                print(chr(9608) * 2 if self.griglia[y][x] or self.pezzo.get()[y][x] else chr(9594) + chr(9592), end='')
            if y == 1:
                print('|    points: ' + str(self.points))
            elif y == 4:
                print('|    lines: ' + str(self.lines))
            elif y >= 7:
                print('|   ', end='')
                for x in range(self.SIZE_X):
                    print(chr(9608) * 2 if self.next.get()[y-7][x] else '  ', end='')
                print()
            else:
                print('|')
        print('+' + '-' * self.SIZE_X*2 + '+')
        # TODO: print level

    def __call__(self):
        self.timer_tasti.reset()
        self.timer_pezzi.reset()
        self.timer_refresh.reset()
        pressable_up = False
        while True:
            if self.timer_tasti.elapsed():
                if is_pressed('LEFT'):
                    self.move_left()
                    self.timer_tasti.reset()
                if is_pressed('RIGHT'):
                    self.move_right()
                    self.timer_tasti.reset()
                if is_pressed('DOWN'):
                    self.move_down()
                    self.timer_tasti.reset()
                if is_pressed('UP') and pressable_up:
                    self.ruota_dx()
                    self.timer_tasti.reset()
            pressable_up = not is_pressed('UP')
            if self.timer_refresh.elapsed():
                self.timer_refresh.reset()
                self.genera_frame()
            if self.timer_pezzi.elapsed():
                self.timer_pezzi.reset()
                self.move_down()


if __name__ == '__main__':
    Game()()
