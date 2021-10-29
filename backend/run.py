from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import boto3
import botocore
from flask_swagger_ui import get_swaggerui_blueprint
from Instance import ec2List, s3List, VPCList

app = Flask(__name__,static_url_path='',static_folder="templates") 
app.config['SECRET_KEY'] = 'wcsfeufhwiquehfdx'
CORS(app)
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name' : "Wooly_Clouds"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def index():
    return render_template('new.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else :
        public_access = request.form['public']
        secret = request.form['secret']
        region = request.form['region']
        try :
            boto_session = boto3.Session(
                aws_access_key_id = public_access,
                aws_secret_access_key = secret,
                region_name = region 
            )
            ec2_client = boto_session.client('ec2')
            ec2_client.describe_instances()
            session['boto_session'] = [public_access, secret, region]
        except botocore.exceptions.ClientError:
            return "key 입력을 다시 확인해 주세요"

        return "login success"

@app.route('/visualize', methods=['GET'])
def visualize():
    userInfo = session.get('boto_session',None)
    boto_session = boto3.Session(
        aws_access_key_id= userInfo[0],
        aws_secret_access_key = userInfo[1],
        region_name= userInfo[2]
    )

    ec2 = ec2List(boto_session,1, '')
    s3 = s3List(boto_session,1, '')
    vpc = VPCList(boto_session, 1,'')

    instanceList = {
        'ec2' : ec2,
        's3' : s3,
        'vpc' : vpc
    }

    return instanceList # rendering 필요 


@app.route('/information/<string:_type>/ID/<string:_instanceId>', methods=['GET'])
def information(_type, _instanceId):

    userInfo = session.get('boto_session',None)
    boto_session = boto3.Session(
        aws_access_key_id= userInfo[0],
        aws_secret_access_key = userInfo[1],
        region_name= userInfo[2]
    )
    
    if _type == 'ec2' :
        result = ec2List(boto_session, 2, _instanceId)
    elif _type == 's3':
        result = s3List(boto_session, 2, _instanceId)
    elif _type == 'vpc':
        result = VPCList(boto_session, 2, _instanceId)

    
    return result # rendering 필요 

@app.route('/option/<string:_option>/type/<string:_type>/ID/<string:_instanceId>', methods=['GET'])
def stopInstance(_option, _type, _instanceId):
    userInfo = session.get('boto_session',None)
    boto_session = boto3.Session(
        aws_access_key_id= userInfo[0],
        aws_secret_access_key = userInfo[1],
        region_name= userInfo[2]
    )
    if _type == 'ec2':
        if _option == '3': # option == 3이면 인스턴스 중지 
            result = ec2List(boto_session, 3, _instanceId)
        elif _option == '4': # option == 4면 인스턴스 삭제
            result = ec2List(boto_session, 4, _instanceId)
    else :
        result = s3List(boto_session, 4, _instanceId) # s3 인스턴스를 삭제한다. 그런데 ec2와는 다르게 ID가 아니라 인스턴스의 이름을 보내야 한다.

    return result


if __name__ == '__main__':
    app.run(port=3000, debug=True)

