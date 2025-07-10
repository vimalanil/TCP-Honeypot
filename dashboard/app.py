<<<<<<< HEAD
from flask import Flask, render_template, request, send_file, redirect, url_for, session
import os
from datetime import datetime
from collections import Counter
import io

app = Flask(__name__)
app.secret_key = "supersecretkey"
LOG_PATH = "../logs/honeypot.log"
=======
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, jsonify, send_file
from collections import Counter
from utils.geoip_lookup import geo_lookup
import csv
import requests

app = Flask(__name__)
LOG_PATH = "../logs/honeypot.log"

# Simple in-memory cache for geo lookups
geo_cache = {}

def safe_geo_country(ip):
    if ip in geo_cache:
        return geo_cache[ip]
    info = geo_lookup(ip)
    if info:
        geo_cache[ip] = info["country"]
        return info["country"]
    return "Unknown"
>>>>>>> d4c922a (my dashboard)

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
<<<<<<< HEAD
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
                           project_name="CyberSentinel")

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
=======
    ips = []
    dates = []

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            for line in f:
                logs.append(line.strip())
                parts = line.split()
                for part in parts:
                    if part.count(".") == 3:
                        ip = part.split(":")[0]  # ✅ remove port if present
                        ips.append(ip)
                        break
                if len(parts) > 0:
                    dates.append(parts[0])

    unique_ips = set(ips)
    countries = []
    for ip in unique_ips:
        country = safe_geo_country(ip)
        countries.append(country)

    return render_template("index.html",
        logs=logs[::-1],
        total_attacks=len(logs),
        unique_countries=len(set(countries)),
        top_ips=Counter(ips).most_common(5),
        filter_ips=sorted(unique_ips),
        filter_dates=sorted(set(dates))
    )


@app.route("/map-data")
def map_data():
    data = []
    seen = set()
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            for line in f:
                parts = line.split()
                ip_port = next((p for p in parts if p.count(".") == 3), None)
                if ip_port:
                    ip = ip_port.split(":")[0]  # ✅ extract only IP part
                    if ip and ip not in seen:
                        print(f"[DEBUG] Looking up {ip}")
                        geo = geo_lookup(ip)
                        print(f"[DEBUG] Result for {ip}: {geo}")
                        if geo:
                            data.append(geo)
                            seen.add(ip)
                        if len(seen) >= 20:  # optional performance limiter
                            break
    return jsonify(data)


@app.route("/attack-data")
def attack_data():
    from datetime import datetime
    timeline = {}
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            for line in f:
                ts = line.split()[0]  # assume first field is timestamp
                try:
                    minute = datetime.strptime(ts, "%Y-%m-%d").strftime("%Y-%m-%d")
                    timeline[minute] = timeline.get(minute, 0) + 1
                except:
                    pass
    labels = list(timeline.keys())
    values = [timeline[k] for k in labels]
    return jsonify({"labels": labels, "values": values})

@app.route("/export-logs")
def export_logs():
    export_path = "../logs/exported_logs.csv"
    with open(LOG_PATH, "r") as infile, open(export_path, "w", newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Log Entry"])
        for line in infile:
            writer.writerow([line.strip()])
    return send_file(export_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

>>>>>>> d4c922a (my dashboard)
