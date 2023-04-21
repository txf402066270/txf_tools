# from sqlalchemy import create_engine
# from elasticsearch import Elasticsearch
# # from pandasticsearch import DataFrame
# from sshtunnel import SSHTunnelForwarder
# import pymysql
# import pandas as pd
#
# class MyObject:
#     def __init__(self):
#         self.server = SSHTunnelForwarder(
#             ssh_address_or_host=('47.92.53.120', 22),  # 指定ssh登录的跳转机的address
#             ssh_username='root',  # 跳转机的用户
#             ssh_pkey=r"C:\Users\Admin\.ssh/id_rsa",
#             # 单 -远程服务器地址+端口
#             # remote_bind_address=('AAA.AAA.AAA.AAA', 3306),
#             # 多 -远程服务器地址+端口
#             remote_bind_address=[
#                                 # mysql
#                                 ('rm-8vbu8s3o3289q6yh5.mysql.zhangbei.rds.aliyuncs.com', 3306),
#                                 # es
#                                 ('rm-8vbu8s3o3289q6yh5.mysql.zhangbei.rds.aliyuncs.com', 9200)
#                                  ]
#         )
#
#         self.server.start()
#
#         # self.engine = create_engine('mysql+pymysql://username:password@127.0.0.1:%s/dbname' % self.server.local_bind_ports[0])
#
#         # 使用elasticsearch
#         self.es = Elasticsearch(
#             ['172.26.119.248'],  # 连接集群，以列表的形式存放各节点的IP地址
#             # sniff_on_start=True,    # 连接前测试
#             sniff_on_connection_fail=True,  # 节点无响应时刷新节点
#             sniff_timeout=100, # 设置超时时间
#             # http_auth=('es', 'password'), # ES用户名密码
#             port=str(self.server.local_bind_ports[1])  # 端口号
#         )
#
#         self.conn = pymysql.connect(host="127.0.0.1",
#                                     user="username",
#                                     password="password",
#                                     db="dbname",
#                                     port=self.server.local_bind_ports[0],
#                                     charset='utf8',
#                                     )
#         self.cursor = self.conn.cursor()
#
#     # 使用pandasticsearh
#     # def getDataFromES(self, index_name):
#     #     dataFrameFromES = DataFrame.from_es(url='http://127.0.0.1:%s' % self.server.local_bind_ports[1],
#     #                                         doc_type=index_name,
#     #                                         compat=5,
#     #                                         # username="es",
#     #                                         # password="password"
#     #                                         )
#     #
#     #     return dataFrameFromES.limit(20000).to_pandas()
#
#
# if __name__ == '__main__':
#     instance = MyObject()
#     sql = """SELECT
#                 COL.COLUMN_NAME
#             FROM INFORMATION_SCHEMA.COLUMNS COL
#             Where  COL.TABLE_NAME='company_patent'; """
#     cur = instance.cursor
#     cur.execute(sql)
#     data = cur.fetchall()
#     # instance.getDataFromES("index_name")
#     # # 使用完将服务关闭
#     # instance.server.close()
#     print(data)


import pymysql
from elasticsearch import Elasticsearch

from sshtunnel import SSHTunnelForwarder
# from utils.logging_ import logger

# ssh的远程服务器的配置
ssh_ip = '47.92.53.120'
ssh_port = 22

# mysql的远程服务器的配置
host = 'rm-8vbu8s3o3289q6yh5.mysql.zhangbei.rds.aliyuncs.com'
user = 'tyc_init1'
passwd = '%vd3ukF7n60iVf78'
db_name = 'gs_db'
port = 3306

# es的远程服务器的配置
es_host = "172.26.119.248"
es_port = 9200
index_name = 'company_info888'


class SSHLikeMysql(object):

    def __init__(self, condition='dev'):
        self.condition = condition

    def sql_server(self):
        """ssh跳板"""
        server = SSHTunnelForwarder(
            ssh_address_or_host=(ssh_ip, ssh_port),  # 指定ssh登录的跳转机的address
            ssh_username='root',  # 跳转机的用户
            ssh_pkey="D:/share/id_rsa",
            # 单 -远程服务器地址+端口
            # remote_bind_address=(host, 3306),
            # 多 -远程服务器地址+端口
            remote_bind_addresses=[
                (host, port),  # sql
                (es_host, es_port)   # es

            ]
        )
        return server

    def sql_db(self):
        """sql对象，链接对象和创建游标使用"""
        server = self.sql_server()
        server.start()
        db = pymysql.connect(
            host='127.0.0.1',
            # 单 -远程服务器端口
            # port=server.local_bind_port,
            # 多 -远程服务器端口
            port=server.local_bind_ports[0],
            user=user,
            passwd=passwd,
            db=db_name,
            charset='utf8',
        )
        return db

    def execute_es(self):
        """es 操作"""
        server = self.sql_server()
        server.start()

        es = Elasticsearch(
            ['127.0.0.1:9200'],  # 连接集群，以列表的形式存放各节点的IP地址
            # sniff_on_start=True,    # 连接前测试
            sniff_on_connection_fail=True,  # 节点无响应时刷新节点
            sniff_timeout=100,  # 设置超时时间
            # http_auth=('es', 'password'),  # ES用户名密码
            port=server.local_bind_ports[1]  # 端口号
        )

        data = es.search(index='ik_person_file', doc_type='doc', body={"query": {"match_all": {}}})
        # return self.es_obj().search(index=index_name, body=body)


    def execut_sql(self, sql):

        """执行查询 查询的结果 data为元祖
            ((1, 3402285986, 'bj', '北京真维嘉真空设备有限公司', 'Beijing Zhenweijia Vacuum Equipment Co.,Ltd.', '真维嘉'））
        """
        server = self.sql_server()
        data = None
        db = self.sql_db()
        cur = db.cursor()
        try:
            cur.execute(sql)
            data = cur.fetchall()
            db.commit()
        except Exception as e:
            print('执行sql语句问题')
            # logger.info("：%s " % e)
        cur.close()
        db.close()
        if server:
            server.close()
        print(data)
        print(type(data))
        return data

sql = """SELECT
            COL.COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS COL
        Where  COL.TABLE_NAME='company_patent'; """

if __name__ == '__main__':

    # SSHLikeMysql().execut_sql(sql=sql)
    SSHLikeMysql().execute_es()