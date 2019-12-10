
# 自定义返回类型
def base_response(code=0, data=None, msg=""):
    if code == -1:
        data = None
        msg = "操作失败" if msg == "" else msg
    if code == -2:
        data = None
        msg = "参数错误"
    return {
        "code": code,
        "data": data,
        "msg": msg
    }