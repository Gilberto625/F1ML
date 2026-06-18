import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder


DATA_URL = "https://raw.githubusercontent.com/Gilberto625/F1MExico/refs/heads/main/Mexico2024.csv"
OUTPUT_PATH = "f1_laptime_bundle.pkl"

CATEGORICAL_COLUMNS = ["Driver", "Compound"]
TARGET_COLUMN = "LapTime"


def main():
    data = pd.read_csv(DATA_URL)

    data = data.dropna(subset=[TARGET_COLUMN]).reset_index(drop=True)

    numeric_cols = data.select_dtypes(include="number").columns.drop(TARGET_COLUMN)
    numeric_medians = data[numeric_cols].median()
    data[numeric_cols] = data[numeric_cols].fillna(numeric_medians)

    encoder = OrdinalEncoder()
    data[CATEGORICAL_COLUMNS] = encoder.fit_transform(data[CATEGORICAL_COLUMNS].astype(str))

    X = data.drop(columns=[TARGET_COLUMN])
    y = data[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    bundle = {
        "model": model,
        "encoder": encoder,
        "feature_columns": list(X.columns),
        "numeric_medians": numeric_medians.to_dict(),
        "categorical_columns": CATEGORICAL_COLUMNS,
        "target_column": TARGET_COLUMN,
        "metrics": {
            "r2": float(r2_score(y_test, y_pred)),
            "mae": float(mean_absolute_error(y_test, y_pred)),
        },
    }

    joblib.dump(bundle, OUTPUT_PATH)

    print(f"Modelo exportado en: {OUTPUT_PATH}")
    print(f"R2 final: {bundle['metrics']['r2']:.4f}")
    print(f"MAE final: {bundle['metrics']['mae']:.4f}")
    print("Variables esperadas:", ", ".join(bundle["feature_columns"]))


if __name__ == "__main__":
    main()
