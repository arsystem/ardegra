class Post:
	def __init__(self, **kwargs):
		self.category       = kwargs.get("category",None)
		self.thread   	    = kwargs.get("thread",None)
		self.permalink 	    = kwargs.get("permalink",None)
		self.author_name    = kwargs.get("author_name",None)
		self.content        = kwargs.get("content",None)
		self.title  		= kwargs.get("title",None)
		self.country 	    = kwargs.get("country",None)
		self.crawler 	    = kwargs.get("crawler",None)
		self.published_date = kwargs.get("published_date",None)
		self._insert_time   = kwargs.get("_insert_time",None)

	def to_dict(self):
		return {
			"category": self.category,
			"thread": self. thread,
			"permalink": self.permalink,
			"author_name": self.author_name,
			"content": self.content,
			"title": self.title,
			"country": self.country,
			"crawler": self.crawler,
			"published_date": self.published_date,
			"_insert_time": self._insert_time
		}