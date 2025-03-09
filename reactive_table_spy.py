import subprocess
import sys

# 定义一个函数来安装缺少的包
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

 # http://127.0.0.1:8050/ 即可。
# 检查并安装需要的包
try:
    import dash
    from dash import dcc, html
    from dash.dependencies import Input, Output
    import plotly.graph_objs as go
    import pandas as pd
    import numpy as np
    import yfinance as yf
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    # 安装所需的包
    install('dash')
    install('plotly')
    install('pandas')
    install('numpy')
    install('yfinance')
    install('requests')
    install('beautifulsoup4')
    install('lxml')  # BeautifulSoup 解析 HTML 可能需要这个包

    # 重新导入安装后的包
    import dash
    from dash import dcc, html
    from dash.dependencies import Input, Output
    import plotly.graph_objs as go
    import pandas as pd
    import numpy as np
    import yfinance as yf
    import requests
    from bs4 import BeautifulSoup


# 爬取 S&P 500 市盈率数据
def scrape_sp500_pe():
    url = 'https://www.multpl.com/s-p-500-pe-ratio/table/by-month'
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to retrieve data")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'datatable'})

    if not table:
        print("Table not found!")
        return None

    rows = table.find_all('tr')
    data = []
    for row in rows[1:]:
        cols = row.find_all('td')
        date = cols[0].text.strip()

        pe_ratio_tag = cols[1]
        abbr_tag = pe_ratio_tag.find('abbr')
        if abbr_tag:
            pe_ratio = abbr_tag.next_sibling.strip() if abbr_tag.next_sibling else None
        else:
            pe_ratio = pe_ratio_tag.text.strip()

        if not pe_ratio or pe_ratio == "":
            continue

        data.append([date, pe_ratio])

    df = pd.DataFrame(data, columns=['Date', 'PE_Ratio'])
    df['Date'] = pd.to_datetime(df['Date'])
    df['PE_Ratio'] = pd.to_numeric(df['PE_Ratio'], errors='coerce')

    return df


# 获取股权风险溢价数据
def get_sp500_risk_p():
    ticker = "^TNX"
    treasury_data = yf.download(ticker, start="2000-01-01", interval='1d')
    treasury_data = treasury_data.droplevel(1, axis=1)
    treasury_data = treasury_data[['Close']].rename(columns={'Close': '10-Year Treasury Yield'})
    treasury_data.index = pd.to_datetime(treasury_data.index)
   
    treasury_data = treasury_data.resample('MS').first()
    treasury_data['10-Year Treasury Yield'] = treasury_data['10-Year Treasury Yield'] / 100
    treasury_data = treasury_data.reset_index(level=0)
    treasury_data = treasury_data.set_index("Date")

    pe_data = scrape_sp500_pe()
    pe_data['Date'] = pd.to_datetime(pe_data['Date'])
    pe_data = pe_data.set_index(['Date'])
    pe_data = pe_data.loc['2000-01-01':]

    pe_data['Earnings Yield'] = 1 / pe_data['PE_Ratio']
    
    
    # **合并数据**
    combined_data = pd.merge(pe_data, treasury_data, left_index=True, right_index=True, how='inner')
    
    # 计算 Equity Risk Premium
    combined_data['Equity Risk Premium'] = combined_data['Earnings Yield'] - combined_data['10-Year Treasury Yield']
    
    return combined_data
    



combined_data = get_sp500_risk_p()

# 创建 Dash 应用
app = dash.Dash(__name__)


# 计算分位点
def calculate_percentiles(data_column):
    p20 = np.percentile(data_column, 20)
    p50 = np.percentile(data_column, 50)
    p70 = np.percentile(data_column, 70)
    return p20, p50, p70


# 创建应用布局
app.layout = html.Div([
    html.H1("Equity Risk Premium and PE Ratio Over Time with Percentiles"),

    # 选择显示的指标：Equity Risk Premium 或 PE Ratio
    dcc.Dropdown(
        id='data-type',
        options=[
            {'label': 'Equity Risk Premium', 'value': 'ERP'},
            {'label': 'PE Ratio', 'value': 'PE'}
        ],
        value='ERP',  # 默认显示 Equity Risk Premium
        style={'width': '50%'}
    ),

    # 选择时间范围的下拉菜单
    dcc.Dropdown(
        id='time-range',
        options=[
            {'label': 'Last 20 Years', 'value': '20Y'},
            {'label': 'Last 10 Years', 'value': '10Y'},
            {'label': 'Last 5 Years', 'value': '5Y'}
        ],
        value='20Y',  # 默认选择过去20年
        style={'width': '50%'}
    ),

    # 显示图表
    dcc.Graph(id='erp-pe-graph')
])


# 回调函数：根据用户选择的时间范围和数据类型更新图表
@app.callback(
    Output('erp-pe-graph', 'figure'),
    [Input('time-range', 'value'), Input('data-type', 'value')]
)
def update_graph(selected_range, selected_data):
    # 根据选择的时间范围过滤数据
    if selected_range == '20Y':
        filtered_data = combined_data[combined_data.index > pd.Timestamp.today() - pd.DateOffset(years=20)]
    elif selected_range == '10Y':
        filtered_data = combined_data[combined_data.index > pd.Timestamp.today() - pd.DateOffset(years=10)]
    elif selected_range == '5Y':
        filtered_data = combined_data[combined_data.index > pd.Timestamp.today() - pd.DateOffset(years=5)]

    # 选择数据类型（Equity Risk Premium 或 PE Ratio）
    if selected_data == 'ERP':
        data_column = filtered_data['Equity Risk Premium']
        yaxis_title = "Equity Risk Premium"
    elif selected_data == 'PE':
        data_column = filtered_data['PE_Ratio']
        yaxis_title = "PE Ratio"

    # 计算分位点
    p20, p50, p70 = calculate_percentiles(data_column)

    # 创建图表
    fig = go.Figure()

    # 添加选定数据的曲线（ERP 或 PE Ratio）
    fig.add_trace(go.Scatter(
        x=filtered_data.index,
        y=data_column,
        mode='lines',
        name=yaxis_title
    ))

    # 添加20%分位线
    fig.add_trace(go.Scatter(
        x=filtered_data.index,
        y=[p20] * len(filtered_data),
        mode='lines',
        name='20th Percentile',
        line=dict(dash='dash', color='green')
    ))

    # 添加50%分位线
    fig.add_trace(go.Scatter(
        x=filtered_data.index,
        y=[p50] * len(filtered_data),
        mode='lines',
        name='50th Percentile',
        line=dict(dash='dash', color='blue')
    ))

    # 添加70%分位线
    fig.add_trace(go.Scatter(
        x=filtered_data.index,
        y=[p70] * len(filtered_data),
        mode='lines',
        name='70th Percentile',
        line=dict(dash='dash', color='red')
    ))

    # 更新图表布局
    fig.update_layout(
        title=f"{yaxis_title} Over Time",
        xaxis_title="Date",
        yaxis_title=yaxis_title,
        xaxis_rangeslider_visible=True
    )

    return fig


# 运行 Dash 应用
if __name__ == '__main__':
    app.run_server(debug=True)
