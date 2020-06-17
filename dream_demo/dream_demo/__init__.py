from flask import Flask
from flask_sqlalchemy import SQLAlchemy   #导入SQLAlchemy模块
from dream_demo.config import Config   #导入数据库链接

app = Flask(__name__)
app.config.from_object(Config)
db=SQLAlchemy(app)
#创建数据库对象
app.config['JSON_AS_ASCII'] = False  #让json返回显示中文而不是utf-8

from dream_demo.models import *   #导入模型
from dream_demo.routes import *   #导入路由

if __name__=='__main__':
     #db.drop_all()   #创建数据库
     #db.create_all()
     app.run(debug=True)
