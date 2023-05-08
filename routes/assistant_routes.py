from flask import Blueprint, request, send_file
from __main__ import db
import json
from models.template_model import Template
from flask_login import current_user, login_required
from io import BytesIO


assistant = Blueprint('assistant', __name__)

@assistant.route("/upload_template")
@login_required
def upload_template():
    file = request.files['template']
    new_template = Template(template_name=file.filename, user_id=current_user.id, template_file=file.stream.read())
    db.session.add(new_template)
    db.session.commit()
    return f"Успешное добавление шалона {file.filename}!"

@assistant.route("/download_template")
@login_required
def download_template():
    template = db.session.query(Template).filter(Template.template_name == request.json['template_name'], Template.user_id == current_user.id).first()
    return send_file(BytesIO(template.template_file), download_name=template.template_name, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

@assistant.route("/delete_template")
@login_required
def delete_template():
    template_name = request.json['template_name']
    db.session.query(Template).filter(Template.template_name == template_name, Template.user_id == current_user.id).delete()
    db.session.commit()
    return f"Шаблон {template_name} успешно удалён"
