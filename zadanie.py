print("Пожалуйста, введите 3 числа через пробел:")
chisla = input()

kount = 0

for i in chisla.split(' '):
    if int(i) < 0:
        kount += 1
print("Количество отрицательных чисел:", kount)