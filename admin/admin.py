from flask_restful import Resource, Api, fields, reqparse, request
from admin import admin_bp
from datetime import datetime
import random
import sys 
sys.path.append("..")
import model
from app import db
from common.BaseResponse import base_response
from common.TokenUtil import generate_token, certify_token, login_required
from common.EmailUtil import EmailUtil


api = Api(admin_bp)

parser = reqparse.RequestParser()
parser.add_argument('user_name', type=str)
parser.add_argument('email', type=str)
parser.add_argument('code', type=str)
parser.add_argument('pwd', type=str)
parser.add_argument('confirm_pwd', type=str)
parser.add_argument('phone', type=str)

class SendEmailCode(Resource):
    # 发邮箱验证码
    def get(self, email):
        if not email:
            return base_response(code=-2)
        user = model.User.query.filter_by(email=email).first()
        if user:
            return base_response(code=-1,msg="邮箱地址已经被注册了")
        # genarate 6 random code
        rand_code = "".join([str(random.randint(0,9)) for n in range(6)])
        
        print('i am here')
        # send email code...
        sender = EmailUtil(email)
        print('after init ')
        sender.send_email_code(rand_code)
        # save code to db
        emailCode = model.EmailCode.query.filter_by(email=email).first()
        if emailCode:
            emailCode.code = rand_code
        else:
            emailCode = model.EmailCode(code=rand_code, email=email)
            db.session.add(emailCode)

        db.session.commit()
        return base_response()


class Register(Resource):
    # 注册
    def post(self):
        param = parser.parse_args()
        # if not param.user_name:
        #     return base_response(code=-2)

        if not param.email:
            return base_response(code=-2)

        if not param.code:
            return base_response(code=-2)

        if not param.pwd:
            return base_response(code=-2)

        if not param.confirm_pwd:
            return base_response(code=-2)

        # if not param.phone:
        #     return base_response(code=-2)
        
        if param.pwd != param.confirm_pwd:
            return base_response(code=-1, msg="两次密码输入不一致")

        right_code = model.EmailCode.query.filter_by(email=param.email).first()
        if not right_code:
            return base_response(code=-1,msg="请重新发送验证码")
        # valid the email code is right
        if right_code.code != param.code:
            return base_response(code=-1,msg="验证码错误")
        else:
            user = model.User(email = param.email)
            user.hash_password(param.pwd)
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)

            ## 返回token
            token = generate_token(param.email)
            return base_response(data={ "token":token, "user": user.json_str() })

class Login(Resource):
    # @login_required
    # def get(self, email):
    #     return email
    
    # def do_something(email, isPass):
    #     return email

    def post(self):
        param = parser.parse_args()
        if not param.email:
            return base_response(code=-2)

        if not param.pwd:
            return base_response(code=-2)

        user = model.User.query.filter_by(email=param.email).first()
        if not user:
            return base_response(code=-1,msg="未找到用户，请注册")
        if user.verify_password(param.pwd):
            token = generate_token(param.email)
            return base_response(data={ "token": token, "user": user.json_str() })
        else:
            return base_response(code=-1,msg="密码错误")




api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(SendEmailCode, '/send-email-code/<string:email>')
