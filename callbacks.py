from dash import Input, Output, State
from layouts import app  # layouts.py에서 app import

# Batfish Host Collapse toggle
@app.callback(
    Output("batfishhost-collapse", "is_open"),
    Input("set-batfish-host-button", "n_clicks"),
    State("batfishhost-collapse", "is_open")
)
def toggle_batfish_host(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Create Network Collapse toggle
@app.callback(
    Output("create-network-collapse", "is_open"),
    Input("create-network-button", "n_clicks"),
    State("create-network-collapse", "is_open")
)
def toggle_create_network(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Batfish Host submit
@app.callback(
    Output('batfish-host-output', 'children'),
    Input('set_batfish_host_submit_button', 'n_clicks'),
    State('batfish_host_input', 'value')
)
def submit_batfish_host(n_clicks, value):
    if n_clicks:
        return str(value)
    return ""

# Create Network submit
@app.callback(
    Output('batfish-network-output', 'children'),
    Input('create_network_submit_button', 'n_clicks')
)
def submit_create_network(n_clicks):
    if n_clicks:
        return "Network created!"
    return ""

# Tabs content callback
@app.callback(
    Output('main-page-tabs-content', 'children'),
    Input('main-page-tabs', 'value')
)
def render_tab_content(tab_value):
    return f"You selected {tab_value} tab."
