from flask_restful import Resource, Api, fields, marshal_with_field, marshal_with
from resources import blog_bp
import sys 
sys.path.append("..") 
from model import *
from app import db

api = Api(blog_bp)

category_fields = {
    'cate_name':   fields.String
}

class Blogs(Resource):
    @marshal_with(category_fields)
    def get(self):
        blogs = Category.query.all()
        print(blogs[0].cate_name)
        if blogs:
            return [blog for blog in blogs], 200
        return { 'message': 'blogs not found' }, 404


api.add_resource(Blogs, '/blogs')