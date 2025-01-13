from .base_controller import BaseController
from models.categories import base_category_object


class CategoriesController(BaseController):
    table_name = "Categories"
    post_data_fields = ["name"]
    return_fields = ["category_id", "name"]
    create_record_object = lambda _, category: base_category_object(category)
