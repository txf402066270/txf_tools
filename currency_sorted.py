class DictSorted(object):
    """字典排序"""

    def __init__(self, *args, **kwargs):
        self.d = args[0]

    def bs_sort(self, order=0, desc=True):
        """
        根据dict的key倒序排列

        order   0代表key  1代表value
        desc    True正序  False倒序

        {1: 3, 5: 0, 0: 4} ==> [(5, 0), (1, 3), (0, 4)]
        """
        return sorted(self.d.items(), key=lambda x: x[order], reverse=desc)

    def sort_ret(self, order=0, desc=True):
        """
        {1: 3, 5: 0, 0: 4} ==> {5: 0, 1: 3, 0: 4}
        """
        return dict(self.bs_sort(order, desc))

    def bs_sort_split(self, order=0, desc=True, s=0, e=None):
        """
        dict切片返回 list
        s:e 取s开始e结束不包含e

        {1: 3, 5: 0, 0: 4}, e=1 ==> [(5, 0)]
        """
        nd = self.bs_sort(order, desc)
        if not e:
            return nd

        else:
            return nd[s: e]

    def sort_ret_split(self, order=0, desc=True, s=0, e=None):
        """
        dict切片返回 dict

        {1: 3, 5: 0, 0: 4}, e=2 ==> {5: 0, 1: 3}
        """
        return dict(self.bs_sort_split(order, desc, s, e))


class ListSorted(object):
    """列表里面嵌套字典排序"""

    def __init__(self, *args, **kwargs):
        self.lst = args[0]

    def sort_ret(self, order, desc=True):
        """
        列表嵌套 dict 根据dict的key进行排序 默认倒序

        order可指定单一的key 也可以指定多个key排序

        lst = [{'level': 19, 'star': 36, 'time': 1},
           {'level': 20, 'star': 40, 'time': 2},
           {'level': 20, 'star': 40, 'time': 3},
           {'level': 20, 'star': 40, 'time': 4},
           {'level': 20, 'star': 40, 'time': 5},
           {'level': 18, 'star': 40, 'time': 1}]
        order = ('level', 'time')
                     ||
                     \/
        [{'level': 20, 'star': 40, 'time': 5},
        {'level': 20, 'star': 40, 'time': 4},
        {'level': 20, 'star': 40, 'time': 3},
        {'level': 20, 'star': 40, 'time': 2},
        {'level': 19, 'star': 36, 'time': 1},
        {'level': 18, 'star': 40, 'time': 1}]

        """
        if isinstance(order, (list, tuple, set, dict)):
            for order_ in order:
                self.lst.sort(key=lambda k: (k.get(order_, 0)), reverse=desc)
            return self.lst
        else:
            self.lst.sort(key=lambda k: (k.get(order, 0)), reverse=desc)
        return self.lst

    def sort_ret_split(self, order, desc=True, s=0, e=None):
        """排序切片"""
        if not e:
            return self.sort_ret(order, desc)
        return self.sort_ret(order, desc)[s:e]


class ListOneSorted(object):
    """纯粹list排序"""
    def __init__(self, *args, **kwargs):
        self.lst = args[0]

    def sort_ret(self, desc=True):
        self.lst.sort(reverse=desc)
        return self.lst

    def sort_ret_split(self, desc=True, s=0, e=None):
        if not e:
            return self.sort_ret(desc)
        return self.sort_ret(desc)[s:e]


class SortGeneric(object):
    """
    根据SortGeneric参数的不同使用不同的类
    [{'level': 18, 'star': 40, 'time': 1}...] 使用 ListSorted
    {'level': 18, 'star': 40, 'time': 1}      使用 DictSorted
    [1, 2, 3, 4, 66, 77, 33, 4, 0]            使用 ListOneSorted
    """

    def __new__(cls, *args, **kwargs):

        if not args:
            raise ValueError("SortGeneric(此位置缺少要排序的dict或者list)")

        arg0 = args[0]
        if isinstance(arg0, dict):
            cls = DictSorted(*args, **kwargs)

        elif isinstance(arg0, list) and isinstance(args[0][0], dict):
            cls = ListSorted(*args, **kwargs)

        elif isinstance(arg0, list):
            cls = ListOneSorted(*args, **kwargs)

        return cls


def txf_sort(carrier, basis, desc=False):
    """
    carrier 载体 要排序的数据
    basis  依据 指定排序的字段
    desc   降序False 升序True
    详细用法见 if __name__ == '__main__' 案例

    carrier 要排序的 dict、list、list嵌套dict
    basis   要排序的字段
        如果carrier是list 就指定嵌套dict的key
            key可以为1个也可以为多个
            basis=('level', 'time')
            basis=‘level’
        如果carrier是dict 就指定0或者1表示按照key还是values排序

    """
    return SortGeneric(carrier).sort_ret(basis, desc=desc)


if __name__ == '__main__':

    # 案例
    lst = [{'level': 19, 'star': 36, 'time': 1},
           {'level': 20, 'star': 40, 'time': 2},
           {'level': 20, 'star': 40, 'time': 3},
           {'level': 20, 'star': 40, 'time': 4},
           {'level': 20, 'star': 40, 'time': 5},
           {'level': 18, 'star': 40, 'time': 1}]

    order = ('level', 'time')
    d = {1: 3, 5: 0, 0: 4}
    l = [1, 2, 3, 4, 66, 77, 33, 4, 0]
    print(SortGeneric(lst).sort_ret(order, desc=False))
    print(SortGeneric(d).sort_ret(1, desc=False))
    print(SortGeneric(l).sort_ret(desc=False))
    # print(txf_sort(lst, order))
