from flask import Blueprint, request, jsonify, Response
from service.user import UserService
from pywebpush import webpush, WebPushException
from config.argsparser import ArgumentsParser

import os
import json

configs = ArgumentsParser()

user = Blueprint('user', __name__)
user_service = UserService()

# Define the private and public keys for Push Notifications
DER_BASE64_ENCODED_PRIVATE_KEY_FILE_PATH = os.path.join(configs.security_keys_path,"private_key.txt")
DER_BASE64_ENCODED_PUBLIC_KEY_FILE_PATH = os.path.join(configs.security_keys_path,"public_key.txt")

VAPID_PRIVATE_KEY = open(DER_BASE64_ENCODED_PRIVATE_KEY_FILE_PATH, "r+").readline().strip("\n")
VAPID_PUBLIC_KEY = open(DER_BASE64_ENCODED_PUBLIC_KEY_FILE_PATH, "r+").read().strip("\n")

@user.route('/register', methods=['GET', 'POST'])
def signup_user():
    data = request.get_json()
    user = user_service.register_user(data)

    return jsonify(user)

@user.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization
    token = user_service.login_user(auth)

    return token

VAPID_CLAIMS = {
"sub": "mailto:develop@raturi.in"
}

def send_web_push(subscription_information, message_body):
    return webpush(
        subscription_info=subscription_information,
        data=message_body,
        vapid_private_key=VAPID_PRIVATE_KEY,
        vapid_claims=VAPID_CLAIMS
    )

@user.route("/subscription/", methods=["GET", "POST"])
def subscription():
    """
        POST creates a subscription
        GET returns vapid public key which clients uses to send around push notification
    """

    if request.method == "GET":
        return Response(response=json.dumps({"public_key": VAPID_PUBLIC_KEY}),
            headers={"Access-Control-Allow-Origin": "*"}, content_type="application/json")

    subscription_token = request.get_json("subscription_token")
    return Response(status=201, mimetype="application/json")

@user.route("/push_v1/",methods=['POST'])
def push_v1():
    message = '{"message": "Push Test v1"}'
    print("is_json",request.is_json)

    if not request.json or not request.json.get('sub_token'):
        return jsonify({'failed':1})

    print("request.json",request.json)

    token = request.json.get('sub_token')
    try:
        token = json.loads(token)
        send_web_push(token, message)
        return jsonify({'success':1})
    except Exception as e:
        print("error",e)
        return jsonify({'failed':str(e)})