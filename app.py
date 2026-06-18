from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "f1_laptime_bundle.pkl"

FEATURE_COLUMNS = [
    "Driver",
    "LapNumber",
    "Position",
    "Sector1Time",
    "Sector2Time",
    "Sector3Time",
    "MaxSpeed",
    "Compound",
]

NUMERIC_COLUMNS = [
    "LapNumber",
    "Position",
    "Sector1Time",
    "Sector2Time",
    "Sector3Time",
    "MaxSpeed",
]

CATEGORICAL_COLUMNS = ["Driver", "Compound"]

app = Flask(__name__)


def load_bundle():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "No se encontro 'f1_laptime_bundle.pkl'. "
            "Ejecuta primero 'exportar_modelo_f1.py' o la celda equivalente en tu notebook."
        )
    return joblib.load(MODEL_PATH)


def build_input_dataframe(form_data):
    row = {column: form_data.get(column, "").strip() for column in FEATURE_COLUMNS}

    for column in NUMERIC_COLUMNS:
        if row[column] == "":
            raise ValueError(f"El campo '{column}' es obligatorio.")
        row[column] = float(row[column])

    for column in CATEGORICAL_COLUMNS:
        if row[column] == "":
            raise ValueError(f"El campo '{column}' es obligatorio.")

    return pd.DataFrame([row], columns=FEATURE_COLUMNS)


@app.route("/")
def home():
    model_ready = MODEL_PATH.exists()
    return render_template("formulario.html", model_ready=model_ready)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        bundle = load_bundle()
        data_df = build_input_dataframe(request.form)

        encoder = bundle["encoder"]
        data_df[CATEGORICAL_COLUMNS] = encoder.transform(data_df[CATEGORICAL_COLUMNS].astype(str))

        prediction = bundle["model"].predict(data_df)[0]

        return jsonify(
            {
                "prediccion_laptime": round(float(prediction), 3),
                "unidad": "segundos",
            }
        )
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    app.run(debug=True)
