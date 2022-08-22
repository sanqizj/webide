import os
import random
from shutil import rmtree


def new_file(path: str, type: str):
    """
    创建一个新的文件或目录

    :param path: 文件或目录的路径
    :param type: ['file', 'dir']标识创建对象的属性
    :return: {"status": True/False, "error"(when False): "..."}
    """
    if type == 'file':
        if not os.path.exists(path):
            fd = open(path, mode='w')
            fd.close()
            if os.path.isfile(path):
                return {'status': True}
            return {'status': False, 'error': 'server error, create failed'}
        return {'status': False, 'error': 'file or dir exists'}
    elif type == 'dir':
        if not os.path.exists(path):
            os.mkdir(path)
            return {'status': True}
        return {'status': False, 'error': 'file or dir exists'}


def rename_file(old_path: str, new_path: str):
    """
    重命名指定文件或路径

    :param old_path: 文件或目录的原有路径
    :param new_path: 文件或目录的新路径
    :return: {"status": True/False, "error"(when False): "..."}
    """
    if os.path.exists(old_path):
        if not os.path.exists(new_path):
            os.rename(old_path, new_path)
            return {'status': True}
        return {'status': False, 'error': 'new name already exists'}
    return {'status': False, 'error': 'old file or dir not exists'}


def delete_file(path: str):
    """
    删除指定路径文件或递归删除指定路径目录

    :param path: 文件或目录路径
    :return: {"status": True/False, "error"(when False): "..."}
    """
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
            if os.path.exists(path):
                return {'status': False, 'error': 'server error,delete failed'}
            return {'status': True}
        elif os.path.isdir(path):
            rmtree(path)
            if os.path.exists(path):
                return {'status': False, 'error': 'server error,delete failed'}
            return {'status': True}
    return {'status': False, 'error': 'file or dir not exists'}


def get_file_tree(path: str):
    """
    根据给定文件夹名称打开指定项目并递归返回所有文件路径树

    :param path: 需要递归获取文件树的路径
    :return: dict封装的文件树,包含名称和类型(dir和file)
    """
    tmp = {}
    for i in os.listdir(path):
        if os.path.isdir(os.path.join(path, i)):
            res = get_file_tree(os.path.join(path, i))
            tmp[i] = (res, 'dir')
        elif os.path.isfile(os.path.join(path, i)):
            tmp[i] = ({}, 'file')
    return tmp


def execute_pyfile(path: str):
    if os.path.exists(path):
        if os.path.isfile(path):
            file_name, file_type = os.path.splitext(path)
            if file_type == '.py':
                log_name = str(random.randint(1000, 9999))
                command = 'python ' + path + ' > ' + log_name
                os.system(command)
                fp = open(log_name)
                res = fp.read()
                fp.close()
                os.remove(log_name)
                return {'status': True, 'content': res}
            return {'status': False, 'content': 'file type error'}
    return {'status': False, 'error': 'file not exists'}


def debug_pyfile(path: str):
    pass

def execute_javafile(path: str):
    pass
