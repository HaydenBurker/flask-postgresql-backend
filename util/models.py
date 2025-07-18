from models.base_model import Model

def table_name_to_model(table_name):
    cls_map = {cls.tablename: cls for cls in Model.__subclasses__()}
    return cls_map.get(table_name)