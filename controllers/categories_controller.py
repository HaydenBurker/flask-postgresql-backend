from .base_controller import BaseController
from models.categories import Category, base_category_object


class CategoriesController(BaseController):
    create_record_object = lambda _, category_data, many=False: [base_category_object(category) for category in category_data] if many else base_category_object(category_data)
    model = Category
