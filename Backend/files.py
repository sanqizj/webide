import os

from flask import Blueprint, request, send_file, json
from werkzeug.utils import secure_filename

from utils.file_utils import new_file, rename_file, delete_file

current_file = Blueprint('files', __name__, url_prefix='/files')


@current_file.route('/<userid>/<path:filepath>/', methods=['GET'])
def get_file_content(userid: str, filepath: str):
    # 获取文件内容
    if request.method == 'GET':
        path = os.path.join('users', userid, filepath)
        try:
            file = open(path)
        except FileNotFoundError:
            return json.jsonify({"status": False, "error": "file not found"})
        return json.jsonify({"status": True, "content": file.read()})
    return json.jsonify({'status': False, 'error': 'wrong method'})


@current_file.route('/new_file/<userid>/<path:filepath>/', methods=['GET'])
def create_file(userid: str, filepath: str):
    if request.method == 'GET':
        path = os.path.join('users', userid, filepath)
        res = new_file(path, request.args.get('type'))
        return json.jsonify(res)
    return json.jsonify({'status': False, 'error': 'wrong method'})


@current_file.route('/rename/<userid>/<path:filepath>/', methods=['GET'])
def rename(userid: str, filepath: str):
    if request.method == 'GET':
        old_path = os.path.join('users', userid, filepath)
        new_path = os.path.join('users', userid, request.args.get('new_path'))
        res = rename_file(old_path, new_path)
        return json.jsonify(res)
    return json.jsonify({'status': False, 'error': 'wrong method'})


@current_file.route('/delete/<userid>/<path:filepath>/', methods=['GET'])
def delete(userid: str, filepath: str):
    if request.method == 'GET':
        path = os.path.join('users', userid, filepath)
        res = delete_file(path)
        return json.jsonify(res)
    return json.jsonify({'status': False, 'error': 'wrong method'})


@current_file.route('/download/<userid>/<path:filepath>/', methods=['GET'])
def download(userid: str, filepath: str):
    if request.method == 'GET':
        filepath = filepath.rstrip('/')
        path = os.path.join('users', userid, filepath)
        if os.path.isfile(path):
            filename = path.split('/')[-1]
            res = send_file(path_or_file=path, download_name=filename)
            return res
        return json.jsonify({'status': False, 'error': 'file not exists'})
    return json.jsonify({'status': False, 'error': 'wrong method'})


@current_file.route('/upload/<userid>/<path:filepath>/', methods=['POST'])
def upload(userid: str, filepath: str):
    if request.method == 'POST':
        file = request.files['file']
        filename = filepath.split('/')[-1]
        filepath = filepath.rstrip(filename)
        path = os.path.join('users', userid, filepath, secure_filename(filename))
        if not os.path.exists(path):
            file.save(path)
            if os.path.exists(path):
                return json.jsonify({'status': True})
            return json.jsonify({'status': False, 'error': 'server error, upload failed'})
        return json.jsonify({'status': False, 'error': 'file already exists'})
    return json.jsonify({'status': False, 'error': 'wrong method'})
