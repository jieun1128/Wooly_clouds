from flask import Flask, render_template
import boto3

app = Flask(__name__)

@app.route('/')
def index():
    boto()
    return render_template('new.html')

def boto():
    ec2_client = boto3.client("ec2", region_name="ap-northeast-2")
    reservations = ec2_client.describe_instances(Filters=[
        {
            "Name" : "instance-state-name",
            "Values" : ["running"],
        }
    ]).get("Reservations")

    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            public_ip = instance["PublicIpAddress"]
            private_ip = instance["PrivateIpAddress"]
            print(f"{instance_id}, {instance_type}, {public_ip}, {private_ip}")

if __name__ == '__main__':
    app.run(port=3000, debug=True)

