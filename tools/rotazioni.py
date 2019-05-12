file = open('input.txt', 'r')

pezzo = eval(file.read())


def ruota(cosa):
    cosa1 = []
    for i in range(len(cosa)):
        riga = []
        for elem in cosa:
            riga.append(elem[len(elem) - 1 - i])
        cosa1.append(riga)
    return cosa1


if __name__ == '__main__':
    print('[' + str(pezzo), end=',\n     ')
    pezzo1 = ruota(pezzo)
    print(pezzo1, end=',\n     ')
    pezzo2 = ruota(pezzo1)
    print(pezzo2, end=',\n     ')
    pezzo3 = ruota(pezzo2)
    print(pezzo3, end=']\n')
    check = ruota(pezzo3)
    print('check:')
    print(check)