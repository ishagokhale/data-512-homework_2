import csv
# These are standard python modules
import json, time, urllib.parse, pandas as pd
#
# The 'requests' module is not a standard Python module. You will need to install this with pip/pip3 if you do not already have it
import requests
#########
#
#    CONSTANTS
#

# The basic English Wikipedia API endpoint
API_ENWIKIPEDIA_ENDPOINT = "https://en.wikipedia.org/w/api.php"
API_HEADER_AGENT = 'User-Agent'

# We'll assume that there needs to be some throttling for these requests - we should always be nice to a free data resource
API_LATENCY_ASSUMED = 0.002       # Assuming roughly 2ms latency on the API and network
API_THROTTLE_WAIT = (1.0/100.0)-API_LATENCY_ASSUMED

# When making automated requests we should include something that is unique to the person making the request
# This should include an email - your UW email would be good to put in there
REQUEST_HEADERS = {
    'User-Agent': '<igokhale@uw.edu>, University of Washington, MSDS DATA 512 - AUTUMN 2024'
}

# This is just a list of English Wikipedia article titles that we can use for example requests
ARTICLE_TITLES = [ 'Bison', 'Northern flicker', 'Red squirrel', 'Chinook salmon', 'Horseshoe bat' ]

# This is a string of additional page properties that can be returned see the Info documentation for
# what can be included. If you don't want any this can simply be the empty string
PAGEINFO_EXTENDED_PROPERTIES = "talkid|url|watched|watchers"
#PAGEINFO_EXTENDED_PROPERTIES = ""

# This template lists the basic parameters for making this
PAGEINFO_PARAMS_TEMPLATE = {
    "action": "query",
    "format": "json",
    "titles": "",           # to simplify this should be a single page title at a time
    "prop": "info",
    "inprop": PAGEINFO_EXTENDED_PROPERTIES
}

#########
#
#    CONSTANTS
#

#    The current LiftWing ORES API endpoint and prediction model
#
API_ORES_LIFTWING_ENDPOINT = "https://api.wikimedia.org/service/lw/inference/v1/models/{model_name}:predict"
API_ORES_EN_QUALITY_MODEL = "enwiki-articlequality"

#
#    The throttling rate is a function of the Access token that you are granted when you request the token. The constants
#    come from dissecting the token and getting the rate limits from the granted token. An example of that is below.
#
API_LATENCY_ASSUMED = 0.002       # Assuming roughly 2ms latency on the API and network
API_THROTTLE_WAIT = ((60.0*60.0)/5000.0)-API_LATENCY_ASSUMED  # The key authorizes 5000 requests per hour

#    When making automated requests we should include something that is unique to the person making the request
#    This should include an email - your UW email would be good to put in there
#    
#    Because all LiftWing API requests require some form of authentication, you need to provide your access token
#    as part of the header too
#
REQUEST_HEADER_TEMPLATE = {
    'User-Agent': "<{email_address}>, University of Washington, MSDS DATA 512 - AUTUMN 2024",
    'Content-Type': 'application/json',
    'Authorization': "Bearer {access_token}"
}
#
#    This is a template for the parameters that we need to supply in the headers of an API request
#
REQUEST_HEADER_PARAMS_TEMPLATE = {
    'email_address' : "",         # your email address should go here
    'access_token'  : ""          # the access token you create will need to go here
}

#
#    A dictionary of English Wikipedia article titles (keys) and sample revision IDs that can be used for this ORES scoring example
#
ARTICLE_REVISIONS = { 'Bison':1085687913 , 'Northern flicker':1086582504 , 'Red squirrel':1083787665 , 'Chinook salmon':1085406228 , 'Horseshoe bat':1060601936 }

#
#    This is a template of the data required as a payload when making a scoring request of the ORES model
#
ORES_REQUEST_DATA_TEMPLATE = {
    "lang":        "en",     # required that its english - we're scoring English Wikipedia revisions
    "rev_id":      "",       # this request requires a revision id
    "features":    True
}

#
#    These are used later - defined here so they, at least, have empty values
#
#
#########
#
#    PROCEDURES/FUNCTIONS
#

