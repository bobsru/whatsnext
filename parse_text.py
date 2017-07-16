__author__ = 'srujanabobba'

import re
import collections

# Parser to get all the words and filter through some common words.
# Returns the words with size more than ${word_size}
word_size = 1
def parser(words):
    #words = re.findall('\w+', open(filename).read().lower())

    remove_words = ['and','with','the','or','very','type','both','latest','position','requires','you','digital','problen','experience','to','in','technologies','are','job','team',\
                    'on','best','of','citizen','like','is','have','if','needs','requirements','programs','professional','contractors','full','we','only','folks','changes','resume','hire','open',\
                    'resources','hands','highly','us','will','hi','years','one','two','three','four','five','development','software','developer','working','contract','limited','code','but','include',\
                    'not','using','skills','including','our','washington','your','service','6','5','4','3','2','1','7','8','9','10','15','familiarity',\
                    'developed','leads','solutions','solving','operational','environment','source','location','activities','administrative','activities','appreciated','specific','excellent','maintenance','share','services','benefit','individuals','requirement',\
                    'direct','related','prototyping','urgent','rate','computer','duration','selected','please','per','various','enforcing','available','be','degree','equivalent','corporation','strong','technical','industry',\
                    'months','participating','tasks','within','market','response','expected','problem','more','responsibilites','junior','starter','kindly','developing','this','reviews','player','pay','self','comfort','requisition','role','details','independent','required',\
                    'tx','fort','worth','good','write','focus','knowledge','title','positions','year','progress','modify','understanding','bachelor','masters','master','participate','targeting','optional','plug','fulltime','involves','primarily','phone','skype','salary','must','process','id','inc',\
                    'dallas','responsibilities','which','interview','experienced','description','annum','time','sex','race','origin','destination','as','irving','ability','preferred','verbal','identify','w2','such','education','tools','well','note','candidate','min','max','bench','looking','under',\
                    'usage','independently','manage','employers','providing','part','possible','monika','competing','chopra','while','a','practices','consultants','115','1099','apply','hour','hours','day','days','led','llc','level','clients','lines','upload','action','cookies','skip',\
                    'global','local','short','long','instructions','let','highest','access','writing','disability','provider','led','free','choice','connectivity','zip','project','processing','system','find','scale','forms','field','save','user','key','value','search','object','',\
                    '','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
    for rem_word in remove_words:
        words = filter(lambda a: a != rem_word, words)

    counters = collections.Counter(words)
    final_words = dict((k, v) for k, v in counters.items() if v >= word_size)
    return final_words.keys()
