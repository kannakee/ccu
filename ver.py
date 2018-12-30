import requests, logging, json, sys
from http_calls import EdgeGridHttpCaller
from akamai.edgegrid import EdgeGridAuth
from config import EdgeGridConfig

if sys.version_info[0] >= 3:
     # python3
     from urllib import parse
else:
     # python2.7
     import urlparse as parse

# Establish an HTTP session
session = requests.Session()

# Load the .edgerc credentials file
section_name = "default"
config = EdgeGridConfig({},section_name)

# Set up verbose output and debugging
if hasattr(config, "debug") and config.debug:
  debug = True
else:
        debug = False

if hasattr(config, "verbose") and config.verbose:
  verbose = True
else:
        verbose = False

# Set the EdgeGrid credentials
session.auth = EdgeGridAuth(
            client_token=config.client_token,
            client_secret=config.client_secret,
            access_token=config.access_token
)

# If include any special headers (used for debugging)
if hasattr(config, 'headers'):
  session.headers.update(config.headers)

# Set up the base URL
baseurl = '%s://%s/' % ('https', config.host)
httpCaller = EdgeGridHttpCaller(session, debug, verbose, baseurl)

# main code
if __name__ == "__main__":
        # Request the entitlement scope for the credentials
        credential_scope = httpCaller.getResult('/-/client-api/active-grants/implicit')

        if verbose: print (json.dumps(credential_scope, indent=2))

        print ("Credential Name: %s" % credential_scope['name'])
        print ("---")
        print ("Created: %s by %s" % (credential_scope['created'], credential_scope['createdBy']))
        print ("Updated: %s by %s" % (credential_scope['updated'], credential_scope['updatedBy']))
        print ("Activated: %s by %s" % (credential_scope['activated'], credential_scope['activatedBy']))
        print ("---")

        for scope in credential_scope['scope'].split(" "):
                o = parse.urlparse(scope)
                apis = o.path.split("/")
                print ('{0:35} {1:10}'.format(apis[3], apis[5]))

