import re, json, urllib
import string, random
from datetime import datetime, date
from email.utils import formatdate
from calendar import timegm

class DateJSONEncoder(json.JSONEncoder):
    """ JSON Encoder class to support date and time encoding """
    
    def default(self, obj):
        if isinstance(obj, datetime):
            return formatdate(timegm(obj.utctimetuple()), usegmt=True)

        if isinstance(obj, date):
            _obj = datetime.combine(obj, datetime.min.time())
            return formatdate(timegm(_obj.utctimetuple()), usegmt=True)

        return json.JSONEncoder.default(self, obj)


def code_generator(size=6, chars=string.ascii_letters+string.digits):
    """
    utility function to generate random identification numbers
    """
    return ''.join(random.choice(chars) for x in range(size)).upper()

def populate_object(obj, data):

 	for key, value in data.items():
 		if obj.has_key(key):
 			obj.key = value

 	return obj

def clean_dict(ignored, _dict):

 	for key in ignored:
 		if key in _dict.keys():
 			_dict.pop(key)

 	return _dict

