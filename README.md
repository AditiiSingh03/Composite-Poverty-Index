Poverty Analysis & Composite Poverty Index (CPI) – Data Science Project

This project focuses on analyzing poverty-related indicators across different states and building a Composite Poverty Index (CPI) using data preprocessing, normalization, correlation-based weighting, and visualization.

The goal is to create a data-driven, quantifiable measure of poverty by combining multiple socioeconomic parameters into a single index.

⭐ Project Overview

Poverty is influenced by several factors such as:

Literacy Rate

Unemployment Rate

Per Capita Income

Population Below Poverty Line (BPL)

Access to Basic Facilities

This project:

Cleans the dataset

Handles missing values

Normalizes all numeric indicators

Calculates weights using correlation-based feature importance

Computes Composite Poverty Index (CPI)

Visualizes state-wise CPI using Matplotlib

📂 Repository Structure
├── poverty_dataset.csv                     # Raw dataset
├── poverty_dataset_clean.csv               # Cleaned dataset
├── poverty_dataset_normalized.csv          # Normalized dataset
├── poverty_dataset_with_cpi.csv            # Dataset with computed CPI
├── Untitled.ipynb                          # Notebook with full analysis
└── README.md                               # Project documentation

🔧 Technologies Used

Python

Pandas

NumPy

Scikit-learn

Matplotlib

Jupyter Notebook

📊 Steps Performed in This Project
1️⃣ Data Loading

Import dataset using pandas

Display initial rows and structure

2️⃣ Data Cleaning

Remove commas from Per Capita Income

Convert numeric columns to proper data types

Handle missing values using median imputation

3️⃣ Normalization

Normalized all numerical indicators using Min-Max Scaling to bring values between 0 and 1.

from sklearn.preprocessing import MinMaxScaler

4️⃣ Feature Weight Calculation

Weights are generated using the sum of correlations of each feature with all others.

Higher weight = greater impact on poverty level.

5️⃣ Composite Poverty Index (CPI)

CPI formula:

CPI = Σ (Normalized Feature × Weight)


A higher CPI indicates worse poverty conditions.

6️⃣ Visualization

Created a State-wise CPI Bar Chart using Matplotlib.

📈 Results

✔ Cleaned & normalized dataset
✔ Automatically computed weightage for each factor
✔ Final CPI values for each state
✔ Visualization of poverty distribution

This helps understand which states are more affected and which factors contribute most to poverty.

🚀 How to Run the Project
1. Clone the repository
git clone (https://github.com/AditiiSingh03/Composite-Poverty-Index)

2. Install dependencies
pip install pandas numpy scikit-learn matplotlib

3. Open the notebook
jupyter notebook

4. Run all cells

The notebook will:

Clean the data

Normalize features

Compute weights

Generate CPI

Plot the graph

🎯 Use Cases

Policy making

Social welfare planning

Academic research

Data-driven poverty forecasting

State-wise poverty comparison

📬 Author

Aditi Singh

B.Tech CSIT | Data Science Enthusiast
