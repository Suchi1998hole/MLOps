***** Diabetes Prediction MLOps Project *****
Model:
A complete end-to-end Machine Learning Operations (MLOps) pipeline for predicting diabetes using the Pima Indians Diabetes dataset. This project demonstrates the full lifecycle from model training to production deployment on Google Cloud.
Project Overview
Goal: Build and deploy a machine learning model that predicts whether a patient has diabetes based on diagnostic measurements.
Dataset: Pima Indians Diabetes Dataset (768 samples, 8 features)
Model: Logistic Regression with StandardScaler normalization
Accuracy: 73.44% on test set
Live API: https://diabetes-api-421235068177.us-central1.run.app/predict

Architecture
Data → Training → Model → Flask API → Docker → Google Cloud Run
                     ↓
              Streamlit UI (Local)

📁 Project Structure
Lab1/
├── data/
│   └── diabetes.csv              # Pima Indians Diabetes dataset
├── model/
│   ├── model.pkl                 # Trained Logistic Regression model
│   └── scaler.pkl                # StandardScaler for feature normalization
├── src/
│   ├── train.py                  # Model training script
│   ├── predict.py                # Prediction logic
│   ├── main.py                   # Flask REST API
│   └── test_api.py               # API testing script
├── streamlit_app.py              # Web interface
├── Dockerfile                    # Container configuration
├── cloudbuild.yaml               # Google Cloud Build config
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore file
└── README.md                     # This file


Implemented Steps:

Step 1: python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Mac/Linux

# Install Dependencies
requirements.txt:
pandas>=2.0.0
scikit-learn>=1.3.0
joblib>=1.3.0
flask>=2.3.0
streamlit>=1.26.0
requests>=2.31.0
numpy>=1.24.0
# Command to install
pip install -r requirements.txt

Step 2: Get the Dataset
bash
# Download Pima Indians Diabetes dataset
curl -o data/diabetes.csv https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv
Outcome: 0 (no diabetes) or 1 (diabetes)

Step 3: Train the Machine Learning Model
3.1 Create src/train.py
# Loads the diabetes dataset Splits data into training and test sets Normalizes features using StandardScaler Trains a Logistic Regression model Saves model and scaler to disk
# Run
python src/train.py

Output:
Starting model training...
Dataset loaded: 768 rows, 9 columns
Features shape: (768, 8)
Target shape: (768,)
Diabetes cases: 268 (34.9%)
Non-diabetes cases: 500 (65.1%)

Training set: 576 samples
Test set: 192 samples

Training Logistic Regression model...
Training accuracy: 0.7051
Test accuracy: 0.7344

✓ Model saved to model/model.pkl
✓ Scaler saved to model/scaler.pkl
Training complete!

Step 4: Create Flask REST API
4.1 Create src/main.py
Flask API with /predict endpoint that:
# Accepts POST requests with JSON patient data Uses the trained model to make predictions Returns prediction and probability scores
# Test API Locally

Terminal 1 - Run Flask Server:
python src/main.py

Terminal 2 - Test API:
python src/test_api.py

Output:
Test Case 1: High Risk Patient
Diagnosis: Diabetes
Diabetes Probability: 69.96%
No Diabetes Probability: 30.04%

Test Case 2: Low Risk Patient
Diagnosis: No Diabetes
Diabetes Probability: 4.59%
No Diabetes Probability: 95.41%

Step 5: Create Streamlit Web Interface
5.1 Create streamlit_app.py
Visual results with color-coded diagnosis and Probability breakdown
5.2 Run Streamlit
streamlit run streamlit_app.py
Opens browser at http://localhost:8501

Step 6: Dockerize the Application
6.1 Create Dockerfile

# Train the model inside the container
RUN mkdir -p model
RUN python src/train.py

6.2 Build Docker Image Locally (Optional)

docker build --platform linux/amd64 -t diabetes-api .

6.3 Run Docker Container Locally (Optional)

docker run -p 8080:8080 -e PORT=8080 diabetes-api
Test: http://localhost:8080/predict


Step 7: Deploy to Google Cloud Run
7.1 Setup Google Cloud

# Install Google Cloud SDK (if not already installed)
brew install --cask google-cloud-sdk 
# Initialize gcloud
gcloud init
# Login to Google Cloud
gcloud auth login
# Set your project
gcloud config set project 
7.2 Enable Required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
7.3 Link Billing Account
gcloud billing accounts list
gcloud billing projects link YOUR_PROJECT_ID --billing-account=YOUR_BILLING_ACCOUNT_ID
7.4 Configure Docker to use gcloud
gcloud auth configure-docker
# Build image
docker build --platform linux/amd64 -t gcr.io/YOUR_PROJECT_ID/diabetes-api .
# Push to Google Container Registry
docker push gcr.io/YOUR_PROJECT_ID/diabetes-api:latest
7.5 Deploy to Cloud Run
gcloud run deploy diabetes-api \
  --image gcr.io/YOUR_PROJECT_ID/diabetes-api:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
Output:
Deploying container to Cloud Run service [diabetes-api]...
✓ Deploying... Done.
✓ Creating Revision...
✓ Routing traffic...
✓ Setting IAM Policy...
Done.
Service [diabetes-api] revision [diabetes-api-00001-xxx] has been deployed 
and is serving 100 percent of traffic.
Service URL: https://diabetes-api-xxxxxxxxx.us-central1.run.app
Step 8: Test Deployed API
8.1 Test with curl
bash
curl -X POST https://YOUR-SERVICE-URL/predict \
  -H "Content-Type: application/json" \
  -d '{
    "pregnancies": 6,
    "glucose": 148,
    "blood_pressure": 72,
    "skin_thickness": 35,
    "insulin": 0,
    "bmi": 33.6,
    "diabetes_pedigree": 0.627,
    "age": 50
  }'
Response:
json
{
  "diagnosis": "Diabetes",
  "prediction": 1,
  "probability_diabetes": 0.6996385452462336,
  "probability_no_diabetes": 0.3003614547537664
}
8.2 Update Streamlit to Use Cloud API
# update the cloud url
api_url = os.environ.get('API_URL', 'https://YOUR-SERVICE-URL/predict')
Run Streamlit:
streamlit run streamlit_app.py

Step9:Monitor Your Application
View Logs in Google Cloud Console
Go to: https://console.cloud.google.com/run
Click on diabetes-api service
Click LOGS tab
