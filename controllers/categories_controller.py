from .base_controller import BaseController
from models.categories import Category


class CategoriesController(BaseController):
    model = Category
