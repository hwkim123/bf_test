import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

main_page_graph_tab_selected = dict(
    padding='10px 20px',
    backgroundColor='#555555',
    color='#fff',
    borderBottom='none',
    borderTop='none',
    fontWeight='bold',
)

main_page_layout = html.Div(id='main-page', children=[

    # Title Bar
    html.Div(
        id='title-bar-div',
        children=[
            html.Header(
                id='title-bar',
                children=[
                    html.H1('Batfish Dashboard', id='title-bar-text')
                ]
            )
        ]
    ),
    html.Br(),

    # Buttons & Inputs
    html.Div(
        style={'position': 'relative', 'left': '7px'},
        children=[
            html.Div([html.Button("Set Batfish Host", id="set-batfish-host-button", className="main_page_button")],
                     className="main_page_button_div"),
            html.Div([html.Button("Create/Delete Network", id="create-network-button", className="main_page_button")],
                     className="main_page_button_div"),
            html.Div([html.Button("Create/Delete Snapshot", id="create-snapshot-button", className="main_page_button")],
                     className="main_page_button_div"),
            html.Div([], className="main_page_button_div", id='select-network-div'),
            html.Div([], className="main_page_button_div", id='select-snapshot-div'),
            html.Div([html.Button("Ask a Question", id="ask-question-button", className="main_page_button")],
                     className="main_page_button_div"),

            # Batfish Host Collapse
            html.Div(
                style=dict(width="1000px"),
                children=[
                    dbc.Collapse(
                        dbc.Card(
                            className='main_page_card',
                            children=[
                                dbc.CardBody(
                                    children=[
                                        dbc.Form(
                                            [
                                                dbc.FormGroup(
                                                    [
                                                        dbc.Input(
                                                            id="batfish_host_input",
                                                            value="",
                                                            placeholder="Enter host",
                                                            persistence=True,
                                                        ),
                                                    ],
                                                    className="mr-3",
                                                ),
                                                dbc.Button(
                                                    "Submit",
                                                    id="set_batfish_host_submit_button",
                                                    color="dark",
                                                    outline=True,
                                                    size="sm",
                                                    style=dict(height="25px"),
                                                ),
                                            ],
                                            inline=True,
                                        )
                                    ]
                                )
                            ],
                        ),
                        id="batfishhost-collapse",
                    ),
                    dbc.Collapse(
                        dbc.Card(
                            className='main_page_card',
                            children=[dbc.CardBody(children=[])],
                        ),
                        id="create-network-collapse",
                    ),
                ],
            ),

            dcc.Store(id='memory-output'),
        ],
    ),

    # Tabs & Content
    html.Div(
        style={'position': 'relative', 'left': '10px', 'display': 'flex'},
        children=[
            html.Div(
                style=dict(width="1000px", flex="1"),
                children=[
                    dcc.Tabs(id='main-page-tabs', value='layer3',
                             children=[
                                 dcc.Tab(selected_style=main_page_graph_tab_selected, className='main-page-graph-tab',
                                         id={'type': 'main_tabs', 'index': 0}, label='Layer 3', value='layer3'),
                                 dcc.Tab(selected_style=main_page_graph_tab_selected, className='main-page-graph-tab',
                                         id={'type': 'main_tabs', 'index': 1}, label='OSPF', value='ospf'),
                                 dcc.Tab(selected_style=main_page_graph_tab_selected, className='main-page-graph-tab',
                                         id={'type': 'main_tabs', 'index': 2}, label='BGP', value='bgp'),
                                 dcc.Tab(selected_style=main_page_graph_tab_selected, className='main-page-graph-tab',
                                         id={'type': 'main_tabs', 'index': 3}, label='Trace Route', value='traceroute'),
                                 dcc.Tab(selected_style=main_page_graph_tab_selected, className='main-page-graph-tab',
                                         id={'type': 'main_tabs', 'index': 4}, label='All Things ACL', value='all_things_acl'),
                             ]),
                    html.Div(id="main-page-tabs-content"),
                ]
            ),
        ],
    ),

    # Hidden Outputs
    html.Div(
        style={'position': 'relative', 'left': '10px'},
        children=[
            html.P(id='cytoscape-mouseoverNodeData-output', style={"display": "none"}),
            html.P(id='cytoscape-mouseoverEdgeData-output', style={"display": "none"}),
            html.P(id='batfish-host-output', style={"display": "none"}),
            html.P(id='batfish-network-output', style={"display": "none"}),
            html.P(id='num_of_traces', style={"display": "none"}),
        ]
    ),

])
