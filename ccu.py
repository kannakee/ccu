#!/bin/bash
import requests, logging, json, sys
from http_calls import EdgeGridHttpCaller
from random import randint
from akamai.edgegrid import EdgeGridAuth
from config import EdgeGridConfig
import urllib
import os
session = requests.Session()
debug = False
verbose = False
section_name = "ccu"
url=raw_input("Enter the url")
if sys.version_info[0] >= 3:
     # python3
     from urllib import parse
else:
     # python2.7
     import urlparse as parse


# If all parameters are set already, use them.  Otherwise
# use the config
config = EdgeGridConfig({"verbose":False},section_name)

if hasattr(config, "debug") and config.debug:
        debug = True

if hasattr(config, "verbose") and config.verbose:
        verbose = True


# Set the config options
session.auth = EdgeGridAuth(
            client_token=config.client_token,
            client_secret=config.client_secret,
            access_token=config.access_token
)

if hasattr(config, 'headers'):
        session.headers.update(config.headers)

baseurl = '%s://%s/' % ('https', config.host)
httpCaller = EdgeGridHttpCaller(session, debug, verbose, baseurl)

def postPurgeRequest(action = "invalidate"):

        purge_obj = {
                        "objects" : [
                                url
                        ]
                    }
        print ("Adding %s request to queue - %s" % (action, json.dumps(purge_obj)));
        purge_post_result = httpCaller.postResult('/ccu/v3/invalidate/url', json.dumps(purge_obj))
        return purge_post_result

if __name__ == "__main__":
        purge_post_result = postPurgeRequest()

