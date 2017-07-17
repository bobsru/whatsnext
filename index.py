__author__ = 'srujanabobba'


import indeedapi
import parse_text
import boto3
import sys
import os
import json


# Get the input skills
input_skills = ['Infrastructure Engineer']

# Send the input skills to indeed search and get the text as input file.
words = indeedapi.get_job_description(input_skills)
#print words
# Get the words from the input file and parse it
tag_results = {}
parsed_words = parse_text.parser(words)


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('so_tags')
# Check value of i and sleep for a second.
i=0
for _word in parsed_words:
    '''
    i+=1
    if(i==100):
        time.sleep(1)
        i=0
    '''
    try:
        _word = _word.replace('.','').strip()
        response = table.get_item(
            Key={
                'tag_name': _word
            }
        )
        if 'Item' in response:
            tag_info = response['Item']
            tag_results[tag_info['tag_name']] = tag_info['tag_count']

    except Exception as e:
        print 'Got error for word: ',_word
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        pass

final_skills = dict((k, v) for k, v in tag_results.items() if v >= 10000)

print ','.join(final_skills.iterkeys())

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))


