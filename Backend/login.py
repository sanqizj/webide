import os

from flask import Blueprint, request, json

from utils.file_utils import new_file
from model import User

login_page = Blueprint('login_page', __name__)


@login_page.route('/login/', methods=['POST'])
def login():
    # 登录对应账户
    if request.method == 'POST':
        data = request.get_json()
        id = data['userid']
        pwd = data['password']
        query = User.query.get(id)
        if query is None:
            return json.jsonify({"status": False, 'error': 'user not exists'})
        if query.password == pwd:
            return json.jsonify({"status": True, "userid": id})
        else:
            return json.jsonify({"status": False, 'error': 'wrong password'})
    return json.jsonify({'status': False, 'error': 'wrong method'})


@login_page.route('/sign_up/', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        data = request.get_json()
        id = data['userid']
        pwd = data['password']
        query = User.query.get(id)
        if query is not None:
            return json.jsonify({'status': False, 'error': 'user already exists'})
        User(id, pwd)
        path = os.path.join('users', id)
        new_file(path, 'dir')
        return json.jsonify({'status': True})
    return json.jsonify({'status': False, 'error': 'wrong method'})