from app import db

# 博客分类
class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    cate_name = db.Column(db.String(50), nullable=False)

    # 反向引用 topic表 每个category对象都有一个topic属性
    topic = db.relationship("Blog", backref="category", lazy="dynamic")
    def __init__(self, cate_name):
        self.cate_name = cate_name

    def __repr__(self):
        return '<Category %r>' % self.cate_name


# 用户信息
# class User(db.Model):
#     __tablename__ = "user"
#     id = db.Column(db.Integer, primary_key=True)
#     loginname = db.Column(db.String(50), nullable=False)
#     uname = db.Column(db.String(30), nullable=False)
#     email = db.Column(db.String(200), nullable=False)
#     url = db.Column(db.String(200))
#     upwd = db.Column(db.String(30), nullable=False)
#     is_author = db.Column(db.String(4), default=0)

#     # 反向引用 topic表 每个user对象都有一个topic属性
#     topic = db.relationship("Topic", backref="user", lazy="dynamic")
#     # 反向引用 reply表 每个user对象都有一个reply属性
#     reply = db.relationship("Reply", backref="user", lazy="dynamic")

#     # 关系：多对多
#     # 增加与topic之间的关联关系
#     voke_topic = db.relationship("Topic",
#                                  secondary="voke",
#                                  backref=db.backref("voke_user", lazy="dynamic"),
#                                  lazy="dynamic"
#                                  )

# 主题内容
class Blog(db.Model):
    __tablename__ = "blog"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False)
    read_num = db.Column(db.Integer, default=0)
    content = db.Column(db.Text, nullable=False)
    images = db.Column(db.Text)

    # 关系：一（blogtyp，category，user）对多 (topic)

    # 外键关联category表每个topic对象都有一个category属性
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    # 外键关联user表每个topic对象都有一个user属性
    # user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
