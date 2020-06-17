from flask import request   #导入request模块
from flask import jsonify   #导入jsonify模块用来返回json数据
from dream_demo.auth import create_token, parse_payload   #导入登录验证模块
from dream_demo.models import *   #导入模型
from dream_demo import app
from dream_demo import db

@app.route('/doLogin',methods=['GET'])   #登陆
def doLogin():
    account = request.args.get('account')   #存储http请求中的输入
    password = request.args.get('password')
    user = db.session.query(User).filter(User.account == account).first()   # 检测用户和密码是否正确
    if user is None:   #查询不到显示无效用户
        return jsonify("无效用户!")
    elif user.password == password:   # 用户名和密码正确，生成token并返回，不正确显示错误
        token = create_token({'user.id': user.user_id})
        return jsonify({'status': True, 'token': token})
    else:
        return jsonify({'status': False, 'error': '用户名或密码错误', 'pass': request.args.get('password')})
