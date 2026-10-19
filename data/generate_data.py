# Генератор данных: путь клиента при оформлении кредитной карты
import csv
import random
from datetime import datetime, timedelta

random.seed(42)

rows = []
event_id = 0

for user_id in range(1, 5001):
    # Признаки пользователя
    channel = random.choices(["organic", "push", "ads"], weights=[50, 20, 30])[0]
    device = random.choices(["ios", "android", "web"], weights=[40, 45, 15])[0]
    age = random.choices(["18-24", "25-34", "35-44", "45+"], weights=[20, 35, 25, 20])[0]

    # Время первого входа: случайный момент в сентябре 2026
    time = datetime(2026, 9, 1) + timedelta(minutes=random.randint(0, 43200))

    # Шаг 1: вход в приложение
    event_id += 1
    rows.append([event_id, user_id, "app_open", time, channel, device, age, ""])

    # Шаг 2: страница карты (push работает лучше всего)
    if channel == "push":
        chance = 0.75
    elif channel == "ads":
        chance = 0.60
    else:
        chance = 0.45
    if random.random() > chance:
        continue
    time = time + timedelta(seconds=random.randint(10, 300))
    event_id += 1
    rows.append([event_id, user_id, "card_page_view", time, channel, device, age, ""])

    # Шаг 3: начал заполнять анкету
    if random.random() > 0.55:
        continue
    time = time + timedelta(seconds=random.randint(20, 600))
    event_id += 1
    rows.append([event_id, user_id, "form_start", time, channel, device, age, ""])

    # Шаг 4: отправил анкету (на Android хуже)
    if device == "ios":
        chance = 0.70
    elif device == "android":
        chance = 0.45
    else:
        chance = 0.60
    if random.random() > chance:
        continue
    time = time + timedelta(minutes=random.randint(3, 25))
    event_id += 1
    rows.append([event_id, user_id, "form_submit", time, channel, device, age, ""])

    # Шаг 5: решение банка (молодым одобряют реже)
    if age == "18-24":
        chance = 0.55
    else:
        chance = 0.75
    time = time + timedelta(minutes=random.randint(1, 15))
    event_id += 1
    if random.random() > chance:
        rows.append([event_id, user_id, "scoring_result", time, channel, device, age, "rejected"])
        continue
    rows.append([event_id, user_id, "scoring_result", time, channel, device, age, "approved"])

    # Шаг 6: карта выпущена
    if random.random() > 0.90:
        continue
    time = time + timedelta(days=random.randint(1, 5))
    event_id += 1
    rows.append([event_id, user_id, "card_issued", time, channel, device, age, ""])

    # Шаг 7: карта активирована
    if random.random() > 0.65:
        continue
    time = time + timedelta(days=random.randint(0, 10))
    event_id += 1
    rows.append([event_id, user_id, "card_activated", time, channel, device, age, ""])

# Сохраняем в CSV
with open("data/card_events.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["event_id", "user_id", "event", "event_time", "channel", "device", "age_group", "result"])
    writer.writerows(rows)

print("Готово! Событий:", len(rows))