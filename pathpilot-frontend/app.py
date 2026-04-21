from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results")
def results():
    degree = request.args.get("degree")
    try:
        response = requests.get((f"http://backend:5000/jobs"), params = {"degree": degree})
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return render_template("results.html", error=str(e))
    return render_template("results.html", federal_jobs=data["federal_jobs"], private_jobs=data["private_jobs"], degree=degree)
if __name__ == "__main__":
    app.run(debug=True, host = "0.0.0.0", port = 5000)