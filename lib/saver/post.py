from ..factory.config import ConfigFactory
from ..exceptions 	  import DuplicateDocument
from urllib.parse 	  import quote_plus
import arrow
import pymongo

class PostSaver:
	def save(self, post=None):
		""" Exceptions:
			- AssertionError
		"""
		assert post is not None, "post is not defined."

		config = ConfigFactory.get_config(ConfigFactory.DATABASE)
		config = config.get("azure-document-db")

		conn = pymongo.MongoClient(config["connectionString"])
		db   = conn[config["database"]]
		db[config["collection"]].create_index("permalink", background=True)

		if db[config["collection"]].count({"permalink": post.permalink}) > 0:
			raise DuplicateDocument("Ops! Duplicate document!")
		db[config["collection"]].insert(post.to_dict())
		conn.close()