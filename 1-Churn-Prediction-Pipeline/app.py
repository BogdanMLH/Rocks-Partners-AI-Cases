from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="Casino Churn Prediction API")

model         = joblib.load("churn_model.joblib")
loaded_scaler = joblib.load("scaler.joblib")

# Risk threshold
# Raise toward 0.5 to reduce false positives, lower to be more aggressive
CHURN_THRESHOLD = 0.35


class Player(BaseModel):
    player_ID:                  int
    Average_Monthly_Deposit:    float
    Months_Since_Registration:  int
    Lifetime_Value:             float


@app.post("/predict")
def predict(player: Player):

    # Build DataFrame
    player_data = pd.DataFrame([{
        'Average_Monthly_Deposit':   player.Average_Monthly_Deposit,
        'Months_Since_Registration': player.Months_Since_Registration,
        'Lifetime_Value':            player.Lifetime_Value,
    }])

    # Engineer the same features computed during training
    player_data['Spend_Per_Month']  = (
        player_data['Lifetime_Value'] / (player_data['Months_Since_Registration'] + 1)
    )
    player_data['Monthly_vs_Total'] = (
        player_data['Average_Monthly_Deposit'] / (player_data['Lifetime_Value'] + 1)
    )

    # Scale and predict
    scaled_data   = loaded_scaler.transform(player_data)
    probabilities = model.predict_proba(scaled_data)
    churn_risk    = probabilities[0][1]

    risk_label = "HIGH" if churn_risk >= CHURN_THRESHOLD else "LOW"

    return {
        'player_ID':      player.player_ID,
        'churn_risk':     round(churn_risk, 2),
        'lifetime_Value': player.Lifetime_Value,
        'risk_label':     risk_label,
        'threshold_used': CHURN_THRESHOLD
    }