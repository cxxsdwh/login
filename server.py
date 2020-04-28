from myutils import *

from flask import Flask, jsonify, request, render_template,Response
from flask_cors import CORS
import imageio

app = Flask(__name__)
CORS(app)

tmp=1
@app.route('/usr')
def index():
    return render_template('./index.html')

@app.route('/usr/account')
def account():
    return render_template('./index.html')

@app.route('/usr/login', methods=['POST'])
def my_login():
    myusr=query_user(request.form['usr'])
    if myusr:
        if 'key' in request.form.keys():
            if qualified(myusr,request.form['key']):
                print('in date')
                new_key=renew_key(myusr)
                response = {'status':0,'key':new_key}
                return jsonify(response), 200
            print('out of date ')
            response = {'status':-1,'key':'out_of_date'}
            return jsonify(response), 200
        elif 'password' in request.form.keys():
            if myusr.password==request.form['password']:
                print('real passwd')
                new_key=renew_key(myusr)
                response = {'status':0,'key':new_key}
                return jsonify(response), 200
    print('wrong passwd')
    response = {'status':-2,'key':'wrong_password'}
    return jsonify(response), 200
@app.route('/usr/home', methods=['GET'])
def my_home():
    return  render_template('./home.html')
    
if __name__ == '__main__':
    port=80
    app.run(host='0.0.0.0', port=port)



