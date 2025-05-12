import streamlit as st

st.set_page_config(page_title="Aviation Unit Converter", page_icon="✈️")

with st.sidebar:
    theme = st.radio("🌗 Theme", ["Light", "Dark"], horizontal=True)

if theme == "Dark":
    st.markdown("""
        <style>
        .stApp {
            background-color: #1e1e1e;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
            <style>
            .stApp {
                background-color: #f9f9f9;
                color: black;
            }
            </style>
        """, unsafe_allow_html=True)


st.markdown("""
    <style>
    button[kind="secondary"] {
        background-color: #FF4B4B !important;
        color: white !important;
        border: none !important;
        border-radius: 6px;
        padding: 0.4em 1em;
        font-weight: bold;
    }

    button[kind="secondary"]:hover {
        background-color: #cc0000 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
Aviation Unit Converter Web App
----------------------------

This Python application provides a graphical interface (Tkinter) to convert between 
various aviation-related units including Length, Weight, Torque, Pressure, Temperature, 
Speed, Fuel Flow, and Volume.

- Developed by: Ergin SABANCI  -  github/erginsa
- Designed for: Aircraft Maintenance and Aviation Professionals
- Fuel Flow conversions are based on standard values for **JET-A1 fuel**.
  (e.g., 1 US gallon ≈ 6.7 lbs JET-A1, 1 liter ≈ 0.8 kg)

Note:
- Temperature conversion is handled separately from the fixed rate dictionary.
- All fields are readonly dropdowns to ensure input consistency.

""")

st.title("✈️ Aviation Unit Converter")
st.markdown("This tool allows aviation-specific unit conversions. Fuel flow calculations are based on **JET-A1** fuel density.")

# ------------------------ #
#     Conversion Logic     #
# ------------------------ #

conversion_rates = {
    "Length": {
        "meters": {"feet": 3.281, "inches": 39.3701, "millimeters": 1000},
        "feet": {"meters": 0.3048, "inches": 12, "millimeters": 304.8},
        "inches": {"meters": 0.0254, "feet": 0.0833, "millimeters": 25.4},
        "millimeters": {"meters": 0.001, "feet": 0.003281, "inches": 0.03937},
    },
    "Weight": {
        "kilograms": {"pounds": 2.205, "grams": 1000},
        "pounds": {"kilograms": 0.453592, "grams": 453.6},
        "grams": {"kilograms": 0.001, "pounds": 0.00220462},
    },
    "Torque": {
        "Nm": {"lbf·ft": 0.7376, "in·lb": 8.8507, "daN·m": 0.1},
        "lbf·ft": {"Nm": 1.35582, "in·lb": 12, "daN·m": 0.4448221615},
        "in·lb": {"Nm": 0.11298483, "lbf·ft": 0.08333, "daN·m": 0.01129848},
        "daN·m": {"Nm": 10, "lbf·ft": 2.248089431, "in·lb": 88.507},
    },
    "Pressure": {
        "psi": {"bar": 0.0689476, "kPa": 6.89476, "inHg": 2.03602},
        "bar": {"psi": 14.5038, "kPa": 100, "inHg": 29.53},
        "kPa": {"psi": 0.145038, "bar": 0.01, "inHg": 0.2953},
        "inHg": {"psi": 0.491154, "bar": 0.0338639, "kPa": 3.38639},
    },
    "Speed": {
        "knots": {"km/h": 1.852, "m/s": 0.514444},
        "km/h": {"knots": 0.539957, "m/s": 0.277778},
        "m/s": {"knots": 1.94384, "km/h": 3.6},
    },
    "Fuel Flow (JET-A1)": {
        "PPH": {"KPH": 0.453592, "GPH": 0.1198264, "L/h": 0.2041},
        "KPH": {"PPH": 2.20462, "GPH": 0.330215, "L/h": 1.25},
        "GPH": {"PPH": 8.35, "KPH": 3.02833, "L/h": 3.78541},
        "L/h": {"PPH": 4.899, "KPH": 0.8, "GPH": 0.264172},
    },
    "Volume": {
        "liters": {"gallons": 0.264172, "quarts": 1.05669},
        "gallons": {"liters": 3.78541, "quarts": 4},
        "quarts": {"liters": 0.946353, "gallons": 0.25},
    },
    "Temperature": {},  # Handled separately
}

def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value

    if from_unit == "Celsius":
        if to_unit == "Fahrenheit":
            return (value * 9 / 5) + 32
        elif to_unit == "Kelvin":
            return value + 273.15

    elif from_unit == "Fahrenheit":
        if to_unit == "Celsius":
            return (value - 32) * 5 / 9
        elif to_unit == "Kelvin":
            return (value - 32) * 5 / 9 + 273.15

    elif from_unit == "Kelvin":
        if to_unit == "Celsius":
            return value - 273.15
        elif to_unit == "Fahrenheit":
            return (value - 273.15) * 9 / 5 + 32

    return None

# ------------------------ #
#     Streamlit Layout     #
# ------------------------ #

category = st.selectbox("Select a category", list(conversion_rates.keys()))

if category == "Temperature":
    units = ["Celsius", "Fahrenheit", "Kelvin"]
else:
    units = list(conversion_rates[category].keys())

col1, col2, col3 = st.columns([1.5, 1, 1.5])

with col1:
    from_unit = st.selectbox("From unit", units, key="from_unit", index=0)
with col2:
    value = st.number_input("Enter value", min_value=0.0, step=0.01, format="%.2f", key="input_value")
with col3:
    to_unit = st.selectbox("To unit", [u for u in units if u != st.session_state.from_unit], key="to_unit", index=1 if len(units) > 1 else 0)


# Initialize session state history
if "history" not in st.session_state:
    st.session_state.history = []

# Single Convert Button with History

convert_clicked = st.button("Convert", key="convert_button")


# Convert Logic
if convert_clicked:
    if category == "Temperature":
        result = convert_temperature(value, from_unit, to_unit)
    else:
        try:
            result = value * conversion_rates[category][from_unit][to_unit]
        except KeyError:
            result = None

    if result is not None:
        st.success(f"Result: {round(result, 4)} {to_unit}")
        st.session_state.history.append(
            f"{value} {from_unit} → {round(result, 4)} {to_unit} ({category})"
        )
    else:
        st.error("Conversion not available for selected units.")


# Show history
if st.session_state.history:
    st.markdown("### 🔁 Conversion History")
    for entry in reversed(st.session_state.history[-10:]):
        st.write(f"- {entry}")
