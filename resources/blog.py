from flask_restful import Resource, Api, fields, reqparse
from resources import blog_bp
from datetime import datetime
import sys 
sys.path.append("..") 
import model
from app import db
from common.BaseResponse import base_response
from common.TokenUtil import generate_token, certify_token, login_required

api = Api(blog_bp)

# category_fields = {
#     'cate_name':   fields.String
# }
parser = reqparse.RequestParser()
parser.add_argument('title', type=str)
parser.add_argument('content', type=str)
parser.add_argument('email', type=str)
parser.add_argument('tag_names', action='append')
parser.add_argument('cate_id', type=int)

class CategoryList(Resource):
    def get(self):
        categorys = model.Category.query.all()
        if categorys:
            return base_response(data=[category.json_str() for category in categorys])
        return base_response(code=-1, msg="没有找到分类")

class BlogList(Resource):
    # 获取所有文章
    @login_required
    def get(self):
        blogs = model.Blog.query.all()
        if blogs:
            return base_response(data=[blog.json_str() for blog in blogs])
        return base_response(code=-1, msg="没有文章")

    # 新增一篇文章
    @login_required
    def post(self):
        param = parser.parse_args()
        token = request.headers['Authorization']
        login_token = model.LoginToken.query.filter_by(token=token).first()
        user = login_token.user
        if not user:
            return base_response(code=-1, msg="用户不存在")

        if not param.title:
            return base_response(code=-2)
            
        if not param.content:
            return base_response(code=-2)

        if not param.cate_id:
            return base_response(code=-2)
    
        blog = model.Blog(title=param.title, content=param.content, category_id=param.cate_id)
        blog.user = user

        all_tags = model.Tag.query.all()
        # 最终博客的tags
        tags = []
        
        if len(param.tag_names) != 0:
            # 循环参数的tag名
            for tag_name in param.tag_names:
                # 判断是否有该tag
            for index in all_tags:
                    if tag_name == all_tags[index].tag_name:
                        tags.append(all_tags[index])
                    else:
                        new_tag = model.Tag(tag_name=tag_name)
                        tags.append(new_tag)

            blog.tags = tags
            
        db.session.add(blog)
        db.session.commit()
        return base_response()

class BlogById(Resource):
    # 根据id查找文章
    @login_required
    def get(self, blog_id):
        blog = model.Blog.query.filter_by(id=blog_id).first()
        return base_response(data=blog.json_str())

class BlogByTitle(Resource):
    # 根据title查找文章
    @login_required
    def get(self, title):
        blog = model.Blog.query.filter_by(title=title).first()
        if blog:
            return base_response(data=blog.json_str())
        return base_response(msg="没有找到文章")

api.add_resource(BlogList, '/blogs')
api.add_resource(BlogById, '/<int:blog_id>')
api.add_resource(BlogByTitle, '/findByTitle/<string:title>')
api.add_resource(CategoryList, '/categorys')
