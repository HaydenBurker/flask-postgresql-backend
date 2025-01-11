from flask import jsonify

from db import connection, cursor
from .base_controller import add_record, get_all_records, get_record_by_id, update_record, delete_record
from models.categories import base_category_object
from util.validate_uuid import validate_uuid4

table_name = "Categories"
post_data_fields = ["name"]
return_fields = ["category_id", "name"]

def add_category():
    return add_record(table_name, post_data_fields, return_fields, base_category_object)

def get_all_categories():
    return get_all_records(table_name, return_fields, base_category_object)

def get_category_by_id(category_id):
    return get_record_by_id(category_id, table_name, return_fields, base_category_object)

def update_category(category_id):
    return update_record(category_id, table_name, post_data_fields, return_fields, base_category_object)

def delete_category(category_id):
    return delete_record(category_id, table_name, return_fields[0])
