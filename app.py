import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")
DB_PATH = os.environ.get("DB_PATH", "patient_records.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT
            )"""
        )


@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    with get_db() as conn:
        if q:
            rows = conn.execute(
                "SELECT * FROM patients WHERE name LIKE ? OR phone LIKE ? ORDER BY id DESC",
                (f"%{q}%", f"%{q}%"),
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM patients ORDER BY id DESC").fetchall()
    return render_template("index.html", patients=rows, q=q)


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", "").strip()
    age = request.form.get("age", "").strip()
    gender = request.form.get("gender", "").strip()
    phone = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()

    if not (name and age.isdigit() and gender and phone):
        flash("Please fill all required fields correctly.", "error")
        return redirect(url_for("index"))

    with get_db() as conn:
        conn.execute(
            "INSERT INTO patients (name, age, gender, phone, address) VALUES (?, ?, ?, ?, ?)",
            (name, int(age), gender, phone, address),
        )
    flash("Patient registered successfully.", "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:patient_id>", methods=["POST"])
def delete(patient_id):
    with get_db() as conn:
        conn.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    flash("Patient record deleted.", "success")
    return redirect(url_for("index"))


@app.route("/health")
def health():
    return {"status": "ok"}, 200


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
