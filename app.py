import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import json
import plotly.express as px

st.set_page_config(page_title="Poverty Prediction & Audit System", layout="wide")

# -----------------------------
# Load files
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("final_master_dataset_10_attributes.csv")

@st.cache_data
def load_feature_importance():
    return pd.read_csv("feature_importance_summary.csv")

@st.cache_resource
def load_model():
    return joblib.load("adaboost_model.pkl")

@st.cache_data
def load_geojson():
    with open("india_states.geojson", "r", encoding="utf-8") as f:
        return json.load(f)

df = load_data()
importance_df = load_feature_importance()
model = load_model()
india_geojson = load_geojson()

# -----------------------------
# Detect target column automatically
# -----------------------------
possible_target_cols = [
    "SDG_Target_Score",
    "SDG_score",
    "SDG Score",
    "Target_Score",
    "score",
    "Score",
    "Poverty Index (SDG)"
]

target_col = None
for col in possible_target_cols:
    if col in df.columns:
        target_col = col
        break

if target_col is None:
    st.error(f"Target score column not found. Available columns are: {list(df.columns)}")
    st.stop()

# -----------------------------
# Detect state column safely
# -----------------------------
if "State" not in df.columns:
    st.error(f"'State' column not found. Available columns are: {list(df.columns)}")
    st.stop()

