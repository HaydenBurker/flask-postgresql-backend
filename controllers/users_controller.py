from flask import request, jsonify

from db import connection, cursor
from .base_controller import add_record, get_all_records, get_record_by_id, update_record, record_activity, delete_record
from models.users import base_user_object
from models.products import base_product_object
from util.validate_uuid import validate_uuid4

table_name = "Users"
post_data_fields = ["first_name", "last_name", "email", "password", "active"]
return_fields = ["user_id", "first_name", "last_name", "email", "active"]

def create_user_object(user):
    user = base_user_object(user)
    user_id = user.get("user_id")
    products = []

    products_query = """SELECT * FROM "Products"
    WHERE created_by_id = %s"""
    cursor.execute(products_query, (user_id,))
    products = cursor.fetchall()
    products = [base_product_object(product) for product in products]

    user["products"] = products
    return user

def add_user():
    return add_record(table_name, post_data_fields, return_fields, create_user_object)

def get_all_users():
    return get_all_records(table_name, return_fields, create_user_object)

def get_user_by_id(user_id):
    return get_record_by_id(user_id, table_name, return_fields, create_user_object)

def update_user(user_id):
    return update_record(user_id, table_name, post_data_fields[:-1], return_fields, create_user_object)

def user_activity(user_id):
    return record_activity(user_id, table_name, return_fields, create_user_object)

def delete_user(user_id):
    return delete_record(user_id, table_name, return_fields[0])
