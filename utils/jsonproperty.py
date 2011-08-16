import json
from google.appengine.ext import db

class JSONProperty(db.TextProperty):
	def validate(self, value):
		return value
		
	def get_value_for_datastore(self, model_instance):
		result = super(JSONProperty, self).get_value_for_datastore(model_instance)
		result = json.dumps(result)
		return db.Text(result)
		
	def make_value_from_datastore(self, value):
		try:
			value = json.loads(str(value))
		except:
			pass
		return super(JSONProperty, self).make_value_from_datastore(value)