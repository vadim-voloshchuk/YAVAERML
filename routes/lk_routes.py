from flask import Blueprint, request
from __main__ import db
import json
from flask_login import login_required, current_user
from models.description_model import Description
from werkzeug.security import generate_password_hash


lk = Blueprint('lk', __name__)

# Возвращает имя, почту и телефон + описание деятельности из отдельной таблицы
@lk.route("/get_user_info", methods=['GET'])
@login_required
def get_user_info():
    try:
        user_description = Description.query.get(current_user.id).description
    except:
        user_description = None
    user_info = {
        "name": current_user.name,
        "email": current_user.email,
        "phone_number": current_user.phone_number,
        "description": user_description
    }
    return json.dumps(user_info)

@lk.route("/edit_user_name")
@login_required
def edit_user_name():
    current_user.name = request.json['name']
    db.session.commit()
    return "Успешно"

@lk.route("/edit_user_email")
@login_required
def edit_user_email():
    current_user.email = request.json['email']
    db.session.commit()
    return "Успешно"

@lk.route("/edit_user_phone_number")
@login_required
def edit_user_phone_number():
    current_user.phone_number = request.json['phone_number']
    db.session.commit()
    return "Успешно"

@lk.route("/edit_user_description")
@login_required
def edit_user_description():
    try:
        db.session.query(Description).filter(Description.user_id == current_user.id).update({"description": request.json['description']}, synchronize_session=False)
    except:
        new_description = Description(user_id=current_user.id, description=request.json['description'])
        db.session.add(new_description)
    db.session.commit()
    return "Успешно"

@lk.route("/change_password")
@login_required
def change_password():
    current_user.password = generate_password_hash(request.json['password'])
    db.session.commit()
    return "Успешно"

@lk.route("/get_design_color")
@login_required
def get_design_color():
    return "OK"

@lk.route("/change_design_color")
@login_required
def change_design_color():
    return "OK"

@lk.route("/choice_of_tariff_plan")
@login_required
def choice_of_tariff_plan():
    return "OK"
