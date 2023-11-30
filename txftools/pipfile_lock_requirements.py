import json


def pipfile_lock_requirements():
    with open('Pipfile.lock', 'r') as f:
        ret = f.read()
        ret = json.loads(ret)
    default = ret['default']

    save_str = ''

    for i in default:
        str_ = i + default[i]['version']
        save_str += str_ + '\n'

    with open('requirements.txt', 'w') as f:
        f.write(save_str)

    print('python_version: ', ret['_meta']['requires']['python_version'])


if __name__ == '__main__':
    pipfile_lock_requirements()