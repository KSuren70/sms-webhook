from flask import Flask, request, jsonify

app = Flask(__name__)

AUTHORIZED_NUMBER = "+12362055011"   # your SMS sender number
latest_sms = None

@app.route('/sms', methods=['POST'])
def sms():
    global latest_sms
    data = request.json

    # Only accept SMS from one number
    if data.get("from") != AUTHORIZED_NUMBER:
        return {"status": "ignored"}, 403

    latest_sms = data
    print("Latest SMS:", latest_sms)
    return {"status": "ok"}

@app.route('/requests', methods=['GET'])
def get_latest():
    if latest_sms is None:
        return jsonify({"data": []})
    return jsonify({"data": [latest_sms]})
