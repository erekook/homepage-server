from app import db
from datetime import datetime

# 博客分类
class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    cate_name = db.Column(db.String(50), nullable=False)

    # 反向引用 blog表 每个category对象都有一个blog属性
    blogs = db.relationship("Blog", backref="blog_category", lazy="dynamic")

    def __repr__(self):
        return '<Category %r>' % self.cate_name

    def json_str(self):
        return {
            "cate_name": self.cate_name
        }


# 用户信息
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    pwd = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    motto = db.Column(db.String(500), nullable=True)
    is_locked = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, nullable=False)

    # 反向引用 blog表 每个user对象都有一个blog属性
    blog = db.relationship("Blog", backref="edit_user", lazy="dynamic")

    def __repr__(self):
        return '<User %r>' % self.user_name

    def json_str(self):
        return {
            "user_name": self.user_name
        }


# 主题内容
class Blog(db.Model):
    __tablename__ = "blog"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    read_num = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship('User', backref="edit_blog", lazy=True)

    # 外键关联category表每个topic对象都有一个category属性
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship('Category', backref=db.backref('category_blogs', lazy=True))
    # 外键关联user表每个topic对象都有一个user属性
    # user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    def __repr__(self):
        return '<blog %r>' % self.title

    def json_str(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "read_num": self.read_num,
            "user": self.user.json_str(),
            "category": self.category.json_str()
        }