import requests

# API endpoint
url = 'http://127.0.0.1:8080/predict'

# Test case 1: High risk patient
print("=" * 50)
print("Test Case 1: High Risk Patient")
print("=" * 50)
data1 = {
    'pregnancies': 6,
    'glucose': 148,
    'blood_pressure': 72,
    'skin_thickness': 35,
    'insulin': 0,
    'bmi': 33.6,
    'diabetes_pedigree': 0.627,
    'age': 50
}

response = requests.post(url, json=data1)

if response.status_code == 200:
    result = response.json()
    print(f"Diagnosis: {result['diagnosis']}")
    print(f"Diabetes Probability: {result['probability_diabetes']:.2%}")
    print(f"No Diabetes Probability: {result['probability_no_diabetes']:.2%}")
else:
    print(f'Error: {response.status_code}')

# Test case 2: Low risk patient
print("\n" + "=" * 50)
print("Test Case 2: Low Risk Patient")
print("=" * 50)
data2 = {
    'pregnancies': 1,
    'glucose': 85,
    'blood_pressure': 66,
    'skin_thickness': 29,
    'insulin': 0,
    'bmi': 26.6,
    'diabetes_pedigree': 0.351,
    'age': 31
}

response = requests.post(url, json=data2)

if response.status_code == 200:
    result = response.json()
    print(f"Diagnosis: {result['diagnosis']}")
    print(f"Diabetes Probability: {result['probability_diabetes']:.2%}")
    print(f"No Diabetes Probability: {result['probability_no_diabetes']:.2%}")
else:
    print(f'Error: {response.status_code}')