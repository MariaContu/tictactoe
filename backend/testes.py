from flask import Flask, request, jsonify

import joblib

modelo = joblib.load('modelo_mlp.pkl')
print("Features usadas pelo modelo:", modelo.feature_names_in_)
