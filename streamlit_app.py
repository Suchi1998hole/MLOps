import streamlit as st
import requests
import os

st.title('Diabetes Prediction System')

st.write("""
This application predicts whether a patient has diabetes based on diagnostic measurements.
Please enter the patient's medical information below.
""")

# input fields
col1, col2 = st.columns(2)

with col1:
    pregnancies = st.number_input('Number of Pregnancies', 
                                  min_value=0, max_value=20, value=1, step=1)
    glucose = st.number_input('Glucose Level (mg/dL)', 
                              min_value=0, max_value=300, value=120, step=1)
    blood_pressure = st.number_input('Blood Pressure (mm Hg)', 
                                     min_value=0, max_value=200, value=70, step=1)
    skin_thickness = st.number_input('Skin Thickness (mm)', 
                                     min_value=0, max_value=100, value=20, step=1)

with col2:
    insulin = st.number_input('Insulin Level (mu U/ml)', 
                              min_value=0, max_value=900, value=80, step=1)
    bmi = st.number_input('BMI (Body Mass Index)', 
                          min_value=0.0, max_value=70.0, value=25.0, step=0.1)
    diabetes_pedigree = st.number_input('Diabetes Pedigree Function', 
                                        min_value=0.0, max_value=3.0, value=0.5, step=0.001, 
                                        format="%.3f")
    age = st.number_input('Age (years)', 
                          min_value=1, max_value=120, value=30, step=1)

# Predict button
if st.button('Predict'):
    # Prepare data
    data = {
        'pregnancies': pregnancies,
        'glucose': glucose,
        'blood_pressure': blood_pressure,
        'skin_thickness': skin_thickness,
        'insulin': insulin,
        'bmi': bmi,
        'diabetes_pedigree': diabetes_pedigree,
        'age': age
    }
    
    try:
   
        # local testing, use localhost
        # deployed app, use your deployed API URL
        api_url = os.environ.get('API_URL', 'https://diabetes-api-421235068177.us-central1.run.app/predict')
        response = requests.post(api_url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            
            # results
            st.markdown("---")
            st.subheader("Prediction Results")
            
            # diagnosis with color coding
            if result['prediction'] == 1:
                st.error(f"Diagnosis: {result['diagnosis']}")
                st.warning(f"Diabetes Risk: {result['probability_diabetes']:.1%}")
            else:
                st.success(f"Diagnosis: {result['diagnosis']}")
                st.info(f"Healthy Probability: {result['probability_no_diabetes']:.1%}")
            
            st.markdown("### Probability Breakdown")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("No Diabetes", 
                         f"{result['probability_no_diabetes']:.1%}")
            with col2:
                st.metric("Diabetes", 
                         f"{result['probability_diabetes']:.1%}")
            
            st.progress(result['probability_diabetes'])
            
        else:
            st.error(f'Error: API returned status code {response.status_code}')
            
    except requests.exceptions.RequestException as e:
        st.error(f'Error connecting to API: {str(e)}')
        st.info('API is running on http://127.0.0.1:8080')

# Data card 
with st.expander("About the Features"):
    st.markdown("""
    - **Pregnancies:** Number of times pregnant
    - **Glucose:** Plasma glucose concentration (2 hours in oral glucose tolerance test)
    - **Blood Pressure:** Diastolic blood pressure (mm Hg)
    - **Skin Thickness:** Triceps skin fold thickness (mm)
    - **Insulin:** 2-Hour serum insulin (mu U/ml)
    - **BMI:** Body mass index (weight in kg/(height in m)²)
    - **Diabetes Pedigree Function:** A function that scores likelihood of diabetes based on family history
    - **Age:** Age in years
    """)