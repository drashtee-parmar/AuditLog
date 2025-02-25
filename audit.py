import os

import pandas as pd
from flask import Flask, jsonify

# Define categories
CATEGORIES = [
    "Account",
    "Advisory Credit",
    "Billing",
    "Security",
    "Transactions"
]


# Create a local directory to store audit logs
def create_local_repo():
    repo_path = "./audit_logs_repository"
    os.makedirs(repo_path, exist_ok=True)
    return repo_path


# Fetch Audit Logs (Simulated Data)
def fetch_audit_logs():
    logs = [
        {"action": "account.created", "actor": "user1", "timestamp": "2025-02-24T12:00:00Z"},
        {"action": "advisory.credit.issued", "actor": "admin", "timestamp": "2025-02-24T12:10:00Z"},
        {"action": "billing.invoice.paid", "actor": "user2", "timestamp": "2025-02-24T12:20:00Z"},
        {"action": "security.password.changed", "actor": "user3", "timestamp": "2025-02-24T12:30:00Z"},
        {"action": "transactions.payment.processed", "actor": "user4", "timestamp": "2025-02-24T12:40:00Z"}
    ]
    return logs


# Preprocess Logs and Categorize
def preprocess_logs(logs):
    df = pd.DataFrame(logs)
    df.fillna("unknown", inplace=True)
    df["category"] = df["action"].apply(lambda x: classify_category(x))
    return df


# Function to classify log events based on categories
def classify_category(action):
    if "account" in action:
        return "Account"
    elif "advisory.credit" in action:
        return "Advisory Credit"
    elif "billing" in action:
        return "Billing"
    elif "security" in action:
        return "Security"
    elif "transactions" in action:
        return "Transactions"
    else:
        return "Uncategorized"


# Save logs to Excel grouped by categories
def save_logs_to_excel(df):
    file_path = "audit_logs_categorized.xlsx"
    with pd.ExcelWriter(file_path) as writer:
        for category in CATEGORIES:
            df_category = df[df["category"] == category]
            df_category.to_excel(writer, sheet_name=category, index=False)
    print(f"Logs categorized and saved to {file_path}")
    return file_path


# API for Audit Log Monitoring
app = Flask(__name__)


@app.route('/audit_logs', methods=['GET'])
def get_logs():
    logs = fetch_audit_logs()
    df = preprocess_logs(logs)
    save_logs_to_excel(df)
    return jsonify(df.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)
