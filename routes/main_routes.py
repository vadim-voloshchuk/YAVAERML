from flask import Blueprint
# from __main__ import db
import json

main = Blueprint('main', __name__)

from __main__ import features, pricing_list, welcome_text

@main.route("/")
def hello():
    return "Hello, main!"

@main.route("/welcome_message", methods=['GET'])
def welcome_message():
    return welcome_text

@main.route("/features_list", methods=['GET'])
def features_list():    
    print(features)
    return json.dumps(features)

@main.route("/pricing", methods = ['GET'])
def pricing():
    print(pricing_list)
    return json.dumps(pricing_list)
