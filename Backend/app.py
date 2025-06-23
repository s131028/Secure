# backend/app.py
from flask import Flask, request, jsonify
import mysql.connector
import bcrypt

app = Flask(__name__)
conn = mysql.connector.connect(host='DB_IP', user='root', password='pass', database='appdb')
cursor = conn.cursor()

@app.route("/signup", methods=["POST"])
def signup():
    data = request.form
    hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (data['username'], hashed))
    conn.commit()
    return jsonify({"status": "user created"})

@app.route("/signin", methods=["POST"])
def signin():
    data = request.form
    cursor.execute("SELECT password FROM users WHERE username=%s", (data['username'],))
    result = cursor.fetchone()
    if result and bcrypt.checkpw(data['password'].encode(), result[0].encode()):
        return jsonify({"status": "login successful"})
    return jsonify({"status": "failed"})
