## Stock Quantitative Strategy Evaluation Metrics

### **\u80a1\u7968\u91cf\u5316\u7b56\u7565\u8bc4\u4ef7\u6307\u6807**

#### 1. **\u5e74\u5316\u6536\u76ca\u7387 (Annualized Return)**
- **Description**: \u8861\u91cf\u7b56\u7565\u5728\u4e00\u5b9a\u671f\u95f4\u5185\u7684\u5e73\u5747\u6536\u76ca\u6c34\u5e73\uff0c\u5e74\u5316\u5904\u7406\u540e\u4fbf\u4e8e\u4e0d\u540c\u65f6\u95f4\u6bb5\u7684\u6536\u76ca\u6bd4\u8f83\u3002
- **Formula**:
  \[
  R_{\text{annual}} = \left(1 + R_{\text{total}}\right)^{\frac{1}{T}} - 1
  \]
  \(R_{\text{total}}\): \u603b\u6536\u76ca\u7387\uff0c\(T\): \u7b56\u7565\u8fd0\u884c\u5e74\u6570

#### 2. **\u6700\u5927\u56de\u64a4 (Maximum Drawdown, MDD)**
- **Description**: \u63cf\u8ff0\u7b56\u7565\u5728\u8fd0\u884c\u671f\u95f4\u53ef\u80fd\u906d\u9047\u7684\u6700\u5927\u8d44\u672c\u635f\u5931\uff0c\u8861\u91cf\u98ce\u9669\u3002
- **Formula**:
  \[
  \text{MDD} = \max\left(\frac{\text{Peak Value} - \text{Trough Value}}{\text{Peak Value}}\right)
  \]

#### 3. **\u590f\u666e\u6bd4\u7387 (Sharpe Ratio)**
- **Description**: \u8861\u91cf\u5355\u4f4d\u98ce\u9669\u5e26\u6765\u7684\u8d85\u989d\u6536\u76ca\u6c34\u5e73\u3002
- **Formula**:
  \[
  \text{Sharpe Ratio} = \frac{R_p - R_f}{\sigma_p}
  \]
  \(R_p\): \u7b56\u7565\u6536\u76ca\u7387\uff0c\(R_f\): \u65e0\u98ce\u9669\u6536\u76ca\u7387\uff0c\(\sigma_p\): \u7b56\u7565\u6536\u76ca\u7387\u7684\u6807\u51c6\u5dee

### **Stock Quantitative Strategy Evaluation Metrics**

#### 1. **Annualized Return**
- **Description**: Measures the average return over a period, annualized to facilitate comparison across time periods.
- **Formula**:
  \[
  R_{\text{annual}} = \left(1 + R_{\text{total}}\right)^{\frac{1}{T}} - 1
  \]
  \(R_{\text{total}}\): Total return, \(T\): Number of years

#### 2. **Maximum Drawdown (MDD)**
- **Description**: Describes the largest capital loss during the strategy period, evaluating risk.
- **Formula**:
  \[
  \text{MDD} = \max\left(\frac{\text{Peak Value} - \text{Trough Value}}{\text{Peak Value}}\right)
  \]

#### 3. **Sharpe Ratio**
- **Description**: Quantifies the excess return per unit of risk taken by the strategy.
- **Formula**:
  \[
  \text{Sharpe Ratio} = \frac{R_p - R_f}{\sigma_p}
  \]
  \(R_p\): Portfolio return, \(R_f\): Risk-free rate, \(\sigma_p\): Standard deviation of portfolio returns

### **\u682a\u5f0f\u91cf\u5bfe\u7b56\u7565\u306e\u8a55\u4fa1\u6307\u6a19**

#### 1. **\u5e74\u7387\u63db\u7b49\u30ea\u30bf\u30fc\u30f3 (Annualized Return)**
- **Description**: \u4e00\u5b9a\u671f\u9593\u5185\u306e\u5e73\u5747\u30ea\u30bf\u30fc\u30f3\u3092\u6e2c\u5b9a\u3057\uff0c\u5e74\u7387\u63db\u7b49\u3057\u3066\u7570\u306a\u308b\u671f\u9593\u306e\u30d1\u30d5\u30a9\u30fc\u30de\u30f3\u30b9\u3092\u6bd4\u8f03\u53ef\u80fd\u306b\u3059\u308b\u3002
- **Formula**:
  \[
  R_{\text{annual}} = \left(1 + R_{\text{total}}\right)^{\frac{1}{T}} - 1
  \]
  \(R_{\text{total}}\): \u7dcf\u30ea\u30bf\u30fc\u30f3\uff0c\(T\): \u6226\u7565\u306e\u904b\u7528\u5e74\u6570

#### 2. **\u6700\u5927\u30c9\u30ed\u30fc\u30c0\u30a6\u30f3 (Maximum Drawdown, MDD)**
- **Description**: \u6226\u7565\u671f\u9593\u4e2d\u306b\u767a\u751f\u3059\u308b\u53ef\u80fd\u6027\u306e\u3042\u308b\u6700\u5927\u8cc7\u672c\u640d\u5931\u3092\u793a\u3057\uff0c\u30ea\u30b9\u30af\u3092\u6e2c\u5b9a\u3059\u308b\u6307\u6a19\u3002
- **Formula**:
  \[
  \text{MDD} = \max\left(\frac{\text{Peak Value} - \text{Trough Value}}{\text{Peak Value}}\right)
  \]

#### 3. **\u30b7\u30e3\u30fc\u30d7\u30ec\u30b7\u30aa (Sharpe Ratio)**
- **Description**: \u30ea\u30b9\u30af1\u5358\u4f4d\u5f53\u305f\u308a\u306e\u8d85\u904e\u30ea\u30bf\u30fc\u30f3\u3092\u6e2c\u5b9a\u3059\u308b\u3002
- **Formula**:
  \[
  \text{Sharpe Ratio} = \frac{R_p - R_f}{\sigma_p}
  \]
  \(R_p\): \u30dd\u30fc\u30c8\u30d5\u30a9\u30ea\u30aa\u30ea\u30bf\u30fc\u30f3\uff0c\(R_f\): \u7121\u30ea\u30b9\u30af\u30ea\u30bf\u30fc\u30f3\uff0c\(\sigma_p\): \u30dd\u30fc\u30c8\u30d5\u30a9\u30ea\u30aa\u30ea\u30bf\u30fc\u30f3\u306e\u6a19\u6e96\u504f\u5dee
