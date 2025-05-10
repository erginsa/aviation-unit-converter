import tkinter as tk
from tkinter import ttk, messagebox

"""
Aviation Unit Converter GUI
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

"""

FONT = ("Arial", 15)

conversion_rates = {
    "Length": {
        "meters": {
            "feet": 3.281,
            "inches": 39.3701,
            "millimeters": 1000
        },
        "feet": {
            "meters": 0.3048,
            "inches": 12,
            "millimeters": 304.8
        },
        "inches": {
            "meters": 0.0254,
            "feet": 0.0833,
            "millimeters": 25.4
        },
        "millimeters": {
            "meters": 0.001,
            "feet": 0.003281,
            "inches": 0.03937
        }
    },
    "Weight": {
        "kilograms": {
            "pounds": 2.205,
            "grams": 1000
        },
        "pounds": {
            "kilograms": 0.453592,
            "grams": 453.6
        },
        "grams": {
            "kilograms": 0.001,
            "pounds": 0.00220462
        }
    },
    "Torque": {
        "Nm": {
            "lbf·ft": 0.7376,
            "in·lb": 8.8507,
            "daN·m": 0.1
        },
        "lbf·ft": {
            "Nm": 1.35582,
            "in·lb": 12,
            "daN·m": 0.4448221615
        },
        "in·lb": {
            "Nm": 0.11298483,
            "lbf·ft": 0.08333,
            "daN·m": 0.01129848
        },
        "daN·m": {
            "Nm": 10,
            "lbf·ft": 2.248089431,
            "in·lb": 88.507
        }
    },
    "Pressure": {
        "psi": {
            "bar": 0.0689476,
            "kPa": 6.89476,
            "inHg": 2.03602
        },
        "bar": {
            "psi": 14.5038,
            "kPa": 100,
            "inHg": 29.53
        },
        "kPa": {
            "psi": 0.145038,
            "bar": 0.01,
            "inHg": 0.2953
        },
        "inHg": {
            "psi": 0.491154,
            "bar": 0.0338639,
            "kPa": 3.38639
        }
    },
    "Speed": {
        "knots": {
            "km/h": 1.852,
            "m/s": 0.514444,
        },
        "km/h": {
            "knots": 0.539957,
            "m/s": 0.277778
        },
        "m/s": {
            "knots": 1.94384,
            "km/h": 3.6
        }
    },
    "Fuel Flow": {
        "PPH": {
            "KPH": 0.453592,
            "GPH": 0.1198264,
            "L/h": 0.2041
        },
        "KPH": {
            "PPH": 2.20462,
            "GPH": 0.330215,
            "L/h": 1.25
        },
        "GPH": {
            "PPH": 8.35,
            "KPH": 3.02833,
            "L/h": 3.78541
        },
        "L/h": {
            "PPH": 4.899,
            "KPH": 0.8,
            "GPH": 0.264172
        }
    },
    "Volume": {
        "liters": {"gallons": 0.264172, "quarts": 1.05669},
        "gallons": {"liters": 3.78541, "quarts": 4},
        "quarts": {"liters": 0.946353, "gallons": 0.25}
    }
}

