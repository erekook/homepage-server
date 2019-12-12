from app import db
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context

# 博客分类
class Category(db.Model):
    __tablename__ = "category"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    cate_name = db.Column(db.String(50), nullable=False)

    # 反向引用 blog表 每个category对象都有一个blog属性
    blogs = db.relationship("Blog", backref="_category", lazy="dynamic")

    def __repr__(self):
        return '<Category %r>' % self.cate_name

    def json_str(self):
        return {
            "cate_name": self.cate_name
        }


class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    pwd = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    motto = db.Column(db.String(500), nullable=True)
    is_locked = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_time = db.Column(db.DateTime, nullable=False)

    # 反向引用 blog表 每个user对象都有一个blog属性
    blog = db.relationship("Blog", backref="_user", lazy="dynamic")
    def hash_password(self, pwd): #给密码加密方法
        self.pwd = pwd_context.encrypt(pwd)
 
    def verify_password(self, pwd): #验证密码方法
        return pwd_context.verify(pwd, self.pwd)

    def __repr__(self):
        return '<User %r>' % self.email

    def json_str(self):
        return {
            "email": self.email
        }


# article
class Blog(db.Model):
    __tablename__ = "blog"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    read_num = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship('User', backref="edit_blog", lazy=True)

    # 外键关联category表每个topic对象都有一个category属性
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship('Category', backref=db.backref('category_blogs', lazy=True))
    
    def __repr__(self):
        return '<blog %r>' % self.title

    def json_str(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "read_num": self.read_num,
            "user": self.user.json_str(),
            "category": self.category.json_str(),
            "create_time": str(self.create_time)
        }


# just a quote
class Quote(db.Model):
    __tablename__ = "quote"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    def __repr__(self):
        return '<quote %r>' % self.content

    def json_str(self):
        return {
            "content": self.content
        }

# 邮箱验证码
class EmailCode(db.Model):
    __tablename__ = "email_code"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    def __repr__(self):
        return '<EmailCode %r>' % self.email

    def json_str(self):
        return {
            "code": self.code,
            "email": self.email,
            "create_time": self.create_time
        }

if __name__ == "__main__":
    db.create_all()