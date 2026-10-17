"""Трекер просмотренных занятий. Запуск из папки проекта: python3 main.py"""

import json
from datetime import date

from schedule import check_schedule, load_schedule, past_lessons

SCHEDULE_FILE = "schedule.json"


def main():
    try:
        schedule = load_schedule(SCHEDULE_FILE)
    except FileNotFoundError:
        print(f"Не найден файл {SCHEDULE_FILE}. Запускай программу из папки проекта.")
        return
    except json.JSONDecodeError as error:
        print(f"Файл {SCHEDULE_FILE} не читается как JSON: строка {error.lineno}, {error.msg}.")
        return

    errors = check_schedule(schedule)
    if errors:
        print(f"В {SCHEDULE_FILE} есть ошибки:")
        for error in errors:
            print(f"  - {error}")
        return

    lessons = past_lessons(schedule, date.today())
    print(f"Прошло занятий: {len(lessons)}")
    for lesson in lessons:
        print(f"  {lesson['date'].strftime('%d.%m')} {lesson['type']} «{lesson['subject']}»")


if __name__ == "__main__":
    main()
