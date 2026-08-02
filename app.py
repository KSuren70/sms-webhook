from flask import Flask, request, jsonify

app = Flask(__name__)

# Your real phone number (the one that sends OTP)
AUTHORIZED_NUMBER = "AOL1"

latest_sms = None

@app.route('/sms', methods=['POST'])
def sms():
    global latest_sms
    data = request.json

    # The SMS Forwarder app sends ONLY:
    # { "message": "From: SENDER\nMESSAGE" }
    raw = data.get("message", "")
    lines = raw.split("\n")

    # Extract sender and message
    sender_line = lines[0].replace("From:", "").strip()
    msg_line = "\n".join(lines[1:]).strip()

    # Authorization check
    if sender_line != AUTHORIZED_NUMBER:
        return {"status": "ignored"}, 403

    # Store clean SMS
    latest_sms = {
        "from": sender_line,
        "message": msg_line
    }

    print("Latest SMS:", latest_sms)
    return {"status": "ok"}


@app.route('/requests', methods=['GET'])
def get_latest():
    if latest_sms is None:
        return jsonify({"data": []})
    return jsonify({"data": [latest_sms]})
