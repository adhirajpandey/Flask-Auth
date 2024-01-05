# import os
# import pathlib
# import requests
# from google.oauth2 import id_token
# from google_auth_oauthlib.flow import Flow
# from pip._vendor import cachecontrol
# from google.auth.transport.requests import Request

# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" 

# GOOGLE_CLIENT_ID = "583370945885-0udqcendh19un4peg4v4fje1qoo2hopl.apps.googleusercontent.com"  #enter your client id you got from Google console
# client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")  #set the path to where the .json file you got Google console is

# flow = Flow.from_client_secrets_file(  #Flow is OAuth 2.0 a class that stores all the information on how we want to authorize our users
#     client_secrets_file=client_secrets_file,
#     scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],  #here we are specifing what do we get after the authorization
#     redirect_uri="http://127.0.0.1:5000/callback"  #and the redirect URI is the point where the user will end up after the authorization
# )

# credentials = flow.credentials
# request_session = requests.session()
# cached_session = cachecontrol.CacheControl(request_session)
# token_request = Request(session=cached_session)

# id_info = id_token.verify_oauth2_token(
#     id_token=credentials._id_token,
#     request=token_request,
#     audience=GOOGLE_CLIENT_ID
# )

def input_validation(username, password):
    if username == "" or password == "":
        return False
    elif len(username) < 3 or len(password) < 8:
        return False
    else:
        return True
    
