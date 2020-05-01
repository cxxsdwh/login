from usr_utils import *
from mail_utils import *
from quest_utils import *

from flask import Flask, jsonify, request, render_template,Response
from flask_cors import CORS
import imageio
import numpy as np
import time
# Instantiate the Node

app = Flask(__name__)
CORS(app)

tmp=1
@app.route('/usr/')
def index():
    return render_template('./index.html')

@app.route('/usr/account')#登陆页面
def account():
    return render_template('./index.html')
@app.route('/usr/create')#创建用户页面
def create():
    return render_template('./create.html')
last_send=0
@app.route('/usr/sendMail',methods=['POST'])#创建用户口
def send():
    global last_send
    if not email_exist(request.form['addr']):
        cur_time=time.time()
        if (cur_time-last_send)>60:
            last_send=cur_time
            mail_key = push_mail(request.form['addr'])
            send_mail(key=mail_key,to=request.form['addr'])
            response = {'status':0}
        else:
            response = {'status':-2,'key':"邮箱冷却中，稍后再试"}
    else:
        response = {'status':-1,'key':"Email have been used"}
    return jsonify(response),200
@app.route('/usr/createUsr',methods=['POST'])#创建用户口
def create_usr():
    #print(request.form.keys())
    if check_mail(request.form['addr'],request.form['mail_key']):
        tmp = create_account(name=request.form['usr'],password=request.form['password'],
                      email=request.form['addr'])
        if tmp:
            response = {'status':0,'key':tmp}
        else:
            response = {'status':-1,'key':"account already exist"}
    else:
        response = {'status':-2,'key':"验证码错误"}
    return jsonify(response),200

@app.route('/usr/login', methods=['POST'])#登陆口
def my_login():
    myusr=query_user(request.form['usr'])
    if myusr:
        if 'key' in request.form.keys():
            if qualified(myusr,request.form['key']):
                print('in date')
                new_key=renew_key(myusr)
                response = {'status':0,'key':new_key}
            else:
                print('out of date ')
                response = {'status':-1,'key':'out_of_date'}
        elif 'password' in request.form.keys():
            if myusr.password==request.form['password']:
                print('real passwd')
                new_key=renew_key(myusr)
                response = {'status':0,'key':new_key}
            else:
                print('wrong passwd')
                response = {'status':-2,'key':'Wrong Password'}
    else:
        print('not exist')
        response = {'status':-2,'key':'Account Not Exist'}
    return jsonify(response), 200
@app.route('/usr/home', methods=['GET'])#登陆后主页
def my_home():
    #loc=request.args['loc']
    return  render_template('./home.html')
@app.route('/usr/quest', methods=['POST'])#问题请求口
def quest():
    myusr=query_user(request.form['usr'])
    if qualified(myusr,request.form['key']):
        tmp=query_quest().filter_by(subject=request.form['subject'])
        res=tmp[np.random.randint(0,tmp.count())].__dict__
        res.pop('_sa_instance_state', None)
        res.update({"status":0})
    else:
        res={{"status":-1}}
    return  jsonify(res),200
if __name__ == '__main__':
    port=80
    app.run(host='0.0.0.0', port=port)


