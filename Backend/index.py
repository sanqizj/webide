from flask import Blueprint, request, json
import os
from utils.file_utils import new_file, rename_file, delete_file, get_file_tree

index_page = Blueprint('index_page', __name__)


@index_page.route('/<userid>/', methods=['GET', 'POST'])
def index(userid: str):
    if request.method == 'GET':
        # 获取userid目录下所有文件夹名称并返回
        path = os.path.join('users', userid)
        tmp = os.listdir(path)
        for i in tmp:
            if not os.path.isdir(os.path.join(path, i)):
                tmp.remove(i)
        return json.jsonify({'status': True, 'projects': tmp})
    return json.jsonify({'status': False, 'error': 'wrong method'})


@index_page.route('/open/<userid>/<project_name>/', methods=['GET'])
def open_project(userid: str, project_name: str):
    if request.method == 'GET':
        path = os.path.join('users', userid, project_name)
        # 获取项目文件树
        if os.path.isdir(path):
            tmp = get_file_tree(path)
            return json.jsonify({'status': True, 'file_tree': tmp})
        return json.jsonify({'status': False, 'error': 'dir not exists'})
    return json.jsonify({'status': False, 'error': 'wrong method'})


@index_page.route('/new_project/<userid>/<project_name>/', methods=['GET'])
def new_project(userid: str, project_name: str):
    # 创建新项目(需要声明项目名称)
    if request.method == 'POST':
        path = os.path.join('users', userid, project_name)
        res = new_file(path, 'dir')
        return json.jsonify(res)
    return json.jsonify({'status': False, 'error': 'wrong method'})


@index_page.route('/rename/<userid>/<old_name>/', methods=['GET'])
def rename_project(userid: str, old_name: str):
    if request.method == 'GET':
        old_path = os.path.join('users', userid, old_name)
        new_path = os.path.join('users', userid, request.args.get('new_name'))
        res = rename_file(old_path, new_path)
        return json.jsonify(res)
    return json.jsonify({'status': False, 'error': 'wrong method'})


@index_page.route('/delete/<userid>/<project_name>/', methods=['GET'])
def delete_project(userid: str, project_name: str):
    if request.method == 'GET':
        path = os.path.join('users', userid, project_name)
        res = delete_file(path)
        return json.jsonify(res)
    return json.jsonify({'status': False, 'error': 'wrong method'})
