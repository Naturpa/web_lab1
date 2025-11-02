import sys


def main():
    # Берем аргументы из командной строки (исключая имя скрипта)
    args = sys.argv[1:]

    # Проверяем наличие опции --sort
    sort_flag = False
    if '--sort' in args:
        sort_flag = True
        args.remove('--sort')

    # Собираем пары ключ-значение
    key_value_pairs = []
    for arg in args:
        if '=' in arg:
            key, value = arg.split('=', 1)  # Разделяем только по первому '='
            key_value_pairs.append((key, value))

    # Сортируем если нужно
    if sort_flag:
        key_value_pairs.sort(key=lambda x: x[0])

    # Выводим результат
    for key, value in key_value_pairs:
        print(f"Key: {key} Value: {value}")


if __name__ == "__main__":
    main()