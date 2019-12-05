from flask import Flask
from flask_restful import Api, Resource
from flask_cors import *
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
CORS(app, resources=r'/*')
app.config.from_pyfile('config.ini')

# 配置数据库的连接
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:960122@175.24.109.208:3306/db_home_project"
# 配置数据库内容在更新时自动提交
# app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
# 配置session所需要的秘钥
# app.config["SECRET_KEY"] = "960122"
# 数据库的初始化
db = SQLAlchemy(app)

from resources import quote_bp, blog_bp
app.register_blueprint(quote_bp)
app.register_blueprint(blog_bp)

if __name__ == '__main__':
    app.run(debug=True)