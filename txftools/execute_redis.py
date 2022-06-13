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
            self.redis_conn = get_redis_connection('personnel_pool')
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
            decode_data = read_ret.decode()
            return decode_data
        return None


def str_save(data, key, outer_time=REDIS_TIME_OUTER):
    """字符串写入redis"""
    ExecutionRedis().save_str(data, key, outer_time=outer_time)


def str_read(key):
    """读取redis的字符串"""
    return ExecutionRedis().read_str(key)


if __name__ == '__main__':
    ExecutionRedis().save_str('rrr', 'key_')