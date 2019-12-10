from flask_restful import Resource, Api, fields, reqparse
from resources import blog_bp
from datetime import datetime
import sys 
sys.path.append("..") 
from model import Blog
from app import db
from common.BaseResponse import base_response

api = Api(blog_bp)

# category_fields = {
#     'cate_name':   fields.String
# }
parser = reqparse.RequestParser()
parser.add_argument('title', type=str)
parser.add_argument('content', type=str)
parser.add_argument('create_time', type=str)
parser.add_argument('user_id', type=int)
parser.add_argument('category_id', type=int)


class BlogList(Resource):
    # 获取所有文章
    def get(self):
        blogs = Blog.query.all()
        if blogs:
            return base_response(data=[blog.json_str() for blog in blogs])
        return base_response(code=-1, msg="没有文章")

    # 新增一篇文章
    def post(self):
        param = parser.parse_args()
        blog = Blog(title=param.title, content=param.content, create_time=datetime.strptime(param.create_time, '%Y-%m-%d'), user_id= param.user_id, category_id=param.category_id)
        db.session.add(blog)
        db.session.commit()
        return base_response()

class BlogById(Resource):
    # 根据id查找文章
    def get(self, blog_id):
        blog = Blog.query.filter_by(id=blog_id).first()
        return base_response(data=blog.json_str())

class BlogByTitle(Resource):
    # 根据title查找文章
    def get(self, title):
        blog = Blog.query.filter_by(title=title).first()
        if blog:
            return base_response(data=blog.json_str())
        return base_response(msg="没有找到文章")

api.add_resource(BlogList, '/blogs')
api.add_resource(BlogById, '/<int:blog_id>')
api.add_resource(BlogByTitle, '/findByTitle/<string:title>')