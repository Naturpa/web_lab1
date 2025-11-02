import time
from datetime import datetime


def print_ku():
    """
    Функция, которая выводит 'Ку' от 1 до 12 раз в зависимости от текущего часа.
    """
    current_hour = datetime.now().hour
    # Преобразуем 24-часовой формат в 12-часовой
    ku_count = current_hour % 12
    if ku_count == 0:
        ku_count = 12

    time_str = datetime.now().strftime('%H:%M:%S')
    print(f"🕐 Время: {time_str}")
    print("🔊 " + "Ку " * ku_count)
    print("─" * 40)


def main():
    """
    Основная функция программы с простой проверкой времени.
    """
    print("🐔 Программа 'Ку-часы' запущена!")
    print("📅 Расписание: каждый час в 00 минут")
    print("⏹️  Для остановки нажмите Ctrl+C")
    print("=" * 50)

    last_executed_hour = -1

    try:
        while True:
            now = datetime.now()
            current_minute = now.minute
            current_hour = now.hour

            # Проверяем, наступили ли 00 минут нового часа
            if current_minute == 0 and current_hour != last_executed_hour:
                print_ku()
                last_executed_hour = current_hour

                # Показываем время следующего запуска
                next_hour = (current_hour + 1) % 24
                print(f"⏰ Следующий запуск в: {next_hour:02d}:00:00")
                print()

            time.sleep(10)  # Проверяем каждые 10 секунд

    except KeyboardInterrupt:
        print("\n\n🛑 Программа остановлена")
        print("👋 До свидания!")


if __name__ == "__main__":
    main()