import os


def human_readable_size(size_bytes):
    """
    Конвертирует размер в байтах в человекочитаемый формат.
    Использует старшие единицы измерения, округленные до целого.
    """
    if size_bytes == 0:
        return "0Б"

    # Единицы измерения и их пороги
    units = [
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


def main():
    # Получаем список всех элементов в текущей папке
    try:
        items = os.listdir()
    except PermissionError:
        print("Ошибка: нет доступа к текущей папке")
        return

    # Обрабатываем каждый элемент
    for item in items:
        # Пропускаем каталоги
        if os.path.isdir(item):
            continue

        # Получаем размер файла
        try:
            file_size = os.path.getsize(item)
            readable_size = human_readable_size(file_size)
            print(f"{item} {readable_size}")
        except (OSError, PermissionError) as e:
            print(f"{item} недоступен ({e})")


if __name__ == "__main__":
    main()