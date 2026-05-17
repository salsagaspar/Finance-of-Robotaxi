import os
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

def train_model():
    data_dir = r"c:\Users\hpvic\OneDrive\Documents\Finance of Robotaxi"
    cleaned_customer_path = os.path.join(data_dir, "cleaned_data", "ds2_customers_cleaned.csv")
    model_dir = os.path.join(data_dir, "models")
    os.makedirs(model_dir, exist_ok=True)
    
    print("--- Memulai Latihan Model Machine Learning Churn ---")
    
    # 1. Load Data
    df = pd.read_csv(cleaned_customer_path)
    
    # 2. Target Definition (Binary Classification: Churn Risk > 0.5)
    df['high_churn_risk'] = (df['churn_risk_score'] > 0.5).astype(int)
    
    # 3. Feature Engineering: Lifetime in Days
    df['join_date'] = pd.to_datetime(df['join_date'])
    ref_date = df['join_date'].max() + pd.Timedelta(days=1)
    df['days_since_joined'] = (ref_date - df['join_date']).dt.days
    
    # 4. Feature Selection
    categorical_features = [
        'loyalty_tier', 'subscription_plan', 'preferred_payment', 
        'account_status', 'referral_source', 'age_group', 'gender', 'city'
    ]
    numerical_features = [
        'total_trips', 'total_spent_usd', 'avg_rating_given', 
        'lifetime_value_usd', 'promo_eligible_flag', 'days_since_joined'
    ]
    
    X = df[categorical_features + numerical_features]
    y = df['high_churn_risk']
    
    # 5. Train/Test Split (Stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 6. Preprocessing Pipeline using ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ]
    )
    
    # 7. Model Pipeline (Preprocessing + Estimator)
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1))
    ])
    
    # 8. Train Model
    print("[OK] Melatih Random Forest Classifier...")
    pipeline.fit(X_train, y_train)
    
    # 9. Evaluate Model
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]
    
    acc = pipeline.score(X_test, y_test)
    roc_auc = roc_auc_score(y_test, y_prob)
    
    print("\n=== Performa Model Prediksi Churn ===")
    print(f"Accuracy Score: {acc:.2%}")
    print(f"ROC-AUC Score: {roc_auc:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # 10. Save Pipeline Model (.pkl)
    model_save_path = os.path.join(model_dir, "churn_classifier.pkl")
    with open(model_save_path, 'wb') as f:
        pickle.dump(pipeline, f)
        
    print(f"\n[OK] Model Churn Classifier berhasil disimpan di: {model_save_path}")
    print("--- ML Training Pipeline Selesai ---")

if __name__ == "__main__":
    train_model()
