import argparse
import os


def format_text_block(frame_height, frame_width, file_name):
    """
    Форматирует текстовый файл и возвращает его содержимое в указанных рамках.

    Args:
        frame_height (int): Высота блока в символах
        frame_width (int): Ширина блока в символах
        file_name (str): Имя файла для форматирования

    Returns:
        str: Отформатированный текст или текст исключения в случае ошибки
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"[Errno 2] No such file or directory: '{file_name}'")

        # Читаем файл
        with open(file_name, 'r', encoding='utf-8-sig') as f:
            content = f.read()

        # Разбиваем на строки и удаляем символы возврата каретки
        lines = content.replace('\r\n', '\n').replace('\r', '\n').split('\n')

        # Обрабатываем строки с переносом
        formatted_lines = []
        for line in lines:
            # Если строка пустая, добавляем пустую строку
            if not line.strip():
                formatted_lines.append('')
                continue

            # Разбиваем длинные строки на части по frame_width
            start = 0
            while start < len(line):
                # Берем часть строки длиной frame_width
                part = line[start:start + frame_width]
                formatted_lines.append(part)
                start += frame_width

        # Берем только нужное количество строк
        result_lines = formatted_lines[:frame_height]

        # Дополняем до нужной высоты пустыми строками если нужно
        while len(result_lines) < frame_height:
            result_lines.append('')

        # Форматируем результат
        result = '\n'.join(result_lines)
        return result

    except Exception as e:
        return str(e)


def main():
    # Создаем парсер аргументов
    parser = argparse.ArgumentParser(description='Форматирование текстового файла в указанные рамки')
    parser.add_argument('--frame-height', type=int, required=True, help='Высота блока в символах')
    parser.add_argument('--frame-width', type=int, required=True, help='Ширина блока в символах')
    parser.add_argument('file_name', help='Имя файла для форматирования')

    # Парсим аргументы
    args = parser.parse_args()

    # Форматируем текст
    result = format_text_block(args.frame_height, args.frame_width, args.file_name)

    # Выводим результат
    print(result)


if __name__ == "__main__":
    main()