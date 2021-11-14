from boto3 import NullHandler, session
import botocore

imageUrl = {
    "VPC" : "https://firebasestorage.googleapis.com/v0/b/confident-35184.appspot.com/o/vpc.png?alt=media&token=746f89eb-c3b1-45c2-b7ab-b5195184ef12",
    "SUBNET" : "https://firebasestorage.googleapis.com/v0/b/confident-35184.appspot.com/o/subnet.png?alt=media&token=74784509-f005-4fae-9771-efaf46822c73",
    "S3" : "https://firebasestorage.googleapis.com/v0/b/confident-35184.appspot.com/o/S3.png?alt=media&token=86dba17a-85e6-446b-b1a5-9581847df29b",
    "EC2" : "https://firebasestorage.googleapis.com/v0/b/confident-35184.appspot.com/o/instance.png?alt=media&token=e464b262-64b8-4388-b2c7-61822b3d1e64"
}

def getRootInfo(session):
    information = {}
    information["element"] = session[2]
    information["imageUrl"] = imageUrl['VPC']
    information["id"] = session[2]
    information["parentId"] = None
    return [information]


def ec2List(boto_session, option, instanceID):
    ec2_client = boto_session.client('ec2')
    if option == 1: # 모든 ec2 인스턴스 정보 불러오기 
        ec2List = []
        responses = ec2_client.describe_instances().get("Reservations")
        for response in responses :
            for instance in response["Instances"]:
                information = {}
                information["element"] = "instance"
                information["imageUrl"] = imageUrl['EC2']
                information["id"] = instance["InstanceId"]
                information["parentId"] = instance["SubnetId"]
                information["name"] = instance["Tags"][0]["Value"]
                ec2List.append(information)
        return ec2List
    elif option == 2 : # 특정 ec2 인스턴스 정보 불러오기 
        try:
            # Describe an instance
            ec2Info = dict()
            response = ec2_client.describe_instances(InstanceIds=[instanceID]).get('Reservations')[0]['Instances'][0]
            ec2Info['InstanceId'] = response['InstanceId']
            ec2Info['ImageId'] = response['ImageId']
            ec2Info['InstanceType'] = response['InstanceType']
            ec2Info['State'] = response['State']['Name']
            ec2Info['Subnet_Id'] = response['SubnetId']
            ec2Info['VpcId'] = response['VpcId']
            ec2Info['Name'] = response['Tags'][0]['Value']
            ec2Info['KeyName'] = response['KeyName']
            ec2Info['GroupName'] = response['SecurityGroups'][0]['GroupName']
            ec2Info['GroupId'] = response['SecurityGroups'][0]['GroupId']
            if response['State']['Name'] == 'running':
                ec2Info['PrivateDnsName'] = response['PrivateDnsName']
                ec2Info['PrivateIpAddress'] = response['PrivateIpAddress']
                ec2Info['PublicDnsName'] = response['PublicDnsName']
                ec2Info['PublicIpAddress'] = response['PublicIpAddress']
            else :
                ec2Info["PrivateDnsName"] = ''
                ec2Info["PrivateIpAddress"] = ''
                ec2Info["PublicDnsName"] = ''
                ec2Info["PublicIpAddress"] = ''

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "MissingParameter":
                print("Error: Missing instance id!!")
            else:
                raise
        return ec2Info
    elif option == 3:           # 인스턴스 중지하기
        try:
            # Stop an instance
            ec2_client.stop_instances(InstanceIds=[instanceID], DryRun=False)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "InvalidInstanceID.Malformed":
                print("Error: Invalid instance id!!")
            else:
                raise
        return "인스턴스 중지 완료"
    else :                      # 인스턴스 삭제하기  (option == 4 일경우)
        try:
            # Terminate an instance
            ec2_client.terminate_instances(InstanceIds=[instanceID], DryRun=False)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "InvalidInstanceID.Malformed":
                print("Error: Invalid instance id!!")
            else:
                raise
        return "인스턴스 삭제 완료"
        


def s3List(boto_session, option, bucketName):
    s3_client = boto_session.client('s3')


    if option == 1 :    # 모든 s3 인스턴스 정보 불러오기 
        list_buckets_resp = s3_client.list_buckets()
        bucketList = []

        for bucket in list_buckets_resp['Buckets']:
            information = {}
            information["element"] = "s3"
            information["imageUrl"] = imageUrl["S3"]
            information["id"] = bucket["Name"]
            information["parentId"] = None
            information["name"] = None
            bucketList.append(information)

        return bucketList
    elif option == 2:               # 특정 s3 인스턴스 정보 불러오기 
        try:
            s3objects = s3_client.list_objects_v2(Bucket=bucketName)

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "NoSuchBucket":
                return "Error: Bucket does not exist!!"
            elif e.response['Error']['Code'] == "InvalidBucketName":
                return "Error: Invalid Bucket name!!"
            else:
                raise
        
        return s3objects['Name']
    elif option == 3:               # s3 인스턴스 삭제하기 
        try:
            s3_client.terminate_instances(InstanceIds=[bucketName], DryRun=False)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "InvalidInstanceID.Malformed":
                print("Error: Invalid instance id!!")
            else:
                raise
        return "삭제 완료"


