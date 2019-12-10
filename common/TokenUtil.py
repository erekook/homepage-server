import time
import base64
import hmac
from functools import wraps
from flask import request
from common.BaseResponse import base_response

#生成token 入参：用户email
def generate_token(key, expire=3600):
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr  = hmac.new(key.encode("utf-8"),ts_byte,'sha1').hexdigest() 
    token = ts_str+':'+sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")

#验证token 入参：用户email 和 token
def certify_token(key, token):
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return False
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        # token expired
        return False
    known_sha1_tsstr = token_list[1]
    sha1 = hmac.new(key.encode("utf-8"),ts_str.encode('utf-8'),'sha1')
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != known_sha1_tsstr:
        # token certification failed
        return False 
    # token certification success
    return True


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **wkargs):
        token = request.headers['Authorization']
        email = f(*args, **wkargs)
        is_pass = certify_token(email, token)
        if not is_pass:
            return base_response(code=-1,msg="未登陆")
        return f(*args, **wkargs)
    return decorated_function