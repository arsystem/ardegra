class DuplicateDocument(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class CannotFindField(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class ValidationError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)