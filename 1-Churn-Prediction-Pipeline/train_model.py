import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler

# Load dataset
# Only keeping columns that map cleanly to casino domain concepts
db = pd.read_csv('data.csv')

db = db.rename(columns={
    'MonthlyCharges': 'Average_Monthly_Deposit',
    'tenure':         'Months_Since_Registration',
    'TotalCharges':   'Lifetime_Value',
    'Churn':          'Will_Churn'
})

# Fix Lifetime_Value
db['Lifetime_Value'] = pd.to_numeric(db['Lifetime_Value'], errors='coerce')
db = db.dropna()

# Engineer features that make real sense in a casino context
db['Spend_Per_Month']  = db['Lifetime_Value'] / (db['Months_Since_Registration'] + 1)
db['Monthly_vs_Total'] = db['Average_Monthly_Deposit'] / (db['Lifetime_Value'] + 1)

# Only casino-meaningful features
X = db[['Average_Monthly_Deposit', 'Months_Since_Registration', 'Lifetime_Value',
        'Spend_Per_Month', 'Monthly_vs_Total']]

y = db['Will_Churn'].map({'Yes': 1, 'No': 0})

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Stratified split — preserves churn ratio in both sets
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# Train
model = RandomForestClassifier(
    n_estimators=200,
    class_weight='balanced',
    random_state=42
)
model.fit(X_train, y_train)

# Save
joblib.dump(model,  'churn_model.joblib')
joblib.dump(scaler, 'scaler.joblib')

# Evaluate
predictions = model.predict(X_test)
print("\n--- Results ---")
print(f"Accuracy: {accuracy_score(y_test, predictions):.2f}")
print("\nDetailed summary:")
print(classification_report(y_test, predictions))
print("\nSaved: churn_model.joblib | scaler.joblib")