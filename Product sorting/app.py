from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For session management

# Database connection helper
def get_db_connection():
    connection = sqlite3.connect("users.db")
    connection.row_factory = sqlite3.Row
    return connection

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Verify user credentials
        connection = get_db_connection()
        user = connection.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        connection.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("index"))
        else:
            return "Invalid username or password!", 401

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        try:
            connection = get_db_connection()
            connection.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            connection.commit()
            connection.close()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return "Username already exists!", 400

    return render_template("register.html")

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return f"Welcome, {session['username']}! <a href='/logout'>Logout</a>"
