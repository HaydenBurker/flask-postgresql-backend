from .base_controller import BaseController
from models.categories import Category


class CategoriesController(BaseController):
    create_record_object = lambda _, category_data, many=False: [category.dump() for category in category_data] if many else category_data.dump()
    model = Category
