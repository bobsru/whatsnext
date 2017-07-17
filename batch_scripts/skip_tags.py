__author__ = 'srujanabobba'

import boto3
from boto3.dynamodb.conditions import Attr


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('so_tags')

response = table.scan(
    FilterExpression=Attr('tag_count').gt(9999)
)
items = response['Items']
with table.batch_writer() as batch:
    for item in items:
        tag_value = False
        if 'tag_skip' in item:
            if item['tag_skip'] == 'true':
                tag_value = True
        if not tag_value:
            user_response = raw_input('Do you want to skip: '+item['tag_name'] + '? y or n: ')
            if(user_response == 'y'):
                print 'Skipping ',item['tag_name']
                batch.put_item(
                   Item={
                        'tag_name': item['tag_name'],
                       'tag_count': item['tag_count'],
                       'tag_skip' : 'true'
                    }
                )

