import os
import pathlib
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv

load_dotenv()


def setup_google_login():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" 

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID") 
    client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")  

    flow = Flow.from_client_secrets_file( 
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],  
    redirect_uri="http://127.0.0.1:5000/callback"  
    )   

    return GOOGLE_CLIENT_ID, flow

def input_validation(username, password):
    if username == "" or password == "":
        return False
    elif len(username) < 3 or len(password) < 8:
        return False
    else:
        return True
    
