from flask import Flask, request, render_template, redirect, url_for


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

        print(username, password)

        return redirect(url_for('index'))

    return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        print(username, password)
        return redirect(url_for('content'))

    return render_template("login.html")

@app.route("/content", methods = ["GET"])
def content():
    return render_template("content.html")


app.run(debug=True)