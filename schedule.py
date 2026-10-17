"""Расписание: какие занятия должны были пройти к сегодняшнему дню."""

import json
from datetime import date, timedelta

# date.weekday() возвращает номер дня недели: понедельник — 0, воскресенье — 6.
WEEKDAYS = {"пн": 0, "вт": 1, "ср": 2, "чт": 3, "пт": 4, "сб": 5, "вс": 6}


def load_schedule(path):
    """Читает расписание из JSON-файла и возвращает его как словарь."""
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def is_date(value):
    """Проверяет, что строка — дата в формате ГГГГ-ММ-ДД."""
    try:
        date.fromisoformat(value)
        return True
    except (TypeError, ValueError):
        return False


def check_schedule(schedule):
    """Ищет ошибки в расписании. Возвращает список ошибок; пустой список — всё в порядке."""
    errors = []
    for key in ["start", "end", "lessons", "cancelled"]:
        if key not in schedule:
            errors.append(f"нет поля «{key}»")
    if errors:
        return errors  # без этих полей дальше проверять нечего

    dates = [schedule["start"], schedule["end"]] + schedule["cancelled"]
    for value in dates:
        if not is_date(value):
            errors.append(f"«{value}» — не дата, нужен формат ГГГГ-ММ-ДД")

    for number, lesson in enumerate(schedule["lessons"], start=1):
        for key in ["weekday", "type", "subject"]:
            if key not in lesson:
                errors.append(f"в занятии №{number} нет поля «{key}»")
        if "weekday" in lesson and lesson["weekday"] not in WEEKDAYS:
            errors.append(f"в занятии №{number} непонятный день недели «{lesson['weekday']}»")
    return errors


def past_lessons(schedule, today):
    """Составляет список занятий, которые прошли до сегодняшнего дня.

    Каждое занятие — словарь с датой, типом и предметом.
    Сегодняшние занятия не считаются: запись могла ещё не появиться.
    """
    start = date.fromisoformat(schedule["start"])
    end = date.fromisoformat(schedule["end"])
    cancelled = [date.fromisoformat(day) for day in schedule["cancelled"]]
    last_day = min(end, today - timedelta(days=1))

    lessons = []
    day = start
    while day <= last_day:
        if day not in cancelled:
            for lesson in schedule["lessons"]:
                if WEEKDAYS[lesson["weekday"]] == day.weekday():
                    lessons.append({"date": day, "type": lesson["type"], "subject": lesson["subject"]})
        day += timedelta(days=1)
    return lessons