def VPCList(boto_session, session, option, vpcID):
    ec2_client = boto_session.client('ec2')

    if option == 1 :       # 모든 VPC List 불러오기 
        responses = ec2_client.describe_vpcs().get("Vpcs")
        vpcList = []
        for response in responses :
            information = {}
            information["element"] = "VPC"
            information["imageUrl"] = imageUrl["VPC"]
            information["id"] = response["VpcId"]
            information["parentId"] = session[2]
            information["name"] = response["Tags"][0]["Value"]
            vpcList.append(information)
        return vpcList
    elif option == 2:                   # 특정 VPC 정보 불러오기 
        try :
            vpcInfo = dict()
            response = ec2_client.describe_vpcs(VpcIds=[vpcID]).get("Vpcs")[0]
            vpcInfo['VpcId'] = response['VpcId']
            vpcInfo['CidrBlock'] = response['CidrBlock']
            vpcInfo['State'] = response['State']
            vpcInfo['Name'] = response['Tags'][0]['Value']
            vpcInfo['AvailabilityZone'] = response['AvailabilityZone']

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "MissingParameter":
                print("Error: Missing instance id!!")
            else:
                raise
        return vpcInfo

def subnetList(boto_session, option, subnetID):
    ec2_client = boto_session.client('ec2')

    if option == 1 :       # 모든 VPC List 불러오기 
        responses = ec2_client.describe_subnets().get('Subnets')
        subnetList = []
        for response in responses :
            information = {}
            information["element"] = "subnet"
            information["imageUrl"] = imageUrl["SUBNET"]
            information["id"] = response["SubnetId"]
            information["parentId"] = response["VpcId"]
            information["name"] = response["Tags"][0]["Value"]
            subnetList.append(information)
        return subnetList
    elif option == 2:
        try :
            subnetInfo = dict()
            response = ec2_client.describe_subnets(SubnetIds=[subnetID]).get("Subnets")[0]
            subnetInfo['SubnetId'] = response['SubnetId']
            subnetInfo['VpcId'] = response['VpcId']
            subnetInfo['AvailabilityZone'] = response['AvailabilityZone']
            subnetInfo['CidrBlock'] = response['CidrBlock']
            subnetInfo['State'] = response['State']
            subnetInfo['Name'] = response['Tags'][0]['Value']

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "MissingParameter":
                print("Error: Missing instance id!!")
            else:
                raise
        return subnetInfo
    

def IGWList(boto_session, option, igwID):
    ec2_client = boto_session.client('ec2')

    if option == 1 :       
        responses = ec2_client.describe_IGWs().get('IGWs')
        IGWList = []
        for response in responses :
            IGWList.append([response['IGWId']])
        return IGWList
    elif option == 2:
        try :
            IGWInfo = dict()
            response = ec2_client.describe_IGWs(IGWIds=[igwID]).get("IGWs")[0]
            IGWInfo['IGWId'] = response['IGWId']
            IGWInfo['AvailabilityZone'] = response['AvailabilityZone']
            IGWInfo['CidrBlock'] = response['CidrBlock']
            IGWInfo['State'] = response['State']
            IGWInfo['Name'] = response['Tags'][0]['Value']

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "MissingParameter":
                print("Error: Missing instance id!!")
            else:
                raise
        return IGWInfo


def NGWList(boto_session, option, ngwID):
    ec2_client = boto_session.client('ec2') 
    if option == 1 :       
        responses = ec2_client.describe_nat_gateways().get('NGWs')
        NGWList = []
        for response in responses :
            NGWList.append([response['NGWId']])
        return NGWList
    elif option == 2:
        try :
            NGWInfo = dict()
            response = ec2_client.describe_IGWs(NGWIds=[ngwID]).get("NGWs")[0]
            NGWInfo['NGWId'] = response['NGWId']
            NGWInfo['AvailabilityZone'] = response['AvailabilityZone']
            NGWInfo['CidrBlock'] = response['CidrBlock']
            NGWInfo['State'] = response['State']
            NGWInfo['Name'] = response['Tags'][0]['Value']

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "MissingParameter":
                print("Error: Missing instance id!!")
            else:
                raise
        return NGWInfo


