from flask import Flask, render_template, request, send_file, redirect, url_for, session
import os
from datetime import datetime
from collections import Counter
import threading
import tkinter as tk
from PIL import Image, ImageTk
import re

app = Flask(__name__)
app.secret_key = "supersecretkey"
LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logs/honeypot.log"))
ALERT_THRESHOLD = 10

# --- Function to show GUI alert with embedded image ---
def system_notification(title, message, image_path="static/alert.png"):
    def show_popup():
        root = tk.Tk()
        root.title(title)
        root.geometry("450x400")
        root.configure(bg='black')
        root.resizable(False, False)

        try:
            img = Image.open(image_path)
            img = img.resize((150, 150))
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(root, image=photo, bg='black')
            img_label.image = photo
            img_label.pack(pady=10)
        except Exception as e:
            print(f"Image error: {e}")

        tk.Label(root, text=message, fg='red', bg='black',
                 font=("Helvetica", 14), wraplength=400, justify="center").pack(pady=10)
        tk.Button(root, text="OK", command=root.destroy, font=("Helvetica", 12),
                  bg='gray', fg='white').pack(pady=10)
        root.mainloop()

    threading.Thread(target=show_popup).start()

# --- Dummy Login ---
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
    ip_counter = Counter()

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            all_logs = f.readlines()

        for line in reversed(all_logs):
            date_match = re.match(r"(\d{4}-\d{2}-\d{2})", line)
            if not date_match:
                continue
            log_date_str = date_match.group(1)
            try:
                log_date = datetime.strptime(log_date_str, "%Y-%m-%d")
            except ValueError:
                continue

            # Filter by date
            if start_date:
                try:
                    if log_date < datetime.strptime(start_date, "%Y-%m-%d"):
                        continue
                except:
                    continue
            if end_date:
                try:
                    if log_date > datetime.strptime(end_date, "%Y-%m-%d"):
                        continue
                except:
                    continue

            # Filter by event type
            if event_type and event_type.lower() not in line.lower():
                continue

            logs.append(line)

            # Categorize log line
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

            # Extract IP
            ip_match = re.search(r"(\d{1,3}\.){3}\d{1,3}", line)
            if ip_match:
                ip = ip_match.group()
                ip_counter[ip] += 1

                if ip_counter[ip] == ALERT_THRESHOLD:
                    system_notification(
                        "🚨 PhantomGate Alert",
                        f"Suspicious activity detected!\nIP: {ip}\nAttempts: {ip_counter[ip]}"
                    )

    return render_template("index.html",
                           logs=logs,
                           start_date=start_date,
                           end_date=end_date,
                           selected_type=event_type,
                           event_counts=dict(event_counts),
                           project_name="PhantomGate")

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
    print("[+] Starting PhantomGate Dashboard at http://localhost:5000")
    app.run(debug=True, port=5000)

