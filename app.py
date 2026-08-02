from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Regex to detect 6‑digit OTP
OTP_REGEX = r"\b\d{6}\b"

latest_sms = None

@app.route('/sms', methods=['POST'])
def sms():
    global latest_sms
    data = request.json

    # Forward SMS sends:
    # {
    #   "sender": "AOL1 (+12362055011)",
    #   "message": "Your Student Success Portal MFA Verification Code is: 179665",
    #   "timestamp": "2026-08-01 23:44:00"
    # }

    sender = data.get("sender", "").strip()
    message = data.get("message", "").strip()

    # Extract OTP from message
    otp_match = re.search(OTP_REGEX, message)
    if not otp_match:
        return {"status": "ignored"}, 403

    otp = otp_match.group(0)

    # Store clean SMS
    latest_sms = {
        "from": sender,
        "message": message,
        "otp": otp
    }

    print("Latest SMS:", latest_sms)
    return {"status": "ok"}, 200


@app.route('/requests', methods=['GET'])
def get_latest():
    if latest_sms is None:
        return jsonify({"data": []})
    return jsonify({"data": [latest_sms]})
