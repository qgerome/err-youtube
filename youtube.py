# This is a Youtube for Err plugins, use this to get started quickly.
import random

from errbot import BotPlugin, botcmd, utils
from client import YoutubeClient
import logging


class Youtube(BotPlugin):
	"""An Err plugin Youtube"""
	def __init__(self):
		super(Youtube, self).__init__()

	def configure(self, configuration):
		super(Youtube, self).configure(configuration)
		if self.config and self.config.get('YOUTUBE_API_KEY'):
			self.set_client(self.config.get('YOUTUBE_API_KEY'))

	def set_client(self, api_key):
		self.client = YoutubeClient(api_key)

	def get_configuration_template(self):
		"""Defines the configuration structure this plugin supports

		You should delete it if your plugin doesn't use any configuration like this"""
		return {'YOUTUBE_API_KEY': u''}

	def check_configuration(self, configuration):
		"""Triggers when the configuration is checked, shortly before activation

		You should delete it if you're not using it to override any default behaviour"""
		super(Youtube, self).check_configuration(configuration)
		if not configuration.get('YOUTUBE_API_KEY'):
			raise utils.ValidationException("'YOUTUBE_API_KEY' is needed")
		self.set_client(configuration.get('YOUTUBE_API_KEY'))

	def get_random_video(self, query):
		return random.choice(self.client.search(query))

	@botcmd(split_args_with=':', template='video')
	def youtube(self, mess, args):
		"""A command which simply returns 'Example'"""
		if not self.config.get('YOUTUBE_API_KEY'):
			return "Seriously ? Am I supposed to guess your api key ?"
		if not args:
			return 'Am I supposed to guess the video you want ?...'
		video = self.get_random_video(args[0])
		logging.debug(video)
		return video

	@botcmd(split_args_with=':', template='video')
	def yt(self, mess, args):
		return self.youtube(mess, args)
