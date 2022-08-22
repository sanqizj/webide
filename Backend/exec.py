import os

from flask import Blueprint, request, json

from utils.file_utils import execute_pyfile, debug_pyfile, execute_javafile

file_exec = Blueprint('exec', __name__)


@file_exec.route('/exec/<userid>/<path:filepath>/', methods=['GET'])
def exec_file(userid: str, filepath: str):
    if request.method == 'GET':
        path = os.path.join('users', userid, filepath)
        res = execute_pyfile(path)
        return json.jsonify(res)
    return json.jsonify({'status': False, 'error': 'wrong method'})


@file_exec.route('/debug/<userid>/<path:filepath>/', methods=['GET'])
def debug_file(userid: str, filepath: str):
    if request.method == 'GET':
        pass