from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from models.app_users import AppUsers, app_user_schema, app_users_schema
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth


def add_user():
    post_data = request.form if request.form else request.json

    new_user = AppUsers.new_user_obj()

    populate_object(new_user, post_data)

    new_user.password = generate_password_hash(new_user.password).decode('utf8')

        
    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to add record"}), 400
    
    return jsonify({"message": "user added", "result": app_user_schema.dump(new_user)}), 201


@authenticate_return_auth
def get_all_users(auth_info):
    users_query = db.session.query(AppUsers).all()

    if auth_info.user.is_admin == True:
        return jsonify({"message": "users found", "results": app_users_schema.dump(users_query)}), 201
    
    return jsonify({"message": "unauthorized"}), 403


@authenticate_return_auth
def get_user_by_id(user_id, auth_info):
    user_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()

    if auth_info.user.is_admin == True or user_id == str(auth_info.user.user_id):
        return jsonify({"message": "user found", "result": app_user_schema.dump(user_query)}), 200
    
    return jsonify({"message": "unauthorized"}), 403


@authenticate_return_auth
def update_user_by_id(user_id, auth_info):
    post_data = request.form if request.form else request.json
    query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()


    if auth_info.user.is_admin == True or user_id == str(auth_info.user.user_id):

        if not auth_info.user.is_admin and 'is_admin' in post_data:
            return jsonify({"message": "forbidden: cannot change is_admin"}), 403
        
        if not query:
            return jsonify({"message": "user not found"}), 404
        

        populate_object(query, post_data)

        if post_data.get('password'):
            password = post_data.get('password')

            query.password = generate_password_hash(password).decode('utf8')
        
        try:
            db.session.commit()

        except:
            db.session.rollback()
            return jsonify({"message": "user could not be updated"}), 400
    
        return jsonify({"message": "user updated", "result": app_user_schema.dump(query)})
    
    return jsonify({"message": "unauthorized"}), 403
        
    

@authenticate_return_auth
def delete_user_by_id(user_id, auth_info):
    query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()

    if auth_info.user.is_admin == True or user_id == str(auth_info.user.user_id):
        
        if not query:
            return jsonify({"message": "user not found"}), 404
        
        try:
            db.session.delete(query)
            db.session.commit()

        except:
            db.session.rollback()
            return jsonify({"message": "user could not be updated"}), 400
        
        return jsonify({"message": "user updated", "result": app_user_schema.dump(query)})
    
    return jsonify({"message": "unauthorized"}), 403

        