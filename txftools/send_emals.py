# smtplib 用于邮件的发信动作
import smtplib
# email 用于构建邮件内容
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# 构建邮件头
from email.header import Header


class SendEmail(object):

    def __init__(self):

        """
        发信方的信息：发信邮箱
        from_addr = '123@qq.com'

        POP3/SMTP服务 开启这个功能给的那串码
        password = 'wdfffddstbzdssxcb'

        发信服务器 qq的默认不用改其他的需要手动修改
        smtp_server = 'smtp.qq.com'
        smtp_port=465

        """
        self.from_addr = '402066270@qq.com'
        self.password = 'wolstbzmmckebicb'
        self.smtp_server = 'smtp.qq.com'
        self.smtp_port = 465
        self.data_encoding = 'utf-8'

    def send_email(self, data=None,
                   data_type='plain',
                   data_header=None,
                   from_header=None,
                   to_addr=None,
                   to_header=None,
                   enclosure_file_list=None,
                   enclosure_file_dict_bytes=None
                   ):
        """
        data: 要发送的数据
        收信方邮箱 单个用户可以为str 多用户使用list
        to_addr = ['yckj1987@126.com']
        data_type:  plain纯文本    html html数据类型
        data_header: 邮件标题
        from_header: 发件人
        to_header: 收件人 一般不用设置
        enclosure_file_list: 附件文件列表 [file1, file2, file3, ...]
        enclosure_file_dict_bytes: 附件 {文件名1: 文件二进制1, 文件名2: 文件二进制2, ...}
        """

        # 创建一个带附件的实例msg
        msg = MIMEMultipart()
        # 邮件头信息
        if not from_header:
            from_header = self.from_addr

        # 发送者
        msg['From'] = Header(from_header)
        msg['To'] = Header(to_header)  # 接收者
        msg['Subject'] = Header(data_header, 'utf-8')  # 邮件主题

        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        msg.attach(MIMEText(data, data_type, self.data_encoding))

        # 邮件附件 文件名
        if enclosure_file_list:
            for file_ in enclosure_file_list:
                # 构造附件
                att = MIMEText(open(file_, 'rb').read(), 'base64', 'utf-8')
                att["Content-Type"] = 'application/octet-stream'
                file_name = file_.split('/')[-1]
                if not file_name:
                    file_name = file_.split(r'\\')[-1]
                att.add_header('Content-Disposition', 'attachment', filename=file_name)
                msg.attach(att)

        # 邮件附件  二进制
        if enclosure_file_dict_bytes:
            for file_name, file_bytes in enclosure_file_dict_bytes.items():
                # 构造附件
                att = MIMEText(file_bytes, 'base64', 'utf-8')
                att["Content-Type"] = 'application/octet-stream'
                att.add_header('Content-Disposition', 'attachment', filename=file_name)
                msg.attach(att)

        try:
            smtpobj = smtplib.SMTP_SSL(self.smtp_server)
            # 建立连接--qq邮箱服务和端口号（可百度查询）
            smtpobj.connect(self.smtp_server, self.smtp_port)
            # 登录--发送者账号和口令
            smtpobj.login(self.from_addr, self.password)
            # 发送邮件
            smtpobj.sendmail(self.from_addr, to_addr, msg.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("无法发送邮件")
        finally:
            # 关闭服务器
            try:
                smtpobj.quit()
            except:
                pass


class SendEmailQQ(SendEmail):

    def __init__(self, from_addr, password):
        super().__init__()
        self.from_addr = from_addr
        self.password = password


def send_email_qq(
        from_addr='402066270@qq.com',
        password='就不告诉你',
        data='测试数据123',
        to_addr=['用户的邮箱'],
        enclosure_file_list=['tests.py'],
        enclosure_file_dict_bytes=None,
        data_header='融道知变-删除数据'):
    """
        data 邮件文本内容
        to_addr=用户邮箱列表
        enclosure_file_list=附件列表
    """

    s = SendEmailQQ(from_addr, password)
    return s.send_email(data=data,
                        to_addr=to_addr,
                        data_header=data_header,
                        enclosure_file_list=enclosure_file_list,
                        enclosure_file_dict_bytes=enclosure_file_dict_bytes
                        )


if __name__ == '__main__':

    with open('tests.py', 'rb') as f:
        enclosure_file_dict_bytes = f.read()

    send_email_qq(
        from_addr='402066270@qq.com',
        password='lxupocvfhxxnbihb',
        data='测试数据123',
        to_addr=['yckj1987@126.com'],
        # enclosure_file_list=['tests.py'],
        enclosure_file_dict_bytes={'test.py': enclosure_file_dict_bytes},
        data_header='融道知变-删除数据')