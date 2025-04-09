import requests
from flask import Flask, jsonify
import datetime

app = Flask(__name__)

# List of websites to monitor
sites = [

    "https://google.com"
    # Add more as needed
]

@app.route('/')
def home():
    return """
    <h1>🔔 Uptime Notifier</h1>
    <p>Welcome to <strong>Uptime Notifier</strong> — your simple tool for checking website uptime.</p>
    <p>Monitoring the following websites:</p>
    <ul>
        {sites}
    </ul>
    <p>➡ <a href="/status">Check Status</a> | 🛠 <a href="/api/status">API Status (JSON)</a></p>
    """.format(sites=''.join(f"<li>{site}</li>" for site in sites))


@app.route('/status')
def check_status():
    result = """
    <html>
    <head><meta http-equiv="refresh" content="30"></head>
    <body>
    <h1>📡 Website Status</h1><ul>
    """
    for site in sites:
        try:
            r = requests.get(site, timeout=5)
            status = f"<span style='color:green;'>✅ UP ({r.elapsed.total_seconds():.2f}s)</span>"
            log_entry = f"[{datetime.datetime.now()}] {site} - UP ({r.elapsed.total_seconds():.2f}s)\n"
        except:
            status = "<span style='color:red;'>❌ DOWN</span>"
            log_entry = f"[{datetime.datetime.now()}] {site} - DOWN\n"
        result += f"<li>{site} - {status}</li>"

        # Append to log file
        with open("log.txt", "a") as f:
            f.write(log_entry)

    result += "</ul><p><a href='/'>⬅ Back</a></p></body></html>"
    return result


@app.route('/api/status')
def api_status():
    statuses = {}
    for site in sites:
        try:
            r = requests.get(site, timeout=5)
            statuses[site] = {"status": "UP", "response_time": r.elapsed.total_seconds()}
        except:
            statuses[site] = {"status": "DOWN", "response_time": None}
    return jsonify(statuses)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
