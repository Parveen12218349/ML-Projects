# app.py
import streamlit as st
import pandas as pd
import joblib

# --------------------------
# Load trained model
# --------------------------
model = joblib.load("bulldozer_model.pkl")

# --------------------------
# Category maps (from training)
# --------------------------
PRODUCT_SIZE_MAP = {"Mini": 1, "Small": 2, "Medium": 3, "Large": 4, "XL": 5}
ENCLOSURE_MAP = {"EROPS": 1, "EROPS w AC": 2, "OROPS": 3, "None": 0}
TRANSMISSION_MAP = {"Standard": 1, "Hydrostatic": 2, "Powershift": 3, "None": 0}
DRIVE_SYSTEM_MAP = {"2WD": 1, "4WD": 2, "Track": 3, "None": 0}
HYDRAULICS_MAP = {"Standard": 1, "Auxiliary": 2, "High Flow": 3, "None": 0}

# --------------------------
# Streamlit UI
# --------------------------
st.title("🚜 Bulldozer Price Prediction App")
st.write("Enter bulldozer details to predict auction price:")

# Numeric inputs
YearMade = st.number_input("Year Made", min_value=1900, max_value=2025, value=2000)
MachineHoursCurrentMeter = st.number_input("Machine Hours", min_value=0, max_value=100000, value=1000)

# Categorical inputs
ProductSize = st.selectbox("Product Size", list(PRODUCT_SIZE_MAP.keys()))
Enclosure = st.selectbox("Enclosure", list(ENCLOSURE_MAP.keys()))
Transmission = st.selectbox("Transmission", list(TRANSMISSION_MAP.keys()))
Drive_System = st.selectbox("Drive System", list(DRIVE_SYSTEM_MAP.keys()))
Hydraulics = st.selectbox("Hydraulics", list(HYDRAULICS_MAP.keys()))
state = st.selectbox("State", ["TX", "CA", "FL", "NY", "Other"])  # keep short list for demo

# --------------------------
# Prepare input for model
# --------------------------
if st.button("Predict Price"):
    input_dict = {
        "YearMade": YearMade,
        "MachineHoursCurrentMeter": MachineHoursCurrentMeter,
        "ProductSize": PRODUCT_SIZE_MAP[ProductSize],
        "Enclosure": ENCLOSURE_MAP[Enclosure],
        "Transmission": TRANSMISSION_MAP[Transmission],
        "Drive_System": DRIVE_SYSTEM_MAP[Drive_System],
        "Hydraulics": HYDRAULICS_MAP[Hydraulics],
        "state": hash(state) % 100  # simple numeric encoding for demo
    }

    input_df = pd.DataFrame([input_dict])

    # Align columns with model
    for col in model.feature_names_in_:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[model.feature_names_in_]

    # Predict
    prediction = model.predict(input_df)[0]
    st.success(f"💰 Predicted Bulldozer Price: ${prediction:,.2f}")
