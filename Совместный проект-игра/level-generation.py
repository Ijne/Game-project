import random

x_list = random.sample(range(0, 31), 30)
y_list = random.sample(range(0, 31), 30)
coord = []
for i in range(30):
    s = []
    for j in range(30):
        s.append((x_list[i], y_list[j]))
    coord.append(s)

for x in range(-7, 8):
    print(x)
    for y in range(-7, 8):
        output = []
        for i in range(len(coord)):
            s = ''
            T = 0
            S = 0
            G = 0
            C = 0
            H = 0
            M = 0
            B = 0
            for j in range(len(coord[i])):
                r = random.randrange(-5, 16, 1)
                if r <= 10:
                    s += '0'
                elif r == 11 and S < 2:
                    s += 'S'
                    S += 1
                elif r == 13 and T < 1:
                    if -5 < x < 5 and -5 < y < 5:
                        s += 'T'
                        T += 1
                    else:
                        s += 't'
                        T += 1
                elif r == 12 and G < 2:
                    if -5 < x < 5 and -5 < y < 5:
                        s += 'G'
                        G += 1
                    else:
                        s += 'g'
                        G += 1
                elif r == 14 and S > 1:
                    if -5 < x < 5 and -5 < y < 5:
                        s += 'C'
                        C += 1
                    else:
                        s += 'M'
                        M += 1
                elif r == 15 and G > 1:
                    if -5 < x < 5 and -5 < y < 5:
                        s += 'H'
                        H += 1
                    else:
                        s += 'B'
                        B += 1
                else:
                    s += '0'
            output.append(s + '\n')

        filename = 'data/levels/default/' + f'level({x}, {y}).txt'
        mapFile = open(filename, 'w+')
        mapFile.writelines(output)
        mapFile.close()
