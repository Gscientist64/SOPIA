from flask import Flask, request, jsonify, send_from_directory
from sopia_engine import query_sop
import os

app = Flask(__name__)

# Serve the index.html file for the root URL
@app.route("/", methods=["GET"])
def home():
    return send_from_directory(os.path.join(app.root_path, 'templates'), 'index.html')

@app.route("/query", methods=["POST"])
def query():
    user_query = request.json.get("query")
    response = query_sop(user_query)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
