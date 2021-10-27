from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import boto3
import botocore
from flask_swagger_ui import get_swaggerui_blueprint
from Instance import ec2List, s3List

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

    ec2 = ec2List(boto_session,'i-0c7e2dbf9143e5ee0')
    s3 = s3List(boto_session,"woolycloudbucket")

    instanceList = {
        'ec2' : ec2,
        's3' : s3
    }

    return instanceList # rendering 필요 


if __name__ == '__main__':
    app.run(port=3000, debug=True)

