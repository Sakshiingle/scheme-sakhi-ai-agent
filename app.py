from flask import Flask, render_template, request, jsonify
from agent import get_schemes

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get-schemes", methods=["POST"])
def fetch_schemes():
    data = request.json or {}

    user_profile = {
        "language": data.get("language", "english"),
        "state": data.get("state", "").strip(),
        "category": data.get("category", "").strip(),
        "age": str(data.get("age", "")).strip(),
        "problem": data.get("problem", "").strip(),
    }

    result = get_schemes(user_profile)
    return jsonify({"response": result})

if __name__ == "__main__":
    app.run(debug=True)