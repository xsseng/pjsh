from flask import Flask,request,Response,render_template
from flask_cors import CORS
import redis
import json

### 数据库参数 ###
# 数据库名称
DB = 0
# 数据库链接地址
DB_HOST = 'localhost'
# 数据库端口
DB_PORT = 6379
# 数据库登录密码
DB_PWD = ''

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app, resources=r'/*')

def redisCon():
	pool = redis.ConnectionPool(host=DB_HOST,port=DB_PORT,db=DB,decode_responses=True,password=DB_PWD)
	r = redis.Redis(connection_pool=pool)
	return r

@app.route('/')
def index():
	return render_template('tools.html')

@app.route('/get_code')
def get_code():
	try:
		r = redisCon()
		resp = {'state':200,'code':r.get('code'),'code_id':r.get('code_id')}
	except:
		resp = {'state':500}
	response = json.dumps(resp)
	return Response(response,mimetype='application/json')

@app.route('/input_code', methods = ['GET', 'POST',])
def input_code():
	try:
		r = redisCon()
		r.set('code',request.form['code'])
		r.incr('code_id', 1)
		resp = {'state':200}
	except:
		resp = {'state':500}
	return Response(json.dumps(resp),mimetype='application/json')

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)
