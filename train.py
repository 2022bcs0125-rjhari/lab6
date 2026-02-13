import json, joblib
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

# ---------------- INFO ----------------
NAME = "R J Hari"
ROLL = "2022BCS0125"

# ---------------- PATHS ----------------
DATA_PATH = "dataset/winequality-red.csv"

OUTPUT_DIR = Path("app/artifacts")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = OUTPUT_DIR / "model.pkl"
RESULTS_PATH = OUTPUT_DIR / "metrics.json"


# ---------------- LOAD DATA ----------------
data = pd.read_csv(DATA_PATH, sep=";")
X = data.drop("quality", axis=1)
y = data["quality"]

# ---------------- SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ===============================
# 🔴 EXPERIMENT-SPECIFIC CODE HERE
# ===============================
from sklearn.linear_model import Ridge

EXP_ID = "EXP-01"
MODEL_NAME = "Ridge Regression (alpha=1.0)"

scaler = StandardScaler()
X_train_proc = scaler.fit_transform(X_train)
X_test_proc = scaler.transform(X_test)

model = Ridge(alpha=1.0)






# ---------------- TRAIN ----------------
model.fit(X_train_proc, y_train)

# ---------------- EVAL ----------------
y_pred = model.predict(X_test_proc)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# ---------------- SAVE ----------------
joblib.dump(model, MODEL_PATH)

results = {
    "experiment": EXP_ID,
    "model": MODEL_NAME,
    "mse": mse,
    "r2_score": r2
}

with open(RESULTS_PATH, "w") as f:
    json.dump(results, f, indent=4)

print("Name:", NAME)
print("Roll:", ROLL)
print("MSE:", mse)
print("R2:", r2)











