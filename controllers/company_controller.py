from flask import request, jsonify

from models.company import Companies, companies_schema, company_schema
from lib.authenticate import authenticate, authenticate_return_auth
from util.reflection import populate_object
from db import db

@authenticate_return_auth
def add_company(auth_info):
    if auth_info.user.is_admin == True:
        post_data = request.form if request.form else request.json

        new_company = Companies.new_company_obj()

        populate_object(new_company, post_data)

        try:
            db.session.add(new_company)
            db.session.commit()

        except:
            db.session.rollback()
            return jsonify({"message": "unable to add company"}), 400

        return jsonify({"message": "company added", "result": company_schema.dump(new_company)}), 201
    
    return jsonify ({"message": "unauthorized"}), 403

@authenticate
def get_all_companies():
    query = db.session.query(Companies).all()

    return jsonify({"message": "company found", "results": companies_schema.dump(query)}), 200

@authenticate
def get_company_by_id(company_id):
    query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not query:
        return jsonify({"message": "company not found"}), 404
    
    return jsonify({"message": "company found", "result": company_schema.dump(query)}), 200


@authenticate_return_auth
def update_company_by_id(company_id, auth_info):
    if auth_info.user.is_admin == True:
        post_data = request.form if request.form else request.json
        query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

        if not query:
            return jsonify({"message": "company not found"}), 404
        

        try:
            populate_object(query, post_data)
            db.session.commit()
        
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update company"}), 400

        return jsonify({"message": "company updated", "result": company_schema.dump(query)}), 200
    
    return jsonify ({"message": "unauthorized"}), 403


@authenticate_return_auth
def delete_company_by_id(company_id, auth_info):
    if auth_info.user.is_admin == True:
        query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

        if not query:
            return jsonify({"message": "company not found"}), 404
        
        try:
            db.session.delete(query)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete company"}), 400
        
        return jsonify({"message": "company deleted"}), 200
    
    return jsonify ({"message": "unauthorized"}), 403
