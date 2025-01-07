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



# Create Dash app

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Initialise the Dash app
app = Dash()

# Custom color scheme
colors = {
    'background': '#1f1f1f',  # Dark background
    'text': '#e4e4e4',  # Light text color
    'accent': '#f39c12',  # Accent color (yellow/orange)
    'plot_bg': '#2a2a2a',  # Plot background (darker)
    'grid_color': '#444444',  # Grid line color
}

# Create the line chart
def create_line_chart(filtered_df):
    fig = px.line(
        filtered_df,
        x="date",
        y="sales",
        title="Pink Morsel Sales Over Time",
        labels={"sales": "Sales ($)", "date": "Date"},
        line_shape="linear"
    )

    # Update chart layout with custom colors and style
    fig.update_layout(
        plot_bgcolor=colors['plot_bg'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        title_font=dict(size=24, family='Arial', color=colors['accent']),
        xaxis=dict(showgrid=True, gridcolor=colors['grid_color']),
        yaxis=dict(showgrid=True, gridcolor=colors['grid_color']),
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis_title='Date',
        yaxis_title='Sales ($)'
    )
    return fig

# App layout
app.layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '20px'}, children=[
    # Heading with style
    html.H1(
        children='Pink Morsel Sales Visualiser',
        style={
            'textAlign': 'center',
            'color': colors['accent'],
            'fontFamily': 'Arial',
            'fontSize': '36px',
            'marginBottom': '20px'
        }
    ),
    
    # Subheading description
    html.Div(
        children='Analyze Pink Morsel Sales by Region and Date.',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'fontFamily': 'Arial',
            'fontSize': '18px',
            'marginBottom': '40px'
        }
    ),
    
    # Region selector (RadioItems)
    dcc.RadioItems(
        id="region-selector",
        options=[
            {"label": "North", "value": "north"},
            {"label": "East", "value": "east"},
            {"label": "South", "value": "south"},
            {"label": "West", "value": "west"},
            {"label": "All", "value": "all"}
        ],
        value="all",  # Default value
        labelStyle={'display': 'inline-block', 'padding': '10px', "color": "white"},
        style={"textAlign": "center", "marginBottom": "30px"}
    ),
    
    # Graph component
    dcc.Graph(
        id='sales-line-chart'
    )
])

# Define the callback to update the figure
@app.callback(
    Output('sales-line-chart', 'figure'),
    [Input('region-selector', 'value')]
)
def update_figure(selected_region):
    # Filter the dataframe based on the selected region
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"] == selected_region]  # Assuming 'region' column exists
    
    # Return the updated figure
    return create_line_chart(filtered_df)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