# -----------------------------
# Title
# -----------------------------
st.title("Multidimensional Poverty Prediction & Audit System")
st.write(
    "This system predicts SDG poverty-related scores using socio-economic indicators, classifies poverty risk, flags anomalies, and supports policy-level what-if analysis."
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Select State")
selected_state = st.sidebar.selectbox("State", sorted(df["State"].unique()))

# -----------------------------
# Risk logic
# -----------------------------
def assign_risk_level(score):
    if score < 60:
        return "High Risk"
    elif score < 72:
        return "Medium Risk"
    else:
        return "Low Risk"

# -----------------------------
# State data
# -----------------------------
state_data = df[df["State"] == selected_state].copy()

# Features for prediction
X_state = state_data.drop(columns=["State", target_col])

predicted = model.predict(X_state)[0]
actual = state_data[target_col].values[0]

residual = actual - predicted
absolute_residual = abs(residual)

threshold = 5
risk_level = assign_risk_level(actual)
red_flag = "Yes" if absolute_residual > threshold else "No"

# -----------------------------
# Metrics
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Predicted Score", f"{predicted:.2f}")
col2.metric("Actual Score", f"{actual:.2f}")
col3.metric("Risk Level", risk_level)
col4.metric("Red Flag", red_flag)

if red_flag == "Yes":
    st.error(
        f"Anomaly detected for {selected_state}: prediction gap is {absolute_residual:.2f}, which exceeds threshold {threshold}."
    )
else:
    st.success(
        f"No major anomaly detected for {selected_state}. Prediction gap is {absolute_residual:.2f}."
    )

# -----------------------------
# State indicators
# -----------------------------
st.subheader("State Indicators")
state_display = state_data.T.reset_index()
state_display.columns = ["Indicator", "Value"]
st.dataframe(state_display, use_container_width=True)

# -----------------------------
# Policy Simulation
# -----------------------------
st.subheader("Policy Simulation")

literacy = st.slider(
    "Literacy Rate",
    40, 100,
    int(state_data["Literacy_Rate"].values[0])
)

sanitation = st.slider(
    "Sanitation Access",
    40, 100,
    int(state_data["Sanitation_Access"].values[0])
)

bank = st.slider(
    "Bank Account Access",
    40, 100,
    int(state_data["Bank_Account_Access"].values[0])
)

sim_data = state_data.copy()
sim_data["Literacy_Rate"] = literacy
sim_data["Sanitation_Access"] = sanitation
sim_data["Bank_Account_Access"] = bank

X_sim = sim_data.drop(columns=["State", target_col])
new_prediction = model.predict(X_sim)[0]
score_change = new_prediction - predicted

sim_col1, sim_col2 = st.columns(2)
sim_col1.metric("New Predicted Score After Policy Change", f"{new_prediction:.2f}")
sim_col2.metric("Change in Predicted Score", f"{score_change:.2f}")

if score_change > 0:
    st.success(f"Predicted score improves by {score_change:.2f} points under the simulated policy changes.")
elif score_change < 0:
    st.warning(f"Predicted score decreases by {abs(score_change):.2f} points under the simulated policy changes.")
else:
    st.info("No change in predicted score under the current simulation.")

# -----------------------------
# Feature importance
# -----------------------------
st.subheader("Feature Importance")
importance_df = importance_df.sort_values(by="Importance", ascending=False)

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(importance_df["Feature"], importance_df["Importance"])
ax.invert_yaxis()
ax.set_xlabel("Importance Score")
ax.set_ylabel("Feature")
ax.set_title("Feature Importance for Poverty Prediction")
st.pyplot(fig)

# -----------------------------
# Top Drivers for Selected State
# -----------------------------
st.subheader("Top Drivers for Selected State")

top_features = importance_df.head(3).copy()
top_features["State Value"] = [
    state_data.iloc[0][feat] if feat in state_data.columns else "N/A"
    for feat in top_features["Feature"]
]

st.write(f"Top contributing indicators for **{selected_state}**:")
st.dataframe(top_features[["Feature", "Importance", "State Value"]], use_container_width=True)

# -----------------------------
# Policy Recommendation Engine
# -----------------------------
st.subheader("Policy Recommendations")

recommendations = []
row = state_data.iloc[0]

if "Bank_Account_Access" in row.index and row["Bank_Account_Access"] < 80:
    recommendations.append("Improve financial inclusion through bank account access and digital payment adoption.")

if "Nutrition_Stunting" in row.index and row["Nutrition_Stunting"] > 30:
    recommendations.append("Strengthen nutrition and child welfare programs to reduce stunting.")

if "Sanitation_Access" in row.index and row["Sanitation_Access"] < 85:
    recommendations.append("Increase investment in sanitation infrastructure and rural hygiene programs.")

if "Secondary_Dropout" in row.index and row["Secondary_Dropout"] > 15:
    recommendations.append("Reduce school dropout rates through targeted education retention programs.")

if "IMR_Health" in row.index and row["IMR_Health"] > 25:
    recommendations.append("Improve maternal and child healthcare services to reduce infant mortality.")

if "Unemployment_Rate" in row.index and row["Unemployment_Rate"] > 6:
    recommendations.append("Promote employment generation schemes and local skill development initiatives.")

if "Literacy_Rate" in row.index and row["Literacy_Rate"] < 75:
    recommendations.append("Expand literacy and adult education initiatives in vulnerable regions.")

if "Avg_MPCE" in row.index and row["Avg_MPCE"] < 6000:
    recommendations.append("Support income growth through livelihood enhancement and welfare support schemes.")

if recommendations:
    for rec in recommendations:
        st.markdown(f"- {rec}")
else:
    st.success("No major policy intervention is suggested based on the current indicator thresholds.")

# -----------------------------
# Full prediction / audit table
# -----------------------------
X_full = df.drop(columns=["State", target_col]).copy()

df_plot = df.copy()
df_plot["Predicted_Score"] = model.predict(X_full)
df_plot["Residual"] = df_plot[target_col] - df_plot["Predicted_Score"]
df_plot["Absolute_Residual"] = df_plot["Residual"].abs()
df_plot["Red_Flag"] = df_plot["Absolute_Residual"].apply(lambda x: "Yes" if x > threshold else "No")
df_plot["Risk_Level"] = df_plot[target_col].apply(assign_risk_level)

# -----------------------------
# Actual vs Predicted plot
# -----------------------------
st.subheader("Actual vs Predicted Scores Across States")

flagged = df_plot[df_plot["Red_Flag"] == "Yes"]

fig2, ax2 = plt.subplots(figsize=(8, 6))

ax2.scatter(
    df_plot[target_col],
    df_plot["Predicted_Score"],
    alpha=0.7,
    label="States / UTs"
)

if not flagged.empty:
    ax2.scatter(
        flagged[target_col],
        flagged["Predicted_Score"],
        color="red",
        s=100,
        label="Red Flag States"
    )

min_val = min(df_plot[target_col].min(), df_plot["Predicted_Score"].min())
max_val = max(df_plot[target_col].max(), df_plot["Predicted_Score"].max())

ax2.plot(
    [min_val, max_val],
    [min_val, max_val],
    linestyle="--",
    linewidth=2,
    label="Ideal Prediction Line"
)

for _, row_flag in flagged.iterrows():
    ax2.text(
        row_flag[target_col] + 0.2,
        row_flag["Predicted_Score"] + 0.2,
        row_flag["State"],
        fontsize=8
    )

ax2.set_xlabel(f"Actual {target_col}")
ax2.set_ylabel("Predicted Score")
ax2.set_title("Actual vs Predicted Scores with Red Flag Detection")
ax2.legend()
st.pyplot(fig2)

# -----------------------------
# Risk Distribution Across States
# -----------------------------
st.subheader("Risk Distribution Across States")

risk_counts = df_plot["Risk_Level"].value_counts()

fig3, ax3 = plt.subplots(figsize=(7, 4))
ax3.bar(risk_counts.index, risk_counts.values)
ax3.set_xlabel("Risk Level")
ax3.set_ylabel("Number of States")
ax3.set_title("Distribution of Poverty Risk Levels")
st.pyplot(fig3)

# -----------------------------
# India Poverty Risk Map
# -----------------------------
st.subheader("India Poverty Risk Map")

map_df = df_plot.copy()

state_name_mapping = {
    "Andaman & Nicobar Islands": "Andaman and Nicobar",
    "Jammu & Kashmir": "Jammu and Kashmir",
    "NCT of Delhi": "Delhi",
    "Dadra & Nagar Haveli and Daman & Diu": "Dadra and Nagar Haveli and Daman and Diu",
    "Odisha": "Orissa"
}

map_df["State"] = map_df["State"].replace(state_name_mapping)

fig_map = px.choropleth(
    map_df,
    geojson=india_geojson,
    featureidkey="properties.NAME_1",
    locations="State",
    color="Risk_Level",
    hover_name="State",
    hover_data={
        target_col: True,
        "Predicted_Score": True,
        "Risk_Level": True
    },
    color_discrete_map={
        "Low Risk": "green",
        "Medium Risk": "yellow",
        "High Risk": "red"
    },
    title="State-wise Poverty Risk Classification"
)

fig_map.update_geos(
    fitbounds="locations",
    visible=False
)

fig_map.update_layout(
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    height=650
)

st.plotly_chart(fig_map, use_container_width=True)

# -----------------------------
# Top High-Risk States
# -----------------------------
st.subheader("Top High-Risk States")

high_risk_states = df_plot[df_plot["Risk_Level"] == "High Risk"][
    ["State", target_col, "Predicted_Score", "Red_Flag"]
]

if not high_risk_states.empty:
    st.dataframe(
        high_risk_states.sort_values(by=target_col, ascending=True).head(5),
        use_container_width=True
    )
else:
    st.info("No states currently classified as High Risk.")

# -----------------------------
# Red Flag Summary
# -----------------------------
st.subheader("Red Flag Summary")
st.dataframe(
    df_plot[["State", target_col, "Predicted_Score", "Absolute_Residual", "Red_Flag"]]
    .sort_values(by=["Red_Flag", "Absolute_Residual"], ascending=[False, False]),
    use_container_width=True
)

# -----------------------------
# Saved Red Flag States File
# -----------------------------
st.subheader("Saved Red Flag States File")

try:
    red_flag_df = pd.read_csv("red_flag_states.csv")
    st.dataframe(red_flag_df, use_container_width=True)
except FileNotFoundError:
    st.info("red_flag_states.csv not found in the folder.")

# -----------------------------
# Key insights
# -----------------------------
st.subheader("Key Insights")

top_feature = importance_df.iloc[0]["Feature"]
top_value = importance_df.iloc[0]["Importance"]

st.markdown(
    f"""
- **{top_feature}** is the strongest predictor in the model with importance score **{top_value:.3f}**.
- The dashboard classifies states into **High, Medium, and Low Risk** categories.
- States with large differences between actual and predicted scores are flagged for **further policy review**.
- The policy simulator helps estimate how improvements in literacy, sanitation, and financial inclusion may influence poverty-related outcomes.
- This system can support **poverty monitoring, anomaly detection, policy analytics, and what-if governance planning**.
"""
)