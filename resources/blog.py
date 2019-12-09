from flask_restful import Resource, Api, fields, marshal_with_field, marshal_with
from resources import blog_bp
import sys 
sys.path.append("..") 
from model import *
from app import db

api = Api(blog_bp)

# category_fields = {
#     'cate_name':   fields.String
# }

class Blogs(Resource):
    # @marshal_with(category_fields)
    def get(self):
        blogs = Blog.query.all()
        if blogs:
            return [blog.json_str() for blog in blogs]
        return { 'message': 'blogs not found' }, 404


api.add_resource(Blogs, '/blogs')