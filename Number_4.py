import os
import zipfile
import datetime
from pathlib import Path


def make_reserve_arc(source, dest):
    """
    Создает резервную копию каталога в формате ZIP с timestamp в имени.

    Args:
        source (str): путь к каталогу, который надо архивировать
        dest (str): путь к каталогу, в который поместить результат
    """
    # Проверяем существование исходного каталога
    if not os.path.exists(source):
        raise FileNotFoundError(f"Исходный каталог не существует: {source}")

    if not os.path.isdir(source):
        raise ValueError(f"Указанный путь не является каталогом: {source}")

    # Проверяем/создаем каталог назначения
    if not os.path.exists(dest):
        os.makedirs(dest, exist_ok=True)
    elif not os.path.isdir(dest):
        raise ValueError(f"Путь назначения не является каталогом: {dest}")

    # Генерируем имя архива с timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    source_name = os.path.basename(os.path.normpath(source))
    archive_name = f"backup_{source_name}_{timestamp}.zip"
    archive_path = os.path.join(dest, archive_name)

    print(f"Создание резервной копии: {source} -> {archive_path}")

    # Создаем ZIP-архив
    try:
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Рекурсивно добавляем все файлы и подкаталоги
            for root, dirs, files in os.walk(source):
                for file in files:
                    file_path = os.path.join(root, file)

                    # Создаем относительный путь для архива
                    arcname = os.path.relpath(file_path, start=source)

                    try:
                        zipf.write(file_path, arcname)
                        print(f"  Добавлен: {arcname}")
                    except (OSError, PermissionError) as e:
                        print(f"  Ошибка при добавлении {file_path}: {e}")
                        continue

        # Проверяем успешность создания
        if os.path.exists(archive_path):
            file_size = os.path.getsize(archive_path)
            size_str = human_readable_size(file_size)
            print(f"Резервная копия успешно создана: {archive_path} ({size_str})")
            return archive_path
        else:
            raise RuntimeError("Не удалось создать архив")

    except Exception as e:
        # Удаляем частично созданный архив в случае ошибки
        if os.path.exists(archive_path):
            os.remove(archive_path)
        raise RuntimeError(f"Ошибка при создании архива: {e}")


def human_readable_size(size_bytes):
    """Конвертирует размер в байтах в человекочитаемый формат."""
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


# Пример использования функции
if __name__ == "__main__":
    # Тестирование функции
    try:
        source_dir = input("Введите путь к каталогу для архивации: ").strip()
        dest_dir = input("Введите путь для сохранения архива: ").strip()

        if not source_dir:
            source_dir = "."  # Текущая папка
        if not dest_dir:
            dest_dir = "."  # Текущая папка

        result = make_reserve_arc(source_dir, dest_dir)
        print(f"\nАрхив создан: {result}")

    except Exception as e:
        print(f"Ошибка: {e}")