# Prepare data

import pandas as pd

# Load and process data
data_file = "data/soul_data.csv"
df = pd.read_csv(data_file)

# Ensure sales is numerical
df["sales"] = df["sales"].str.replace("$", "", regex=False).str.replace(",", "").astype(float)

# Convert date to datetime
df["date"] = pd.to_datetime(df["date"])

# Sort data by date
df = df.sort_values(by="date")



#Create Dash app

from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = Dash()

# Create the line graph
fig = px.line(
    df,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={"sales": "Sales ($)", "date": "Date"},
    line_shape="linear"
)

# Add a layout to the app
app.layout = html.Div([
    html.H1("Pink Morsel Sales Visualiser", style={"textAlign": "center"}),

    dcc.Graph(
        id='sales-line-chart',
        figure=fig
    )
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
