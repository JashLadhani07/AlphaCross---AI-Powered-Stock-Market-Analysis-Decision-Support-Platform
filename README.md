# 📈 AlphaCross - AI-Powered Stock Market Analysis & Decision Support Platform

AlphaCross is an AI-powered stock analysis platform that combines **technical analysis, machine learning, explainable AI, financial news intelligence, NLP, and conversational AI** to help investors make more informed trading decisions.

Unlike traditional crossover screeners, AlphaCross combines **historical price action**, **technical indicators**, **XGBoost predictions**, **SHAP explanations**, and **AI-generated market insights** into a single interactive dashboard supporting **500 NSE-listed companies**.

---

## ✨ Features

### 📊 Technical Analysis
- Live NSE stock analysis
- EMA 20 & EMA 50 crossover strategy
- RSI calculation
- Price volatility analysis
- Interactive stock charts
- Technical trend summary

---

### 🤖 Machine Learning Prediction

Predict future stock movement using an **XGBoost classifier** trained on engineered technical features.

Outputs:
- Bullish
- Bearish
- Neutral

Along with:
- Prediction confidence
- Technical indicators
- Trading recommendation

---

### 🧠 Explainable AI (XAI)

Predictions are no longer black boxes.

AlphaCross uses **SHAP (SHapley Additive Explanations)** to identify which technical indicators contributed the most toward each prediction.

Top contributing features include:

- EMA 20
- EMA 50
- EMA Momentum
- RSI
- Returns
- Volatility

---

### 📰 AI News Intelligence

Every stock is analyzed using recent financial news.

Pipeline:

NewsData API
→ Article Cleaning
→ Deduplication
→ Groq Llama 3.3 70B
→ Financial Sentiment Analysis

The system generates:

- Latest Headlines
- AI Summary
- Bullish / Bearish / Neutral Sentiment
- Confidence Score
- Risk Factors
- Overall Market Impact

---

### 💬 AI Stock Assistant

Integrated chatbot capable of answering questions related to:

- Technical indicators
- EMA crossover strategy
- Predictions
- Backtesting
- Market concepts
- Stock analysis

---

### 📈 AI Chart Explanation

Generate natural language explanations directly from price charts.

The model analyzes:

- EMA crossover
- Trend
- RSI
- Price movement
- Momentum

and produces an investor-friendly explanation.

---

### 📉 Historical Backtesting

Evaluate strategy performance using historical data.

Metrics include:

- Trade History
- Win Rate
- Final Portfolio Value
- Profit Factor
- Risk Reward Ratio
- Average Profit
- Average Loss
- Maximum Drawdown
- Maximum Gain
- Maximum Loss
- Total PnL

---

### 🔍 Universe Screening

Screen all supported NSE stocks based on:

- EMA crossover
- Technical indicators
- ML prediction

Identify bullish opportunities across the market.

---

### 📊 Universe Backtesting

Run historical crossover strategy on multiple stocks simultaneously and compare performance across the universe.

---

### 📱 Modern Dashboard

Interactive dashboard built with React featuring:

- Stock Search
- Quick Access Stocks
- Live Technical Indicators
- ML Prediction Card
- AI Daily Summary
- News Intelligence Panel
- Interactive Charts
- Performance Dashboard
- AI Chatbot

---

# 🏗️ Project Architecture

```
                ┌────────────────────┐
                │ React Frontend     │
                └─────────┬──────────┘
                          │
                          ▼
                 FastAPI Backend
                          │
     ┌──────────┬─────────┼──────────┬─────────┐
     ▼          ▼         ▼          ▼         ▼
 Market Data  ML Model  News AI   Backtesting  Chatbot
     │          │         │          │
     ▼          ▼         ▼          ▼
 Yahoo      XGBoost     Groq      Strategy
 Finance      +          LLM      Evaluation
            SHAP
```

---

# 🧠 AI Pipeline

```
Select Stock
      │
      ▼
Fetch Historical Market Data
      │
      ▼
Feature Engineering
      │
      ▼
XGBoost Prediction
      │
      ▼
SHAP Explainability
      │
      ▼
News Intelligence
      │
      ▼
Groq Financial Analysis
      │
      ▼
Dashboard Visualization
```

---

# ⚙️ Tech Stack

## Frontend

- React.js
- Tailwind CSS
- Axios
- Chart.js

