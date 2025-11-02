import argparse


def main():
    parser = argparse.ArgumentParser()

    # Добавляем опцию --sort как флаг
    parser.add_argument('--sort', action='store_true',
                        help='сортировать вывод по ключу')

    # Добавляем аргументы вида "ключ=значение" (любое количество)
    parser.add_argument('key_value_pairs', nargs='*',
                        help='аргументы в формате ключ=значение')

    args = parser.parse_args()

    # Собираем пары ключ-значение
    pairs = []
    for item in args.key_value_pairs:
        if '=' in item:
            key, value = item.split('=', 1)  # Разделяем только по первому '='
            pairs.append((key, value))

    # Сортируем если нужно
    if args.sort:
        pairs.sort(key=lambda x: x[0])

    # Выводим результат
    for key, value in pairs:
        print(f"Key: {key} Value: {value}")


if __name__ == "__main__":
    main()