from flask import Blueprint, request, send_file
from __main__ import db
import json
from models.template_model import Template
from models.chat_names_model import ChatNames
from models.messages_model import Messages
from models.file_model import File
from flask_login import current_user, login_required
from io import BytesIO

try:
    from fictitious_nn.fictitious_nn import processing_message
except:
    pass


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

@assistant.route("/add_chat")
@login_required
def add_chat():
    new_chat = ChatNames(user_id=current_user.id, chat_name=request.json['chat_name'])
    db.session.add(new_chat)
    db.session.commit()
    return "Новый чат создан"

@assistant.route("/get_chat_names")
@login_required
def get_chat_names():
    try:
        all_user_chats = db.session.query(ChatNames).filter(ChatNames.user_id == current_user.id).all()
    except:
        return "У вас ещё нет чатов с системой"
    chat_names_dict = {
        "chat_names": [each.chat_name for each in all_user_chats]
    }
    return json.dumps(chat_names_dict)

@assistant.route("/get_messages")
@login_required
def get_messages():

    def retrieve_mes_info(mes):
        if mes.have_file:
            file_name = db.session.query(File).filter(File.chat_id == mes.chat_id, File.message_number == mes.message_number).first().file_name
        else:
            file_name = None

        return [mes.message_number, mes.message, mes.is_user, file_name]
    
    count = int(request.json['count'])
    chat_name = request.json['chat_name']
    chat_id = db.session.query(ChatNames).filter(ChatNames.user_id == current_user.id, ChatNames.chat_name == chat_name).first().chat_id
    try:
        last_message_number = db.session.query(Messages, db.sql.func.max(Messages.message_number)).filter(Messages.chat_id == chat_id).first()[1]
    except:
        # last_message_number = None
        return "Здесь ещё нет сообщений"
    
    start_message_number = last_message_number - count + 1
    if start_message_number < 0:
        messages_lst = db.session.query(Messages).filter(Messages.chat_id == chat_id).all()
    else:
        messages_lst = db.session.query(Messages).filter(Messages.chat_id == chat_id, Messages.message_number <= last_message_number, Messages.message_number >= start_message_number).all()
    
    messages = {
        "messages": [retrieve_mes_info(each) for each in messages_lst]
    }
    # print(messages)
    return json.dumps(messages)

@assistant.route("/send_message")
@login_required
def send_message():
    cur_chat_name = request.json['chat_name']
    user_message = request.json['message']
    chat_names_raw = db.session.query(ChatNames).filter(ChatNames.user_id == current_user.id, ChatNames.chat_name == cur_chat_name).first()
    template_raw = db.session.query(Template).filter(Template.template_id == chat_names_raw.template_id).first()
    try:
        template_binary_file = template_raw.template_file
    except:
        template_binary_file = None
    sys_answer, file = processing_message(user_message, template_binary_file)

    new_gen_file = True if file != None else False

    chat_id = db.session.query(ChatNames).filter(ChatNames.user_id == current_user.id, ChatNames.chat_name == cur_chat_name).first().chat_id
    new_message = Messages(chat_id=chat_id, message=user_message, is_user=True, have_file=False)
    sys_message = Messages(chat_id=chat_id, message=sys_answer, is_user=False, have_file=new_gen_file)
    db.session.add(new_message)
    db.session.add(sys_message)
    db.session.commit()
    file_name = None
    new_message_number = db.session.query(Messages, db.sql.func.max(Messages.message_number)).filter(Messages.chat_id == chat_id).first()[1]
    if new_gen_file:
        file_name = f"Ответ системы на {new_message_number} сообщение чата {cur_chat_name} на основе {template_raw.template_name}"
        new_file = File(chat_id=chat_names_raw.chat_id, message_number=new_message_number,
                        file_name=file_name,
                        file=file)
        db.session.add(new_file)
        db.session.commit()
    answer = {
        "user_message_number": new_message_number - 1,
        "sys_message_number": new_message_number,
        "answer": sys_answer,
        "file_name": file_name
    }
    return json.dumps(answer)

@assistant.route("/attach_template")
@login_required
def attach_template():
    template_name = request.json['template_name']
    chat_name = request.json['chat_name']
    count_such_name = db.session.query(Template.template_name).filter(Template.user_id == current_user.id).count()
    if count_such_name > 0:
        return "Шаблон с таким именем уже существует"
    template_id = db.session.query(Template).filter(Template.user_id == current_user.id, Template.template_name == template_name).first().template_id
    db.session.query(ChatNames).filter(ChatNames.user_id == current_user.id, ChatNames.chat_name == chat_name).update({"template_id": template_id}, synchronize_session=False)
    db.session.commit()
    return f"Шаблон {template_name} прикреплён к  чату {chat_name}"

@assistant.route("/unlink_template")
@login_required
def unlink_template():
    chat_name = request.json['chat_name']
    db.session.query(ChatNames).filter(ChatNames.user_id == current_user.id, ChatNames.chat_name == chat_name).update({"template_id": None}, synchronize_session=False)
    db.session.commit()
    return f"Шаблон откреплён от чата {chat_name}."

@assistant.route("/download_file")
@login_required
def download_file():
    chat_name = request.json['chat_name']
    message_number = int(request.json['message_number'])
    chat_id = db.session.query(ChatNames).filter(ChatNames.user_id == current_user.id, ChatNames.chat_name == chat_name).first().chat_id
    file_raw = db.session.query(File).filter(File.chat_id == chat_id, File.message_number == message_number).first()
    return send_file(BytesIO(file_raw.file), download_name=file_raw.file_name)
