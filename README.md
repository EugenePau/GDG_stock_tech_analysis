# yahoo-finance-scraper

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
📖 Introduction

GDG Stock Technical Analysis is a Python-based tool designed to process parsed stock data and evaluate trading signals using various technical indicators. It also generates technical analysis graphs for better visualization of stock trends.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🚀 Features

✔️ Processes stock data (parsed from Yahoo Finance or other sources)
✔️ Evaluates trading signals using multiple strategies:

  Moving Averages (MA)

  Moving Average Convergence Divergence (MACD)

  Relative Strength Index (RSI)

  Stochastic Oscillator (KD)

  Support & Resistance Levels

✔️ Plots technical analysis graphs for visualization

✔️ Easily integrates with yahoo-finance-scraper for real-time analysis

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

⚙️ Installation

🔹 Prerequisites

Python 3.8+

pip (Python package manager)

Git (optional, for cloning the repository)

feedparser

pandas

pandas_ta

matplotlib.pyplot

mplfinance

numpy

scipy.signal

yfinance

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

▶️ Usage

1Run the main.py
```sh
python main.py
```


------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

📂 Project Structure

```
GDG_stock_tech_analysis
├── 📂 src/               # Source code for analysis
│   ├── analysis.py     # Technical indicator calculations
│   ├── parser.py          # Graph plotting functions
│   ├── synthesizer.py      # Main stock analysis logic
│   ├── utils.py      # Main stock analysis logic
├── config.py            # Configuration settings
├── main.py              # Runs the stock analysis
├── requirements.txt     # Required Python packages
├── README.md            # Project documentation
```
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🤝 Contributing

Contributions are welcome! 🚀

To contribute:

Fork the repository

Create a new branch (git checkout -b feature-branch)

Make your changes

Commit your changes (git commit -m "Added new feature")

Push to GitHub (git push origin feature-branch)

Open a Pull Request


------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
