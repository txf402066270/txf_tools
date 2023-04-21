# pip install pycryptodomex
# pip install rsa
from Cryptodome.Cipher import AES, DES3
import base64
import os
import rsa  # 4.9


class AESDecodeEncode(object):
    """aes 加密"""
    key = '0CoJUm6Qyw8W8jud'
    vi = '0102030405060708'

    @classmethod
    def set_aes(cls, key=None, data=None, vi=None):
        key = key or cls.key
        vi = vi or cls.vi
        pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        data = pad(data)
        cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
        encrypted_bytes = cipher.encrypt(data.encode('utf8'))
        bs64_strs = base64.b64encode(encrypted_bytes)  # type byte
        ret = bs64_strs.decode('utf8')
        return ret

    @classmethod
    def get_aes(cls, key, data, vi):
        key = key or cls.key
        vi = vi or cls.vi
        data = data.encode('utf8')
        encode_bytes = base64.decodebytes(data)
        cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
        text_decrypted = cipher.decrypt(encode_bytes)
        unpad = lambda s: s[0:-s[-1]]
        text_decrypted = unpad(text_decrypted)
        text_decrypted = text_decrypted.decode('utf8')
        return text_decrypted

    def execute_demo(self):
        # aesde = AESDecodeEncode
        # key = '0CoJUm6Qyw8W8jud'  # 自己密钥
        # data = 'sdadsdsdsfd'  # 需要加密的内容
        # vi = '0102030405060708'
        # enctext = aesde.set_aes(key, data)
        # print(enctext)
        # text_decrypted = get_aes(key, enctext)
        # print(text_decrypted)
        pass


class DES3ECBDecodeEncode(object):
    # 加密模式为 ECB
    def __init__(self, key, encode_text=None, decode_text=None, is_bs64=False):
        """
        :param key:          b'4J6r0E4406Uo3eo0D182wH5G'
        :param encode_text:  Python rocks!
        :param decode_text:  b'@\xa9\n\xfaa\xcc\xd5\x8f\xf8V}5H\x08zC'
        """
        self.key = key
        self.encode_text = encode_text
        self.is_bs64 = is_bs64
        self.decode_text = decode_text
        self.des = DES3.new(self.key, DES3.MODE_ECB)  # 创建一个DES实例

    def pad(self):
        text = self.encode_text
        while len(text) % 8 != 0:
            text += ' '
        return text

    def encode_des3_data(self):
        pad_text = self.pad()

        encode_text = self.des.encrypt(pad_text.encode('utf-8'))  # 加密
        if self.is_bs64:
            encode_text = base64.b64encode(encode_text)
        return encode_text

    def decode_des3_data(self):
        decode_text = self.decode_text
        if self.is_bs64:
            decode_text = base64.b64decode(decode_text)
        return self.des.decrypt(decode_text).decode().rstrip(' ')  # 解密

    def execute_demo(self):
        """
        key = b'4J6r0E4406Uo3eo0D182wH5G'
        text = 'Python rocks!'
        v = DES3DecodeEncode(key=key, encode_text=text, decode_text=b'@\xa9\n\xfaa\xcc\xd5\x8f\xf8V}5H\x08zC', is_bs64=False)
        ed = v.encode_des3_data()
        print(ed)
        dd = v.decode_des3_data()
        print(dd)
        """
        pass


