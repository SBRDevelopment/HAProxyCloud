from boto.exception import EC2ResponseError
from boto.ec2.connection import EC2Connection
from boto.ec2.tag import Tag

def get_instances(tags):
    filters = {'instance-state-name': 'running'}
    for tag in tags:
        filters['tag:'+tag['key']] = tag['value']
    
    conn = EC2Connection()
    
    try:
        instances = []
        reservations = conn.get_all_instances(filters=filters)
        for reservation in reservations:
            for instance in reservation.instances:
                instances.append(instance)
        return instances
    except EC2ResponseError as e:
        return []