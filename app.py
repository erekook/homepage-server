from flask import Flask
from flask_restful import Api, Resource
from flask_cors import *
from flask_sqlalchemy import SQLAlchemy
import logging


app = Flask(__name__)
CORS(app, resources=r'/*')
app.config.from_pyfile('config.ini')
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
# 配置数据库的连接
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:960122@127.0.0.1:3306/db_home_project"
# 连接池大小
app.config["SQLALCHEMY_POOL_SIZE"] = 100
app.config["SQLALCHEMY_MAX_OVERFLOW"] = 100
# 连接超时时间
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 15
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 配置数据库内容在更新时自动提交
# app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
# 配置session所需要的秘钥
# app.config["SECRET_KEY"] = "960122"
# 数据库的初始化
db = SQLAlchemy(app)

from resources import quote_bp, blog_bp
from admin import admin_bp
app.register_blueprint(quote_bp)
app.register_blueprint(blog_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    #gunicorn_logger = logging.getLogger('gunicorn.error')
    #app.logger.handlers = gunicorn_logger.handlers
    #app.logger.setLevel(gunicorn_logger.level)
    app.run(host='0.0.0.0', port=5051)
