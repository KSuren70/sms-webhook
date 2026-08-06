from flask import Flask, request, jsonify
import re

app = Flask(__name__)

OTP_REGEX = r"\b\d{6}\b"

latest_sms = None

@app.route("/sms", methods=["POST"])
def receive_sms():
    data = request.get_json()

    # Your SMS Forwarder app sends only:
    # { "subject": "...", "message": "full SMS text" }
    sms_text = data.get("message", "")

    # Extract OTP
    match = re.search(OTP_REGEX, sms_text)
    otp = match.group(0) if match else None

    global latest_sms
    latest_sms = sms_text

    return jsonify({
        "status": "ok",
        "otp": otp,
        "raw": sms_text
    })
