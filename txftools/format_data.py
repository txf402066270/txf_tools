# -*- coding:utf-8 -*-
import copy
import json


class FormatData(object):
    """数据格式化"""

    def set_only_field(self, dict_data, keys):
        """
        根据字典的key取值 将值通过_连在一起
        对应的key没结果忽略

        dict_data = {'a':1, 'b':2, 'c':3}
        keys = ['a', 'b']
        return {'1_2': {'a':1, 'b':2, 'c':3}}
        """

        if not isinstance(keys, (list, tuple, set)):
            keys = [keys]
        join_data = []
        for i in keys:
            if dict_data[i]:
                join_data.append(dict_data[i])
        if not join_data:
            return ''
        return '_'.join(join_data)

    def merge_values(self, *args, connect='||', original=True):
        """
        original True保留原始的数据类型
        保留原始的数据
            connect 字符串连接符
        args 要合并的数据
        +====================+=====================================================+
        |  数据类型           |   处理手段                                            |
        +--------------------+-----------------------------------------------------+
        |  tuple             |   tuple->list  list+list    tuple(list+list)        |
        +--------------------+-----------------------------------------------------+
        |  list              |   list+list                                         |
        +--------------------+-----------------------------------------------------+
        |  set               |   set->list  list+list    set(list+list)            |
        +--------------------+-----------------------------------------------------+
        |  dict              |   dict={} dict.update(dictn)                        |
        +--------------------+-----------------------------------------------------+
        |  int               |   sum([int1, int2, ...])                            |
        +--------------------+-----------------------------------------------------+
        |  str               |   str1||str2||str... 更新为 [str1, str2, str3...]    |
        +--------------------+-----------------------------------------------------+
        |  json_str          |   original=True 转为对应的类型操作再转回json_str        |
        |                    |   original=False 转为对应的类型操作不转回json_str       |
        +--------------------+-----------------------------------------------------+
        """
        ret = []

        data_type = None

        for i in args:
            if i:
                if isinstance(i, int):
                    ret.append(i)
                    data_type = 'int'
                elif isinstance(i, str):
                    data_type = 'str'
                    try:
                        eval_i = json.loads(i)
                    except Exception as e:
                        eval_i = i
                    if isinstance(eval_i, int):
                        ret.append(i)
                    else:
                        ret.append(eval_i)
                else:
                    ret.append(i)
                    data_type = type(i)
        if not ret:
            return ret

        return_data = None
        if all(isinstance(x, int) for x in ret):
            return_data = sum(ret)
        elif all(isinstance(x, str) for x in ret):
            if original:
                return_data = connect.join(ret)
            else:
                return_data = ret
        elif all(isinstance(x, set) for x in ret):
            return_data = set([i for s in ret for i in s])
        elif all(isinstance(x, list) for x in ret):
            return_data = [i for s in ret for i in s]
        elif all(isinstance(x, dict) for x in ret):
            d = {}
            for i in ret:
                d.update(i)
            return_data = d
        elif all(isinstance(x, tuple) for x in ret):
            return_data = tuple([j for i in ret for j in i])

        if (data_type == 'str') and (not isinstance(ret[0], str)) and original:
            return_data = json.dumps(return_data)

        return return_data

    def set_merge_key(self, data_dict, only_keys, merge_keys):
        """
        如果 merge_keys没有 我们就认为它除了 only_keys指定的字段全部都要合并
        return merge_keys
                [{'relations': '1534805731762020352', 'industry_domain': '通信与信息系统', 'user_name': '刘亚东', 'achv_name': '宽带网的开发与发展||加强自主创新发展信息产业', 'school': '黑龙江省电子信息产品监督检验院', 'psnl_lable': "{'a': 1, 'b':2}||{'a': 1, 'b':2 'c':3}"}]

        """
        if not merge_keys:
            merge_keys = list(data_dict.keys())
            if not isinstance(only_keys, (list, tuple, set)):
                only_keys = [only_keys]
            for k in only_keys:
                merge_keys.remove(k)
        return merge_keys

    def list_dict_merge_only_keys(self, data_list, only_keys, merge_keys, connect='||', original=True):
        """
        merge_keys:
            ['achv_name', 'psnl_lable', 'industry_domain','school']
        only_keys: 'relations'
        data_list:
            [{
                'relations': '1534805731762020352',
                'industry_domain': '通信与信息系统',
                'user_name': '刘亚东',
                'achv_name': '["宽带网的开发与发展"]',
                'school': 1,
                'psnl_lable': '{"a": 1, "b":2 }',
                'testl': [0, 1, 2, 4, 5],
                'testt': (0, 1, 2, 4, 5),
                'tests': {0, 1, 2, 4, 5},
                'testd': {1: 2, 'dd': 4}
            }, {
                'relations': '1534805731762020352',
                'industry_domain': '通信与信息系统1',
                'user_name': '刘亚东',
                'achv_name': '["加强自主创新发展信息产业"]',
                'school': 2,
                'psnl_lable': '{"a": 1, "b":2, "c":3}',
                'testl': [0, 1, 2, 4, 5],
                'testt': (0, 1, 2, 4, 5, 6, 7),
                'tests': {0, 1, 2, 4, 5, 6, 7, 9},
                'testd': {1: 2, 'd': 4}
            }]
        return
            [{
                'relations': '1534805731762020352',
                'industry_domain': '通信与信息系统||通信与信息系统1',
                'user_name': '刘亚东',
                'achv_name': '["\宽\带\网\的\开\发\与\发\展", "\加\强\自\主\创\新\发\展\信\息\产\业"]',
                'school': 3,
                'psnl_lable': '{"a": 1, "b": 2, "c": 3}',
                'testl': [0, 1, 2, 4, 5],
                'testt': (0, 1, 2, 4, 5, 0, 1, 2, 4, 5, 6, 7),
                'tests': {0, 1, 2, 4, 5, 6, 7, 9},
                'testd': { 1: 2, 'dd': 4, 'd': 4}
            }]

        """

        merge_keys = self.set_merge_key(data_list[0], only_keys, merge_keys)

        ret = {}
        for i in data_list:
            only_key = self.set_only_field(dict_data=i, keys=only_keys)

            if only_key not in ret:
                ret[only_key] = i
            else:
                for j in merge_keys:
                    if ret[only_key][j] != i[j]:
                        ret[only_key][j] = self.merge_values(ret[only_key][j], i[j], connect=connect, original=original)

        return list(ret.values())

    def list_dict_merge_no_keys(self, data_list, int_flot=True, original=True):
        """
        int_flot = True dict的值为纯int or float

            x={'a':1,'b':2,'c':3}
            y={'c':4,'b':5}
            from collections import Counter
            X,Y=Counter(x),Counter(y)
            z=dict(X+Y)
            print(z)
            {'a': 1, 'b': 7, 'c': 7}

        int_flot = False dict的值为非（int or float）

        """
        # dict的值为纯int or float
        if int_flot:
            from collections import Counter
            bs = Counter({})
            for d in data_list:
                bs += Counter(d)
            return dict(bs)
        # dict的值为非int or float
        else:
            bs = {}
            for d in data_list:
                for j in d:
                    if j not in bs:
                        bs[j] = d[j]
                    else:
                        bs[j] = self.merge_values(bs[j], d[j], original=original)
            return bs

    def list_dict_merge(self, data_list, only_keys, merge_keys, connect='||', original=True):
        """
        有 only_keys 表示将
        """
        if only_keys:
            return self.list_dict_merge_only_keys(data_list, only_keys, merge_keys, connect=connect, original=original)
        else:
            return self.list_dict_merge_no_keys(data_list)

    def list_dict_replace_key(self, data, base_dict):
        """
        将 [{},{}] 或者 {}
        dict中的key替换为base_dict的value

        base_dict {'id': 'ID', 'create_time': '创建时间', 'update_time': '更新时间', 'is_delete': 'is delete', 'tb_key': '字段名称', 'tb_value': '结果', 'tb_date': '时间', 'year_q': '年度季度标识', 'company_code': '公司编号'}
        data      [{'id': 1, 'create_time': datetime.datetime(2022, 5, 17, 9, 53, 39, 807886, tzinfo=datetime.timezone.utc), 'update_time': datetime.datetime(2022, 5, 17, 9, 53, 39, 807886, tzinfo=datetime.timezone.utc), 'is_delete': False, 'tb_key': '财务历史信息表_人数', 'tb_value': 29860.0, 'tb_date': '2014', 'year_q': 'y', 'company_code': '000001'}, {'id': 2, 'create_time': datetime.datetime(2022, 5, 17, 9, 53, 39, 807886, tzinfo=datetime.timezone.utc), 'update_time': datetime.datetime(2022, 5, 17, 9, 53, 39, 807886, tzinfo=datetime.timezone.utc), 'is_delete': False, 'tb_key': '财务历史信息表_净利润(上期)', 'tb_value': None, 'tb_date': '2014', 'year_q': 'y', 'company_code': '000001'}, {'id': 3, 'create_time': datetime.datetime(2022, 5, 17, 9, 53, 39, 807886, tzinfo=datetime.timezone.utc), 'update_time': datetime.datetime(2022, 5, 17, 9, 53, 39, 807886, tzinfo=datetime.timezone.utc), 'is_delete': False, 'tb_key': '财务历史信息表_净利润(本期)', 'tb_value': 19802000000.0, 'tb_date': '2014', 'year_q': 'y', 'company_code': '000001'}]>
        return    [{'ID': 1}, {'创建时间': datetime.datetime(2022, 5, 17, 9, 53, 39, 807886, tzinfo=datetime.timezone.utc)}, {'更新时间': datetime.datetime(2022, 5, 17, 9, 53, 39, 807886, tzinfo=datetime.timezone.utc)}, {'is delete': False}, {'字段名称': '财务历史信息表_人数'}, {'结果': 29860.0}, {'时间': '2014'}, {'年度季度标识': 'y'}, {'公司编号': '000001'}, {'ID': 2}, {'创建时间': datetime.datetime(2022, 5, 17, 9, 53, 39, 807886, tzinfo=datetime.timezone.utc)}, {'更新时间': datetime.datetime(2022, 5, 17, 9, 53, 39, 807886, tzinfo=datetime.timezone.utc)}, {'is delete': False}, {'字段名称': '财务历史信息表_净利润(上期)'}, {'结果': None}, {'时间': '2014'}, {'年度季度标识': 'y'}, {'公司编号': '000001'}, {'ID': 3}, {'创建时间': datetime.datetime(2022, 5, 17, 9, 53, 39, 807886, tzinfo=datetime.timezone.utc)}, {'更新时间': datetime.datetime(2022, 5, 17, 9, 53, 39, 807886, tzinfo=datetime.timezone.utc)}, {'is delete': False}, {'字段名称': '财务历史信息表_净利润(本期)'}, {'结果': 19802000000.0}, {'时间': '2014'}, {'年度季度标识': 'y'}, {'公司编号': '000001'}]

        """
        ret = []
        if isinstance(data, dict):
            ret = {}
            for i in data:
                ret[base_dict[i]] = data[i]

        if isinstance(data, list):
            ret = []
            for dt in data:
                for i in dt:
                    ret.append({base_dict[i]: dt[i]})
        return ret


