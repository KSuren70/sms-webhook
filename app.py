from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Detect 6‑digit OTP
OTP_REGEX = r"\b\d{6}\b"

# Store latest SMS text
latest_sms = None


# ---------------------------------------------------------
# 1. POST /sms  (Your old Postman tests)
# ---------------------------------------------------------
@app.route("/sms", methods=["POST"])
def sms_post():
    global latest_sms

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No JSON received"}), 400

    sms_text = data.get("message", "")
    latest_sms = sms_text

    match = re.search(OTP_REGEX, sms_text)
    otp = match.group(0) if match else None

    return jsonify({
        "status": "ok",
        "otp": otp,
        "message": sms_text
    })


# ---------------------------------------------------------
# 2. POST /requests  (SMS Forwarder app)
# ---------------------------------------------------------
@app.route("/requests", methods=["POST"])
def receive_sms():
    global latest_sms

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No JSON received"}), 400

    # SMS Forwarder sends only:
    # { "subject": "...", "message": "{sms}" }
    sms_text = data.get("message", "")
    latest_sms = sms_text

    match = re.search(OTP_REGEX, sms_text)
    otp = match.group(0) if match else None

    return jsonify({
        "status": "ok",
        "otp": otp,
        "message": sms_text
    })


# ---------------------------------------------------------
# 3. GET /requests  (Selenium OTP reader)
# ---------------------------------------------------------
@app.route("/requests", methods=["GET"])
def get_latest_sms():
    global latest_sms

    if latest_sms is None:
        return jsonify({"data": []})

    match = re.search(OTP_REGEX, latest_sms)
    otp = match.group(0) if match else None

    return jsonify({
        "data": [{
            "message": latest_sms,
            "otp": otp
        }]
    })


# ---------------------------------------------------------
# START SERVER
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
