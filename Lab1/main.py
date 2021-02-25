import numpy as np


def count_a(var):   # Функция подсчета матрицы А

    c = np.array([(0.2, 0, 0.2, 0, 0),
                  (0, 0.2, 0, 0.2, 0),
                  (0.2, 0, 0.2, 0, 0.2),
                  (0, 0.2, 0, 0.2, 0),
                  (0, 0, 0.2, 0, 0.2)])

    d = np.array([(2.33, 0.81, 0.67, 0.92, -0.53),
                  (-0.53, 2.33, 0.81, 0.67, 0.92),
                  (0.92, -0.53, 2.33, 0.81, 0.67),
                  (0.67, 0.92, -0.53, 2.33, 0.81),
                  (0.81, 0.67, 0.92, -0.53, 2.33)])

    a = var * c + d
    a = np.c_[a, np.repeat([4.2], 5)]
    return a


def gauss_solve(a, n):  # Функция решения методом Гаусса

    b = np.zeros(n)

    for i in range(n):              # Прямой ход
        if a[i][i] == 0.00:
            raise ZeroDivisionError()
        for j in range(i + 1, n):
            q = a[j][i] / a[i][i]       # Вычисление множителя i-го шага
            for k in range(n + 1):
                a[j][k] = a[j][k] - q * a[i][k]     # Вычисление новых элементов строк

    b[n - 1] = a[n - 1][n] / a[n - 1][n - 1]    # Нахождение первого корня

    for i in range(n - 2, -1, -1):      # Обратный ход
        b[i] = a[i][n]
        for j in range(i + 1, n):
            b[i] = b[i] - a[i][j] * b[j]
        b[i] = b[i] / a[i][i]

    print('\nРешение системы уравнений методом Гаусса: ')
    for i in range(n):
        print(f"X[{i+1}]={round(b[i], 2)}")


def main():
    try:
        var = input("Введите вариант: ")
        var = int(var)
        a = count_a(var)
        gauss_solve(a.copy(), 5)
    except ZeroDivisionError:
        print("Деление на ноль!")
    except ValueError:
        print("Введите число!")


main()