def list_nesting_dict_merge(data_list, only_keys=None, merge_keys=None, connect='||', original=True):
    """
    data_list [{}, {}] or [] or {}
    original=True 合并后结果保留原来的类型  参考 merge_values

    将dict进行合并
    没有only_keys，是所有dict的相同的key的值进行合并

    有only_keys，将only_keys相同的dict 指定的merge_keys进行合并 merge_keys没指定的就不处理默认为第一个的值

    没有merge_keys, 全部的key去掉only_keys剩下的就是merge_keys
    合并的规则   参考 merge_values(self, *args, connect='||')
    """
    data_list = copy.deepcopy(data_list)
    if not data_list:
        return []
    return FormatData().list_dict_merge(data_list=data_list, only_keys=only_keys, merge_keys=merge_keys, connect=connect, original=original)


class TreeListMutualTurn(object):
    """tree 和 list 相互转换"""

    def __init__(self):
        self.tree_to_list_ret = []
        self.list_to_tree_ret = {}

    def list_to_tree(self, data, key, father_key, relations_key='children'):
        """
        切记 要处理的数据 的key的值和 father_key不能有相同的，如果有会出现 Circular reference detected
        list ==> tree

        in
            [{"code": "1", "parent_code": "0"},
            {"code": "11", "parent_code": "1"},
            {"code": "111", "parent_code": "11"},
            {"code": "1111", "parent_code": "111"},
            {"code": "11111", "parent_code": "1111"},
            {"code": "111111", "parent_code": "111111"},
            {"code": "2", "parent_code": "0"},
            {"code": "22", "parent_code": "2"},
            {"code": "222", "parent_code": "22"}
            ]

        out
            {
                '1': {
                    'sub': [{
                        'sub': [{
                            'sub': [{
                                'sub': [{
                                    'sub': [],
                                    'code': '11111',
                                    'parent_code': '1111'
                                }],
                                'code': '1111',
                                'parent_code': '111'
                            }],
                            'code': '111',
                            'parent_code': '11'
                        }],
                        'code': '11',
                        'parent_code': '1'
                    }],
                    'code': '1',
                    'parent_code': '0'
                },
                '0': {
                    'sub': [{
                        'sub': [{
                            'sub': [{
                                'sub': [{
                                    'sub': [{
                                        'sub': [],
                                        'code': '11111',
                                        'parent_code': '1111'
                                    }],
                                    'code': '1111',
                                    'parent_code': '111'
                                }],
                                'code': '111',
                                'parent_code': '11'
                            }],
                            'code': '11',
                            'parent_code': '1'
                        }],
                        'code': '1',
                        'parent_code': '0'
                    }, {
                        'sub': [{
                            'sub': [{
                                'sub': [],
                                'code': '222',
                                'parent_code': '22'
                            }],
                            'code': '22',
                            'parent_code': '2'
                        }],
                        'code': '2',
                        'parent_code': '0'
                    }]
                },
                '11': {
                    'sub': [{
                        'sub': [{
                            'sub': [{
                                'sub': [],
                                'code': '11111',
                                'parent_code': '1111'
                            }],
                            'code': '1111',
                            'parent_code': '111'
                        }],
                        'code': '111',
                        'parent_code': '11'
                    }],
                    'code': '11',
                    'parent_code': '1'
                },
                '111': {
                    'sub': [{
                        'sub': [{
                            'sub': [],
                            'code': '11111',
                            'parent_code': '1111'
                        }],
                        'code': '1111',
                        'parent_code': '111'
                    }],
                    'code': '111',
                    'parent_code': '11'
                },
                '1111': {
                    'sub': [{
                        'sub': [],
                        'code': '11111',
                        'parent_code': '1111'
                    }],
                    'code': '1111',
                    'parent_code': '111'
                },
                '11111': {
                    'sub': [],
                    'code': '11111',
                    'parent_code': '1111'
                },
                '111111': {
                    'sub': [{ ...
                    }],
                    'code': '111111',
                    'parent_code': '111111'
                },
                '2': {
                    'sub': [{
                        'sub': [{
                            'sub': [],
                            'code': '222',
                            'parent_code': '22'
                        }],
                        'code': '22',
                        'parent_code': '2'
                    }],
                    'code': '2',
                    'parent_code': '0'
                },
                '22': {
                    'sub': [{
                        'sub': [],
                        'code': '222',
                        'parent_code': '22'
                    }],
                    'code': '22',
                    'parent_code': '2'
                },
                '222': {
                    'sub': [],
                    'code': '222',
                    'parent_code': '22'
                }
            }

        """

        for a in data:
            self.list_to_tree_ret.setdefault(a[key], {relations_key: []})
            self.list_to_tree_ret.setdefault(a[father_key], {relations_key: []})
            self.list_to_tree_ret[a[key]].update(a)
            self.list_to_tree_ret[a[father_key]][relations_key].append(self.list_to_tree_ret[a[key]])

        return self.list_to_tree_ret

    def tree_to_list(self, data, dict_len, subs='children'):
        """将树结构转 平滑的dict
        data: dict
        subs: 子key
        dict_len: dict达到多长就新增到list

        输入
        {'children': [{'children': [{'children': [{'children': [{'children': [], 'code': '11111', 'parent_code': '1111'}], 'code': '1111', 'parent_code': '111'}], 'code': '111', 'parent_code': '11'}], 'code': '11', 'parent_code': '1'}], 'code': '1', 'parent_code': '0'}
        输出
            [{'code': '1', 'parent_code': '0'}, {'code': '11', 'parent_code': '1'}, {'code': '111', 'parent_code': '11'}, {'code': '1111', 'parent_code': '111'}, {'code': '11111', 'parent_code': '1111'}]

        """

        def set_ret(data):
            d = {}
            keys = list(data.keys())
            try:
                keys.remove(subs)
                keys.append(subs)
            except:
                pass

            for i in keys:
                if i != subs:
                    d[i] = data[i]

                if len(d) == dict_len:
                    self.tree_to_list_ret.append(d)
                    d = {}

                elif i == subs:
                    self.tree_to_list(data[i], dict_len=dict_len, subs=subs)

        if isinstance(data, dict):
            set_ret(data)

        elif isinstance(data, list):
            for ddata in data:
                set_ret(ddata)


