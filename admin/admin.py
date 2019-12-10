from flask_restful import Resource, Api, fields, reqparse, request
from admin import admin_bp
from datetime import datetime
import sys 
sys.path.append("..")
import model
from app import db
from common.BaseResponse import base_response
from common.TokenUtil import generate_token, certify_token, login_required


api = Api(admin_bp)

parser = reqparse.RequestParser()
parser.add_argument('user_name', type=str)
parser.add_argument('email', type=str)
parser.add_argument('pwd', type=str)
parser.add_argument('confirm_pwd', type=str)
parser.add_argument('phone', type=str)

class Register(Resource):
    def post(self):
        param = parser.parse_args()
        if not param.user_name:
            return base_response(code=-2)

        if not param.email:
            return base_response(code=-2)

        if not param.pwd:
            return base_response(code=-2)

        if not param.confirm_pwd:
            return base_response(code=-2)

        if not param.phone:
            return base_response(code=-2)
        
        if param.pwd != param.confirm_pwd:
            return base_response(code=-1, msg="两次密码输入不一致")

        user = model.User(user_name = param.user_name, email = param.email, phone = param.phone)
        # user.user_name = param.user_name
        # user.email = param.email
        user.hash_password(param.pwd)
        # user.phone = param.phone
        # user.create_time = datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        
        return base_response()

class Login(Resource):
    @login_required
    def get(self, email):
        return email
    
    # def do_something(email, isPass):
    #     return email

    # def post(self):
    #     param = parser.parse_args()
    #     if not param.email:
    #         return base_response(code=-2)

    #     if not param.pwd:
    #         return base_response(code=-2)

    #     user = model.User.query.filter_by(email=param.email).first()
    #     if not user:
    #         return base_response(code=-1,msg="未找到用户，请注册")
    #     if user.verify_password(param.pwd):
    #         token = generate_token(param.email)
    #         return base_response(data={"token":token})
    #     else:
    #         return base_response(code=-1,msg="密码错误")




api.add_resource(Register, '/register')
api.add_resource(Login, '/login/<string:email>')

