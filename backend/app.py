# -----------------------------
# IMPORTAÇÃO DE BIBLIOTECAS
# rode no terminal pip install flask flask-cors numpy pandas joblib scikit-learn
# -----------------------------

# Framework web simples e rápido para criar APIs
from flask import Flask, request, jsonify

# Para salvar e carregar objetos Python (modelos treinados, encoders, etc)
import joblib

# Para permitir que o frontend (em outra porta) consiga acessar essa API
from flask_cors import CORS

# Manipulação de arrays e matrizes numéricas
import numpy as np

# Manipulação de tabelas (usado para o modelo MLP que espera DataFrame)
import pandas as pd

# -----------------------------
# CONFIGURAÇÃO DO SERVIDOR FLASK
# -----------------------------
app = Flask(__name__)
CORS(app)  # Libera o acesso da API para qualquer frontend (como o React)

# -----------------------------
# CARREGAMENTO DOS MODELOS
# -----------------------------

# Carrega o modelo de KNN treinado e salvo com joblib
modelo_knn = joblib.load('modelo_knn.pkl')

# Carrega o modelo de MLP treinado e salvo com joblib
modelo_mlp = joblib.load('modelo_mlp.pkl')

# Carrega o modelo de xgb treinado e salvo com joblib
modelo_xgb = joblib.load('modelo_xgb.pkl')

modelo_rf = joblib.load('modelo_rf.pkl')




# Carrega o encoder (LabelEncoder) usado no KNN para converter rótulos (ex: "Empate" → 0)
encoder = joblib.load('encoder.pkl')

# -----------------------------
# MAPEAMENTO DOS SÍMBOLOS DO TABULEIRO
# -----------------------------
# Converte o formato do tabuleiro enviado pelo frontend (ex: 'x', 'o', 'b') para números
# Isso é necessário para os modelos conseguirem entender a entrada
symbol_map = {'x': 1, 'o': -1, 'b': 0}

class_mapping = {
    0: 'Empate',
    1: 'Jogador O venceu',
    2: 'Jogador X venceu',
    3: 'Tem jogo'
}


# -----------------------------
# FUNÇÃO DE PREVISÃO USADA PELOS DOIS MODELOS
# -----------------------------
def prever_modelo(modelo, is_knn=False):
    """
    Essa função recebe um modelo (KNN ou MLP) e faz a previsão com base no tabuleiro enviado pelo frontend.
    O parâmetro 'is_knn' define se devemos usar NumPy (para KNN) ou DataFrame com colunas nomeadas (para MLP).
    """
    try:
        # Recebe os dados JSON enviados no POST (um array com 9 posições do tabuleiro)
        data = request.get_json()
        tabuleiro = data.get('tabuleiro', [])

        # Mapeia as letras ('x', 'o', 'b') para números (1, -1, 0)
        entrada = [symbol_map.get(v, 0) for v in tabuleiro]
        

        # Se o modelo for KNN, a entrada é um array NumPy simples
        if is_knn:
            entrada = np.array(entrada).reshape(1, -1)

        # Se for MLP, é necessário passar um DataFrame com os nomes corretos das colunas
        else:
            entrada = pd.DataFrame([entrada], columns=[
                'topLeft', 'topMid', 'topRight',
                'midLeft', 'midMid', 'midRight',
                'botLeft', 'botMid', 'botRight'
            ])
            print("DataFrame recebido pela IA:\n", entrada)


        # Faz a previsão com o modelo
        pred = modelo.predict(entrada)

        # Para KNN, precisamos reverter o número para a string original (ex: 0 → "Empate")
        # Para MLP, já retorna direto como string, então usamos pred[0]
        label = encoder.inverse_transform(pred)[0] if is_knn else pred[0]

        # Retorna a resposta em formato JSON
        response = jsonify({'resultado': label})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    # Caso ocorra algum erro (ex: dados inválidos), retornamos erro 500 com mensagem
    except Exception as e:
        response = jsonify({'erro': str(e)})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 500

# -----------------------------
# ENDPOINTS (rotas) PARA O FRONTEND
# -----------------------------

# Rota para o modelo KNN (usa is_knn=True)
@app.route('/preverknn', methods=['POST'])
def prever_knn():
    return prever_modelo(modelo_knn, is_knn=True)

# Rota para o modelo MLP
@app.route('/prevermlp', methods=['POST'])
def prever_mlp():
    return prever_modelo(modelo_mlp)

@app.route('/preverxgb', methods=['POST'])
def prever_xgb():
    try:
        data = request.get_json()
        tabuleiro = data.get('tabuleiro', [])
        entrada = [symbol_map.get(v, 0) for v in tabuleiro]

        entrada = np.array(entrada).reshape(1, -1)

        pred = modelo_xgb.predict(entrada)
        classe = int(pred[0])  # converte para int no caso de numpy.int64

        label = class_mapping.get(classe, "Classe desconhecida")

        response = jsonify({'resultado': label})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except Exception as e:
        response = jsonify({'erro': str(e)})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 500
    
@app.route('/preverrf', methods=['POST'])
def prever_rf():
    try:
        data = request.get_json()
        tabuleiro = data.get('tabuleiro', [])
        entrada = [symbol_map.get(v, 0) for v in tabuleiro]

        entrada = np.array(entrada).reshape(1, -1)

        pred = modelo_rf.predict(entrada)
        label = str(pred[0])  # já está em string ('Empate', etc.)

        response = jsonify({'resultado': label})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except Exception as e:
        response = jsonify({'erro': str(e)})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 500



# -----------------------------
# INICIALIZAÇÃO DO SERVIDOR
# -----------------------------
if __name__ == '__main__':
    # A API será executada localmente na porta 5001
    app.run(debug=True, port=5001)
