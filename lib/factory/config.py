
from ..config.database import DatabaseConfig

class ConfigFactory:
	DATABASE = 1

	@classmethod
	def get_config(self, config_name=None):
		""" Exceptions: 
			- AssertionError
		"""
		assert config_name is not None, "config_name is not defined."

		if config_name == ConfigFactory.DATABASE:
			return DatabaseConfig()