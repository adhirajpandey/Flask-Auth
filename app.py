from flask import Flask, request, render_template, redirect, url_for, session
import dao
import os


app = Flask(__name__)
app.secret_key = os.urandom(12)


@app.route("/", methods = ["GET"])
@app.route("/index", methods = ["GET"])
def index():
    return render_template("index.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if dao.check_if_username_exists(username):
            register_error = "Username already exists"
            return render_template("register.html", error = register_error)
        else:
            dao.insert_username_password_admin(username, password, False)

        return redirect(url_for('index'))

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
            if user_details[2] == password:
                session['username'] = username
                return redirect(url_for('content'))
            else:
                login_error = "Incorrect Password"  
                return render_template("login.html", error = login_error)

    return render_template("login.html")

@app.route("/content", methods = ["GET"])
def content():
    if 'username' in session:
        return render_template("content.html", username = session['username'])
    else:
        return redirect(url_for('login'))

@app.route("/logout", methods = ["GET"])
def logout():
    if 'username' in session:
        session.pop('username', None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('index'))

app.run(debug=True)