import os
import pathlib
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

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
    
def setup_http_auth_users():
    users = {
    os.getenv("HTTP_AUTH_USER") : os.getenv("HTTP_AUTH_PASS")
    }
    return users

@auth.verify_password
def verify_password(username, password):
    users = setup_http_auth_users()
    if username in users and password == users[username]:
        return username
    

def get_db_choice():
    db_choice = os.getenv("DB_CHOICE")
    return db_choice