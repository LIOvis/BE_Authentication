from flask import request, jsonify

from models.product import Products, product_schema, products_schema
from lib.authenticate import authenticate, authenticate_return_auth
from util.reflection import populate_object
from models.category import Categories
from models.company import Companies
from db import db

@authenticate_return_auth
def add_product(auth_info):
    if auth_info.user.is_admin == True:
        post_data = request.form if request.form else request.json

        new_product = Products.new_product_obj()

        populate_object(new_product, post_data)

        try:
            db.session.add(new_product)
            db.session.commit()

        except:
            db.session.rollback()
            return jsonify({"message": "unable to add product"}), 400

        return jsonify({"message": "product added", "result": product_schema.dump(new_product)}), 201
    
    return jsonify({"message": "unauthorized"}), 403


@authenticate_return_auth
def add_product_to_category(auth_info):
    if auth_info.user.is_admin == True:
        post_data = request.form if request.form else request.json

        fields = ['product_id', 'category_id']
        required_fields = ['product_id', 'category_id']

        values = {}

        for field in fields:
            field_data = post_data.get(field)

            if field in required_fields and not field_data:
                return jsonify({"message": f"{field} is required"}), 404
            
            values[field] = field_data

        product_query = db.session.query(Products).filter(Products.product_id == values['product_id']).first()
        category_query = db.session.query(Categories).filter(Categories.category_id == values['category_id']).first()

        if not product_query:
            return jsonify({"message": "product not found"}), 404
        
        if not category_query:
            return jsonify({"message": "category not found"}), 404

        try:
            product_query.categories.append(category_query)
            db.session.commit()

        except:
            db.session.rollback()
            return jsonify({"message": "unable to add product to category"}), 400

        return jsonify({"message": "product added to category", "results": product_schema.dump(product_query)}), 200
    
    return jsonify({"message": "unauthorized"}), 403


@authenticate_return_auth
def get_all_products(auth_info):
    if auth_info.user.is_admin == True:
        query = db.session.query(Products).all()

        return jsonify({"message": "products found", "results": products_schema.dump(query)}), 200

    return jsonify({"message": "unauthorized"}), 403

@authenticate_return_auth
def get_product_by_id(product_id, auth_info):

    query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not query:
        return jsonify({"message": "product not found"}), 404

    if auth_info.user.is_admin == False and query.active == False:
        return jsonify({"message": "unauthorized"}), 403

    return jsonify({"message": "product found", "result": product_schema.dump(query)}), 200


@authenticate
def get_all_active_products():
    query = db.session.query(Products).filter(Products.active == True).all()

    return jsonify({"message": "products found", "results": products_schema.dump(query)}), 200


@authenticate_return_auth
def get_products_by_company(company_id, auth_info):
    query = []
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
        return jsonify({"message": "company not found"}), 404
    
    if auth_info.user.is_admin == True:
        query = db.session.query(Products).filter(Products.company_id == company_id).all()

    else:
        query = db.session.query(Products).filter(Products.company_id == company_id, Products.active == True).all()
        
    
    
    return jsonify({"message": "products found", "results": products_schema.dump(query)}), 200


@authenticate_return_auth
def update_product_by_id(product_id, auth_info):
    if auth_info.user.is_admin == True:
        post_data = request.form if request.form else request.json
        query = db.session.query(Products).filter(Products.product_id == product_id).first()

        if not query:
            return jsonify({"message": "product not found"}), 404
        
        try:
            populate_object(query, post_data)
            db.session.commit()
        
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update product"}), 400

        return jsonify({"message": "product updated", "result": product_schema.dump(query)}), 200
    
    return jsonify({"message": "unauthorized"}), 403


@authenticate_return_auth
def delete_product_by_id(product_id, auth_info):
    if auth_info.user.is_admin == True:
        query = db.session.query(Products).filter(Products.product_id == product_id).first()

        if not query:
            return jsonify({"message": "product not found"}), 404
        
        try:
            db.session.delete(query)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete product"}), 400
        
        return jsonify({"message": "product deleted"}), 200
    
    return jsonify({"message": "unauthorized"}), 403
