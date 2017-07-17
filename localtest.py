__author__ = 'srujanabobba'

event = {
    "currentIntent": {
        "slots": {
            "Skill": "testing, selenium"
        },
        "name": "ImproveIntent",
        "confirmationStatus": "None"
    },
    "bot": {
        "alias": "",
        "version": "$LATEST",
        "name": "WhatsNext"
    },
    "userId": "kkpu9e608t72gtn7k1dy2uiwcjkm6odf",
    "inputTranscript": "testing, selenium",
    "invocationSource": "FulfillmentCodeHook",
    "outputDialogMode": "Text",
    "messageVersion": "1.0",
    "sessionAttributes": {}
}

import index
index.lambda_handler(event,"")
