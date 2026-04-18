import requests
from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask application
app = Flask(__name__)
app.secret_key = "myproject_super_secret_2026"

# API key for weather service
API_KEY = "22b8becea516f2bef7c4cb10a4e200d9"


# -----------------------------
# Function: get_weather
# Description: Fetch weather data from API
# -----------------------------
def get_weather(city):
    """
    Fetch weather data based on city name.
    Returns temperature and weather description.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()

    # Check if response contains valid weather data
    if data.get("main"):
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"{city}: {temp}°C, {desc}"
    else:
        return "City not found"


# -----------------------------
# Function: init_db
# Description: Initialize database and create table
# -----------------------------
def init_db():
    """
    Create SQLite database and 'logs' table if it does not exist.
    """
    conn = sqlite3.connect("data.db")
    
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,         
        password TEXT
                                    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        city TEXT,
        weather TEXT,
        spending INTEGER,
        mood TEXT)
    """)
    conn.close()


# Initialize database on app startup
init_db()


# -----------------------------
# Function: get_logs
# Description: Retrieve stored records from database
# -----------------------------
def get_logs(user_id):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT city, spending FROM logs WHERE user_id=?",
        (user_id,)
    )

    data = cursor.fetchall()
    conn.close()
    return data


# -----------------------------
# Function: generate_advice
# Description: Generate rule-based suggestions
# -----------------------------
def generate_advice(spending, weather):
    """
    Generate simple advice based on spending amount and weather condition.
    """
    if int(spending) > 100 and "rain" in weather.lower():
        return "You spent a lot and it's rainy - stay at home and save money!"
    elif int(spending) < 50:
        return "Good job! You're saving money!"
    else:
        return "Your spending is normal."


# -----------------------------
# Route: Home Page
# Description: Handle user input and main logic
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    """
    Handle user input, fetch weather, store data,
    and generate advice for display.
    """
    if "user_id" not in session:
        return redirect("/login")
    
    weather = ""
    advice = ""

    if request.method == "POST":
        # Get user input from form
        city = request.form.get("city")
        spending = request.form.get("spending")
        mood = request.form.get("mood")

        # Handle empty spending input
        if not spending:
            spending = 0

        # Fetch weather data
        weather = get_weather(city)

        # Store data in database
        conn = sqlite3.connect("data.db")
        user_id = session["user_id"]
        conn.execute(
            "INSERT INTO logs (user_id, city, weather, spending, mood) VALUES (?, ?, ?, ?, ?)",
            (user_id, city, weather, spending, mood)
        )
        conn.commit()
        conn.close()

        # Generate advice based on input
        advice = generate_advice(spending, weather)

    # Retrieve history logs for display
    logs = get_logs(session["user_id"])

    return render_template(
    "index.html",
    weather=weather,
    advice=advice,
    logs=logs,
    username=session.get("username")
    )

@app.route("/login", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("login.html", message="Please fill all fields")

        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, password FROM users WHERE username=?",
            (username,)
        )

        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            session["username"] = username
            return redirect("/")

        return render_template("login.html", message="Invalid username or password")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("register.html", message="Please fill all fields")

        hashed = generate_password_hash(password)

        conn = sqlite3.connect("data.db")

        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed)
            )
            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            return render_template("register.html", message="Username already exists")

        conn.close()
        return redirect("/login")

    return render_template("register.html")
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)