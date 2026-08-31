from flask import Flask, request, jsonify
from handle_rfid import handle_uid

app = Flask(__name__)


@app.route("/rfid", methods=["POST"])
def rfid():
    data = request.get_json()
    if not data or "uid" not in data:
        return jsonify({"error": "missing uid"}), 400

    scanner_id = data.get("scanner_id", 1)
    handle_uid(data["uid"], scanner_id=scanner_id, source="http")
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
