__author__ = 'srujanabobba'

import boto3
from boto3.dynamodb.conditions import Attr,Key


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('so_tags')

response = table.scan(
    FilterExpression=Attr('tag_count').gt(9999)
)


# response = table.query(
#
#     ExpressionAttributeNames={ "#yr": "year" }, # Expression Attribute Names for Projection Expression only.
#     KeyConditionExpression=Key('tag_count').gt(9999) & Key('tag_skip').between('A', 'L')
# )

items = response['Items']

with table.batch_writer() as batch:
    for item in items:

        if 'tag_skip' not in item:

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
            else:
                batch.put_item(
                    Item={
                        'tag_name': item['tag_name'],
                        'tag_count': item['tag_count'],
                        'tag_skip': 'false'
                    }
                )

