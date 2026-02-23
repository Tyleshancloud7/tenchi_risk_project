
import pandas as pd
from tabulate import tabulate
import random
import time
import os

# -------------------
# SETUP
# -------------------

# Ensure results folder exists
os.makedirs("results", exist_ok=True)

# Load input CSV
df = pd.read_csv("data/third_party_services.csv")

# -------------------
# FUNCTIONS
# -------------------

# Normalize values to 0–100 scale
def normalize(value, min_val, max_val):
    return max(0, min(100, (value - min_val) / (max_val - min_val) * 100))

# Calculate risk scores for each service
def calculate_risk(df):
    risk_scores = []
    for _, row in df.iterrows():
        ports_count = len(str(row['exposed_ports']).split(','))
        exposed_ports_score = normalize(ports_count, 0, 10)
        ssl_score = normalize(365 - row['ssl_expiry_days'], 0, 365)
        vuln_score = normalize(row['known_vulnerabilities'], 0, 10)
        headers_score = 100 - normalize(row['security_headers'], 0, 5)

        total_risk = (
            0.3 * exposed_ports_score +
            0.3 * ssl_score +
            0.3 * vuln_score +
            0.1 * headers_score
        )
        risk_scores.append(round(total_risk, 2))

    df['risk_score'] = risk_scores
    return df

# Simulate daily changes
def simulate_day(df):
    # SSL expiry decreases
    df['ssl_expiry_days'] = df['ssl_expiry_days'].apply(lambda x: max(0, x - random.randint(1,3)))
    # New vulnerabilities may appear
    df['known_vulnerabilities'] = df['known_vulnerabilities'].apply(lambda x: x + random.randint(0,1))
    return df

# -------------------
# 7-DAY MONITORING LOOP
# -------------------

for day in range(1, 8):
    print(f"\n📅 Day {day} Monitoring Results\n")

    df = simulate_day(df)
    df = calculate_risk(df)

    # Print full table
    print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

    # Highlight high-risk services
    high_risk = df[df['risk_score'] > 50]
    if not high_risk.empty:
        print("\n⚠️ High-Risk Services:")
        print(tabulate(high_risk, headers='keys', tablefmt='pretty', showindex=False))

    # Save CSV for the day
    df.to_csv(f"results/day_{day}.csv", index=False)

    time.sleep(1)  # optional pause between days
