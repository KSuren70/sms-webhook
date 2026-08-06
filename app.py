from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Detect 6‑digit OTP
OTP_REGEX = r"\b\d{6}\b"

# Store latest SMS text
latest_sms = None


# ---------------------------------------------------------
# RECEIVE SMS FROM SMS FORWARDER (POST)
# ---------------------------------------------------------
@app.route("/requests", methods=["POST"])
def receive_sms():
    global latest_sms

    # Try to parse JSON safely
    data = request.get_json(silent=True)

    if not data:
        # SMS Forwarder sometimes sends empty body → avoid crash
        print("Empty or invalid JSON received:", request.data)
        return jsonify({"error": "No JSON received"}), 400

    # SMS Forwarder sends only:
    # { "subject": "...", "message": "FULL_SMS_TEXT" }
    sms_text = data.get("message", "")

    latest_sms = sms_text

    # Extract OTP
    match = re.search(OTP_REGEX, sms_text)
    otp = match.group(0) if match else None

    return jsonify({
        "status": "ok",
        "otp": otp,
        "message": sms_text
    })


# ---------------------------------------------------------
# READ LATEST SMS FOR SELENIUM (GET)
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