---

## Backend

- FastAPI
- Python
- Pandas
- NumPy

---

## Machine Learning

- XGBoost
- Scikit-Learn
- Feature Engineering

---

## Explainable AI

- SHAP

---

## NLP & LLM

- Groq API
- Llama 3.3 70B Versatile
- Prompt Engineering

---

## Data Sources

- Yahoo Finance
- NewsData.io

---

## APIs Used

- Yahoo Finance API
- NewsData API
- Groq API

---

# 📂 Project Structure

## 📂 Project Structure

```text
AlphaCross
│
├── backend
│   ├── main.py
│   ├── test_backend.py
│   ├── __init__.py
│   │
│   ├── ai
│   │   ├── chat.py
│   │   └── __init__.py
│   │
│   ├── data
│   │   └── nifty500.csv
│   │
│   ├── ml
│   │   ├── backtest.py
│   │   ├── data_fetch.py
│   │   ├── engine.py
│   │   ├── explain.py
│   │   ├── features.py
│   │   ├── model_xgb.py
│   │   ├── nse500_fetcher.py
│   │   ├── stocks_list.py
│   │   ├── universe_backtest.py
│   │   ├── universe_screen.py
│   │   ├── utils.py
│   │   └── __init__.py
│   │
│   └── news
│       ├── news_service.py
│       └── __init__.py
│
├── frontend
│   ├── public
│   │   └── index.html
│   │
│   ├── src
│   │   ├── api
│   │   │   └── api.js
│   │   │
│   │   ├── components
│   │   │   ├── ChartDisplay.jsx
│   │   │   ├── Chatbot.jsx
│   │   │   ├── Loader.jsx
│   │   │   ├── NewsCard.jsx
│   │   │   ├── PerformanceTable.jsx
│   │   │   ├── PredictionCard.jsx
│   │   │   ├── StockSelector.jsx
│   │   │   ├── SummaryCard.jsx
│   │   │   └── TopMovers.jsx
│   │   │
│   │   ├── pages
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ScreeningResults.jsx
│   │   │   └── UniverseBacktestDashboard.jsx
│   │   │
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   │
│   ├── package.json
│   ├── tailwind.config.js
│   └── postcss.config.js
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/AlphaCross.git

cd AlphaCross
```

---

## Backend

```bash
pip install -r requirements.txt
```

Run backend

```bash
uvicorn backend.main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm start
```

---

# 🔑 Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
NEWSDATA_API_KEY=YOUR_NEWSDATA_API_KEY
```

---

# 📊 Machine Learning Features

The prediction model uses engineered features including:

- EMA 20
- EMA 50
- EMA 20 Slope
- EMA 50 Slope
- RSI
- Daily Returns
- Historical Volatility

---

# 📈 Prediction Labels

The model predicts one of three classes:

| Label | Meaning |
|--------|----------|
| 🟢 Bullish | Upward momentum expected |
| 🔴 Bearish | Downward momentum expected |
| ⚪ Neutral | No strong directional signal |

---

# 🧠 Explainable AI

Instead of producing a prediction alone, AlphaCross explains *why* the prediction was made.

SHAP highlights the most influential indicators contributing to the model's decision, improving transparency and interpretability.

---

# 📰 News Intelligence Workflow

```
NewsData API
        │
        ▼
Recent Articles
        │
        ▼
Cleaning & Deduplication
        │
        ▼
Groq Llama 3.3
        │
        ▼
Financial NLP
        │
        ▼
Sentiment + Risks + Summary
```

---

# 📊 Dashboard Modules

- Stock Selector
- Technical Indicators
- ML Prediction
- Interactive Price Chart
- AI Chart Explanation
- AI Daily Summary
- News Intelligence
- Historical Backtesting
- Universe Screening
- AI Chatbot

---

# 💡 Future Improvements

- Portfolio Optimization
- Multi-Timeframe Analysis
- Real-Time Streaming Data
- Fundamental Analysis Integration
- Reinforcement Learning Strategies
- Paper Trading
- Portfolio Risk Analytics

---

# 👨‍💻 Developed By

**Jash Ladhani**
**Aaryan Lunis**

B.Tech Computer Engineering

AI • Machine Learning • Financial Analytics • Explainable AI • NLP

---

## ⭐ If you found this project interesting, consider giving it a star!
