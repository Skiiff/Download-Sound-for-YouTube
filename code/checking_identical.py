import pandas as pd
import Levenshtein
from tqdm import tqdm
import os
def run():
    print("checking identical start")
    print("="*68)
    print("Что бы вернуться введите back")
    print("="*68)
    #Проверка правильности ввода
    def read_csv_with_retry(prompt):
        while True:
            filename = input(prompt)
            if filename == "back":
                return None
            # Автоподстановка .csv
            if not filename.lower().endswith(".csv"):
                filename += ".csv"
            # Проверяем, существует ли файл
            if not os.path.exists(filename):
                print(f"Файл '{filename}' не найден. Попробуйте снова.")
                continue
            try:
                df = pd.read_csv(filename)
                return df
            except pd.errors.EmptyDataError:
                print(f"Файл '{filename}' пустой. Попробуйте другой файл.")
            except pd.errors.ParserError:
                print(f"Файл '{filename}' не является корректным CSV. Попробуйте снова.")
            except Exception as e:
                print(f"Произошла ошибка: {e}. Попробуйте снова.")
    #Запрос файлов
    df1 = read_csv_with_retry("Укажите имя файла 1: ")
    if df1 is None:
        return
    df2 = read_csv_with_retry("Укажите имя файла 2: ")
    if df2 is None:
        return
     
    combined = pd.concat([df1, df2])
    combined.to_csv("combined.csv", index=False)
    # Порог похожести (0.8 = 80% схожести)
    SIMILARITY_THRESHOLD = 0.8

    # Чтение CSV
    df = pd.read_csv("combined.csv")

    # Приводим к нижнему регистру для сравнения
    df["Artist_lower"] = df["Artist"].str.lower()
    df["Track_lower"] = df["Track"].str.lower()

    # Списки индексов
    to_drop = set()
    deleted_rows = []

    for i in tqdm(range(len(df)), desc="Progress"):
        if i in to_drop:
            continue
        for j in range(i + 1, len(df)):
            if j in to_drop:
                continue
            # Вычисляем коэффициент похожести Левенштейна
            artist_sim = Levenshtein.ratio(df.loc[i, "Artist_lower"], df.loc[j, "Artist_lower"])
            track_sim = Levenshtein.ratio(df.loc[i, "Track_lower"], df.loc[j, "Track_lower"])
        
            if artist_sim >= SIMILARITY_THRESHOLD and track_sim >= SIMILARITY_THRESHOLD:
                to_drop.add(j)
                deleted_rows.append(df.loc[j, ["Artist", "Track"]])

    # Удаляем дубликаты
    df_cleaned = df.drop(index=to_drop).drop(columns=["Artist_lower", "Track_lower"])

    # Создаём DataFrame с удалёнными записями
    df_deleted = pd.DataFrame(deleted_rows)

    # Сохраняем CSV
    df_cleaned.to_csv("final_file.csv", index=False)
    df_deleted.to_csv("deleted_duplicates.csv", index=False)

    # Выводим удалённые записи
    print("Удалённые записи:")
    print(df_deleted)

    print(f"\nВсего удалено {len(deleted_rows)} похожих записей")