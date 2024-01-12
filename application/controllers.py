from flask import current_app as app, request, render_template, redirect, url_for, session, abort, Request, redirect, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import application.helper as helper
import os
import application.sqlite_dao as dao

from google.oauth2 import id_token
from google.auth.transport.requests import Request as google_request

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


GOOGLE_CLIENT_ID, flow = helper.setup_google_login()

# Setup the Flask-JWT-Extended
app.config["JWT_SECRET_KEY"] = os.urandom(12)
jwt = JWTManager(app)


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
                session['admin'] = user_details[3]
                return redirect(url_for('restricted_content1'))
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

@app.route("/content1", methods = ["GET"])
def content1():
    return render_template("content1.html")

@app.route("/content2", methods = ["GET"])
def content2():
    return render_template("content2.html")

@app.route("/content3", methods = ["GET"])
def content3():
    return render_template("content3.html")

@app.route("/restricted_content3", methods = ["GET"])
def restricted_content3():
    if 'username' in session and session['admin'] == 1:
        return render_template("restricted_content3.html", usersdata = dao.fetch_all_users())
    else:
        return redirect(url_for('login'))
        

@app.route("/restricted_content2", methods = ["GET"])
@helper.auth.login_required
def restricted_content2():
    return render_template("restricted_content2.html")
    
# Google Login  
def login_is_required(function): 
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()

    return wrapper

@login_is_required    
@app.route("/restricted_content1", methods = ["GET"])
def restricted_content1():
    if 'username' in session:
        return render_template("restricted_content1.html", username = session['username'])
    else:
        return redirect(url_for('login'))

@app.route("/google_login", methods = ["GET", "POST"])
def google_login():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

@app.route("/callback", methods = ["GET", "POST"])
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials

    # Use the access token to verify the ID token
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=google_request(),
        audience=GOOGLE_CLIENT_ID
    )

    # Store user information in the session
    session["google_id"] = id_info.get("sub") 
    session["username"] = id_info.get("name")
    session["email"] = id_info.get("email")

    return redirect("/restricted_content1")


@app.route("/delete_user", methods = ["POST"])
def delete_user():
    if 'username' in session and session['admin'] == 1:
        username = request.form.get('username')
        dao.delete_user(username)
        return redirect(url_for('restricted_content3'))
    else:
        return redirect(url_for('login'))
    
@app.route("/escalate_user", methods = ["POST"])
def escalate_user():
    if 'username' in session and session['admin'] == 1:
        username = request.form.get('username')
        dao.escalate_user(username)
        return redirect(url_for('restricted_content3'))
    else:
        return redirect(url_for('login'))
    

@app.route("/jwt_token", methods = ["POST"])
def hello():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = {"id": 1, "username": "test", "password": "test1"}

    if username != user["username"] or password != user["password"]:
        # The user entered bad credentials
        return jsonify({"msg": "Bad username or password"}), 401
    
    # Create a new token with the user id inside
    access_token = create_access_token(identity=user['id'])
    return jsonify({ "token": access_token, "user_id": user['id'] })


# Protect a route with jwt_required, which will kick out requests without a valid JWT
@app.route("/jwt_protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user_id = get_jwt_identity()
    print(current_user_id)
    users = [{"id": 1, "username": "test1", "password": "pass1", "protected_data": "This is protected"},
                {"id": 2, "username": "test2", "password": "pass2", "protected_data": "This is also protected"}]
    
    for user in users:
        if user["id"] == current_user_id:
            return jsonify({"protected_data": user["protected_data"]})
        else:
            return jsonify({"msg": "Not found"}), 404

if __name__ == "__main__":

    
    
    app.run(debug=True)