class HtmlFormatData(object):
    def header_format(self, headers, format_out=False, ensure_ascii=True):
        """
        ensure_ascii: True 中文字符转移为unicode
        format_out: False 输出的格式为dict
        ensure_ascii: True 输出的格式为json
        """
        d = {}
        for i in headers.split('\n'):
            if i.startswith(':'):
                i = i.replace(':', '', 1)
            d[i.split(':')[0].strip()] = i.split(':')[1].strip()
        if not format_out:
            return d

        else:
            # indent 缩进空格 等于一个tab
            return json.dumps(d, indent=4, ensure_ascii=ensure_ascii)


def bs64_str(data, out_type='s'):
    """
    base64和bytes互相转换
    data 数据
    out_type: s:str b:bytes

    out_type=s data type is bytes
    out_type=b data type is str

    测试
    data = b'123'

    vs = bs64_str(data, out_type='s')
    vb = bs64_str(vs, out_type='b')
    print(vs)  # MTIz
    print(vb)  # b'123'
    """
    import base64

    if out_type == 's':
        base64_data = base64.b64encode(data)
        return base64_data.decode()
    else:
        return base64.b64decode(data)


if __name__ == '__main__':
    # l = [{
    #             'relations': '1534805731762020352',
    #             'industry_domain': '通信与信息系统',
    #             'user_name': '刘亚东',
    #             'achv_name': '["宽带网的开发与发展"]',
    #             'school': 1,
    #             'psnl_lable': '{"a": 1, "b":2 }',
    #             'testl': [0, 1, 2, 4, 5],
    #             'testt': (0, 1, 2, 4, 5),
    #             'tests': {0, 1, 2, 4, 5},
    #             'testd': {1: 2, 'dd': 4}
    #         }, {
    #             'relations': '1534805731762020352',
    #             'industry_domain': '通信与信息系统1',
    #             'user_name': '刘亚东',
    #             'achv_name': '["加强自主创新发展信息产业"]',
    #             'school': 2,
    #             'psnl_lable': '{"a": 1, "b":2, "c":3}',
    #             'testl': [0, 1, 2, 4, 5],
    #             'testt': (0, 1, 2, 4, 5, 6, 7),
    #             'tests': {0, 1, 2, 4, 5, 6, 7, 9},
    #             'testd': {1: 2, 'd': 4}
    #         }]
    #
    # print(list_nesting_dict_merge(l, only_keys='relations', merge_keys=None, original=False))

    v = HtmlFormatData().header_format(""":authority: event.csdn.net
:method: GET
:path: /logstores/csdn-pc-tracking-pageview/track_ua.gif?APIVersion=0.6.0&cid=10_19716719970-1669191024099-171770&sid=10_1673666420072.385659&pid=blog&uid=&did=10_19716719970-1669191024099-171770&dc_sid=c1c807a17d10002c66d451d5d55bdde5&ref=&curl=https%3A%2F%2Fblog.csdn.net%2Flly1122334%2Farticle%2Fdetails%2F102858447&utm=&spm=1001.2101&extra=%7B%22titAb%22%3A%22old2%22%7D&tos=4455&adb=0&cCookie=c_segment%3D10%3Bc_sid%3Dc1c807a17d10002c66d451d5d55bdde5%3Bc_first_page%3Dhttps%253A%2F%2Fblog.csdn.net%2Flly1122334%2Farticle%2Fdetails%2F102858447%3Bc_session_id%3D10_1673666420072.385659%3Bc_pref%3Ddefault%3Bc_ref%3Ddefault%3Bc_first_ref%3Ddefault%3Bc_dsid%3D11_1673666419013.322923%3Bc_page_id%3Ddefault%3B&t=1673666419&screen=1440*900&un=&urn=1673666419022-b1a26952-b769-494b-8cc1-be2e513c5bf1&vType=&log_id=39&sign=fa50e8750b41f1bec13084062282047e
:scheme: https
accept: */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
content-type: text/plain;charset=UTF-8
origin: https://blog.csdn.net
referer: https://blog.csdn.net/lly1122334/article/details/102858447
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-site
user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36""",
                                       ensure_ascii=False,)
    print(v)

    print([{1:3, 5: 5}])

