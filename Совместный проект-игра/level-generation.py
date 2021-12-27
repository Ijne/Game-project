import random

x_list = random.sample(range(0, 21), 20)
y_list = random.sample(range(0, 21), 20)
coord = []
for i in range(20):
    s = []
    for j in range(20):
        s.append((x_list[i], y_list[j]))
    coord.append(s)

for x in range(-5, 6):
    print(x)
    for y in range(-5, 6):
        output = []
        for i in range(len(coord)):
            s = ''
            T = 0
            S = 0
            G = 0
            C = 0
            for j in range(len(coord[i])):
                r = random.randrange(0, 15, 1)
                if r <= 10:
                    s += '0'
                elif r == 11 and S < 2:
                    s += 'S'
                    S += 1
                elif r == 13 and T < 1:
                    s += 'T'
                    T += 1
                elif r == 12 and G < 2:
                    s += 'G'
                    G += 1
                elif r == 14 and C < 1 and S > 1:
                    s += 'C'
                    C += 1
                else:
                    s += '0'
            output.append(s + '\n')

        filename = 'data/levels/default/' + f'level({x}, {y}).txt'
        mapFile = open(filename, 'w+')
        mapFile.writelines(output)
        mapFile.close()
