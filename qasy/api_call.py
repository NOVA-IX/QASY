"""
Example presents error handling for submissions.create() API method
"""
import json
from sphere_engine import CompilersClientV4
from sphere_engine.exceptions import SphereEngineException
import time
from urllib.request import urlopen

# define access parameters
with open('creds.json', 'r') as f:
    creds = json.load(f)

accessToken = creds['accessToken']
endpoint = creds['endpoint']


# initialization
client = CompilersClientV4(accessToken, endpoint)


def runAPI(source, compiler):
    try:
        submission_id = client.submissions.create(source, compiler)
        time.sleep(5)
        response = client.submissions.get(submission_id['id'])
        # print(response)
        if response['result']['streams']['error']:
            url = response['result']['streams']['error']['uri']
            file = urlopen(url)
            decoded_line = ""
            for line in file:
                decoded_line += line.decode("utf-8")
            return decoded_line, 1
        elif response['result']['streams']['output']:
            url = response['result']['streams']['output']['uri']
            file = urlopen(url)
            decoded_line = ""
            for line in file:
                decoded_line += line.decode("utf-8")
            return decoded_line, 2
        elif response['result']['streams']['cmpinfo']:
            url = response['result']['streams']['cmpinfo']['uri']
            file = urlopen(url)
            decoded_line = ""
            for line in file:
                decoded_line += line.decode("utf-8")
            return decoded_line, 1
    except SphereEngineException as e:
        if e.code == 401:
            print('Invalid access token')
        elif e.code == 402:
            print('Unable to create submission')
        elif e.code == 400:
            print('Error code: ' + str(e.error_code) +
                  ', details available in the message: ' + str(e))
