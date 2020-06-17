from flask import Flask
from dream_demo import db   #导入数据库对象


class User(db.Model):   #建立模型 用户
    __tablename__="users"   #数据库表名
    user_id = db.Column(db.Integer,primary_key=True)   #主键 自增
    name = db.Column(db.String(16),unique=True)   #用户名
    num_class = db.Column(db.String(120))
    account = db.Column(db.String(16), unique=True)  # 用户名
    password = db.Column(db.String(128))   #密码


class  Dream(db.Model):   #建立模型 文章
    __tablename__="dreams"    #数据库表名
    dream_id = db.Column(db.Integer,primary_key=True)    #主键 自增
    text = db.Column(db.Text())   #内容
    now_time = db.Column(db.Integer)
    deadline = db.Column(db.Integer)
    like_count = db.Column(db.Integer, default=0)
    isPublic = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))    #外键
    user = db.relationship('User', backref='dreams')   #关联 用户