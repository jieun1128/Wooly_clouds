from boto3 import session
import botocore

def ec2List(boto_session, option, instanceID):
    ec2_client = boto_session.client('ec2')
    if option == 1: # 모든 ec2 인스턴스 정보 불러오기 
        ec2List = []
        responses = ec2_client.describe_instances().get("Reservations")
        for response in responses :
            for instance in response["Instances"]:
                ec2List.append([instance["InstanceId"],instance["SubnetId"],instance["VpcId"]])
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
            bucketList.append(bucket['Name'])

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


def VPCList(boto_session, option, vpcID):
    ec2_client = boto_session.client('ec2')

    if option == 1 :       # 모든 VPC List 불러오기 
        responses = ec2_client.describe_vpcs().get("Vpcs")
        vpcList = []
        for response in responses :
            vpcList.append(response['VpcId'])
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
            subnetList.append([response['SubnetId'],response['VpcId']])
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
    
    return ''

def NGWList(boto_session, opttion, ngwID):

    return ''


