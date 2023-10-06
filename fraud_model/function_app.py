import azure.functions as func
import logging
import json
import pandas as pd
import joblib

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION )

@app.route(route="fraud_model")
def fraud_model(req: func.HttpRequest) -> func.HttpResponse:


    # Load the one hot encoding information
    with open('encoding_info.json', 'r') as file:
        encoding_info = json.load(file)

    categorical_columns = encoding_info['categorical_columns']
    encoded_columns = encoding_info['encoded_columns']
    binary_columns = ['is_prime', 'has_previous_fraud', 'device_used_before']
    numerical_columns = ['linea_tc', 'interes_tc', 'monto', 'hora', 'dcto', 'cashback', 'n_user_transactions', 'n_dispositivos_acumulados']

    # Extract input data from the event
    req_body = req.get_json()
    model_name = req_body.get('model')
    threshold = req_body.get('threshold')
    inputs = req_body.get('inputs')

    logging.info(f'model_name:{model_name}')
    logging.info(f'threshold:{threshold}')
    logging.info(f'inputs:{inputs}')

    # Load the trained model and scaler
    model = joblib.load(f'saved_models/{model_name}_model.pkl')
    scaler = joblib.load('saved_models/scaler.pkl')
    
    # Prepare input data as a DataFrame
    input_data = pd.DataFrame([inputs])

    # One-hot encoding 
    for col in categorical_columns:
        input_data = pd.concat([input_data, pd.get_dummies(input_data[col], prefix=col)], axis=1)
        input_data.drop(col, axis=1, inplace=True)

    # Ensure that the encoded columns match the training data's encoded columns
    missing_columns = set(encoded_columns) - set(input_data.columns)
    for col in missing_columns:
        input_data[col] = 0  

    # Numerica scaler
    input_data[numerical_columns] = scaler.transform(input_data[numerical_columns])

    # Bool -> Int
    input_data[binary_columns] = input_data[binary_columns].astype(int)

    # order cols
    input_data = input_data[encoded_columns]

    # Apply the threshold to determine if it's fraud or not
    fraud_probability = model.predict_proba(input_data.drop('fraude', axis=1))[:, 1]
    is_fraud = fraud_probability > threshold

    # Prepare the response
    response = {
        'model_name': model_name,
        'is_fraud': bool(is_fraud[0]),
        'fraud_probability': float(fraud_probability[0])
    }


    return func.HttpResponse(
        json.dumps(response),
        mimetype="application/json"
        )

    