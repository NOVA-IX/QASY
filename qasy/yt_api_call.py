import googleapiclient.discovery
import googleapiclient.errors

import os
from dotenv import load_dotenv

load_dotenv()

api_service_name = os.getenv("API_SERVICE_NAME")
api_version = os.getenv("API_VERSION")
client_secrets_file = os.getenv("YOUTUBE_API_KEY")


def ytApi(query):
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=client_secrets_file)

    request = youtube.search().list(
        part="snippet",
        maxResults=5,
        order="viewCount",
        q=query
    )
    response = request.execute()

    return response
