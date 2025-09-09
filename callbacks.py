import json
import time
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from components.batfish import Batfish
from components.functions import save_file, delete_old_files
from components.functions import get_traceroute_details, get_layer3_graph
from components.functions import get_ospf_graph, get_bgp_graph
from components.functions import get_traceroute_content, get_acl_content


# -------------------- Mouseover Callbacks --------------------
@app.callback(
    Output('cytoscape-mouseoverNodeData-output', 'children'),
    [Input('cytoscape', 'mouseoverNodeData')]
)
def displayTapNodeData(data):
    if data:
        return "You recently hovered over the device: " + data.get('label', '')


@app.callback(
    Output('cytoscape-mouseoverEdgeData-output', 'children'),
    [Input('cytoscape', 'mouseoverEdgeData')]
)
def displayTapEdgeData(data):
    if data:
        try:
            return f"You recently hovered over the edge between: {data['source']} {data.get('source_label', '')} and {data['target']} {data.get('target_label', '')}"
        except KeyError:
            return f"You recently hovered over the edge between: {data.get('source','')} and {data.get('target','')}"


# -------------------- Collapse Toggles --------------------
@app.callback(
    Output("batfishhost-collapse", "is_open"),
    [Input("set-batfish-host-button", "n_clicks"),
     Input("set_batfish_host_submit_button", "n_clicks")],
    [State("batfishhost-collapse", "is_open")],
)
def batfish_host_toggle_collapse(n, submit_button, is_open):
    if n or submit_button:
        return not is_open
    return is_open


@app.callback(
    Output("create-network-collapse", "is_open"),
    [Input("create-network-button", "n_clicks"),
     Input("create_network_submit_button", "n_clicks")],
    [State("create-network-collapse", "is_open")],
)
def create_network_toggle_collapse(n, submit_button, is_open):
    if n or submit_button:
        return not is_open
    return is_open


@app.callback(
    Output("create-network-collapse", "children"),
    [Input("set_batfish_host_submit_button", "n_clicks")],
)
def dummy_return(n):
    # 기존 create_network_children는 get_batfish_networks에서 처리됨
    return dash.no_update


# -------------------- Batfish Host --------------------
@app.callback(
    Output("batfish-host-output", "children"),
    [Input("batfish_host_input", "value"),
     Input("set_batfish_host_submit_button", "n_clicks")]
)
def set_batfish_host(value, n):
    ctx = dash.callback_context
    if not ctx.triggered or ctx.triggered[0]['prop_id'].split('.')[0] != "set_batfish_host_submit_button":
        raise PreventUpdate
    return value


# -------------------- Network Management --------------------
@app.callback(
    Output("batfish-network-output", "children"),
    [Input("create-network-form", "value"),
     Input("create_network_submit_button", "n_clicks")],
    [State("batfish_host_input", "value")]
)
def create_network(network_name, submit, batfish_host):
    ctx = dash.callback_context
    if not ctx.triggered or ctx.triggered[0]['prop_id'].split('.')[0] != "create_network_submit_button":
        raise PreventUpdate
    batfish = Batfish(batfish_host)
    batfish.set_network(network_name)
    return f"Network '{network_name}' created."


@app.callback(Output('delete-success', 'children'),
              [Input('delete_network_submit_button', 'n_clicks')],
              [State('delete_network_dropdown', 'value'),
               State("batfish_host_input", "value")])
def delete_network(submit, delete_network_name, batfish_host):
    ctx = dash.callback_context
    if not ctx.triggered or ctx.triggered[0]['prop_id'].split('.')[0] != "delete_network_submit_button":
        raise PreventUpdate
    batfish = Batfish(batfish_host)
    batfish.delete_network(delete_network_name)
    return f"Network '{delete_network_name}' deleted."


@app.callback(
    [Output("select-network-snapshot-modal", "children"),
     Output("select-network-div", "children"),
     Output("create-network-collapse", "children")],
    [Input("set_batfish_host_submit_button", "n_clicks"),
     Input("batfish_host_input", "value")]
)
def get_batfish_networks(n, value):
    ctx = dash.callback_context
    if not ctx.triggered or ctx.triggered[0]['prop_id'].split('.')[0] != "set_batfish_host_submit_button":
        raise PreventUpdate
    batfish = Batfish(value)
    options = [{'label': network, 'value': network} for network in batfish.get_existing_networks]

    dropdown1 = dcc.Dropdown(
        id="select-network-button",
        placeholder='Select a Network',
        className="main_page_dropdown",
        options=options,
        value=None
    )

    dropdown2 = dcc.Dropdown(
        id="modal-select-network-button",
        placeholder='Select a Network',
        style={'margin': '5px', 'width': '150px'},
        options=options,
        value=None
    )

    create_delete_network_children = [
        dbc.Form([
            dbc.FormGroup([dbc.Input(id="create-network-form", value="", placeholder="New Network Name")]),
            dbc.Button("Submit", id="create_network_submit_button", color="dark", outline=True, size="sm"),
            dcc.Dropdown(id="delete_network_dropdown", placeholder='Select a Network', options=options, value=None),
            dbc.Button("Delete", id="delete_network_submit_button", color="dark", outline=True, size="sm"),
            html.H1(id="delete-success", style={"display": "none"})
        ], inline=True)
    ]

    return dropdown2, dropdown1, create_delete_network_children


# -------------------- Snapshot / File Handling --------------------
# (원본 그대로, 단 쉼표 제거 및 ctx.triggered None 처리)
@app.callback(
    Output("select-snapshot-div", "children"),
    [Input("batfish_host_input", "value"),
     Input("select-network-button", "value")]
)
def set_batfish_snapshot(host_value, network_value):
    if not network_value:
        raise PreventUpdate
    batfish = Batfish(host_value)
    batfish.set_network(network_value)
    options = [{'label': snapshot, 'value': snapshot} for snapshot in batfish.get_existing_snapshots()]
    dropdown = dcc.Dropdown(
        id="select-snapshot-button",
        placeholder='Select Snapshot',
        className="main_page_dropdown",
        options=options,
        value=None
    )
    return dropdown
