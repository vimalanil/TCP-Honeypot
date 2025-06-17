from flask import Flask, render_template
import os

app = Flask(__name__)
LOG_PATH = "../logs/honeypot.log"  # path to your log file

@app.route("/")
def index():
    logs = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            logs = f.readlines()
    return render_template("index.html", logs=logs)

if __name__ == "__main__":
    app.run(debug=True, port=5000)


