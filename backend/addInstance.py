import botocore

def addEC2(boto_session, information):
    ec2 = boto_session.resource("ec2")

    # 인스턴스 생성 
    try :
        instances = ec2.create_instances(
            ImageId="ami-0ba5cd124d7a79612",
            InstanceType="t2.micro",
            MaxCount=1,
            MinCount=1,
            NetworkInterfaces=[{
            "SubnetId": information["subnetId"],
            "DeviceIndex": 0,
            "AssociatePublicIpAddress": True,
            "Groups": [information["groups"]]
            }],
        KeyName=information["keyname"])
    except :
        return "입력을 다시 확인해 주세요"
    instance = instances[0]

    # 인스턴스 이름 지정 
    instance.create_tags(
            Tags=[{"Key": "Name", "Value": information["name"]}])

    # 생성될 때까지 기다리기 
    instance.wait_until_running()

    return "생성 완료"


def addVPC(boto_session, information):
    ec2client = boto_session.client("ec2")
    ec2resource = boto_session.resource("ec2")

    try :
        vpcInit = ec2client.create_vpc(CidrBlock=information["cidrBlock"])
    except :
        return "입력을 다시 확인해 주세요"
    vpc = ec2resource.Vpc(vpcInit["Vpc"]["VpcId"])
    vpc.create_tags(Tags=[{"Key": "Name", "Value": information["Name"]}])


    return "생성 완료"


def addSubnet(boto_session, information):
    ec2resource = boto_session.resource("ec2")
    try :
        vpc = ec2resource.Vpc(information["VpcId"])
    except :
        return "VPC ID를 다시 입력해 주세요"

    try : 
        subnet = vpc.create_subnet(CidrBlock=information["cidrBlock"], AvailabilityZone=information["availabilityZone"])
    except : 
        return "입력을 다시 확인해 주세요"

    subnet.create_tags(Tags=[{"Key": "Name", "Value": information["name"]}])

    return "생성 완료"

def addS3(boto_session, session, information):
    s3_client = boto_session.client('s3')
    try:
        s3_client.create_bucket(ACL='private',
                                Bucket=information["name"],
                                CreateBucketConfiguration={
                                'LocationConstraint': session[2]})

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "BucketAlreadyOwnedByYou":
            return "Error: Bucket already created and owned by you!!"
        elif e.response['Error']['Code'] == "BucketAlreadyExists":
            return "Error: Bucket already exist!!"
        elif e.response['Error']['Code'] == "InvalidBucketName":
            return "Error: Invalid Bucket name!!"
        else:
            raise

    return "생성 완료"

