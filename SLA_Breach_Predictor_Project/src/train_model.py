import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

print("--- 1. Script started...")

try:
    df = pd.read_csv('data/incident.csv')
except FileNotFoundError:
    print("Error: incident.csv not found!")
    exit()

# --- 2. Define Features (X) and Target (y) ---
# We are *only* using columns that exist in your file.
features = ['priority', 'category', 'assignment_group']

# We will "fake" a target variable from 'state'
# 'Closed' = 0 (Not breached), everything else = 1 (Breached)
target = 'state' 

# Prepare X (features) - fill any missing values
X = df[features].fillna('None') 
# Prepare y (target)
y = df[target].apply(lambda x: 0 if x == 'Closed' else 1)

print("--- 2. Features and target are set.")

# --- 3. Define Data Preprocessing ---
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), features)
    ])

# --- 4. Define the Model ---
model = RandomForestClassifier(n_estimators=100, random_state=42)

# --- 5. Create a Pipeline ---
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', model)])

# --- 6. Split and Train the Model ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("--- 3. Training the new model...")
pipeline.fit(X_train, y_train)

# --- 7. Save the Model ---
joblib.dump(pipeline, 'sla_predictor.pkl')
print("--- 4. New 'sla_predictor.pkl' model has been saved.")