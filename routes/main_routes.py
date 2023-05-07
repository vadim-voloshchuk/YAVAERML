from flask import Blueprint
# from __main__ import db
import json

main = Blueprint('main', __name__)

@main.route("/")
def hello():
    return "Hello, main!"

@main.route("/welcome_message", methods=['GET'])
def welcome_message():
    with open('files/welcome_message.txt', encoding='utf-8') as file:
        text = file.read()
    return text

@main.route("/features_list", methods=['GET'])
def features_list():
    with open('files/features_list.txt', encoding='utf-8') as file:
        end_count = 0
        next_feature = True
        previous_text = False
        features_titles = []
        features_text = []
        features = {}

        while True:
            line = file.readline()

            if line == '\n':
                end_count += 1

                if end_count == 2:
                    break
                else:
                    next_feature = True
                    previous_text = False
                    continue

            if previous_text:
                features_text[-1] = features_text[-1] + line
                continue

            if next_feature:
                features_titles.append(line.rstrip('\n'))
                next_feature = False
                end_count = 0
            else:
                features_text.append(line)
                previous_text = True

    for index in range(len(features_titles)):
        features[features_titles[index]] = features_text[index]
    
    print(features)
    
    return json.dumps(features)

@main.route("/pricing", methods = ['GET'])
def pricing():
    with open('files/pricing.txt', encoding='utf-8') as file:
        lines = file.readlines()
    
    pricing_dict = {}
    for number in range(int(len(lines)/2)):
        index = number * 2
        pricing_dict[lines[index].rstrip('\n')] = lines[index+1].rstrip('\n').split('\t')

    print(pricing_dict)

    return json.dumps(pricing_dict)
