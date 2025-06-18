import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import time
import random
import warnings



class DCFCalculator:
    def __init__(self, discount_rate, terminal_growth_rate, forecast_years):
        """
        初始化 DCFCalculator 类
        
        参数：
            discount_rate: 折现率
            terminal_growth_rate: 终值增长率
            forecast_years: 预测年限
        """
        self.discount_rate = discount_rate
        self.terminal_growth_rate = terminal_growth_rate
        self.forecast_years = forecast_years

    def calculate_dcf(self, ticker, retry=3):
        """
        对单个股票进行DCF估值计算。
        
        参数：
            ticker: 股票代码字符串
            retry: 防止因网络问题或访问频繁导致的数据获取失败
        
        返回：
            DCF估值，如果数据缺失或条件不满足则返回 None
        """
        for attempt in range(retry):
            try:
                stock = yf.Ticker(ticker)
                # 获取现金流和财务数据
                cashflow = stock.cashflow
                financials = stock.financials
                break
            except Exception as e:
                print(f"{ticker} 数据获取错误（第 {attempt+1} 次尝试）: {e}")
                time.sleep(random.uniform(2, 4))
        else:
            # 重试后仍失败，返回 None
            return None

        if "Free Cash Flow" not in cashflow.index:
            print(f"{ticker} 缺少自由现金流数据")
            return None

        try:
            fcf = cashflow.loc["Free Cash Flow"].iloc[0]
        except Exception as e:
            print(f"{ticker} 读取自由现金流出错: {e}")
            return None

        # 排除自由现金流为负的情况
        if fcf < 0:
            print(f"{ticker} 的自由现金流为负，跳过DCF计算")
            return None

        if "Total Revenue" in financials.index and financials.shape[1] >= 2:
            try:
                revenue_series = financials.loc["Total Revenue"]
                # 假设 financials 的列顺序为从最新到较旧，取前最多 4 个期间数据
                num_periods = min(financials.shape[1], 4)
                revenues = revenue_series.iloc[:num_periods]
                growth_rates = []
                for i in range(len(revenues) - 1):
                    rev_current = revenues.iloc[i]
                    rev_previous = revenues.iloc[i + 1]
                    if rev_previous != 0:
                        growth = (rev_current - rev_previous) / rev_previous
                        growth_rates.append(growth)
                if growth_rates:
                    growth_rate = sum(growth_rates) / len(growth_rates)
                else:
                    growth_rate = 0.0
            except Exception as e:
                print(f"{ticker} 计算收入增长率出错: {e}")
                growth_rate = 0.0
        else:
            growth_rate = 0.0

        # 排除平均增长率为负的情况
        #if growth_rate < 0:
            #print(f"{ticker} 的平均收入增长率为负，跳过DCF计算")
            #return None

        fcf_forecasts = []
        fcf_current = fcf
        for i in range(1, self.forecast_years + 1):
            fcf_next = fcf_current * (1 + growth_rate)
            fcf_forecasts.append(fcf_next)
            fcf_current = fcf_next

        pv_fcfs = [fcf_forecasts[i] / ((1 + self.discount_rate) ** (i + 1)) for i in range(self.forecast_years)]
        terminal_value = fcf_forecasts[-1] * (1 + self.terminal_growth_rate) / (self.discount_rate - self.terminal_growth_rate)
        pv_terminal = terminal_value / ((1 + self.discount_rate) ** self.forecast_years)
        
        dcf_value = sum(pv_fcfs) + pv_terminal
        return dcf_value



    def batch_calculate_dcf(self, ticker_list):
        """
        对股票列表中的每个股票批量计算DCF估值，并获取市值及计算DCF与市值比值，
        同时预防频繁访问导致被block。
        
        参数：
            ticker_list: 股票代码列表，如 ["AAPL", "MSFT", ...]
            
        返回：
            一个 DataFrame，包含每个股票的代码、DCF估值、当前市值及DCF/市值比值
        """
        records = []
        for ticker in ticker_list:
            dcf = self.calculate_dcf(ticker)
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                market_cap = info.get("marketCap")
                current_price = info.get("regularMarketPrice")
                float_shares = info.get("floatShares")
            except Exception:
                market_cap = None
                current_price = None
            if dcf is not None and current_price not in (None, 0) and float_shares not in (None, 0):
                # 重新计算市值并互斥地做空值保护
                my_market_cap = current_price * float_shares
                ratio = dcf / my_market_cap
                theoretical_price = dcf / float_shares
            else:
                # 任意一个数据缺失，就直接给出 None
                my_market_cap = None
                ratio = None
                theoretical_price = None

            records.append({
                "Ticker": ticker,
                "DCF_Value": dcf,
                "Market_Cap": my_market_cap,
                "Current_Price": current_price,
                "DCF_MarketCap_Ratio": ratio,
                "Theoretical_Price": theoretical_price
            })
            time.sleep(random.uniform(1, 3))

        return pd.DataFrame(records)

    @staticmethod
    def get_sp500_tickers():
        """
        爬取维基百科上的 S&P500 成分股代码
        
        返回：
            包含所有 S&P500 股票代码的列表
        """
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # 查找包含成分股的表格
        table = soup.find("table", {"id": "constituents"})
        if table is None:
            table = soup.find_all("table")[0]  # 备用方案：取页面上的第一个表格

        tickers = []
        rows = table.find_all("tr")[1:]  # 跳过表头
        for row in rows:
            cells = row.find_all("td")
            ticker = cells[0].text.strip()  # 第 1 列是股票代码
            tickers.append(ticker)

        return tickers

if __name__ == "__main__":
    # 内部测试代码

    # 测试爬取 S&P500 股票代码
    sp500_tickers = DCFCalculator.get_sp500_tickers()
    print("S&P500 股票代码数量:", len(sp500_tickers))
    print("部分股票代码:", sp500_tickers[:10])
    
    # 使用部分股票代码进行DCF计算测试（可根据需要调整测试股票）
    #test_tickers = sp500_tickers[:3]  # 仅测试前3个股票
    #tickers = ["AAPL", "MSFT", "GOOGL","T"]
    discount_rate = 0.07
    terminal_growth_rate = 0.02
    forecast_years = 5

    calculator = DCFCalculator(discount_rate, terminal_growth_rate, forecast_years)
    dcf_df = calculator.batch_calculate_dcf(test_tickers)
    print(dcf_df)