def request_pageinfo_per_article(article_title = None, 
                                 endpoint_url = API_ENWIKIPEDIA_ENDPOINT, 
                                 request_template = PAGEINFO_PARAMS_TEMPLATE,
                                 headers = REQUEST_HEADERS):
    
    # article title can be as a parameter to the call or in the request_template
    if article_title:
        request_template['titles'] = article_title

    if not request_template['titles']:
        raise Exception("Must supply an article title to make a pageinfo request.")

    if API_HEADER_AGENT not in headers:
        raise Exception(f"The header data should include a '{API_HEADER_AGENT}' field that contains your UW email address.")

    if 'uwnetid@uw' in headers[API_HEADER_AGENT]:
        raise Exception(f"Use your UW email address in the '{API_HEADER_AGENT}' field.")

    # make the request
    try:
        # we'll wait first, to make sure we don't exceed the limit in the situation where an exception
        # occurs during the request processing - throttling is always a good practice with a free
        # data source like Wikipedia - or any other community sources
        if API_THROTTLE_WAIT > 0.0:
            time.sleep(API_THROTTLE_WAIT)
        response = requests.get(endpoint_url, headers=headers, params=request_template)
        json_response = response.json()
    except Exception as e:
        print(e)
        json_response = None
    return json_response

def request_ores_score_per_article(article_revid = None, email_address=None, access_token=None,
                                   endpoint_url = API_ORES_LIFTWING_ENDPOINT, 
                                   model_name = API_ORES_EN_QUALITY_MODEL, 
                                   request_data = ORES_REQUEST_DATA_TEMPLATE, 
                                   header_format = REQUEST_HEADER_TEMPLATE, 
                                   header_params = REQUEST_HEADER_PARAMS_TEMPLATE):
    
    #    Make sure we have an article revision id, email and token
    #    This approach prioritizes the parameters passed in when making the call
    if article_revid:
        request_data['rev_id'] = article_revid
    if email_address:
        header_params['email_address'] = email_address
    if access_token:
        header_params['access_token'] = access_token
    
    #   Making a request requires a revision id - an email address - and the access token
    if not request_data['rev_id']:
        raise Exception("Must provide an article revision id (rev_id) to score articles")
    if not header_params['email_address']:
        raise Exception("Must provide an 'email_address' value")
    if not header_params['access_token']:
        raise Exception("Must provide an 'access_token' value")
    
    # Create the request URL with the specified model parameter - default is a article quality score request
    request_url = endpoint_url.format(model_name=model_name)
    
    # Create a compliant request header from the template and the supplied parameters
    headers = dict()
    for key in header_format.keys():
        headers[str(key)] = header_format[key].format(**header_params)
    
    # make the request
    try:
        # we'll wait first, to make sure we don't exceed the limit in the situation where an exception
        # occurs during the request processing - throttling is always a good practice with a free data
        # source like ORES - or other community sources
        if API_THROTTLE_WAIT > 0.0:
            time.sleep(API_THROTTLE_WAIT)
        #response = requests.get(request_url, headers=headers)
        response = requests.post(request_url, headers=headers, data=json.dumps(request_data))
        json_response = response.json()
    except Exception as e:
        print(e)
        json_response = None
    return json_response

def get_final_csv():
    # read in poltician names from given CSV file
    politicians = pd.read_csv('Downloads/politicians_by_country_AUG.2024.csv')

    # set up empty dictionary to store article names and quality prediction 
    pred = {}

    # iterate through poltician names needed to make the API call
    for article in politicians.name.to_list():

        #make API request inputing article title (poltician name)
        info = request_pageinfo_per_article(article)

        #get page ID to access last revision ID in dictionary
        page_id = list(info["query"]["pages"].keys())[0]

        #skip articles that do not have revision ID
        if "lastrevid" not in list(info["query"]["pages"][page_id].keys()):
            print("could not find lastrevid for", article)
            continue

        # access revision ID
        rev_id = info["query"]["pages"][page_id]["lastrevid"]

        # make ORES API request using revision ID, email, and access token
        score = request_ores_score_per_article(article_revid= rev_id,
                                        email_address="igokhale@uw.edu",
                                        access_token=ACCESS_TOKEN)
        
        # skip article if score does not exist
        if score is None:
            continue

        #some dictionaries did not contain 'enwiki' key 
        if 'enwiki' not in list(score.keys()):
            print('nothing in score from this', article)
            continue

        #convert revision id from interger to string
        rev_id = str(rev_id)

        # skip article if revision ID is not located
        if rev_id not in list(score['enwiki']['scores'].keys()):
            print("could not find rev id")
            continue

        # access quality prediction score
        quality = score['enwiki']['scores'][rev_id]['articlequality']['score']['prediction']
        
        # save article title as key and quality as value in dictionary
        pred[article] = quality

    # write article and quality prediction to file
    with open('quality_pred.csv', mode='w', newline='') as file:
        print('writing csv')
        writer = csv.writer(file)
        
        # write the header
        writer.writerow(['article', 'quality_pred'])
        
        # write the data
        for key, value in pred.items():
            writer.writerow([key, value])

def main():
    get_final_csv()

if __name__ == "__main__":
    main()