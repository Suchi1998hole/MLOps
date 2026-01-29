import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib

def run_training():
    """
    Train the Diabetes prediction model
    """
    print("Starting model training...")
    
    # Read the training data
    # Column names for Pima Indians Diabetes dataset
    column_names = ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 
                    'insulin', 'bmi', 'diabetes_pedigree', 'age', 'outcome']
    
    dataset = pd.read_csv('data/diabetes.csv', names=column_names, header=None)
    
    # Convert all columns to numeric (important!)
    for col in dataset.columns:
        dataset[col] = pd.to_numeric(dataset[col], errors='coerce')
    
    # Remove any rows with NaN values
    dataset = dataset.dropna()
    
    print(f"Dataset loaded: {dataset.shape[0]} rows, {dataset.shape[1]} columns")
    
    # Display first few rows
    print("\nFirst few rows of data:")
    print(dataset.head())
    
    # Split into features (X) and target (y)
    X = dataset.drop("outcome", axis=1).copy()
    y = dataset["outcome"].copy()
    
    print(f"\nFeatures shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    print(f"Diabetes cases: {int(y.sum())} ({y.sum()/len(y)*100:.1f}%)")
    print(f"Non-diabetes cases: {int((1-y).sum())} ({(1-y).sum()/len(y)*100:.1f}%)")
    
    # Create train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    
    print(f"\nTraining set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Standardize features (important for logistic regression)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train the model
    print("\nTraining Logistic Regression model...")
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train_scaled, y_train)
    model.feature_names = X.columns.tolist()
    
    # Calculate accuracy
    train_accuracy = model.score(X_train_scaled, y_train)
    test_accuracy = model.score(X_test_scaled, y_test)
    
    print(f"\nTraining accuracy: {train_accuracy:.4f}")
    print(f"Test accuracy: {test_accuracy:.4f}")
    
    # Persist the trained model and scaler
    if not os.path.exists("model"):
        os.makedirs("model")
    
    joblib.dump(model, "model/model.pkl")
    joblib.dump(scaler, "model/scaler.pkl")
    
    print("\n✓ Model saved to model/model.pkl")
    print("✓ Scaler saved to model/scaler.pkl")
    print("Training complete!")

if __name__ == "__main__":
    run_training()