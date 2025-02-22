# 📊 Stock Crossover Detector

A powerful Python tool for detecting Golden Cross and Death Cross signals in stock data using Simple Moving Averages (SMA). This application helps traders identify potential bullish and bearish market trends with volume confirmation analysis.

## 🌟 Features

- **Advanced Signal Detection**
  - Golden Cross (bullish) identification using 50-day and 150-day SMAs
  - Death Cross (bearish) pattern recognition
  - Volume analysis for signal confirmation

- **Comprehensive Analysis Options**
  - Individual stock analysis
  - Batch processing from file input
  - S&P 500 companies coverage
  - NASDAQ-100 companies coverage

- **Rich Output Formats**
  - Interactive visual plots with highlighted crossover points
  - Detailed TXT reports
  - CSV export for further analysis
  - Organized output directory structure

## 📋 Requirements

```bash
pip install yfinance matplotlib pandas colorama
```

## 🚀 Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/stock-crossover-detector.git
   cd stock-crossover-detector
   ```

2. **Run the Application**
   ```bash
   python "BREAKOUT APP V1.py"
   ```

3. **Select Analysis Mode**
   - `F` - File Mode: Analyze stocks listed in a text file
   - `M` - Manual Mode: Enter stock tickers manually
   - `S` - S&P 500 Mode: Analyze S&P 500 stocks
   - `N` - NASDAQ Mode: Analyze NASDAQ-100 stocks

## 📈 Output Examples

The application generates comprehensive output files in the `output_files` directory:

```
output_files/
├── plots/
│   ├── AAPL_2025-02-22.png
│   └── GOOGL_2025-02-22.png
├── File_2025-02-22_14-30.txt
└── File_2025-02-22_14-30.csv
```

### Signal Indicators

- 📈 **Golden Cross (Bullish)**: 50-day SMA crosses above 150-day SMA
- 📉 **Death Cross (Bearish)**: 50-day SMA crosses below 150-day SMA

## 🔍 Understanding Crossovers

- **Golden Cross**: A bullish signal occurring when the short-term moving average crosses above the long-term moving average, potentially indicating the beginning of an uptrend.
- **Death Cross**: A bearish signal occurring when the short-term moving average crosses below the long-term moving average, potentially indicating the beginning of a downtrend.

## ⚠️ Disclaimer

This tool is for informational purposes only. Always conduct thorough research and consider multiple factors before making investment decisions.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Dr. Jaron(Shagalov Yaron) - Creator of the Stock Crossover Detector

## 📞 Support

If you encounter any issues or have questions, please [open an issue](https://github.com/your-username/stock-crossover-detector/issues) on GitHub.
