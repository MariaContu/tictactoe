from flask import Flask, request, jsonify, make_response
import joblib
import numpy as np

app = Flask(__name__)

# Carrega o modelo
modelo = joblib.load('modelo_knn.pkl')
encoder = joblib.load('encoder.pkl')

symbol_map = {'x': 1, 'o': -1, 'b': 0}

@app.route('/preverknn', methods=['OPTIONS', 'POST'])
def prever():
    # Preflight CORS
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response, 200

    # POST real
    try:
        data = request.get_json()
        tabuleiro = data.get('tabuleiro', [])
        entrada = [symbol_map.get(v, 0) for v in tabuleiro]
        entrada = np.array(entrada).reshape(1, -1)
        pred = modelo.predict(entrada)
        label = encoder.inverse_transform(pred)[0]
        response = jsonify({'resultado': label})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        response = jsonify({'erro': str(e)})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
