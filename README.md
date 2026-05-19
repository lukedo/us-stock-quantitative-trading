# US Stock Quantitative Trading

美股量化分析与模拟交易系统，基于富途 OpenAPI 提供实时行情和仿真交易。

## 架构

```
futu-api SDK  ←→  OpenD (本地网关)  ←→  富途服务器
      ↓
  Python 项目
  ├── src/data/       数据获取与缓存
  ├── src/analysis/   技术分析与期权定价
  └── src/simulator/  模拟交易引擎
```

## 快速开始

### 1. 安装依赖

```bash
pip3 install -r requirements.txt
```

### 2. 启动 OpenD

下载安装 OpenD 并登录富途账号，确保本地服务运行在 `127.0.0.1:11111`。

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 配置 OpenD 地址和交易环境
```

### 4. 验证连接

```python
from futu import *
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
ret, data = quote_ctx.get_global_state()
print(data)
quote_ctx.close()
```

### 5. 运行 Notebooks

```bash
jupyter notebook notebooks/
```

## 项目结构

```
├── src/
│   ├── config.py              # 配置管理
│   ├── data/
│   │   ├── base_provider.py   # 数据源抽象接口
│   │   ├── futu_provider.py   # 富途 API 数据源
│   │   ├── yahoo_provider.py  # Yahoo Finance 备选
│   │   └── cache.py           # 本地缓存
│   ├── analysis/
│   │   ├── technical.py       # 技术指标
│   │   ├── options_pricing.py # 期权定价与 Greeks
│   │   └── strategies.py      # 交易策略
│   └── simulator/
│       ├── engine.py          # 模拟交易引擎
│       ├── account.py         # 账户管理
│       ├── order_book.py      # 订单簿
│       └── metrics.py         # 绩效评估
├── notebooks/                 # Jupyter Notebooks
├── data/                      # 数据缓存
├── docs/                      # 文档
└── tests/                     # 测试
```

## 数据源

| 数据 | 主数据源 | 备选 |
|------|---------|------|
| 实时行情 | 富途 OpenAPI | Yahoo Finance |
| 历史K线 | 富途 OpenAPI | Yahoo Finance |
| 期权链 | 富途 OpenAPI | - |
| 基本面 | 富途 OpenAPI | Yahoo Finance |

## 交易环境

默认使用 **模拟交易**（`TrdEnv.SIMULATE`），虚拟资金，无风险。

---
*非投资建议，仅供学习参考。*
