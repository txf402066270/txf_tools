# import os
# from collections import namedtuple
#
#
# class LazyProperty(object):
#     def __init__(self, func):
#         # 初始化func为serverHost函数
#         self.func = func
#
#     def __get__(self, instance, owner):
#         if instance is None:
#             return self
#         else:
#             value = self.func(instance)
#             # 会将结果值通过setattr方法存入到instance实例的__dict__中
#             setattr(instance, self.func.__name__, value)
#             return value
#
#
# class ConfigHandler:
#     def __init__(self):
#         pass
#     # 返回一个LazyProperty实例
#     @LazyProperty
#     def serverHost(self):
#         return os.environ.get("HOST", setting.HOST)
#
# setting = namedtuple("setting", ["HOST"])
# setting.HOST = "g"
#
# # 测试一
# a = ConfigHandler()
# # print(a.__dict__)
# # 1. 注解先是创建了LazyProperty(serverHost)的实例
# # 2. 再是语法糖进行了赋值serverHost = LazyProperty(serverHost)
# # 3. 当第一次进行调用的时候, instance = configHandler**实例**,
# # self.func(instance实例) == 调用serverHost(instance实例)从而获得了真正值value。
# # 而之后的 setattr处将self实例的__dict__中添加了serverHost-value，
# # 再次访问self.serverHost时, 已经不再是函数,
# # 而是value值(serverHost不再从ConfigHandler.__dict__中取, 而是实例a.__dict__中取)
# # print(a.serverHost)
# # print("say")
# # print(a.__dict__)
# #
# # # 测试二
# # # 如果先执行类的__dict__能看到类的serverHost是一个**描述器对象实例**=> 'serverHost': <__main__.LazyProperty object at 0x0000020A1AEB7FD0>
# print(ConfigHandler.__dict__)
# # 通过__dir__能见到serverHost为实例的一个方法
# print(a.__dir__())
# # 此时a.__dict__为空
# print(a.serverHost)
# # 等到调用过a.serverHost后可以发现a.__dict__中多了serverHost
# print(a.__dict__)
# # 由于实例__dict__会优先于类的__dict__使用，所以直接返回了value值
import os
from collections import namedtuple


# class A(object):
#     def __init__(self, func, *args, **kwargs):
#         print('self.func')
#         print(func)
#         self.func = func
#         self.args = args
#         self.kwargs = kwargs
#
#     def __get__(self, instance, owner):
#         print('instance')
#         print(instance)
#         if not instance:
#             return self
#         return self.func(instance, *self.args, **self.kwargs)
#
# class B(object):
#     @A
#     def serverHost(self, a, b):
#         print(a, b)
#         return 'os.environ.get("HOST", setting.HOST)'
#
# bb = B(1, 2)
# print(bb.__dict__)
# # print(bb.__class__.__name__)
# print(bb.serverHost(bb))
#
#

class A(object):

    def __get__(self, instance, owner):
        """
        首先明确一点，拥有这个方法的类，必须产生一个实例，
        并且这个实例是另外一个类的类属性(注意一定是类属性，通过self的方式产生就不属于__get__范畴了)。
        instance 被代理类的实例实例  如果是类调用就是None
        owner    被代理类
        """
        print(instance)
        print(owner)
        return '属性被赋值的结果'

    def __set__(self, instance, value):
        """
        self 表示描述符类的实例对象，
        instance 表示被代理类的实例对象，
        value 表示属性的值
        """
        print('__set__')
        print(instance, value)
        print('_end_ set _end_')


class B(object):
    c = A()


# print(B.c)
# None
# <class '__main__.B'>
# 属性被赋值的结果
# print('==========')
# print(B().c)
# <__main__.B object at 0x000001B1113EAFA0>
# <class '__main__.B'>
# 属性被赋值的结果

# B().c = '修改'
# print(B().c)
if __name__ == '__main__':
    class A(object):
        name = 2

        def __init__(self):
            self.name1 = 1

        def abdd(self):
            return 'av'

        def __del__(self, instance):
            print('删除调用这里')
            print(instance)
            return instance



    # print(hasattr(A(), 'name1'))
    # print(hasattr(A, 'name'))
    # print(hasattr(A(), 'abdd'))
    # print(hasattr(A(), '324423'))
    # True
    # True
    # False
    def setattr_f():
        return '111'
    a = A()
    # print(getattr(a, 'abdd')())
    # print(getattr(a, 'nameeee', 'a'))
    setattr(a, 'year', 2022)  # 无法给
    setattr(a, 'setattr_f', setattr_f)
    print(a.setattr_f())
    del a.name1
# setattr
# setattr
# setattr
# init
# {'name': 2, 'nam1e': 2, 'name1': 2}
# print(A()())
#     init
# call
# return: call



