from flask import Flask, render_template
import boto3

app = Flask(__name__)
ec2_client = boto3.client("ec2", region_name="ap-northeast-2")

@app.route('/')
def index():
   # boto()
    #create_instance()
    #deleteInstance()
    return render_template('new.html')

def boto():
    reservations = ec2_client.describe_instances(Filters=[
        {
            "Name" : "instance-state-name",
            "Values" : ["running"],
        }
    ]).get("Reservations")
    for reservation in reservations:
        print(reservation["Instances"])
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            public_ip = instance["PublicIpAddress"]
            private_ip = instance["PrivateIpAddress"]
            subnet_id = instance["SubnetId"]
            vpc_id = instance["VpcId"]

            print(f"{instance_id}, {instance_type}, {public_ip}, {private_ip}, {subnet_id}, {vpc_id}")

def create_instance():
    ec2 = boto3.resource('ec2')

    # 인스턴스 생성 
    instances = ec2.create_instances(
        ImageId='ami-0ba5cd124d7a79612',
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1,
        NetworkInterfaces=[{
        'SubnetId': "subnet-06cf995b42d89862f",
        'DeviceIndex': 0,
        'AssociatePublicIpAddress': True,
        'Groups': ["sg-015bc3d5c02501a5d"]
        }],
    KeyName='my_key')
    
    instance = instances[0]

    # 인스턴스 이름 지정 
    instance.create_tags(
            Tags=[{"Key": "Name", "Value": "newInstance"}])

    # 생성될 때까지 기다리기 
    instance.wait_until_running()

    # 생성 후 정보 출력 
    print('Instance Id: ', instance.id)
    print('Connect Ec2 instance with the following SSH command once initializing process gets completed.')
    print('Check AWS console for current status.')
    print('ssh -i "{}.pem" {}@{}'.format("ec2-keypair",
              'ec2-user', instance.public_ip_address))


def deleteInstance():
    response = ec2_client.terminate_instances(InstanceIds=["i-01f2977637288ef27"])
    print(response)

if __name__ == '__main__':
    app.run(debug=True)

