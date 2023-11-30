import os


def del_file_task(file_path: str, number: int, delete_file_flg=False):
    """
    清理指定文件夹下的文件，按照最新的时间保留number条
    Delete specified file keep the specified number of files

    file_path:
        execute file path
    count:
        How many are reserved
    delete_file_flg:
        chose True false
        return delete file list
    """
    files = os.listdir(file_path)
    if not file_path.endswith('/'):
        file_path += '/'
    file_dict = [{'time': os.path.getctime(file_path + i), 'file_path': file_path + i} for i in files]
    file_dict_sort = sorted(file_dict, key=lambda x: x['time'], reverse=True)

    for del_file in file_dict_sort[number:]:
        try:
            os.remove(del_file['file_path'])
        except Exception as e:
            print('delete file error info: {}'.format(e))
    if delete_file_flg:
        return file_dict_sort[number:]
    return True


if __name__ == '__main__':
    del_file_task(r'C:\Users\Admin\Desktop/1', 2)