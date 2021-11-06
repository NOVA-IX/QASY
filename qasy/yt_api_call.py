import googleapiclient.discovery
import googleapiclient.errors
import json

with open('creds.json', 'r') as f:
    creds = json.load(f)

api_service_name = creds['api_service_name']
api_version = creds['api_version']
client_secrets_file = creds['youtube_api_key']


def ytApi(query):
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=client_secrets_file)

    request = youtube.search().list(
        part="snippet",
        maxResults=2,
        order="viewCount",
        q=query
    )
    response = request.execute()

    return response
