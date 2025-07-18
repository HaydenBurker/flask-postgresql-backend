import sys
import csv

from db import cursor

from util.models import table_name_to_model

def export_table(model, file_name):
    fields = model().dump_update().keys()

    with open(f"csv/export/{file_name}", "w") as export_file:
        query = f'SELECT * FROM "{model.tablename}"'
        cursor.execute(query)
        records = model.load_many(cursor.fetchall())

        csv_writer = csv.DictWriter(export_file, fieldnames=fields)
        csv_writer.writeheader()
        csv_writer.writerows([record.dump_update() for record in records])

if __name__ == "__main__":
    if len(sys.argv) > 2:
        table_name = sys.argv[1]
        file_name = sys.argv[2]

        model = table_name_to_model(table_name)
        if model:
            export_table(model, file_name)
