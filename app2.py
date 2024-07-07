from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

class EndpointChecker:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.response_code = None
        self.is_alive = False

    def check(self):
        try:
            response = requests.get(self.endpoint)
            self.response_code = response.status_code
            self.is_alive = self.response_code == 200
        except requests.RequestException:
            self.response_code = None
            self.is_alive = False

    def get_result(self):
        return {
            "QueriedAt": datetime.utcnow().isoformat(),
            "ResponseCode": self.response_code,
            "IsAlive": self.is_alive
        }

@app.route('/check_endpoint', methods=['GET'])
def check_endpoint():
    endpoint = request.args.get('endpoint')
    if not endpoint:
        return jsonify({"error": "No endpoint provided"}), 400
    
    checker = EndpointChecker(endpoint)
    checker.check()
    result = checker.get_result()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
