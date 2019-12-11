from flask_restful import Resource, Api
from resources import quote_bp
import random
import sys 
sys.path.append("..") 
import model
from app import db
from common.BaseResponse import base_response


api = Api(quote_bp)

class Quotes(Resource):
    def get(self):
        quotes = model.Quote.query.all()
        if quotes:
            return base_response(data=quotes[random.randint(0,len(quotes)-1)].json_str())
        return base_response(code=-1, msg="没有查询到结果")

api.add_resource(Quotes, '/rand')