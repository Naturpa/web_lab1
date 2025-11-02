import argparse


def main():
    parser = argparse.ArgumentParser()

    # Добавляем позиционный аргумент, который принимает любое количество значений
    parser.add_argument('args', nargs='*', help='произвольные аргументы')

    # Парсим аргументы
    parsed_args = parser.parse_args()

    # Проверяем, есть ли аргументы
    if parsed_args.args:
        for arg in parsed_args.args:
            print(arg)
    else:
        print("no args")


if __name__ == "__main__":
    main()