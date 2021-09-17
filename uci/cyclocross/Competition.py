import json
import re

class Competition():

	def __init__(self, name=None, discipline=None, dates=None, _class=None, venue=None, country=None, season=None, url=None, id=None,):
		self.name = name
		self.discipline = type
		self.dates = dates
		self.competition_class = _class
		self.venue = venue
		self.country = country
		self.season = season
		self.url =  url
		self.id = id

		if url and not id:
			self.id = self.id_from_url(url)
		
	def to_json(self):
		return json.dumps(self.__dict__)

	@staticmethod
	def from_json(self, competition_json):
		competition_dict = json.loads(competition_json)
		return Competition

	@staticmethod
	def url_from_id(id):
		return f"https://dataride.uci.org/iframe/CompetitionResults/{id}/3/"

	@staticmethod
	def id_from_url(url):
		match = re.search("^http.*/CompetitionResults/(\d+)/.*$", url)

		if match and match.groups() and len(match.groups()) == 1:
			return match.groups()[0]
		else:
			raise Exception("URL does not look like CompetitionResults")
