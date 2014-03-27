from flask import jsonify, json
import hashlib
from google.appengine.ext import ndb
import logging

class Profile(ndb.Model):
    id = ndb.StringProperty()
    name = ndb.StringProperty()
    description = ndb.StringProperty()
    create_date = ndb.DateTimeProperty(auto_now_add=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
    

def validate_profile(profile):
    """
    Validate the JSON profile above
    
    """
    if 'name' in profile and 'description' in profile:
        return True
    else:
        return False
        
        
def save_profile(profile):
    """
    Save the profile
    
    Return the unique id
    """
    # SHA-2 the jsonify'd profile
    id = hashlib.sha256(json.dumps(profile)).hexdigest()
    
    profile_store = Profile(id=id, name=profile['name'], description=profile['description'])
    profile_store.put()
    
    return id
    
    
def get_profile(profileId):
    """
    Get the profile specified in profileId
    
    """
    # profile_key = ndb.Key("Profile", profileId)
    profiles = Profile.query(Profile.id == profileId).order(-Profile.create_date).fetch(1)
    logging.info("Received: %s" % profiles)
    if len(profiles) > 0:
        logging.info("Received: %s" % str(profiles[0].create_date))
        return profiles[0].to_dict()
    else:
        return {}
        
        
        
