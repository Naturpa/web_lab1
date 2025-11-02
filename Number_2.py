import os
import zipfile


def human_readable_size(size_bytes):
    """
    Конвертирует размер в байтах в человекочитаемый формат.
    Использует старшие единицы измерения, округленные до целого.
    """
    if size_bytes == 0:
        return "0Б"

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


def decode_filename(filename):
    """
    Пытается корректно декодировать имя файла из разных кодировок.
    """
    try:
        # Сначала пробуем UTF-8 (стандарт для ZIP)
        return filename.encode('cp437').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        try:
            # Если не получается, пробуем CP866 (Windows)
            return filename.encode('cp437').decode('cp866')
        except (UnicodeEncodeError, UnicodeDecodeError):
            try:
                # Пробуем просто как UTF-8
                return filename
            except:
                # Если все fails, возвращаем как есть
                return filename


def print_zip_structure(zip_path):
    """
    Выводит структуру ZIP-архива с отступами и размерами файлов.
    Корректно обрабатывает русские имена файлов.
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            # Собираем все пути и их типы
            items = []

            for info in zip_file.infolist():
                if info.filename:  # Пропускаем пустые имена
                    # Декодируем имя файла
                    decoded_filename = decode_filename(info.filename)

                    # Определяем тип элемента
                    if decoded_filename.endswith('/'):
                        item_type = 'dir'
                        path = decoded_filename.rstrip('/')
                    else:
                        item_type = 'file'
                        path = decoded_filename

                    items.append((item_type, path, info.file_size))

            # Если архив пустой
            if not items:
                return

            # Сортируем по пути
            items.sort(key=lambda x: x[1])

            # Множество для отслеживания выведенных директорий
            printed_dirs = set()

            for item_type, path, size in items:
                if not path:  # Пропускаем пустые пути
                    continue

                parts = path.split('/')

                # Сначала выводим все родительские директории
                for i in range(len(parts) - (1 if item_type == 'file' else 0)):
                    dir_path = '/'.join(parts[:i + 1])
                    if dir_path and dir_path not in printed_dirs:
                        indent = "  " * i
                        print(f"{indent}{parts[i]}")
                        printed_dirs.add(dir_path)

                # Выводим файл с размером
                if item_type == 'file':
                    indent = "  " * (len(parts) - 1)
                    size_str = human_readable_size(size)
                    print(f"{indent}{parts[-1]} {size_str}")

    except zipfile.BadZipFile:
        print(f"Ошибка: файл {zip_path} не является корректным ZIP-архивом")
    except Exception as e:
        print(f"Ошибка при чтении архива: {e}")


def main():
    zip_path = input("Введите путь к ZIP-архиву: ").strip()

    if not os.path.exists(zip_path):
        print("Ошибка: указанный файл не существует")
        return

    if not zipfile.is_zipfile(zip_path):
        print("Ошибка: указанный файл не является ZIP-архивом")
        return

    print_zip_structure(zip_path)


if __name__ == "__main__":
    main()