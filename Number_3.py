import os
from pathlib import Path


def human_readable_size(size_bytes):
    """
    Конвертирует размер в байтах в человекочитаемый формат.
    Использует старшие единицы измерения, округленные до целого.
    """
    if size_bytes == 0:
        return "0Б"

    units = [
        (1024 ** 4, "ТБ"),
        (1024 ** 3, "ГБ"),
        (1024 ** 2, "МБ"),
        (1024, "КБ"),
        (1, "Б")
    ]

    for divisor, unit in units:
        if size_bytes >= divisor:
            size = round(size_bytes / divisor)
            return f"{size}{unit}"

    return "0Б"


def get_directory_size(directory_path):
    """
    Рекурсивно вычисляет суммарный размер всех файлов в каталоге и его подкаталогах.
    """
    total_size = 0

    try:
        with os.scandir(directory_path) as entries:
            for entry in entries:
                if entry.is_file(follow_symlinks=False):
                    try:
                        total_size += entry.stat().st_size
                    except (OSError, PermissionError):
                        continue
                elif entry.is_dir(follow_symlinks=False):
                    try:
                        total_size += get_directory_size(entry.path)
                    except (OSError, PermissionError):
                        continue
    except (OSError, PermissionError):
        pass

    return total_size


def find_top_directories(start_path, top_n=10):
    """
    Находит TOP-N самых больших каталогов по заданному пути.
    """
    directory_sizes = []

    # Проверяем, что начальный путь существует
    if not os.path.exists(start_path):
        print(f"Ошибка: путь '{start_path}' не существует")
        return []

    # Если начальный путь - файл, а не директория
    if os.path.isfile(start_path):
        print(f"Ошибка: '{start_path}' является файлом, а не директорией")
        return []

    print(f"Сканирование каталога: {start_path}")
    print("Это может занять некоторое время...")

    # Рекурсивно обходим все подкаталоги
    try:
        for root, dirs, files in os.walk(start_path):
            # Пропускаем системные директории и точки монтирования
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            try:
                # Вычисляем размер текущей директории
                dir_size = get_directory_size(root)
                directory_sizes.append((root, dir_size))

                # Выводим прогресс
                dir_name = os.path.basename(root) if root != start_path else os.path.basename(start_path)
                print(f"Обработано: {dir_name} - {human_readable_size(dir_size)}")

            except (OSError, PermissionError):
                continue

    except KeyboardInterrupt:
        print("\nСканирование прервано пользователем")
        return []

    # Сортируем по размеру в порядке убывания
    directory_sizes.sort(key=lambda x: x[1], reverse=True)

    # Возвращаем TOP-N
    return directory_sizes[:top_n]


def main():
    """
    Основная функция программы.
    """
    # Запрашиваем путь у пользователя
    start_path = input("Введите путь для анализа (по умолчанию - текущая папка): ").strip()

    # Если путь не указан, используем текущую папку
    if not start_path:
        start_path = "."

    # Получаем абсолютный путь
    start_path = os.path.abspath(start_path)

    print(f"Анализируем каталог: {start_path}")
    print("=" * 50)

    # Находим TOP-10 самых больших каталогов
    top_directories = find_top_directories(start_path, 10)

    print("\n" + "=" * 50)
    print("TOP-10 самых больших каталогов:")
    print("=" * 50)

    if not top_directories:
        print("Не удалось найти каталоги для анализа")
        return

    # Выводим результаты
    for i, (directory, size) in enumerate(top_directories, 1):
        # Получаем только имя каталога (без полного пути)
        dir_name = os.path.basename(directory) if directory != start_path else os.path.basename(start_path)
        if not dir_name:  # Если это корневой каталог
            dir_name = directory

        size_str = human_readable_size(size)
        print(f"{i}. {dir_name} - {size_str}")

        # Дополнительная информация (полный путь для больших каталогов)
        if size > 1024 ** 3:  # Если больше 1ГБ
            print(f"   Полный путь: {directory}")


if __name__ == "__main__":
    main()