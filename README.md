# SLA Breach Predictor in ITSM

**Author:** Atri Ghosh

## Project Overview
This project integrates a Machine Learning model with ServiceNow to proactively identify incidents at risk of breaching their SLA. It uses a RandomForest model served via a Python Flask API and connects to ServiceNow using an event-driven architecture.

## Repository Structure
- **`/src`**: Contains the Python ML model training script, the Flask API server, and the ServiceNow Script Actions.

## Technology Stack
- **Frontend:** ServiceNow (Incident Management)
- **Backend:** Python 3.9, Flask, Scikit-learn
- **Integration:** REST API, ngrok, ServiceNow Event Registry
- **Model:** Random Forest Classifier

## How to Run
1. Run `train_model.py` to generate the model artifact.
2. Start the API using `python app.py`.
3. Expose the local server using `ngrok http 5000`.
4. Update the ServiceNow REST Message with the new ngrok URL.
