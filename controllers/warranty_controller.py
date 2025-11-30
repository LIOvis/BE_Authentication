from flask import request, jsonify

from models.warranty import Warranties, warranties_schema, warranty_schema
from lib.authenticate import authenticate_return_auth
from util.reflection import populate_object
from db import db

@authenticate_return_auth
def add_warranty(auth_info):
    if auth_info.user.is_admin == True:
        post_data = request.form if request.form else request.json

        new_warranty = Warranties.new_warranty_obj()

        populate_object(new_warranty, post_data)

        try:
            db.session.add(new_warranty)
            db.session.commit()

        except:
            db.session.rollback()
            return jsonify({"message": "unable to add warranty"}), 400

        return jsonify({"message": "warranty added", "result": warranty_schema.dump(new_warranty)}), 201
    
    return jsonify({"message": "unauthorized"}), 403


@authenticate_return_auth
def get_all_warranties(auth_info):
    query = []

    if auth_info.user.is_admin == True:
        query = db.session.query(Warranties).all()
    else:
        query = db.session.query(Warranties).filter(Warranties.product.active == True).all()

    return jsonify({"message": "warranties found", "results": warranties_schema.dump(query)}), 200


@authenticate_return_auth
def get_warranty_by_id(warranty_id, auth_info):
    query = False

    if auth_info.user.is_admin == True:
        query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
    else:
        query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id, Warranties.product.active == True).first()

    if not query:
        return jsonify({"message": "warranty not found"}), 404
    

    return jsonify({"message": "warranty found", "result": warranty_schema.dump(query)}), 200


@authenticate_return_auth
def update_warranty_by_id(warranty_id, auth_info):
    if auth_info.user.is_admin == True:
        post_data = request.form if request.form else request.json
        query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

        if not query:
            return jsonify({"message": "warranty not found"}), 404 

        try:
            populate_object(query, post_data)
            db.session.commit()
        
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update warranty"}), 400

        return jsonify({"message": "warranty updated", "result": warranty_schema.dump(query)}), 200
    
    return jsonify({"message": "unauthorized"}), 403


@authenticate_return_auth
def delete_warranty_by_id(warranty_id, auth_info):
    if auth_info.user.is_admin == True:
        query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

        if not query:
            return jsonify({"message": "warranty not found"}), 404
        
        try:
            db.session.delete(query)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete warranty"}), 400
        
        return jsonify({"message": "warranty deleted"}), 200
    
    return jsonify({"message": "unauthorized"}), 403