# Tenchi Third-Party Risk Monitoring Project

This project simulates a **7-day monitoring of third-party services** to track cyber risk scores. It is inspired by Tenchi's focus on **Third-Party Cyber Risk Management (TPCRM)**.

## Project Features

- Simulates changes in:
  - Exposed ports
  - SSL expiry
  - Known vulnerabilities
  - Security headers
- Calculates **weighted risk scores** for each service
- Highlights high-risk services (`risk_score > 50`)
- Saves daily CSVs in `results/`
- Provides an **interactive Plotly dashboard** to visualize trends

## Folder Structure

