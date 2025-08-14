import camelot
import os
import traceback

input_dir = "inputs"
output_dir = "output"

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.lower().endswith(".pdf"):
        input_path = os.path.join(input_dir, filename)
        print(f"\nОбрабатываем файл: {filename}")

        tables = None

        try:
            tables = camelot.read_pdf(
                input_path, pages="all", flavor="stream", strip_text="\n"
            )
        except Exception as e:
            print(f"⚠️ Stream-режим не сработал: {e}")

        if tables is None or len(tables) == 0:
            try:
                tables = camelot.read_pdf(
                    input_path, pages="all", flavor="lattice", strip_text="\n"
                )
            except Exception as e:
                print(f"❌ Lattice-режим тоже не сработал: {e}")
                traceback.print_exc()
                continue

        print(f"Найдено таблиц: {len(tables)}")

        for i, table in enumerate(tables):
            csv_name = f"{os.path.splitext(filename)[0]}_table_{i+1}.csv"
            output_path = os.path.join(output_dir, csv_name)
            table.to_csv(output_path)
            print(f"✅ Сохранено: {output_path}")
