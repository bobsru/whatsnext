__author__ = 'srujanabobba'

import boto3
import stackexchange
import yaml
import time

with open("settings.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

# Set the API KEY for StackOverflow
so = stackexchange.Site(stackexchange.StackOverflow, cfg['stackexchange']['api_key'],impose_throttling=False)

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('so_tags')

#Get tags
page_no = 1

while True:
    print 'Fetching tags for page: ',page_no
    if(page_no%50 == 0):
        time.sleep(30)
    tag_info = so.tags(sort='popular',page=page_no,pagesize=100)

    # Break if there are no tags
    if(len(tag_info.items) == 0):
        print 'No more tags. So breaking from loop'
        break

    # Continue if there are tags for all the tag items
    with table.batch_writer() as batch:
        for each_tag in tag_info.items:
            batch.put_item(
               Item={
                    'tag_name': each_tag.name,
                   'tag_count': each_tag.count
                }
            )

    page_no+= 1 # Increase the page_no for the next iteration







'''
# Update tag counts for the tags
            table.update_item(
                Key={
                    'tag_name': each_tag.name
                },
                UpdateExpression='SET tag_count = :val1',
                ExpressionAttributeValues={
                    ':val1': each_tag.count
                }
            )
'''