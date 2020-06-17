from flask import Flask

class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:3306/dream"   #登陆MySQL
    SQLALCHEMY_TRACK_MODIFICATIONS=True   #设置sqlalchemy自动跟踪数据库