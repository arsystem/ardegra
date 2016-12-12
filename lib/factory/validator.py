from ..validator.database_config import DatabaseConfigValidator

class ValidatorFactory:
	DATABASE_CONFIG = 1

	@classmethod
	def get_validator(self, validator_name=None):
		""" Exceptions: 
			- AssertionError
		"""
		assert validator_name is not None, "validator_name is not defined."

		if validator_name == ValidatorFactory.DATABASE_CONFIG:
			return DatabaseConfigValidator()