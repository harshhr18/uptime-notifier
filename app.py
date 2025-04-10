from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

sites = ["https://google.com", "https://youtube.com"]

@app.route('/')
def home():
    return render_template("index.html", sites=sites)

@app.route('/api/check_single')
def check_single():
    site = request.args.get("site")
    if not site:
        return jsonify({"error": "No site provided"}), 400
    try:
        r = requests.get(site, timeout=5)
        return jsonify({
            "site": site,
            "status": "UP",
            "response_time": f"{r.elapsed.total_seconds():.2f}s"
        })
    except:
        return jsonify({
            "site": site,
            "status": "DOWN",
            "response_time": "N/A"
        })

if __name__ == '__main__':
    app.run(debug=True)
