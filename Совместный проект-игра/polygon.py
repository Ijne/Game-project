name = 'level(0, 0).txt'
name_2 = 'level(-5, 0).txt'
name_3 = 'level(0, -5).txt'
x = name_2[name_2.find('(') + 1:name_2.find(',')].strip()
y = name_2[name_2.find(',') + 1:name_2.find(')')].strip()
print(x, y)
