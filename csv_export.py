import sys
import csv

from db import cursor

from models.base_model import Model

def table_name_to_model(table_name):
    cls_map = {cls.tablename: cls for cls in Model.__subclasses__()}
    return cls_map.get(table_name)

def export_table(model, file_name):
    fields = model().fields
    with open(f"csv/export/{file_name}", "w") as export_file:
        query = f'SELECT {",".join(fields)} FROM "{model.tablename}"'
        cursor.execute(query)
        records = cursor.fetchall()

        csv_writer = csv.writer(export_file)
        csv_writer.writerow(fields)
        csv_writer.writerows(records)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        table_name = sys.argv[1]
        file_name = sys.argv[2]

        model = table_name_to_model(table_name)
        if model:
            export_table(model, file_name)
