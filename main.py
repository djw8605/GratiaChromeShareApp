"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask
from flask import request, abort, jsonify

from profile import validate_profile, save_profile, get_profile

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

test_profile = {
    "name": "Test Profile",
    "id": "testid"
}


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route('/api/profile', methods = ['PUT'])
def putProfile():
    """
    Save the profile.
    
    Returns: URL to retrieve the profile
    """
    # First, validate the json of the data
    if not request.json:
        abort(404)
        
    if validate_profile(request.json):
        id = save_profile(request.json)
        return_dict = { "id": id, "url": "%s/%s" % (request.url, id) }
        return jsonify( return_dict )
    else:
        abort(500)
    
    

@app.route('/api/profile/<profileId>', methods = ['GET'])
def getProfile(profileId):
    """
    Get the profile JSON
    
    Returns: Profile JSON
    """
    if profileId == "test":
        return jsonify( test_profile )
    else:
        return jsonify( get_profile(profileId) )
    


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
