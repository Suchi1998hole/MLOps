from flask import Flask, request, jsonify
from predict import predict_diabetes
import os

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():

    # request data
    data = request.get_json()
    
    # Extract features
    pregnancies = float(data['pregnancies'])
    glucose = float(data['glucose'])
    blood_pressure = float(data['blood_pressure'])
    skin_thickness = float(data['skin_thickness'])
    insulin = float(data['insulin'])
    bmi = float(data['bmi'])
    diabetes_pedigree = float(data['diabetes_pedigree'])
    age = float(data['age'])
    
    # debugging purpose
    print(f"Input: pregnancies={pregnancies}, glucose={glucose}, bp={blood_pressure}, "
          f"skin={skin_thickness}, insulin={insulin}, bmi={bmi}, "
          f"pedigree={diabetes_pedigree}, age={age}")
    
    # prediction
    result = predict_diabetes(pregnancies, glucose, blood_pressure, skin_thickness,
                             insulin, bmi, diabetes_pedigree, age)
    
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "diabetes-prediction-api"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)