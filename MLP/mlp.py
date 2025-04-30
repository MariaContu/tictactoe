import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report

# Carregar os dados
df_treino = pd.read_csv("tictactoe_treino.csv")
df_teste = pd.read_csv("tictactoe_teste.csv")
df_validacao = pd.read_csv("tictactoe_validacao.csv")

# Mapeamento das letras para números
mapa = {'x': 1, 'o': -1, 'b': 0}  # 'x' = 1, 'o' = -1, 'b' = 0 (empty)

# Aplicar o mapeamento nos dados
df_treino = df_treino.applymap(lambda x: mapa.get(x, x) if isinstance(x, str) else x)
df_teste = df_teste.applymap(lambda x: mapa.get(x, x) if isinstance(x, str) else x)
df_validacao = df_validacao.applymap(lambda x: mapa.get(x, x) if isinstance(x, str) else x)

# Separar as features (X) e os rótulos (y) para treino, teste e validação
X_treino = df_treino.drop(columns=['class'])
y_treino = df_treino['class']

X_teste = df_teste.drop(columns=['class'])
y_teste = df_teste['class']

X_validacao = df_validacao.drop(columns=['class'])
y_validacao = df_validacao['class']

# Inicializar e treinar o modelo
clf = MLPClassifier(solver='adam', hidden_layer_sizes=(40), learning_rate_init=0.05, momentum=0.5, verbose=True)
clf.fit(X_treino, y_treino)

# Avaliar o modelo na validação
y_pred_validacao = clf.predict(X_validacao)

# Exibir as previsões com os rótulos reais
# print("Previsões e Rótulos Reais no Conjunto de Validação:")
# for i in range(len(y_validacao)):
#     print(f"Real: {y_validacao.iloc[i]}, Previsto: {y_pred_validacao[i]}")

# Relatório de desempenho na validação
print("Desempenho na validação:")
print(classification_report(y_validacao, y_pred_validacao))

# Avaliar o modelo nos dados de teste
y_pred_teste = clf.predict(X_teste)

# Relatório de desempenho no teste
print("Desempenho no teste:")
print(classification_report(y_teste, y_pred_teste))

# Acurácia no teste
accuracy = accuracy_score(y_teste, y_pred_teste)
print(f"Acurácia no teste: {accuracy:.2f}")

print(clf.classes_)
