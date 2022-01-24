top = (hero.position[0] % 10,  hero.position[1] % 10)
bottom = (top[0] + 20,  top[1] + 20)
veiw_field = []
for x in range(top[x], bottom[x] + 1):
    column = []
    for y in range(top[y], bottom[y] + 1):
        column.append(board.field[x][y])
    view_field.apppend(column)

