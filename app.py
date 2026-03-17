from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Create database and table
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS searches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT,
        result TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# Rule-based AI detection
def detect_scam(number):

    if number.startswith("+92"):
        return "Scam"

    elif number.startswith("+234"):
        return "Suspicious"

    elif len(number) < 10:
        return "Invalid Number"

    else:
        return "Safe"


@app.route("/", methods=["GET","POST"])
def index():

    result = None

    if request.method == "POST":
        number = request.form["number"]

        result = detect_scam(number)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
        "INSERT INTO searches (phone,result) VALUES (?,?)",
        (number,result)
        )

        conn.commit()
        conn.close()

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
    "SELECT phone,result FROM searches ORDER BY id DESC LIMIT 5"
    )

    history = cursor.fetchall()
    conn.close()

    return render_template("index.html", result=result, history=history)


if __name__ == "__main__":
    app.run(debug=True)