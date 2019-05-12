from tetris import Timer, sleep, time

if __name__ == '__main__':
    t = Timer(1)
    print(time(), t.start)
    while 1:
        if t.elapsed():
            t.reset()
            print(t.start, time())
