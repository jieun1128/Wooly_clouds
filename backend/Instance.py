import boto3
import botocore

def ec2List(boto_session, option):
    ec2_client = boto_session.client('ec2')
    if option == "": # 모든 ec2 인스턴스 정보 불러오기 
        ec2List = []
        responses = ec2_client.describe_instances().get("Reservations")
        for response in responses :
            for instance in response["Instances"]:
                ec2List.append([instance["InstanceId"],instance["SubnetId"],instance["VpcId"]])
        return ec2List
    else : # 특정 ec2 인스턴스 정보 불러오기 
        ec2Info = dict()
        try:
            # Describe an instance
            response = ec2_client.describe_instances(InstanceIds=[option]).get("Reservations")
            ec2Info['InstanceId'] = response[0]['Instances'][0]['InstanceId']
            ec2Info['ImageId'] = response[0]['Instances'][0]['ImageId']
            ec2Info["InstanceType"] = response[0]['Instances'][0]['InstanceType']
            ec2Info["State"] = response[0]['Instances'][0]['State']['Name']
            ec2Info["Subnet_Id"] = response[0]['Instances'][0]["SubnetId"]
            ec2Info["VpcId"] = response[0]['Instances'][0]["VpcId"]
            if response[0]['Instances'][0]['State']['Name'] == 'running':
                ec2Info["PrivateDnsName"] = response[0]['Instances'][0]['PrivateDnsName']
                ec2Info["PrivateIpAddress"] = response[0]['Instances'][0]['PrivateIpAddress']
                ec2Info["PublicDnsName"] = response[0]['Instances'][0]['PublicDnsName']
                ec2Info["PublicIpAddress"] = response[0]['Instances'][0]['PublicIpAddress']
            else :
                ec2Info["PrivateDnsName"] = ''
                ec2Info["PrivateIpAddress"] = ''
                ec2Info["PublicDnsName"] = ''
                ec2Info["PublicIpAddress"] = ''

            return ec2Info
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "MissingParameter":
                print("Error: Missing instance id!!")
            else:
                raise
    return


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
            elif e.response['Error']['Code'] == "AllAccessDisabled":
                print("Error: You do not have access to the Bucket!!")
            else:
                raise
        
        return s3objects['Name']










