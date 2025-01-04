import uuid
from flask import request, jsonify

from db import get_connection

def create_product_object(product, cursor):
    [product_id, name, created_by_id] = product
    created_by_user = created_by_id
    if created_by_id:
        create_by_id_query = """SELECT user_id, first_name, last_name, email, active FROM "Users"
        WHERE user_id = %s"""
        cursor.execute(create_by_id_query, (created_by_id,))
        [user_id, first_name, last_name, email, active] = cursor.fetchone()

        created_by_user = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "active": active
        }
    return {
        "product_id": product_id,
        "name": name,
        "created_by": created_by_user
    }

def add_product():
    post_data = request.json
    with get_connection() as [connection, cursor]:
        insert_query = """INSERT INTO "Products"
        VALUES (%s, %s, %s) RETURNING *"""
        cursor.execute(insert_query, (str(uuid.uuid4()), post_data.get("name"), post_data.get("created_by_id")))
        product = cursor.fetchone()
        connection.commit()

        product = create_product_object(product, cursor)

    return jsonify({"message": "product added", "results": product}), 201

def get_all_products():
    with get_connection() as [_, cursor]:
        get_all_query = 'SELECT * FROM "Products"'
        cursor.execute(get_all_query)
        products = cursor.fetchall()

        products = [create_product_object(product, cursor) for product in products]

    return jsonify({"message": "products found", "results": products}), 200

def get_product_by_id(product_id):
    with get_connection() as [_, cursor]:
        get_by_id_query = """SELECT * FROM "Products"
        WHERE product_id = %s"""
        cursor.execute(get_by_id_query, (product_id,))
        product = cursor.fetchone()
        if not product:
            return jsonify({"message": "product not found"}), 404

        product = create_product_object(product, cursor)
    return jsonify({"message": "product found", "results": product}), 200

def update_product(product_id):
    post_data = request.json
    with get_connection() as [connection, cursor]:
        get_by_id_query = """SELECT * FROM "Products"
        WHERE product_id = %s"""
        cursor.execute(get_by_id_query, (product_id,))
        product = cursor.fetchone()
        if not product:
            return jsonify({"message": "product not found"}), 404

        [product_id, name, created_by_id] = product

        update_query = """UPDATE "Products"
        SET name = %s,
        created_by_id = %s
        WHERE product_id = %s RETURNING *"""
        cursor.execute(update_query, (post_data.get("name", name), post_data.get("created_by_id", created_by_id), product_id))
        product = cursor.fetchone()
        connection.commit()
        product = create_product_object(product, cursor)

    return jsonify({"message": "product updated", "results": product}), 200

def delete_product(product_id):
    with get_connection() as [connection, cursor]:
        get_by_id_query = """SELECT product_id FROM "Products"
        WHERE product_id = %s"""
        cursor.execute(get_by_id_query, (product_id,))
        product = cursor.fetchone()
        if not product:
            return jsonify({"message": "product not found"}), 404

        [product_id] = product

        delete_query = """DELETE FROM "Products"
        WHERE product_id = %s"""
        cursor.execute(delete_query, (product_id,))
        connection.commit()

    return jsonify({"message": "deleted product"}), 200
