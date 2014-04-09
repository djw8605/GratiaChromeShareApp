from flask import jsonify, json, request
import re
import urlparse
import logging

# Include any style sheet that we need here
embed_intro = """
document.write('<link rel="stylesheet" href="%(url)s/assets/embed.css">');
document.write(' """

# End the embed
embed_end = """');
"""

def create_html(imageURL, name, description):
    html = """
    <div class="osg-usage-graphs-container">
    <div class="osg-usage-graphs-image">%(imageTag)s</div>
    <div class="osg-usage-graphs-content">
    <div class="osg-usage-graphs-title">
    <h2>%(name)s</h2>
    </div>
    <p>%(description)s</p>
    </div>
    </div>
    """ % ({'imageTag': write_img_tags(imageURL), 'name': name, 'description': description})
    return html

def write_img_tags(imageURL):
    return "<img src=\"%s\"></img>" % imageURL

def convertParams(param):
    return re.sub(r"\s*,\s*", "\|", param)

def create_embed(profile):
    # Get the url for the embed.css
    url_split = urlparse.urlparse(request.url)
    url = "%s://%s" % ( url_split.scheme, url_split.netloc )
    
    total_html = []
    # 1. Read in the profile's graphs
    profile_object = json.loads(profile['profile_json'])
    if profile_object.has_key('graphs'):
        for key in profile_object['graphs']:
            # Create the query params
            params = '&'.join([ "%s=%s" % ( param_key, convertParams(param) ) for param_key, param in profile_object['graphs'][key]['queryParams'].iteritems() ])
            imageURL = "?".join([profile_object['graphs'][key]['baseUrl'], params])
            total_html.append(create_html(imageURL, profile_object['graphs'][key]['name'], profile_object['graphs'][key]['description']))
            
    
    # 3. Write out the image tags
    generated_html = ''.join(total_html)
    
    return embed_intro % {'url': url} + generated_html.replace("\n", "") + embed_end
    
    



