import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score

# Mapeamento das classes para números
class_mapping = {
    'Empate': 0,
    'Jogador O venceu': 1,
    'Jogador X venceu': 2,
    'Tem jogo': 3
}

# Conversão dos valores de string para números
def converter(val):
    if val == 'x':
        return 1
    elif val == 'o':
        return -1
    elif val == 'b':
        return 0
    else:
        return val  # mantém a classe original

# Carregar os arquivos
treino = pd.read_csv("tictactoe_treino.csv")
teste = pd.read_csv("tictactoe_teste.csv")
validacao = pd.read_csv("tictactoe_validacao.csv")

# Aplicar conversão
X_treino = treino.drop('class', axis=1).applymap(converter)
y_treino = treino['class'].map(class_mapping)

X_teste = teste.drop('class', axis=1).applymap(converter)
y_teste = teste['class'].map(class_mapping)

X_validacao = validacao.drop('class', axis=1).applymap(converter)
y_validacao = validacao['class'].map(class_mapping)

# Criar e treinar o modelo XGBoost
clf = XGBClassifier(
    n_estimators=100,           # número de árvores
    learning_rate=0.1,         # taxa de aprendizado
    max_depth=5,                # profundidade máxima das árvores
    random_state=42,            # para reprodutibilidade
    objective='multi:softmax',  # tipo de saída para múltiplas classes
    num_class=4                 # número de classes (Empate, Jogador X, Jogador O, Tem jogo)
)

clf.fit(X_treino, y_treino)

# Avaliar no teste
y_pred_teste = clf.predict(X_teste)
print("=== Avaliação no conjunto de TESTE ===")
print("Acurácia:", accuracy_score(y_teste, y_pred_teste))
print(classification_report(y_teste, y_pred_teste))

# Avaliar na validação
y_pred_validacao = clf.predict(X_validacao)
print("=== Avaliação no conjunto de VALIDAÇÃO ===")
print("Acurácia:", accuracy_score(y_validacao, y_pred_validacao))
print(classification_report(y_validacao, y_pred_validacao))

# Mostrar classes aprendidas
print("Classes aprendidas:", clf.classes_)
