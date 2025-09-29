import unittest
import csv
import os
from main import run_main  # импорт функции вместо subprocess

CSV_FILE = "offices.csv"

class TestOfficesCSV(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(CSV_FILE):
            os.remove(CSV_FILE)
        run_main()  # запускаем напрямую
        print("\n=== Основной скрипт выполнен ===")

    def test_file_created(self):
        self.assertTrue(os.path.exists(CSV_FILE), "Файл offices.csv не создан")
        print("✔ Файл CSV создан")

    def test_csv_header(self):
        with open(CSV_FILE, encoding="utf-8") as f:
            header = next(csv.reader(f, delimiter=";"))
        self.assertEqual(header, ["Country", "CompanyName", "FullAddress"])
        print("✔ Заголовки CSV корректны")

    def test_offices_count(self):
        with open(CSV_FILE, encoding="utf-8") as f:
            rows = list(csv.reader(f, delimiter=";"))[1:]
        self.assertTrue(1 <= len(rows) <= 50, f"Некорректное количество офисов: {len(rows)}")
        print(f"✔ Количество офисов: {len(rows)}")

    def test_office_data_format(self):
        with open(CSV_FILE, encoding="utf-8") as f:
            rows = list(csv.reader(f, delimiter=";"))[1:]
        for row in rows:
            self.assertEqual(len(row), 3)
            self.assertTrue(all(col.strip() for col in row))
        print("✔ Все строки CSV корректны")

if __name__ == "__main__":
    unittest.main(verbosity=2)
