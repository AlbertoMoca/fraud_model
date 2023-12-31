#  :credit_card: Modelo de Detección de Fraudes 

Este repositorio esta enfocado a el analisis y detección de fraudes que incluye:
- Un análisis descriptivo de los datos y el modelado (Random Forest, Gradient Boosting, AdaBoost, SVM, Neural Network) en el archivo **analysis_and_modeling.ipynb**
    - Relacion entre las variables y el fraude
    - Tratamiento de los datos
        - Extraccion de caracteristicas basadas en historial del cliente (El dispositivo se usó antes?, Hay Fraudes previos?, Numero de dispositivos usados anteriormente, Numero de transacciones )
        - Variables categoricas -> One Hot Encoding 
        - Oversampling para balancer los casos con y sin fraude
    - Entrenamiento y preparacion para uso en PROD.
- Implementacion de modelos en la carpeta **fraud_model**, que se pueden consumir a través de una función serverless en Azure en la siguiente URL: https://fraudtest.azurewebsites.net/api/test3

### Consumo del Modelo

Puede utilizar la función en Azure para predecir la probabilidad de fraude en una transacción utilizando el siguiente formato JSON como entrada:


```
input_data = {
  "model": "AdaBoost",                 # Nombre del modelo a utilizar (como vienen en la tabla de resultados).
  "threshold": 0.5,                    # Umbral de decisión para clasificar fraude o no fraude.
  "inputs": {                          # Datos de entrada para la predicción.
    "género": "M",                     # Género del titular de la tarjeta .
    "establecimiento": "Tienda departamental",  # Tipo de establecimiento de la transacción.
    "ciudad": "Guadalajara",           # Ciudad donde se realizó la transacción.
    "status_txn": "Aceptada",          # Estado de la transacción (por ejemplo, Aceptada).
    "dispositivo_marca": "Apple",      # Marca del dispositivo utilizado en la transacción.
    "dispositivo_proveedor": "ATT",     # Proveedor del dispositivo utilizado.
    "is_prime": True,                  # Si el titular de la tarjeta es miembro Prime (verdadero o falso).
    "has_previous_fraud": True,         # Si ha habido fraudes anteriores en la cuenta (verdadero o falso).
    "device_used_before": True,        # Si el dispositivo se ha utilizado anteriormente (verdadero o falso).
    "linea_tc": 1000,                  # Límite de crédito de la tarjeta de crédito.
    "interes_tc": 0.15,                # Tasa de interés de la tarjeta de crédito.
    "monto": 500,                      # Monto de la transacción.
    "hora": 14,                        # Hora en la que se realizó la transacción (formato militar).
    "dcto": 50,                        # Descuento aplicado en la transacción.
    "cashback": 10,                    # Cashback obtenido en la transacción.
    "n_user_transactions": 5,          # Número de transacciones anteriores del usuario.
    "n_dispositivos_acumulados": 2     # Número de dispositivos utilizados anteriormente en la cuenta.
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
token = 'sumSaOkAhXr6bBmEyuSBDIzyB9_CX3x-nY8nY_iEZI0lAzFuslrhJg==' # METER EN .env
url = f"https://fraudtest.azurewebsites.net/api/test3?code={token}"

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
| Random Forest | 0.9709 | 0.0 | 0.0 | 0.0 | 
| Gradient Boosting | 0.7612 | 0.0658 | 0.5449 | 0.1174 | 
| AdaBoost | 0.6801 | 0.0554 | 0.6218 | 0.1018 | 
| SVM | 0.8765 | 0.0771 | 0.2949 | 0.1222 | 
| Neural Network | 0.9365 | 0.0490 | 0.0641 | 0.0556 | 




