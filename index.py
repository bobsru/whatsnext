__author__ = 'srujanabobba'


import indeedapi
import parse_text
import boto3
import sys
import time
import os
import logging




logger = logging.getLogger()
logger.setLevel(logging.DEBUG)



""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message, response_card):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message,
            'responseCard': response_card
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message, response_card):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message,
            'responseCard': response_card
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


def build_response_card(title, subtitle, options):
    """
    Build a responseCard with a title, subtitle, and an optional set of options which should be displayed as buttons.
    """
    buttons = None
    if options is not None:
        buttons = []
        for i in range(min(5, len(options))):
            buttons.append(options[i])

    return {
        'contentType': 'application/vnd.amazonaws.card.generic',
        'version': 1,
        'genericAttachments': [{
            'title': title,
            'subTitle': subtitle,
            'buttons': buttons
        }]
    }



""" --- Functions that control the bot's behavior --- """
def get_related_skills(intent_request):
    """
    :param intent_request:
    :return: related skills
    """
    print intent_request['currentIntent']['slots']
    input_skills = intent_request['currentIntent']['slots']['Skill']
    learn = None
    if 'Learn' in intent_request['currentIntent']['slots']:
        learn = intent_request['currentIntent']['slots']['Learn']


    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}





    if input_skills and learn is None:

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
                    if 'tag_skip' in tag_info:
                        if tag_info['tag_skip'] != 'true':
                            tag_results[tag_info['tag_name']] = tag_info['tag_count']

            except Exception as e:
                print 'Got error for word: ',_word
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                pass

        final_skills = dict((k, v) for k, v in tag_results.items() if v >= 10000)

        employer_skills =  ','.join(final_skills.iterkeys())
        print employer_skills



        build_options = [
            {'text': 'Yes', 'value': 'yes'},
            {'text': 'No', 'value': 'no'}
        ]
        return elicit_slot(
            output_session_attributes,
            intent_request['currentIntent']['name'],
            intent_request['currentIntent']['slots'],
            'Learn',
            {'contentType': 'PlainText', 'content': 'Here are the skills employers are looking for ' + employer_skills},
            build_response_card(
                'Learn today', 'Do you want to know more about where you can learn these courses or concepts?',
                build_options
            )
        )

    else:
        if learn == 'yes':
            return close(
                output_session_attributes,
                'Fulfilled',
                {
                    'contentType': 'PlainText',
                    'content': 'Great! Here are the websites to learn. \nwww.udemy.com \nwww.coursera.com'
                }
            )
        else:
            return close(
                output_session_attributes,
                'Fulfilled',
                {
                    'contentType': 'PlainText',
                    'content': 'OK! Thank you for using WhatsNext bot. Have a great learning!'
                }
            )







""" --- Intents --- """


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'ImproveIntent':
        return get_related_skills(intent_request)
    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/Chicago time zone.
    os.environ['TZ'] = 'America/Chicago'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)






