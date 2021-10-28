import boto3
import botocore

def ec2List(boto_session, option, ID):
    ec2_client = boto_session.client('ec2')
    if option == 1: # 모든 ec2 인스턴스 정보 불러오기 
        ec2List = []
        responses = ec2_client.describe_instances().get("Reservations")
        for response in responses :
            for instance in response["Instances"]:
                ec2List.append([instance["InstanceId"],instance["SubnetId"],instance["VpcId"]])
        return ec2List
    elif option == 2: # 인스턴스 종료하기
        print(1)
    else : # 특정 ec2 인스턴스 정보 불러오기 
        try:
            # Describe an instance
            ec2Info = dict()
            response = ec2_client.describe_instances(InstanceIds=[ID]).get('Reservations')[0]['Instances'][0]
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


def s3List(boto_session, option):
    s3_client = boto_session.client('s3')


    if option == "" :    # 모든 s3 인스턴스 정보 불러오기 
        list_buckets_resp = s3_client.list_buckets()
        bucketList = []

        for bucket in list_buckets_resp['Buckets']:
            bucketList.append(bucket['Name'])

        return bucketList
    else:               # 특정 s3 인스턴스 정보 불러오기 
        try:
            s3objects = s3_client.list_objects_v2(Bucket=option)

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "NoSuchBucket":
                print("Error: Bucket does not exist!!")
            elif e.response['Error']['Code'] == "InvalidBucketName":
                print("Error: Invalid Bucket name!!")
            else:
                raise
        
        return s3objects['Name']


def VPCList(boto_session, option):
    ec2_client = boto_session.client('ec2')

    if option == "" :       # 모든 VPC List 불러오기 
        responses = ec2_client.describe_vpcs().get("Vpcs")
        vpcList = []
        for response in responses :
            vpcList.append(response['VpcId'])
        return vpcList
    else:                   # 특정 VPC 정보 불러오기 
        try :
            vpcInfo = dict()
            response = ec2_client.describe_vpcs(VpcIds=[option]).get("Vpcs")[0]
            vpcInfo['VpcId'] = response['VpcId']
            vpcInfo['CidrBlock'] = response['CidrBlock']
            vpcInfo['State'] = response['State']
            vpcInfo['Name'] = response['Tags'][0]['Value']

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "MissingParameter":
                print("Error: Missing instance id!!")
            else:
                raise
    return vpcInfo

# def subnetList(boto_session, option):
#     ec2_client = boto_session.client('ec2')

#     if option == "" :       # 모든 VPC List 불러오기 
#         responses = ec2_client.describe_subnets()
#         # vpcList = []
#         # for response in responses :
#         #     vpcList.append(response['VpcId'])
#         # return vpcList
#         print(responses)
#         return
#     else: 
#         return





