from flask import Flask, request, jsonify
import re

app = Flask(__name__)

OTP_REGEX = r"\b\d{6}\b"
latest_sms = None

@app.route("/requests", methods=["POST"])
def receive_sms():
    data = request.get_json(silent=True)

    if not data:
        print("RAW DATA:", request.data)
        return jsonify({"error": "No JSON received"}), 400

    sms_text = data.get("message", "")

    match = re.search(OTP_REGEX, sms_text)
    otp = match.group(0) if match else None

    return jsonify({
        "status": "ok",
        "otp": otp,
        "message": sms_text
    })
