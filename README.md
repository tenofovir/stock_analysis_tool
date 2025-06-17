## Stock Quantitative Strategy Evaluation Metrics

#### 1. **年化收益率 (Annualized Return, 年率換算リターン)**
- **Description**: Measures the average return over a period, annualized to facilitate comparison across time periods.
- **Formula**: (Insert Formula Image Here)

#### 2. **最大回撤 (Maximum Drawdown, 最大ドローダウン)**
- **Description**: Describes the largest capital loss during the strategy period, evaluating risk.
- **Formula**: (Insert Formula Image Here)

#### 3. **夏普比率 (Sharpe Ratio, シャープレシオ)**
- **Description**: Quantifies the excess return per unit of risk taken by the strategy.
- **Formula**: (Insert Formula Image Here)



# DCF 模型公式介绍 (DCF Model Formula Introduction / ディスカウンテッド・キャッシュ・フロー モデル)

DCF（Discounted Cash Flow）模型是一种评估公司或资产未来现金流现值的方法。在中文中称为 **贴现现金流模型**，在英文中称为 **Discounted Cash Flow Model**，在日文中称为 **ディスカウンテッド・キャッシュ・フロー (DCF) モデル**。

## 基本公式

DCF 模型的基本公式为：

$$
DCF = \sum_{t=1}^{n} \frac{FCF_t}{(1 + r)^t} + \frac{TV}{(1 + r)^n}
$$

其中：
- **FCF_t (自由现金流 / Free Cash Flow / 自由現金流)**：第 *t* 年的自由现金流
- **r (折现率 / Discount Rate / 割引率)**：反映资金时间价值及风险的折现率
- **n (预测期 / Forecast Period / 予測期間)**：现金流预测的年限
- **TV (终值 / Terminal Value / ターミナルバリュー)**：预测期结束后的持续价值，通常使用下面的公式计算：
  
  $$
  TV = \frac{FCF_{n} \times (1 + g)}{r - g}
  $$

  其中 **g (终值增长率 / Terminal Growth Rate / 終価成長率)** 表示终值增长率。

## 模型说明

1. **自由现金流 (FCF / Free Cash Flow / 自由現金流)**  
   表示公司在扣除运营和资本支出后的可用现金流量，是公司进行再投资或分红的基础。

2. **折现率 (r / Discount Rate / 割引率)**  
   通常采用公司的加权平均资本成本（WACC）作为折现率，以反映投资的风险及资金的时间价值。折现率越高，代表你对这笔投资要求越高的“补偿”，认为风险更大、未来更不确定。
   
   5%（风险低） - 10%(风险高)

3. **终值 (TV / Terminal Value / ターミナルバリュー)**  
   用于估计预测期后公司未来现金流的现值，通常采用永续增长模型计算。






# WACC

$$
\text{WACC} = \frac{E}{E+D}\cdot r_e + \frac{D}{E+D}\cdot r_d\cdot (1-T)
$$

其中：  
- \(E\)（Equity / エクイティ）：股权市值  
- \(D\)（Debt / 負債）：债务总额  
- \(r_e\)（Cost of Equity / エクイティコスト）：股权成本  
- \(r_d\)（Cost of Debt / 負債コスト）：债务成本  
- \(T\)（Tax Rate for Calcs / 計算用税率）：企业税率
'''



$$
r_e = r_f + \beta (r_m - r_f)
$$

其中：  
- \(r_e\)（Cost of Equity / エクイティコスト）：股权成本  
- \(r_f\)（Risk-Free Rate / 無リスク金利）：无风险利率  
- \(\beta\)（Beta / ベータ）：股票的贝塔值，衡量股票相对于市场的波动性  
- \(r_m - r_f\)（Market Risk Premium / 市場リスクプレミアム）：市场风险溢价，即市场期望收益率与无风险利率之差
'''
