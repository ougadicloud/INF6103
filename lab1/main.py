import sys

sys.path.insert(0, "..")

import json
import os

from utils import Logger, resource_creator, resource_deleter

log = Logger(__name__)


def lab1_create():
    log.info("Creating infrastructure for Lab 1")

    vpc_id = resource_creator.create_vpc(region="ca-central-1", cidr_block="10.0.0.0/16", name="inf6103-vpc")
    if not vpc_id:
        return False

    subnet_id = resource_creator.create_subnet(
        vpc_id=vpc_id,
        region="ca-central-1",
        cidr_block="10.0.1.0/24",
        availability_zone="ca-central-1a",
        name="inf6103-subnet",
    )
    if not subnet_id:
        return False

    igw_id = resource_creator.create_internet_gateway(vpc_id=vpc_id, region="ca-central-1", name="inf6103-igw")
    if not igw_id:
        return False

    rt_id = resource_creator.create_route_table(
        vpc_id=vpc_id, internet_gateway_id=igw_id, region="ca-central-1", name="inf6103-rt"
    )
    if not rt_id:
        return False

    association_id = resource_creator.associate_subnet_with_route_table(
        subnet_id=subnet_id, route_table_id=rt_id, region="ca-central-1"
    )
    if not association_id:
        return False

    ingress_rules = [
        {
            "IpProtocol": "tcp",
            "FromPort": 22,
            "ToPort": 22,
            "IpRanges": [{"CidrIp": "0.0.0.0/0", "Description": "SSH"}],
        },
        {
            "IpProtocol": "tcp",
            "FromPort": 8080,
            "ToPort": 8081,
            "IpRanges": [{"CidrIp": "0.0.0.0/0", "Description": "Lab ports"}],
        },
    ]

    sg_id = resource_creator.create_security_group(
        vpc_id=vpc_id, ingress_rules=ingress_rules, region="ca-central-1", name="inf6103-sg"
    )
    if not sg_id:
        return False

    key_name = resource_creator.create_key_pair(region="ca-central-1", key_name="inf6103-key")
    if not key_name:
        return False

    user_data = resource_creator.load_user_data(file_path="user_data.tpl")
    if not user_data:
        return False

    instance_ids = resource_creator.create_ec2_instance(
        subnet_id=subnet_id,
        security_group_id=sg_id,
        region="ca-central-1",
        instance_type="m7i-flex.large",
        key_name=key_name,
        image_id="ami-0c08b0f4f9d446eaa",
        name="inf6103-instance",
        user_data=user_data,
    )
    if not instance_ids:
        return False

    infrastructure = {
        "vpc_id": vpc_id,
        "subnet_id": subnet_id,
        "igw_id": igw_id,
        "rt_id": rt_id,
        "sg_id": sg_id,
        "key_name": key_name,
        "instance_ids": instance_ids,
        "region": "ca-central-1",
    }

    with open("infra.json", "w") as f:
        json.dump(infrastructure, f, indent=2)

    log.info("Lab 1 infrastructure created successfully")
    log.info(f"VPC ID: {vpc_id}")
    log.info(f"Subnet ID: {subnet_id}")
    log.info(f"IGW ID: {igw_id}")
    log.info(f"Route Table ID: {rt_id}")
    log.info(f"Association ID: {association_id}")
    log.info(f"Security Group ID: {sg_id}")
    log.info(f"Key Pair: {key_name}")
    log.info(f"Instance IDs: {instance_ids}")

    return True


def lab1_delete():
    log.info("Deleting Lab 1 infrastructure")

    if not os.path.exists("infra.json"):
        log.error("infra.json not found. Run create first")
        return False

    with open("infra.json", "r") as f:
        infrastructure = json.load(f)

    region = infrastructure.get("region", "ca-central-1")

    resource_deleter.terminate_instance(instance_ids=infrastructure["instance_ids"], region=region)
    resource_deleter.delete_security_group(security_group_id=infrastructure["sg_id"], region=region)
    resource_deleter.delete_route_table(route_table_id=infrastructure["rt_id"], region=region)
    resource_deleter.delete_internet_gateway(
        internet_gateway_id=infrastructure["igw_id"], vpc_id=infrastructure["vpc_id"], region=region
    )
    resource_deleter.delete_subnet(subnet_id=infrastructure["subnet_id"], region=region)
    resource_deleter.delete_vpc(vpc_id=infrastructure["vpc_id"], region=region)
    resource_deleter.delete_key_pair(key_name=infrastructure["key_name"], region=region)

    os.remove("infra.json")

    log.info("Lab 1 infrastructure deleted successfully")

    return True


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "delete":
        lab1_delete()
    else:
        lab1_create()
