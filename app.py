from flask import Flask, request, render_template, redirect, url_for
import dao


app = Flask(__name__)


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
        
        user_details = dao.fetch_user_by_username(username)

        if user_details:
            if user_details[2] == password:
                return redirect(url_for('content'))
            else:
                login_error = "Incorrect Password"
                return render_template("login.html", error = login_error)

    return render_template("login.html")

@app.route("/content", methods = ["GET"])
def content():
    return render_template("content.html")


app.run(debug=True)