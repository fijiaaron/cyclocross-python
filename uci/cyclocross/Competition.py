import json
import re

class Competition():

	def __init__(self, name=None, type=None, dates=None, _class=None, venue=None, country=None, url=None, id=None, season=None):
		self.competition_name = name
		self.competition_type = type
		self.competition_dates = dates
		self.competition_class = _class
		self.competition_venue = venue
		self.competition_country = country
		self.competition_url =  url
		self.competition_id = id
		self.competition_season = season

	def to_json(self):
		return json.dumps(self.__dict__)

	def from_json(self):
		json.loads

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
