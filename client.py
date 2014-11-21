from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import logging


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "REPLACE_ME"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

get_video_url = "https://www.youtube.com?v={0}".format


def extract_video(video):
	videoId = video['id']['videoId']
	return {
		'id': videoId,
	    'title': video['snippet']['title'],
	    'description' : video['snippet']['description'],
	    'video_url': get_video_url(videoId),
	    'thumbnails': video['snippet']['thumbnails']
	}


class YoutubeClient(object):
	def __init__(self, dev_key):
		self.dev_key = dev_key
		self.youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=dev_key)

	def search(self, q, type="video", location=None, location_radius=None, part="id,snippet", max_results=30):
		videos = self.youtube.search().list(
			q=q,
			type=type,
			location=location,
			locationRadius=location_radius,
			part=part,
			maxResults=max_results
		).execute()

		return [extract_video(x) for x in videos['items']]