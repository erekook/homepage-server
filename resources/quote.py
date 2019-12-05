from flask_restful import Resource, Api
from resources import quote_bp

api = Api(quote_bp)

class Quotes(Resource):
    def get(self):
        return '爱上你我劫数难逃，为你坐爱情的牢，一辈子让情锁在我胸口绕。'


api.add_resource(Quotes, '/quotes')