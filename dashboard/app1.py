from flask import Flask, render_template, request, send_file, redirect, url_for, session
import os
from datetime import datetime
from collections import Counter
import io

app = Flask(__name__)
app.secret_key = "supersecretkey"
LOG_PATH = "../logs/honeypot.log"

# --- Dummy Login System ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- Main Dashboard ---
@app.route("/", methods=["GET"])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    event_type = request.args.get("type")
    logs = []
    event_counts = Counter()

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            all_logs = f.readlines()

        for line in reversed(all_logs):
            try:
                log_date_str = line[:10]  # e.g., '2025-06-17'
                log_date = datetime.strptime(log_date_str, "%Y-%m-%d")
            except ValueError:
                continue

            # Apply date range filters
            if start_date and log_date < datetime.strptime(start_date, "%Y-%m-%d"):
                continue
            if end_date and log_date > datetime.strptime(end_date, "%Y-%m-%d"):
                continue

            # Apply event type filter
            if event_type and event_type.lower() not in line.lower():
                continue

            logs.append(line)

            # Count event types
            if "SSH" in line:
                event_counts["SSH"] += 1
            elif "GeoIP" in line:
                event_counts["GeoIP"] += 1
            elif "Error" in line:
                event_counts["Error"] += 1
            elif "Connection" in line:
                event_counts["Connection"] += 1
            else:
                event_counts["Other"] += 1

    return render_template("index.html", logs=logs,
                           start_date=start_date,
                           end_date=end_date,
                           selected_type=event_type,
                           event_counts=dict(event_counts),
                           project_name="PhantomPort")

# --- Clear logs ---
@app.route("/clear_logs")
def clear_logs():
    if os.path.exists(LOG_PATH):
        open(LOG_PATH, 'w').close()
    return redirect(url_for('index'))

# --- Download logs ---
@app.route("/download_logs")
def download_logs():
    if os.path.exists(LOG_PATH):
        return send_file(LOG_PATH, as_attachment=True)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
