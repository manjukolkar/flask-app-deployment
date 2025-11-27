from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2, os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # You can make this an env variable later

# DB credentials from environment
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "demo")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/")
def index():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY, name TEXT)")
        conn.commit()
        cur.execute("SELECT id, name FROM users ORDER BY id DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("index.html", rows=rows)
    except Exception as e:
        return render_template("error.html", message=str(e))

@app.route("/add", methods=["POST"])
def add_user():
    name = request.form.get("name")
    if not name:
        flash("Name cannot be empty", "danger")
        return redirect(url_for("index"))
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users(name) VALUES (%s)", (name,))
        conn.commit()
        cur.close()
        conn.close()
        flash("User added successfully!", "success")
    except Exception as e:
        flash(f"Database error: {str(e)}", "danger")
    return redirect(url_for("index"))

@app.route("/healthz")
def healthz():
    try:
        conn = get_connection()
        conn.close()
        return "ok", 200
    except Exception:
        return "db-error", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
