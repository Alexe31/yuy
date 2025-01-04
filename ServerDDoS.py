from flask import Flask, request, jsonify

app = Flask(__name__)

AUTHORIZED = True  # Schimbă această variabilă pentru a permite/bloca rularea programului

@app.route('/check_authorization', methods=['GET'])
def check_authorization():
    return jsonify({'authorized': AUTHORIZED})

if __name__ == '__main__':
    app.run(port=5000)
