import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_daq as daq
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


# Batfish 모듈 임포트 예시
# from pybatfish.client.session import Session
# from batfish_module import Batfish  # 사용하시는 Batfish 클래스

app = dash.Dash(__name__)
server = app.server

# -----------------
# 레이아웃 정의
# -----------------
app.layout = html.Div([
    html.H1("Batfish Dashboard"),
    html.Div([
        dcc.Input(id="batfish_host_input", type="text", placeholder="Batfish Host"),
        dcc.Input(id="create-network-form", type="text", placeholder="Network Name"),
        html.Button("Create Network", id="create_network_submit_button"),
        html.Div(id="batfish-network-output")
    ]),
    html.Div([
        dcc.Dropdown(
            id="select-snapshot-button",
            placeholder='Select Snapshot',
            className="main_page_dropdown",
            options=[],  # 옵션은 콜백에서 동적으로 채움
            value=None
        ),
    ])
])

# -----------------
# 콜백 예시: 네트워크 생성
# -----------------
@app.callback(
    Output("batfish-network-output", "children"),
    [Input("create_network_submit_button", "n_clicks")],
    [State("create-network-form", "value"),
     State("batfish_host_input", "value")]
)
def create_network(n_clicks, network_name, batfish_host):
    if n_clicks is None:
        raise PreventUpdate

    # Batfish 연결 및 네트워크 생성
    batfish = Batfish(batfish_host)  # 실제 클래스에 맞춰 수정
    batfish.set_network(network_name)

    return f"Network '{network_name}' created successfully."

# -----------------
# 콜백 예시: JSON 처리 후 노드 리스트 반환
# -----------------
@app.callback(
    Output("select-snapshot-button", "options"),
    [Input("select-network-button", "value")],
    [State("batfish_host_input", "value")]
)
def update_snapshot_options(selected_network, batfish_host):
    if not selected_network:
        raise PreventUpdate

    # Batfish에서 snapshot 가져오기 (예시)
    batfish = Batfish(batfish_host)
    nodes = batfish.get_nodes(selected_network)  # 예시 메서드

    try:
        json_data = json.loads(str(nodes).replace("\'", "\""))
        node_list = [d['data']['label'] for d in json_data if 'data' in d and 'label' in d['data']]
    except (json.JSONDecodeError, TypeError):
        node_list = []

    options = [{"label": n, "value": n} for n in node_list]
    return options

# -----------------
# 서버 실행
# -----------------
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