class RSADecodeEncode(object):
    """目前只支持 自己生成的
    BEGIN RSA PRIVATE KEY 格式
    """

    def __init__(self, pubkey_path=None, pri_path=None):
        self.pub_path = pubkey_path or str(os.getcwd()) + '/pub_key.txt'
        self.pri_path = pri_path or str(os.getcwd()) + '/pri_key.txt'

    def set_pubkey_privkey(self, nbits=1024):
        pubkey, privkey = rsa.newkeys(nbits)
        return pubkey, privkey

    def save_keys(self, pubkey, privkey):
        """
        public_key_bytes
                -----BEGIN RSA PUBLIC KEY-----
                MIIBCgKCAQEAh151YMf/6i.........
                -----END RSA PUBLIC KEY-----

        private_key_bytes
                -----BEGIN RSA PRIVATE KEY-----
                MIIEqAIBAAKCAQEAhl4lYMf/6iW6wXHa8BJs5DPPX20azt3hCzZvI85/G/aoNhbY
                1AApA..............
                -----END RSA PRIVATE KEY-----
                """
        public_key_bytes, private_key_bytes = pubkey.save_pkcs1(), privkey.save_pkcs1()
        with open(self.pub_path, 'wb') as f:
            f.write(public_key_bytes)

        with open(self.pri_path, 'wb') as f:
            f.write(private_key_bytes)
        return pubkey, privkey

    def handle_pub_key(self, key):
        """
        处理公钥
        公钥格式pem，处理成以-----BEGIN PUBLIC KEY-----开头，-----END PUBLIC KEY-----结尾的格式
        :param key:pem格式的公钥，无-----BEGIN PUBLIC KEY-----开头，-----END PUBLIC KEY-----结尾
        :return:
        """
        start = '-----BEGIN PUBLIC KEY-----\n'
        end = '-----END PUBLIC KEY-----'
        result = ''
        # 分割key，每64位长度换一行
        divide = int(len(key) / 64)
        divide = divide if (divide > 0) else divide + 1
        line = divide if (len(key) % 64 == 0) else divide + 1
        for i in range(line):
            result += key[i * 64:(i + 1) * 64] + '\n'
        result = start + result + end
        return result

    def handle_pri_key(self, pri_key):
        return self.handle_pub_key(pri_key)

    def format_pub_key(self, pubkey_path=None, pub_key=None):
        if not pub_key:
            with open(pubkey_path or self.pub_path, 'rb') as f:
                pub_data = f.read()
                pub_key = rsa.PublicKey.load_pkcs1(pub_data)
        else:
            pub_key = self.handle_pub_key(pub_key)
            pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)
        return pub_key

    def format_pri_key(self, pri_path=None, pri_key=None):
        if not pri_key:
            with open(pri_path or self.pri_path, 'rb') as f:
                pri_data = f.read()
                pri_key = rsa.PrivateKey.load_pkcs1(pri_data)
        else:
            pri_key = self.handle_pri_key(pri_key)
            pri_key = rsa.PublicKey.load_pkcs1_openssl_pem(pri_key)
        return pri_key

    def set_ras(self, message, pubkey_path=None, pub_key=None):
        pub_key = self.format_pub_key(pubkey_path, pub_key=pub_key)

        crypto = b''
        divide = int(len(message) / 117)
        divide = divide if (divide > 0) else divide + 1
        line = divide if (len(message) % 117 == 0) else divide + 1

        get_len = ''
        for i in range(line):
            v = rsa.encrypt(message[i * 117:(i + 1) * 117].encode(), pub_key)
            crypto += v
            if not get_len:
                get_len = len(v)
        crypto1 = base64.b64encode(crypto)
        return crypto1.decode('utf-8'), get_len

    def decode_message_type(self, message):
        if isinstance(message, str):
            return base64.b64decode(message)
        elif isinstance(message, bytes):
            return message
        else:
            raise ValueError('你的类型我无法确定')

    def get_ras(self, message, pri_path=None, pri_key=None, get_len=None):
        if not get_len:
            get_len = 128
        message = self.decode_message_type(message)
        pri_key = self.format_pri_key(pri_path, pri_key)
        crypto = b''
        divide = int(len(message) / get_len)
        divide = divide if (divide > 0) else divide + 1
        line = divide if (len(message) % get_len == 0) else divide + 1
        for i in range(line):
            decode_text = message[i * get_len:(i + 1) * get_len]
            crypto += rsa.decrypt(decode_text, pri_key)

        return crypto.decode()


def set_des3_ecd(key, encode_text, is_bs64=True):
    """
    返回的数据 如果是bs64的 is_bs64=True 反之
    """
    v = DES3ECBDecodeEncode(key=key, encode_text=encode_text, is_bs64=is_bs64)
    ed = v.encode_des3_data()
    return ed


def get_des3_ecd(key, decode_text, is_bs64=True):
    """
    decode_text  如果是bs64的 is_bs64=True 反之
    """
    v = DES3ECBDecodeEncode(key=key, decode_text=decode_text, is_bs64=is_bs64)
    dd = v.decode_des3_data()
    return dd


def set_aes(key, source_str, vi):
    """
    # 密钥（key）, 密斯偏移量（iv）
    source_str  str 此参数是生成 aes的参数，此参数如果有值就直接加密
    """
    return AESDecodeEncode().set_ret(key, source_str, vi)


def get_aes(key, source_str, vi):
    # 密钥（key）, 密斯偏移量（iv）
    return AESDecodeEncode().get_aes(key, source_str, vi)


def rsa_save_pub_pri_key(nbits=1024, pubkey_path=None, pri_path=None):
    r = RSADecodeEncode(pubkey_path, pri_path)
    pubkey, privkey = r.set_pubkey_privkey(nbits=nbits)
    RSADecodeEncode().save_keys(pubkey, privkey)


def set_rsa(message, pubkey_path, len_=False):
    r = RSADecodeEncode()
    ret, get_len = r.set_ras(message, pubkey_path)
    if len_:
        return ret, get_len
    return ret


def get_rsa(message, pri_path, get_len=None):
    r = RSADecodeEncode()
    ret = r.get_ras(message, pri_path, get_len)
    return ret