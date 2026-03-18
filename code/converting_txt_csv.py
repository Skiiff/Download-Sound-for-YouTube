import csv
def run():
    print("convert script start")

    print("="*68)
    print("Что бы вернуться введите back")
    print("="*68)
    # Вводим название файла без расширения
    name = input('Введите название txt файла (без .txt): ')
    if name == "back":
        return
    # Открываем исходный TXT файл
    try:
        with open(f'{name}.txt', 'r', encoding='utf-8') as txt_file:
            lines = txt_file.readlines()
    except FileNotFoundError:
        print(f'Файл {name}.txt не найден!')
        return

    # Создаем CSV файл
    with open(f'{name}.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Записываем заголовок
        writer.writerow(['Artist', 'Track'])

        for line in lines:
            line = line.strip()
            if not line:
                continue  # пропускаем пустые строки
            if ' - ' in line:
                artist, track = line.split(' - ', 1)  # разделяем только по первому дефису
                writer.writerow([artist.strip(), track.strip()])
            else:
                # если строка не соответствует формату, записываем только в первый столбец
                writer.writerow([line.strip(), ''])

    print(f'Файл {name}.csv успешно создан.')