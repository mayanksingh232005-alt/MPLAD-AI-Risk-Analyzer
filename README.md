# MPLAD AI Risk Analyzer

AI-powered anomaly detection and risk analysis system for MPLAD allocation records.

## Objective

The MPLAD AI Risk Analyzer identifies unusual patterns in MPLAD allocation data and generates an easy-to-understand risk score for further review.

Note: An anomaly indicates an unusual statistical pattern. It does not automatically mean fraud or wrongdoing.

## Features

- Excel / CSV dataset upload
- Automatic data cleaning
- Machine Learning based anomaly detection
- Risk Score from 0–100
- Low / Medium / High Risk classification
- Risk distribution analysis
- High-risk record identification
- Complete analysis table
- CSV report download

## Technology Stack

Language:
Python 3.14

Frontend / Web Application:
Streamlit 1.62.0

Data Processing:
Pandas
NumPy

Machine Learning:
Scikit-learn

Model Loading:
Joblib

Input File Support:
XLSX
XLS
CSV

Web Server:
Streamlit

## Libraries

streamlit
pandas
numpy
scikit-learn
joblib
openpyxl
python-calamine

## AI Model

Model Type:
Machine Learning based Unsupervised Anomaly Detection

Trained Model Files:

mplad_anomaly_model.pkl
mplad_scaler.pkl
mplad_model_features.pkl

The trained model, scaler and feature list are loaded by the application during runtime.

## Project Structure

MPLAD_AI_Prototype/
│
├── app.py
├── mplad_anomaly_model.pkl
├── mplad_scaler.pkl
├── mplad_model_features.pkl
├── Allocated Limit for Honble MPs.xlsx
└── README.md

## Project Workflow

Upload Dataset
       ↓
Read Excel / CSV
       ↓
Data Cleaning
       ↓
Column Validation
       ↓
Feature Preparation
       ↓
Categorical Encoding
       ↓
Feature Scaling
       ↓
ML Anomaly Detection
       ↓
Anomaly Prediction
       ↓
Risk Score 0–100
       ↓
Risk Classification
       ↓
High-Risk Record Review
       ↓
CSV Report Export

## Data Processing

The application performs the following steps:

1. Reads Excel or CSV data.
2. Removes unnecessary unnamed columns.
3. Cleans column names.
4. Removes the Grand Total row.
5. Cleans allocated amount values.
6. Handles missing numeric values.
7. Prepares model features.
8. Encodes categorical variables.
9. Scales the input data.
10. Sends the processed data to the trained ML model.

## Model Features

Categorical Features:

- State
- Elected/Nominated

Numerical Features:

- Allocated Amount
- Term_Start_Year
- Term_End_Year

## Anomaly Detection

The model generates an anomaly prediction:

-1 = Anomaly / Unusual Record

1 = Normal Record

The anomaly result is further converted into a Risk Score between 0 and 100.

## Risk Classification

0–39   = Low Risk

40–69  = Medium Risk

70–100 = High Risk

## Application Dashboard

The dashboard provides:

- Total Records
- Normal Records
- Anomalies
- Anomaly Percentage
- Risk Distribution
- High-Risk Records
- Complete Analysis Table
- Downloadable CSV Report

## Input

Supported file formats:

.xlsx
.xls
.csv

Example dataset:

Allocated Limit for Honble MPs.xlsx

## Output

The application generates:

MPLAD_AI_Risk_Analysis.csv

The output contains the analyzed records along with anomaly and risk information.

## Installation

Open Command Prompt in the project folder.

Run:

py -m pip install streamlit pandas numpy scikit-learn joblib openpyxl python-calamine

## Run the Application

Open Command Prompt and navigate to the project folder:

cd "C:\Users\user\Downloads\MPLAD_AI_Prototype"

Then run:

py -m streamlit run app.py

The application will start on:

http://localhost:8501

Open the above address in a web browser.

## How the System Works

The user uploads an MPLAD allocation dataset.

The application cleans and validates the data.

Required features are prepared and transformed into a format suitable for the ML model.

The trained anomaly-detection model analyzes every record.

Unusual records receive an anomaly flag and higher risk score.

The dashboard displays the overall risk analysis and high-risk records.

The final analysis can be downloaded as a CSV report.

## Project Purpose

The main purpose of this project is to provide an AI-assisted screening system that helps identify unusual MPLAD allocation patterns quickly and supports further human review.

## Important Note

This application is a risk-screening and anomaly-detection system.

An anomaly does not automatically indicate fraud, corruption or illegal activity.

All flagged records should be reviewed and verified by authorized personnel before any administrative or investigative action is taken.

## Project Summary

Project Name:
MPLAD AI Risk Analyzer

Domain:
AI / Machine Learning / Data Analytics

Language:
Python 3.14

Framework:
Streamlit 1.62.0

ML:
Unsupervised Anomaly Detection

Input:
MPLAD Allocation Dataset

Output:
Anomaly Detection + Risk Score + Risk Level

Deployment:
Localhost using Streamlit

Main Application:
app.py

Model:
mplad_anomaly_model.pkl

Scaler:
mplad_scaler.pkl

Feature File:
mplad_model_features.pkl
