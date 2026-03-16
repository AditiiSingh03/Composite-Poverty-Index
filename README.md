# Multidimensional Poverty Prediction & Policy Simulation Dashboard

This project builds a data-driven system to analyze multidimensional poverty across Indian states using socio-economic indicators.  
The system predicts SDG poverty scores, detects anomalies, and provides policy simulation tools for decision-makers.

The dashboard allows interactive exploration of poverty indicators and enables users to simulate policy interventions.

---

## Project Overview

Poverty is a multidimensional issue influenced by education, health, financial inclusion, sanitation, and employment.

This project builds a machine learning system that:

• Predicts poverty-related SDG scores for Indian states  
• Detects anomalies between actual and predicted outcomes  
• Classifies states into poverty risk categories  
• Provides policy simulation tools to test potential improvements  
• Visualizes poverty risk geographically across India

---

## Dataset

The dataset contains socio-economic indicators for Indian states.

Features used in the model include:

- Literacy Rate
- Average Monthly Per Capita Consumption Expenditure (MPCE)
- Unemployment Rate
- Infant Mortality Rate (IMR)
- Secondary School Dropout Rate
- Sanitation Access
- Nutrition Stunting
- Bank Account Access

Target variable:

SDG Poverty Target Score

---

## Machine Learning Model

The model used in this project is:

AdaBoost Regressor

The model predicts poverty scores based on socio-economic indicators and evaluates prediction errors to identify anomalies.

---

## Dashboard Features

The interactive Streamlit dashboard provides the following capabilities:

### State-Level Analysis

Users can select any Indian state to view:

- Actual poverty score
- Predicted poverty score
- Risk classification
- Anomaly detection

---

### Policy Simulation Engine

Users can simulate policy improvements by adjusting:

- Literacy Rate
- Sanitation Access
- Bank Account Access

The system recalculates the predicted poverty score based on the new values.

---

### Feature Importance Analysis

The dashboard shows which indicators most influence poverty outcomes.

Example insights:

Financial inclusion (Bank Account Access)  
Health indicators (Infant Mortality Rate)  
Consumption expenditure levels

---

### Poverty Risk Map

The dashboard includes a choropleth map of India showing:

- High Risk States
- Medium Risk States
- Low Risk States

This enables quick geographical understanding of poverty risk distribution.

---

### Anomaly Detection

States with large gaps between predicted and actual scores are flagged for further policy investigation.

---

## Technologies Used

Python  
Streamlit  
Scikit-learn  
Pandas  
Matplotlib  
Plotly  

---

## How to Run the Project

Clone the repository
