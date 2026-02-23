import pandas as pd
import plotly.express as px
import os

# Load all daily CSVs
dfs = []
for day in range(1, 8):
    file_path = f"results/day_{day}.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df['day'] = day
        dfs.append(df)

# Combine into one dataframe
all_data = pd.concat(dfs)

# Add a color column based on risk score
all_data['color'] = all_data['risk_score'].apply(lambda x: 'High Risk (>50)' if x > 50 else 'Normal')

# ---------------------------
# Risk Trend Line Chart
# ---------------------------
fig = px.line(
    all_data,
    x='day',
    y='risk_score',
    color='service_name',
    line_dash='color',  # Different line style for high-risk
    markers=True,
    title="7-Day Third-Party Risk Monitoring"
)

# Highlight high-risk points in red
for service in all_data['service_name'].unique():
    service_data = all_data[all_data['service_name'] == service]
    fig.add_scatter(
        x=service_data['day'],
        y=service_data['risk_score'],
        mode='markers',
        marker=dict(
            color=service_data['risk_score'].apply(lambda x: 'red' if x > 50 else 'blue'),
            size=10
        ),
        name=f"{service} points",
        showlegend=False
    )

# Layout tweaks
fig.update_layout(
    xaxis_title="Day",
    yaxis_title="Risk Score",
    yaxis=dict(range=[0, 100])
)

fig.show()