units_dict = {
    "Length": ["meters", "feet", "inches", "millimeters"],
    "Weight": ["kilograms", "pounds", "grams"],
    "Torque": ["Nm", "lbf·ft", "in·lb", "daN·m"],
    "Pressure": ["psi", "bar", "kPa", "inHg"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Speed": ["knots", "km/h", "m/s"],
    "Fuel Flow": ["PPH", "KPH", "GPH", "L/h"],
    "Volume": ["liters", "gallons", "quarts"]
}


def convert_temperatures(value, from_unit, to_unit):
    if from_unit == "Celsius" and to_unit == "Fahrenheit":
        return (value * 9 / 5) + 32
    elif from_unit == "Fahrenheit" and to_unit == "Celsius":
        return (value - 32) * 5 / 9
    elif from_unit == "Celsius" and to_unit == "Kelvin":
        return value + 273.15
    elif from_unit == "Kelvin" and to_unit == "Celsius":
        return value - 273.15
    elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
        return (value - 32) * 5 / 9 + 273.15
    elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
        return (value - 273.15) * 9 / 5 + 32
    elif from_unit == to_unit:
        return value
    else:
        return None


def only_float(char):
    return char.isdigit() or char == "."


def update_units(event):
    category = current_var.get()

    if category == "Temperature":
        units = ["Celsius", "Fahrenheit", "Kelvin"]
    elif category in conversion_rates:
        units = list(conversion_rates[category].keys())
    else:
        units = []

    from_unit_combobox["values"] = units
    to_unit_combobox["values"] = units
    from_unit_var.set(units[0] if units else "")
    to_unit_var.set(units[1] if len(units) > 1 else "")


def calculate_conversion():
    try:
        value = float(user_input_entry.get())
        category = current_var.get()
        from_unit = from_unit_var.get()
        to_unit = to_unit_var.get()

        result = None

        if category == "Temperature":
            result = convert_temperatures(value, from_unit, to_unit)

        elif category in conversion_rates:
            if from_unit in conversion_rates[category] and to_unit in conversion_rates[category][from_unit]:
                factor = conversion_rates[category][from_unit][to_unit]
                result = value * factor
            elif from_unit == to_unit:
                result = value
            else:
                result_label2.config(text="Conversion not defined")
                return

        else:

            result_label2.config(text="Invalid category")
            return

        result_label2.config(text=f"{round(result, 4)} {to_unit}")
        user_input_entry.config(bg="white")

    except ValueError:
        user_input_entry.config(bg="misty rose")
        messagebox.showerror("Invalid Input", "Please enter integer or float number.")


window = tk.Tk()
window.title("Ergin's Aviation Converter")
window.config(width=600, height=400, bg="linen", padx=50, pady=50)
window.resizable(False, False)

# Just only float
vcdm = (window.register(only_float), "%S")

# Main Frame
main_frame = tk.Frame(bg="linen")
main_frame.grid()

# Labels
category_choose_label = tk.Label(main_frame, text="Choose a Category", font=FONT, bg="linen")
category_choose_label.grid(row=1, column=1)

unit_label = tk.Label(main_frame, text="Unit:", bg="old lace", font=FONT, anchor="e")
unit_label.grid(row=2, column=0, sticky="e")

from_label = tk.Label(main_frame, text="From Unit:", bg="old lace", font=FONT, anchor="e")
from_label.grid(row=3, column=0, sticky="e")

to_label = tk.Label(main_frame, text="To Unit:", bg="old lace", font=FONT, anchor="e")
to_label.grid(row=5, column=0, sticky="e")

result_label1 = tk.Label(main_frame, text="Result:", bg="old lace", font=FONT, anchor="e")
result_label1.grid(row=7, column=0, sticky="e")

result_label2 = tk.Label(main_frame, text="0", bg="old lace", font=("Arial", 20), width=15)
result_label2.grid(row=7, column=1)

# Combobox for Category
current_var = tk.StringVar()
combobox = ttk.Combobox(main_frame, textvariable=current_var, font=FONT, state="readonly")
combobox["values"] = ("Length", "Weight", "Torque", "Pressure", "Temperature", "Speed", "Fuel Flow", "Volume")
combobox.grid(row=2, column=1, pady=5)
combobox.bind("<<ComboboxSelected>>", update_units)

from_unit_var = tk.StringVar()
from_unit_combobox = ttk.Combobox(main_frame, textvariable=from_unit_var, font=FONT, state="readonly")
from_unit_combobox.grid(row=3, column=1)

to_unit_var = tk.StringVar()
to_unit_combobox = ttk.Combobox(main_frame, textvariable=to_unit_var, font=FONT, state="readonly")
to_unit_combobox.grid(row=5, column=1)

# Button
calculate_button = tk.Button(main_frame, text="Calculate", font=FONT, relief="raised", command=calculate_conversion)
calculate_button.grid(row=6, column=1, pady=5)

# Entry
user_input_entry = tk.Entry(main_frame, font=FONT, width=12, justify="right")
user_input_entry.insert(0, "0")
user_input_entry.grid(row=4, column=1, pady=5, sticky="e")
user_input_entry.config(validate="key", validatecommand=vcdm)  # for only_float function

window.mainloop()
