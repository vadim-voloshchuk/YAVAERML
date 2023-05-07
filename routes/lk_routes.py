from flask import Blueprint, request
from __main__ import db, pricing_list
import json
from flask_login import login_required, current_user
from models.description_model import Description
from models.config_lk_model import ConfigLK
from models.user_model import User
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
    design_color = {
        "design_color": ConfigLK.query.get(current_user.id).design
        }
    return json.dumps(design_color)

@lk.route("/change_design_color")
@login_required
def change_design_color():
    db.session.query(ConfigLK).filter(ConfigLK.user_id == current_user.id).update({"design": request.json['design']}, synchronize_session=False)
    db.session.commit()
    return "Успешно"

@lk.route("/get_tariff_plan")
@login_required
def get_tariff_plan():
    tariff_plan = {
        "tariff_plan": ConfigLK.query.get(current_user.id).tariff_plan
        }
    return json.dumps(tariff_plan)

@lk.route("/choice_of_tariff_plan")
@login_required
def choice_of_tariff_plan():
    choice = request.json['tariff_plan']
    if choice in pricing_list.keys():
        db.session.query(ConfigLK).filter(ConfigLK.user_id == current_user.id).update({"tariff_plan": request.json['tariff_plan']}, synchronize_session=False)
        db.session.commit()
        return "Успешно"
    return "Такого тарифного плана не существует"

@lk.route("/delete_account")
def delete_account():
    db.session.query(User).filter(User.id == current_user.id).delete()
    db.session.commit()
    return "Аккаунт успешно удалён"
