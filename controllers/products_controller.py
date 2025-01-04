import uuid
from flask import request, jsonify

from db import get_connection

def add_product():
    post_data = request.json
    with get_connection() as [connection, cursor]:
        insert_query = """INSERT INTO "Products"
        VALUES (%s, %s, %s) RETURNING *"""
        cursor.execute(insert_query, (str(uuid.uuid4()), post_data.get("name"), post_data.get("created_by_id")))
        [product_id, name, created_by_id] = cursor.fetchone()
        connection.commit()

    return jsonify({"message": "product added", "results": {
        "product_id": product_id,
        "name": name,
        "created_by_id": created_by_id
    }}), 201

def get_all_products():
    with get_connection() as [_, cursor]:
        get_all_query = 'SELECT * FROM "Products"'
        cursor.execute(get_all_query)
        products = cursor.fetchall()

        for i, product in enumerate(products):
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

            products[i] = {
                "product_id": product_id,
                "name": name,
                "created_by": created_by_user
            }

    return jsonify({"message": "products found", "results": products}), 200
