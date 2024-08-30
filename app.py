import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objs as go

# Generate sample data
data = {
    'Date': pd.date_range(start='2024-01-01', periods=100, freq='D'),
    'Sales': np.random.randint(100, 200, size=100)
}
df = pd.DataFrame(data)
df.set_index('Date', inplace=True)

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout with dropdown and date picker
app.layout = html.Div([
    dcc.Dropdown(
        id='metric-dropdown',
        options=[
            {'label': 'Sales', 'value': 'Sales'},
            {'label': 'Another Metric', 'value': 'Sales'},  # You can add more metrics as needed
        ],
        value='Sales'
    ),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=df.index.min(),
        end_date=df.index.max(),
        display_format='YYYY-MM-DD'
    ),
    dcc.Graph(id='sales-graph')
])

# Callback function to update the graph based on user input
@app.callback(
    Output('sales-graph', 'figure'),
    [Input('metric-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graph(selected_metric, start_date, end_date):
    # Filter the dataframe based on the selected date range
    filtered_df = df.loc[start_date:end_date]

    # Create a Plotly figure
    fig = go.Figure()

    # Add a line plot to the figure
    fig.add_trace(go.Scatter(
        x=filtered_df.index,
        y=filtered_df[selected_metric],
        mode='lines+markers',
        name=selected_metric
    ))

    # Update the layout of the figure
    fig.update_layout(
        title=f'Daily {selected_metric} Over Time',
        xaxis_title='Date',
        yaxis_title=selected_metric,
        template='plotly'
    )

    # Return the figure to be rendered in the dcc.Graph component
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
