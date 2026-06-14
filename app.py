from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

logs = []

@app.route("/login", methods=["POST"])
def login():
    data = request.json

    return jsonify({
        "status": "ok",
        "user": data.get("username")
    })


@app.route("/download", methods=["POST"])
def download():
    data = request.json
    logs.append(data)
    print("DOWNLOAD:", data)

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)