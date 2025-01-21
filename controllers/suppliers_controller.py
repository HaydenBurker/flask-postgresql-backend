from flask import request, jsonify

from db import connection, cursor

from .base_controller import BaseController
from models.suppliers import base_supplier_object
from models.product_suppliers import base_product_supplier_object
from models.products import base_product_object
from util.validate_uuid import validate_uuid4

def create_product_supplier_object(product_supplier):
    product_supplier = base_product_supplier_object(product_supplier)
    product_id = product_supplier.get("product_id")

    product_query = """SELECT * FROM "Products"
    WHERE product_id = %s"""
    cursor.execute(product_query, (product_id,))
    product = cursor.fetchone()
    product = base_product_object(product)
    product_supplier["product"] = product
    del product_supplier["product_id"]
    del product_supplier["supplier_id"]

    return product_supplier

def create_supplier_object(supplier):
    supplier = base_supplier_object(supplier)
    supplier_id = supplier.get("supplier_id")

    product_suppliers_query = """SELECT * FROM "ProductSuppliers"
    WHERE supplier_id = %s"""
    cursor.execute(product_suppliers_query, (supplier_id,))
    product_suppliers = cursor.fetchall()
    product_suppliers = [create_product_supplier_object(product_supplier) for product_supplier in product_suppliers]
    supplier["product_suppliers"] = product_suppliers

    return supplier

class SuppliersController(BaseController):
    table_name = "Suppliers"
    post_data_fields = ["company_name", "contact_name", "email", "phone_number", "address", "active"]
    default_values = ["", "", "", "", "", True]
    return_fields = ["supplier_id", "company_name", "contact_name", "email", "phone_number", "address", "active"]
    create_record_object = lambda _, supplier: create_supplier_object(supplier)

    def add_product_supplier(self):
        post_data = request.json
        product_id = post_data.get("product_id")
        supplier_id = post_data.get("supplier_id")

        if not validate_uuid4(product_id):
            return jsonify({"message": "invalid product id"}), 400
        product_query = """SELECT product_id FROM "Products"
        WHERE product_id = %s"""
        cursor.execute(product_query, (product_id,))
        product = cursor.fetchone()
        if not product:
            return jsonify({"message": "product not found"}), 404

        if not validate_uuid4(post_data.get("supplier_id")):
            return jsonify({"message": "invalid supplier id"}), 400
        supplier_query = """SELECT * FROM "Suppliers"
        WHERE supplier_id = %s"""
        cursor.execute(supplier_query, (supplier_id,))
        supplier = cursor.fetchone()
        if not supplier:
            return jsonify({"message": "supplier not found"}), 404

        supplier_add_product_supplier_query = """INSERT INTO "ProductSuppliers" (product_id, supplier_id, supply_price, supply_date)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (product_id, supplier_id) DO UPDATE
        SET product_id = EXCLUDED.product_id,
        supplier_id = EXCLUDED.supplier_id,
        supply_price = EXCLUDED.supply_price,
        supply_date = EXCLUDED.supply_date"""
        try:
            cursor.execute(supplier_add_product_supplier_query, (product_id, supplier_id, post_data.get("supply_price", 0), post_data.get("supply_date")))
            connection.commit()
        except:
            connection.rollback()
            return jsonify({"message": "unable to add product supplier to supplier"}), 400

        return jsonify({"message": "added product supplier to supplier", "results": self.create_record_object(supplier)}), 200
