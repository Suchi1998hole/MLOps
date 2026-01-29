import numpy as np
import joblib
import os
from train import run_training

# model loading
model = joblib.load("model/model.pkl")
scaler = joblib.load("model/scaler.pkl")

def predict_diabetes(pregnancies, glucose, blood_pressure, skin_thickness, 
                     insulin, bmi, diabetes_pedigree, age):
  
    # rearrange input data columwise
    input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness,
                           insulin, bmi, diabetes_pedigree, age]])
    
    # Scaling
    input_data_scaled = scaler.transform(input_data)
    
    # prediction
    prediction = model.predict(input_data_scaled)
    
    # probability scores
    probability = model.predict_proba(input_data_scaled)[0]
    
    return {
        'prediction': int(prediction[0]),
        'probability_no_diabetes': float(probability[0]),
        'probability_diabetes': float(probability[1]),
        'diagnosis': 'Diabetes' if prediction[0] == 1 else 'No Diabetes'
    }

if __name__ == "__main__":
    # Check for model existence
    if os.path.exists("model/model.pkl"):
        print("Model loaded successfully")
    else:
        print("Model not found. Training model first")
        os.makedirs("model", exist_ok=True)
        run_training()