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

FALLBACK_DRIVER_OPTIONS = [
    "ALO",
    "BOT",
    "COL",
    "GAS",
    "HAM",
    "HUL",
    "LAW",
    "LEC",
    "MAG",
    "NOR",
    "OCO",
    "PER",
    "PIA",
    "RUS",
    "SAI",
    "STR",
    "VER",
    "ZHO",
]

FALLBACK_COMPOUND_OPTIONS = ["HARD", "MEDIUM", "SOFT"]

DRIVER_LABELS = {
    "ALO": "Fernando Alonso",
    "BOT": "Valtteri Bottas",
    "COL": "Franco Colapinto",
    "GAS": "Pierre Gasly",
    "HAM": "Lewis Hamilton",
    "HUL": "Nico Hulkenberg",
    "LAW": "Liam Lawson",
    "LEC": "Charles Leclerc",
    "MAG": "Kevin Magnussen",
    "NOR": "Lando Norris",
    "OCO": "Esteban Ocon",
    "PER": "Sergio Perez",
    "PIA": "Oscar Piastri",
    "RUS": "George Russell",
    "SAI": "Carlos Sainz",
    "STR": "Lance Stroll",
    "VER": "Max Verstappen",
    "ZHO": "Zhou Guanyu",
}

COMPOUND_LABELS = {
    "HARD": "Duro",
    "MEDIUM": "Medio",
    "SOFT": "Blando",
}

FALLBACK_NUMERIC_EXAMPLES = {
    "LapNumber": [1, 12, 35, 55, 71],
    "Position": [1, 5, 10, 15, 20],
    "Sector1Time": [28.5, 29.0, 29.5],
    "Sector2Time": [31.5, 32.1, 32.8],
    "Sector3Time": [20.8, 21.2, 21.8],
    "MaxSpeed": [315, 329, 340],
}

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
        row[column] = row[column].upper()

    return pd.DataFrame([row], columns=FEATURE_COLUMNS)


def build_option_list(values, labels):
    return [
        {
            "value": value,
            "label": f"{value} - {labels.get(value, value)}",
        }
        for value in values
    ]


def get_form_context():
    context = {
        "model_ready": MODEL_PATH.exists(),
        "driver_options": build_option_list(FALLBACK_DRIVER_OPTIONS, DRIVER_LABELS),
        "compound_options": build_option_list(FALLBACK_COMPOUND_OPTIONS, COMPOUND_LABELS),
        "numeric_examples": FALLBACK_NUMERIC_EXAMPLES,
        "default_values": {
            "Driver": "VER",
            "Compound": "MEDIUM",
            "LapNumber": 35,
            "Position": 9,
            "Sector1Time": 28.956,
            "Sector2Time": 32.096,
            "Sector3Time": 21.23,
            "MaxSpeed": 329,
        },
    }

    if not context["model_ready"]:
        return context

    try:
        bundle = load_bundle()
        encoder = bundle["encoder"]
        context["driver_options"] = build_option_list(list(encoder.categories_[0]), DRIVER_LABELS)
        context["compound_options"] = build_option_list(list(encoder.categories_[1]), COMPOUND_LABELS)

        medians = bundle.get("numeric_medians", {})
        for column in NUMERIC_COLUMNS:
            if column in medians:
                context["default_values"][column] = round(float(medians[column]), 3)
    except Exception as exc:
        context["model_ready"] = False
        context["model_error"] = str(exc)

    return context


@app.route("/")
def home():
    return render_template("formulario.html", **get_form_context())


@app.route("/predict", methods=["POST"])
def predict():
    try:
        bundle = load_bundle()
        data_df = build_input_dataframe(request.form)

        encoder = bundle["encoder"]
        try:
            data_df[CATEGORICAL_COLUMNS] = encoder.transform(data_df[CATEGORICAL_COLUMNS].astype(str))
        except ValueError as exc:
            raise ValueError(
                "Selecciona un Driver y un Compound de la lista. "
                "El modelo solo acepta categorias vistas durante el entrenamiento."
            ) from exc

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
