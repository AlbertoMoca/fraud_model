#  :credit_card: Modelo de Detección de Fraudes 

Este repositorio contiene un modelo de detección de fraudes que incluye:
- Un análisis descriptivo de los datos y el modelado (Random Forest, Gradient Boosting, AdaBoost, SVM, Neural Network) en el archivo **analysis_and_modeling.ipynb** 
- Implementaciones de modelos en la carpeta **fraud_model**, que se pueden consumir a través de una función serverless en Azure en la siguiente URL: https://fraudtest.azurewebsites.net/api/test3?code=sumSaOkAhXr6bBmEyuSBDIzyB9_CX3x-nY8nY_iEZI0lAzFuslrhJg==

### Consumo del Modelo

Puede utilizar la función en Azure para predecir la probabilidad de fraude en una transacción utilizando el siguiente formato JSON como entrada:


```
{
  "model": "AdaBoost",
  "threshold": 0.5,
  "inputs": {
    "género": "M",
    "establecimiento": "Tienda departamental",
    "ciudad": "Guadalajara",
    "status_txn": "Aceptada",
    "dispositivo_marca": "Apple",
    "dispositivo_proveedor": "ATT",
    "is_prime": true,
    "has_previous_fraud": true,
    "device_used_before": true,
    "linea_tc": 1000,
    "interes_tc": 0.15,
    "monto": 500,
    "hora": 14,
    "dcto": 50,
    "cashback": 10,
    "n_user_transactions": 5,
    "n_dispositivos_acumulados": 2
  }
}
```
La función devolverá una respuesta en formato JSON que incluye el nombre del modelo, si se considera que es un fraude y la probabilidad de fraude deacuerdo al modelo usado:

```
{
  "model_name": "AdaBoost",
  "is_fraud": true,
  "fraud_probability": 0.5116966658859685
}
```

Ejemplo:
```
import requests
import json

# URL de la función en Azure
url = "https://fraudtest.azurewebsites.net/api/test3?code=sumSaOkAhXr6bBmEyuSBDIzyB9_CX3x-nY8nY_iEZI0lAzFuslrhJg=="

# Datos de entrada en formato JSON
input_data = {
  "model": "AdaBoost",
  "threshold": 0.5,
  "inputs": {
    "género": "M",
    "establecimiento": "Tienda departamental",
    "ciudad": "Guadalajara",
    "status_txn": "Aceptada",
    "dispositivo_marca": "Apple",
    "dispositivo_proveedor": "ATT",
    "is_prime": True,
    "has_previous_fraud": True,
    "device_used_before": True,
    "linea_tc": 1000,
    "interes_tc": 0.15,
    "monto": 500,
    "hora": 14,
    "dcto": 50,
    "cashback": 10,
    "n_user_transactions": 5,
    "n_dispositivos_acumulados": 2
  }
}

# Realizar la solicitud 
response = requests.post(url, json=input_data)
result = response.json()

# Mostrar la respuesta
print("Nombre del modelo:", result["model_name"])
print("Es fraude:", result["is_fraud"])
print("Probabilidad de fraude:", result["fraud_probability"])
```

### Selección del Modelo

Para la eleccion del modelo a usar y el umbral (probabilidad predicha necesaria para que una transaccion se clasifique como fraudulenta) es importante tomar en cuenta el objetivo por ejemplo si lo mas importante es capturar la mayor cantidad de fraude un recall alto es un buen indicador para el modelo.


| Modelo | Accuracy | Precision | Recall | F1 Score |
|---|---|---|---|---|
| Random Forest | 0.972 | 0.552 | 0.104 | 0.175 |
| Gradient Boosting | 0.842 | 0.132 | 0.818 | 0.228 |
| AdaBoost | 0.822 | 0.130 | 0.916 | 0.227 |
| SVM      | 0.935 | 0.220 | 0.506 | 0.306 |
| Red Neuronal | 0.957 | 0.271 | 0.299 | 0.284 |










