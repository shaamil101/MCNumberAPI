from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "cdc33e44d693a3a58451898d4ec9df862c65b954"

@app.route('/', methods=['GET'])
@app.route('/<reference_number>', methods=['GET'])
def allowed_to_operate(reference_number=None):
    """
    Endpoint to fetch the 'allowedToOperate' status for a given reference number.
    """
    try:
        reference_number = request.args.get('mc_number')
        url = f"https://mobile.fmcsa.dot.gov/qc/services/carriers/{reference_number}?webKey={API_KEY}"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            # Extract the 'allowedToOperate' field
            allowed_to_operate = data.get("content", {}).get("carrier", {}).get("allowedToOperate")
            if allowed_to_operate is not None:
                return jsonify({
                    "allowed_to_operate": allowed_to_operate
                }), 200
            else:
                return jsonify({
                    "error": "Field 'allowedToOperate' not found in response."
                }), 404
        else:
            return jsonify({
                "error": f"FMCSA API returned an error: {response.status_code}",
                "details": response.text
            }), response.status_code

    except Exception as e:
        return jsonify({
            "error": "An error occurred while processing the request.",
            "details": str(e)
        }), 500

import os
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
