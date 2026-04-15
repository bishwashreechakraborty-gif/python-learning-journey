from flask import Flask, render_template, request, redirect

app = Flask(__name__)

users = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            return f"Welcome {username}!"
        else:
            return "Invalid credentials"

    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    users[username] = password
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)