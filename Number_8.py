import argparse


def main():
    parser = argparse.ArgumentParser()
    # Добавляем аргументы, которые могут принимать любые значения
    parser.add_argument('numbers', nargs='*', help='целочисленные параметры')

    try:
        parsed_args = parser.parse_args()
        numbers = parsed_args.numbers

        # Проверяем количество переданных параметров
        if len(numbers) == 0:
            print("NO PARAMS")
        elif len(numbers) == 1:
            print("TOO FEW PARAMS")
        elif len(numbers) > 2:
            print("TOO MANY PARAMS")
        else:
            # Пробуем преобразовать в целые числа и вычислить сумму
            num1 = int(numbers[0])
            num2 = int(numbers[1])
            result = num1 + num2
            print(result)

    except Exception as e:
        # В случае любых других ошибок выводим имя класса исключения
        print(type(e).__name__)


if __name__ == "__main__":
    main()