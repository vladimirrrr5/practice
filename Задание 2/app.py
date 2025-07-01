from flask import Flask, jsonify
import math

app = Flask(__name__)

@app.route('/api/gcd/<int:a>/<int:b>', methods=['GET'])
def gcd(a, b):
    result = math.gcd(a, b)
    return jsonify({"number1": a, "number2": b, "gcd": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)