import copy
import json

import redis

REDIS_TIME_OUTER = 3600 * 24 * 365  # 过期时间一年

# djangosettings的redis配置
# CACHES = {
#     "personnel_pool": {
#                 "BACKEND": "django_redis.cache.RedisCache",
#                 "LOCATION": "redis://127.0.0.1:6379/9",
#                 "OPTIONS": {
#                     "CLIENT_CLASS": "django_redis.client.DefaultClient",
#                     "CONNECTION_POOL_KWARGS": {"max_connections": 10000},
#                     "DECODE_RESPONSES": True,
#                     "PASSWORD": "",
#                 }
#             }
# }

class ExecutionRedis(object):
    def __init__(self, redis_name=None, redis_host="127.0.0.1", redis_port=6379, redis_db=9):
        if redis_name:
            from django_redis import get_redis_connection
            self.redis_conn = get_redis_connection(redis_name)
        else:
            self.redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True, db=redis_db)

    def save_str(self, data, key, outer_time=REDIS_TIME_OUTER):
        try:
            self.redis_conn.setex(key, outer_time, data)
            return True
        except Exception as e:
            print('写入redis错误: {}'.format(e))
            return False

    def read_str(self, key):
        read_ret = self.redis_conn.get(key)
        if read_ret:
            try:
                return read_ret.decode()
            except:
                pass
            return read_ret
        return None


def str_save(data, key, redis_name=None, redis_host="127.0.0.1", redis_port=6379, redis_db=9, outer_time=REDIS_TIME_OUTER):
    """字符串写入redis"""
    return ExecutionRedis(redis_name=redis_name,
                          redis_host=redis_host,
                          redis_port=redis_port,
                          redis_db=redis_db).save_str(data, key, outer_time=outer_time)


def str_read(key, redis_name=None, redis_host="127.0.0.1", redis_port=6379, redis_db=9):
    """读取redis的字符串"""
    return ExecutionRedis(redis_name=redis_name,
                          redis_host=redis_host,
                          redis_port=redis_port,
                          redis_db=redis_db).read_str(key)


def rw_redis(key, redis_name=None, redis_host="127.0.0.1",  redis_port=6379, redis_db=9, json_type=False, outer_time=REDIS_TIME_OUTER):
    """
    key        保存redis的key

    redis_name django_redis settings的CACHES配置的redis的名称 如果使用django settings的配置 后面的 redis_host redis_port redis_db不用管
    如果不用django settings cache的配置 请指定redis_host redis_port redis_db

    json_type 读取的数据是否需要json.loads  true表示需要 默认是不需要的
    outer_time 过期时间单位秒 默认是1年

    用法
       将{1:3}转 “{1:3}” 保存到redis的default库 默认保存1年
       在outer_time内都可以使用test_直接读取redis 不用走test方法生成
    @rw_redis('test_', redis_name='default', json_type=True)
    def test():
        return {1:3}
    """
    def outer(f):
        def inner(*args, **kwargs):
            try:
                redis_key = kwargs['redis_key']
            except:
                redis_key = key
                print('---------')
                print(redis_key)
            redis_data = str_read(redis_key, redis_name=redis_name, redis_host=redis_host, redis_port=redis_port, redis_db=redis_db)
            if redis_data:
                if json_type:
                    try:
                        redis_data = json.loads(redis_data)
                    except:
                        pass
                return redis_data

            data = f(*args, **kwargs)

            if data:
                ret_data = copy.deepcopy(data)
                if isinstance(data, (list, dict, tuple, set)):
                    data = json.dumps(data)
                redis_flg = str_save(data=data, key=redis_key, redis_name=redis_name, redis_host=redis_host,
                                     redis_port=redis_port, redis_db=redis_db, outer_time=outer_time)
                if not redis_flg:
                    raise ValueError('写入redis失败')
                return ret_data

            return None
        return inner
    return outer


if __name__ == '__main__':
    @rw_redis(key=None, redis_host="127.0.0.1",  redis_port=6379, redis_db=0, json_type=True, outer_time=60)
    def tt(a, b, *args, **kwargs):
        print('这里')
        return '{a: b}1'

    print(tt('a', 1, redis_key='test_redis_key11'))