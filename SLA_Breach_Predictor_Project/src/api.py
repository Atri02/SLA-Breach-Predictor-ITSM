from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load model
print("--- 1. Loading model 'sla_predictor.pkl'...")
model = joblib.load('sla_predictor.pkl')
print("--- 2. Model loaded successfully.")

@app.route('/predict', methods=['POST'])
def predict():
    
    print("\n--- 3. /predict ENDPOINT HIT ---")
    
    try:
        data = request.json
        print(f"--- 4. RECEIVED DATA: {data}")
        
        # Convert JSON to DataFrame, must match training
        input_df = pd.DataFrame([data])
        
        prediction_proba = model.predict_proba(input_df)
        breach_prob = prediction_proba[0][1] # Get probability of "1"
        
        print(f"--- 5. PREDICTION SUCCESSFUL. Probability: {breach_prob}")
        
        return jsonify({'breach_probability': breach_prob})
        
    except Exception as e:
        print(f"--- 6. ERROR DURING PREDICTION: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)