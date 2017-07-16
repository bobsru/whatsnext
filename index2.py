__author__ = 'srujanabobba'

import stackexchange
import indeedapi
import parse_text
import httplib
import json
import time
import urllib
# Set the API KEY for StackOverflow
so = stackexchange.Site(stackexchange.StackOverflow, "F3wbtgR7YlCH7he7VZuiUg((",impose_throttling=False)

# Get the input skills
input_skills = ['java']

# Send the input skills to indeed search and get the text as input file.
words = indeedapi.get_job_description(input_skills)
#print words
# Get the words from the input file and parse it
tag_results = {}
parsed_words = parse_text.parser(words)
print parsed_words
i=0
for _word in parsed_words:
    i+=1
    if(i==50):
        time.sleep(30)
        i=0
    try:
        _word = _word.replace('.','').strip()
        print _word
        tag_info = so.tags(inname=_word.encode('utf-8'),sort='popular')

        for each_tag in tag_info.items:
            if each_tag.name in parsed_words:
                tag_results[each_tag.name] = each_tag.count

    except httplib.BadStatusLine:
        print 'Got badstatusline error for ',_word

        pass
    except stackexchange.core.StackExchangeError:
        print 'Got stackexchange error for ',_word
        pass

final_skills = dict((k, v) for k, v in tag_results.items() if v >= 3000)
print json.dumps(final_skills,indent=4)

