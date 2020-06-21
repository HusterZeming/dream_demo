from dream_demo.forms import *
from dream_demo import app
from flask import g   #全局变量g存储用户信息
from dream_demo import db
import time
import datetime
import random


@app.before_request   #在处理request之前进行用户身份验证
def jwt_query_params_auth():
    if request.path == '/doLogin':   #登陆时跳过验证
        return
    token = request.headers.get('authorization')   #通过请求头写入token
    result = parse_payload(token)   #解析token来校验传入的token
    if not result['status']:
        return jsonify(result)
    g.info = result['data']   #全局变量g存储用户信息


@app.route("/dream_list",methods= ['GET'])  #展示的梦想
def dream_list():
    dreams = db.session.query(Dream).filter(Dream.isPublic == 1, Dream.deadline > Dream.now_time).all()
    random.shuffle(dreams)   #随机出现
    user_id = g.info['user.id']
    dream_list = {"code": 0, "data": []}
    index = 0
    for dream in dreams:
        likes = db.session.query(Like).filter(Like.dream_id == dream.dream_id, Like.user_id == user_id).first()
        if likes:
            isLike = 1
        elif likes == None:
            isLike = 0
        time_demo = time.localtime(dream.now_time)
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time_demo)
        data = {
            "dream_id": dream.dream_id,  # 标识dream的唯一id
            "name": dream.user.name,
            "text": dream.text,  # 愿望内容
            "time": now_time,  # 发布时间
            "like_count": dream.like_count,# 点赞数
            "isLike": isLike,
        }
        dream_list['data'].insert(index, data)
        index += 1
    return jsonify(dream_list)


@app.route("/like",methods=['POST'])   #点赞
def like():
    dream_id = request.args.get('dream_id')   #存储http请求中的输入
    user_id = g.info['user.id']
    likes = db.session.query(Like).filter(Like.dream_id == dream_id, Like.user_id == user_id).first()
    if likes:
        return jsonify("已点过赞")
    elif likes == None:
        new_like = Like(dream_id = dream_id, user_id = user_id)
        new_like.dream = db.session.query(Dream).filter(Dream.dream_id == dream_id).first()
        new_like.user = db.session.query(User).filter(User.user_id == user_id).first()
        db.session.add(new_like)  # 加入数据库
        db.session.commit()   #提交到数据库
        dream = db.session.query(Dream).filter(Dream.dream_id == dream_id).first()
        dream.like_count += 1
        db.session.commit()  # 提交到数据库
        return jsonify("点赞成功")


@app.route("/post",methods=['POST'])   #发表梦想
def post():
    user_id = g.info['user.id']    #存储http请求中的输入
    text = request.args.get('text')
    is_public = request.args.get('isPublic')
    deadline = request.args.get('deadline')
    if deadline == "XX":
        deadline = "2080-01-01 10:00:00"  #如果传入XX默认为永久
    num_time = time.mktime(time.strptime(deadline, '%Y-%m-%d %H:%M:%S'))
    dtime = datetime.datetime.now()
    now_time = time.mktime(dtime.timetuple())
    new_dream = Dream(text=text, isPublic=int(is_public), deadline=int(num_time), user_id=user_id, now_time=int(now_time))
    new_dream.user = db.session.query(User).filter(User.user_id == user_id).first()   #关联到用户
    db.session.add(new_dream)   #加入数据库
    db.session.commit()   #提交到数据库
    return jsonify("发布成功")


@app.route("/update",methods=['POST'])   #更新梦想
def update():
    user_id = g.info['user.id']    #存储http请求中的输入
    dream_id = request.args.get('dream_id')
    text = request.args.get('text')
    is_public = request.args.get('isPublic')
    deadline = request.args.get('deadline')
    if deadline == "XX":
        deadline = "2080-01-01 10:00:00"  #如果传入XX默认为永久
    num_time = time.mktime(time.strptime(deadline, '%Y-%m-%d %H:%M:%S'))
    dtime = datetime.datetime.now()
    now_time = time.mktime(dtime.timetuple())
    dream = db.session.query(Dream).filter(Dream.dream_id == dream_id).first()
    dream.text = text
    dream.isPublic = int(is_public)
    dream.deadline = int(num_time)
    dream.now_time = int(now_time)
    db.session.commit()   #提交到数据库
    return jsonify("更新成功")


@app.route("/edit",methods=['POST'])   #编辑信息
def send():
    user_id = g.info['user.id']     #存储http请求中的输入
    name = request.args.get('name')
    num_class = request.args.get('num_class')
    user = db.session.query(User).filter(User.user_id == user_id).first()
    user.name = name
    user.num_class = num_class
    db.session.commit()   #提交到数据库
    return jsonify("编辑成功")


@app.route("/personal_list",methods=['GET'])  #个人梦想清单
def personal_list():
    user_id = g.info['user.id']
    dreams = db.session.query(Dream).filter(User.user_id == user_id).all()
    dream_list = {"code": 0, "data": []}
    index = 0
    for dream in dreams:
        now_time_demo = time.localtime(dream.now_time)
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', now_time_demo)
        deadline_demo = time.localtime(dream.deadline)
        deadline = time.strftime('%Y-%m-%d %H:%M:%S', deadline_demo)
        data = {
            "dream_id": dream.dream_id, #标识dream的唯一id
            "text": dream.text, #愿望内容
            "time": now_time, #发布时间
            "deadline": deadline, #公开时间
            "like_count": dream.like_count#点赞数
        }
        dream_list['data'].insert(index, data)
        index +=1
    return jsonify(dream_list)


@app.route("/delete",methods= ['POST'])   #删除梦想
def delete():
    dream_id = request.args.get('dream_id')
    dream = db.session.query(Dream).filter(Dream.dream_id == dream_id).first()
    likes = db.session.query(Like).filter(Like.dream_id == dream_id).all()
    for like in likes:
        db.session.delete(like)
    db.session.delete(dream)   #从数据库中将文章删除
    db.session.commit()   #提交到数据库
    return jsonify("删除成功")

