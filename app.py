from flask import Flask, request, render_template, redirect, url_for, session, abort, Request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import dao
import helper
import os
import requests

import os
import pathlib
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from google.auth.transport.requests import Request


app = Flask(__name__)
app.secret_key = os.urandom(12)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" 

GOOGLE_CLIENT_ID = ""  
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")  

flow = Flow.from_client_secrets_file( 
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],  
    redirect_uri="http://127.0.0.1:5000/callback"  
)

def login_is_required(function): 
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()

    return wrapper

@app.route("/", methods = ["GET"])
@app.route("/index", methods = ["GET"])
def index():
    return render_template("index.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if not helper.input_validation(username, password):
            register_error = "Invalid Input Values, Try Again !"
            return render_template("register.html", error = register_error)

        hashed_password = generate_password_hash(password)

        if dao.check_if_username_exists(username):
            register_error = "Username already exists"
            return render_template("register.html", error = register_error)
        else:
            dao.insert_username_password_admin(username, hashed_password, False)

        return redirect(url_for('login'))

    return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not dao.check_if_username_exists(username):
            login_error = "Username does not exist"
            return render_template("login.html", error = login_error)

        user_details = dao.fetch_user_by_username(username)

        if user_details:
            if check_password_hash(user_details[2], password):
                session['username'] = username
                return redirect(url_for('restricted_content'))
            else:
                login_error = "Incorrect Username/Password"  
                return render_template("login.html", error = login_error)

    return render_template("login.html")

@app.route("/logout", methods = ["GET"])
def logout():
    if 'username' in session:
        session.pop('username', None)
        session.clear()
        return redirect(url_for('login'))
    else:
        return redirect(url_for('index'))

@login_is_required    
@app.route("/restricted_content", methods = ["GET"])
def restricted_content():
    if 'username' in session:
        return render_template("restricted_content.html", username = session['username'])
    else:
        return redirect(url_for('login'))

@app.route("/content1", methods = ["GET"])
def content1():
    return render_template("content1.html")

@app.route("/content2", methods = ["GET"])
def content2():
    return render_template("content2.html")

@app.route("/content3", methods = ["GET"])
def content3():
    return render_template("content3.html")

@app.route("/google_login", methods = ["GET", "POST"])
def google_login():
        authorization_url, state = flow.authorization_url()
        session['state'] = state
        return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  #state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub") 
    session["username"] = id_info.get("name")
    session["email"] = id_info.get("email")

    return redirect("/restricted_content")


app.run(debug=True)