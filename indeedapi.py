__author__ = 'srujanabobba'


from indeed import IndeedClient
import urllib2
from bs4 import BeautifulSoup # For HTML parsing



'''
Function for web scraping
'''


from nltk.corpus import stopwords
def text_cleaner(website):
    '''
    Inputs: a URL to investigate
    Outputs: Cleaned text only
    '''
    try:
        site = urllib2.urlopen(website).read() # Connect to the job posting
    except:
        return   # Need this in case the website isn't there anymore or some other weird connection problem

    soup_obj = BeautifulSoup(site,'html.parser') # Get the html from the site

    for script in soup_obj(["script", "style"]):
        script.extract() # Remove these two elements from the BS4 object



    text = soup_obj.get_text() # Get the text from this



    lines = (line.strip() for line in text.splitlines()) # break into lines



    chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # break multi-headlines into a line each

    def chunk_space(chunk):
        chunk_out = chunk + ' ' # Need to fix spacing issue
        return chunk_out


    text = ''.join(chunk_space(chunk) for chunk in chunks if chunk).encode('utf-8') # Get rid of all blank lines and ends of line


    # Now clean out all of the unicode junk (this line works great!!!)

    try:
        text = text.decode('unicode_escape').encode('ascii', 'ignore') # Need this as some websites aren't formatted
    except:                                                            # in a way that this works, can occasionally throw
        return                                                         # an exception



    text = text.lower().split()  # Go to lower case and split them apart


    stop_words = set(stopwords.words("english")) # Filter out any stop words
    text = [w for w in text if not w in stop_words]

    text = list(set(text)) # Last, just get the set of these. Ignore counts (we are just looking at whether a term existed
                            # or not on the website)

    return text


# Main code

def get_job_description(input_skills):
    client = IndeedClient('7863709885041358')

    params = {
        'q' : input_skills,
        'userip' : "1.2.3.4",
        'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
        'limit' : 25
    }
    job_urls = []
    search_response = client.search(**params)
    for job in search_response['results']:
        job_urls.append(job['url'])
    bunch_of_words = []
    for each_url in job_urls:
        bunch_of_words.extend(text_cleaner(each_url))

    return bunch_of_words


