from flask import request, jsonify

from models.category import Categories, categories_schema, category_schema
from lib.authenticate import authenticate, authenticate_return_auth
from util.reflection import populate_object
from db import db

@authenticate_return_auth
def add_category(auth_info):
    if auth_info.user.is_admin == True:
        post_data = request.form if request.form else request.json

        new_category = Categories.new_category_obj()

        populate_object(new_category, post_data)

        try:
            db.session.add(new_category)
            db.session.commit()

        except:
            db.session.rollback()
            return jsonify({"message": "unable to add category"}), 400

        return jsonify({"message": "category added", "result": category_schema.dump(new_category)}), 201
    
    return jsonify ({"message": "unauthorized"}), 403

@authenticate
def get_all_categories():
    query = db.session.query(Categories).all()

    return jsonify({"message": "category found", "results": categories_schema.dump(query)}), 200

@authenticate
def get_category_by_id(category_id):
    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not query:
        return jsonify({"message": "category not found"}), 404
    
    return jsonify({"message": "category found", "result": category_schema.dump(query)}), 200


@authenticate_return_auth
def update_category_by_id(category_id, auth_info):
    if auth_info.user.is_admin == True:
        post_data = request.form if request.form else request.json
        query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

        if not query:
            return jsonify({"message": "category not found"}), 404
        

        try:
            populate_object(query, post_data)
            db.session.commit()
        
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update category"}), 400

        return jsonify({"message": "category updated", "result": category_schema.dump(query)}), 200
    
    return jsonify ({"message": "unauthorized"}), 403


@authenticate_return_auth
def delete_category_by_id(category_id, auth_info):
    if auth_info.user.is_admin == True:
        query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

        if not query:
            return jsonify({"message": "category not found"}), 404
        
        try:
            db.session.delete(query)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete category"}), 400
        
        return jsonify({"message": "category deleted"}), 200
    
    return jsonify ({"message": "unauthorized"}), 403
