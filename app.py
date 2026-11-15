"""Nishtha Shankar - Portfolio website (Flask backend).

Backend features (Python):
  1. Contact form  -> validated server-side and saved to SQLite
  2. Visitor counter -> counts unique visitors per browser session
  3. Admin view of messages -> /admin/messages?key=YOUR_ADMIN_KEY
"""
import os
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, g, jsonify, render_template, request, session

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = os.environ.get("DB_PATH", str(BASE_DIR / "portfolio.db"))

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-me-in-production")

# Hackathon certificates. Drop an image with the matching filename into
# static/img/certs/ and it appears automatically (until then a placeholder shows).
CERTIFICATES = [
    {
        "title": "Smart India Hackathon 2026",
        "subtitle": "Internal Hackathon · JAIN (Deemed-to-be University)",
        "date": "11 – 12 September 2026",
        "file": "sih-2026.jpg",
    },
    {
        "title": "Manipal 2026 Hackathon",
        "subtitle": "Certificate of Participation",
        "date": "2026",
        "file": "manipal-2026.jpg",
    },
    {
        "title": "Smart India Hackathon 2025",
        "subtitle": "24 hrs Internal Hackathon · JAIN (Deemed-to-be University)",
        "date": "12 – 13 September 2025",
        "file": "sih-2025.jpg",
    },
    {
        "title": "Inceptrix 2025 Hackathon",
        "subtitle": "Certificate of Participation",
        "date": "2025",
        "file": "inceptrix-2025.jpg",
    },
]


# ---------- database ----------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS counter (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                visits INTEGER NOT NULL
            );
            INSERT OR IGNORE INTO counter (id, visits) VALUES (1, 0);
            """
        )


init_db()

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def cert_list():
    out = []
    for c in CERTIFICATES:
        exists = (BASE_DIR / "static" / "img" / "certs" / c["file"]).exists()
        out.append({**c, "exists": exists})
    return out


# ---------- routes ----------
@app.route("/")
def index():
    db = get_db()
    # count each browser session once
    if not session.get("counted"):
        db.execute("UPDATE counter SET visits = visits + 1 WHERE id = 1")
        db.commit()
        session["counted"] = True
    visits = db.execute("SELECT visits FROM counter WHERE id = 1").fetchone()["visits"]
    return render_template("index.html", visits=visits, certificates=cert_list())


@app.post("/contact")
def contact():
    data = request.get_json(silent=True) or request.form
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    errors = {}
    if not 2 <= len(name) <= 80:
        errors["name"] = "Please enter your name."
    if not EMAIL_RE.match(email) or len(email) > 120:
        errors["email"] = "Please enter a valid email."
    if not 5 <= len(message) <= 2000:
        errors["message"] = "Message should be 5–2000 characters."
    if errors:
        return jsonify(ok=False, errors=errors), 400

    db = get_db()
    db.execute(
        "INSERT INTO messages (name, email, message, created_at) VALUES (?, ?, ?, ?)",
        (name, email, message, datetime.now(timezone.utc).isoformat(timespec="seconds")),
    )
    db.commit()
    return jsonify(ok=True, message=f"Thank you, {name.split()[0]}! Your message has been received.")


@app.get("/admin/messages")
def admin_messages():
    key = os.environ.get("ADMIN_KEY")
    if not key or request.args.get("key") != key:
        return jsonify(error="Not authorised"), 403
    rows = get_db().execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
