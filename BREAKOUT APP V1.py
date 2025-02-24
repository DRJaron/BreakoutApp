import subprocess
import sys

def install_libraries():
    """Automatically installs necessary libraries if not already installed."""
    required_libraries = [
        "yfinance", "pandas", "matplotlib", "colorama", "reportlab"
    ]
    
    for lib in required_libraries:
        try:
            __import__(lib)
        except ImportError:
            print(f"📦 Installing {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

# Run installation check
install_libraries()


import yfinance as yf
import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json
import os 
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)  # Ensures colors reset after each print statement


print(Fore.CYAN + "📊 STOCK CROSSOVER DETECTOR") 
print(Fore.CYAN + "BY DR.JARON")
print(Fore.CYAN +  "V1.0") 

# Function to create the directory
def create_output_directory():
    output_dir = 'output_files'
    # Create 'output_files' directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

# Function to check for SMA crossovers with volume confirmation
from colorama import Fore, Style

def check_stock_crossover(ticker, threshold=0.005, plot=True):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="1y", interval="1d")

        if df.empty or len(df) < 150:
            return None  # Not enough data

        # Calculate moving averages
        df["SMA50"] = df["Close"].rolling(window=50, min_periods=1).mean()
        df["SMA150"] = df["Close"].rolling(window=150, min_periods=1).mean()

        # Volume trend check
        df["VolumeAvg5"] = df["Volume"].rolling(window=5).mean()
        df["VolumeAvg10"] = df["Volume"].rolling(window=10).mean()

        last_sma50 = df["SMA50"].iloc[-1]
        last_sma150 = df["SMA150"].iloc[-1]
        prev_sma50 = df["SMA50"].iloc[-2]
        prev_sma150 = df["SMA150"].iloc[-2]

        last_vol_avg5 = df["VolumeAvg5"].iloc[-1]
        prev_vol_avg5 = df["VolumeAvg5"].iloc[-2]
        last_vol_avg10 = df["VolumeAvg10"].iloc[-1]

        # Check for crossovers
        bullish_cross = prev_sma50 < prev_sma150 and last_sma50 >= last_sma150
        bearish_cross = prev_sma50 > prev_sma150 and last_sma50 <= last_sma150

        # Ensure recent volume is increasing
        volume_up = last_vol_avg5 > last_vol_avg10 and last_vol_avg5 > prev_vol_avg5

        signal = None
        trend = None

        if bullish_cross and volume_up:
            signal = Fore.LIGHTGREEN_EX + Style.BRIGHT + "📈 GOLDEN CROSS (BULLISH) 🚀" + Style.RESET_ALL
            trend = "bullish"
        elif bearish_cross and volume_up:
            signal = Fore.RED + "📉 DEATH CROSS (BEARISH) ❌" + Style.RESET_ALL
            trend = "bearish"

        if signal:  # Only return if there's a valid crossover
            volume_text = Fore.GREEN + "📈 Volume: Up" + Style.RESET_ALL if volume_up else Fore.RED + "📉 Volume: Down" + Style.RESET_ALL
            result = f"{Fore.CYAN}📌 Ticker: {ticker}{Style.RESET_ALL}\n{Fore.YELLOW}⚠️ Signal: {signal}{Style.RESET_ALL}\n{volume_text}\n"
            return (ticker, signal, volume_text, trend)  # Return structured data for counting

    except Exception as e:
        print(Fore.RED + f"⚠️ Error with {ticker}: {e}" + Style.RESET_ALL)
        return None

# Function to plot stock data and save the plot image
def plot_stock(df, ticker, trend, output_dir="output_files"):
    try:
        # Ensure the index is in datetime format
        if df.index.dtype == "O":  
            df.index = pd.to_datetime(df.index)

        # Check for missing SMAs and calculate if needed
        if 'SMA50' not in df.columns:
            df['SMA50'] = df['Close'].rolling(window=50).mean()
        if 'SMA150' not in df.columns:
            df['SMA150'] = df['Close'].rolling(window=150).mean()

        # Set up the plot
        plt.figure(figsize=(12, 6))

        # Plot the close price and the SMAs
        plt.plot(df.index, df["Close"], label="Close Price", color="black", alpha=0.7, linewidth=2)
        plt.plot(df.index, df["SMA50"], label="SMA50", color="blue", linestyle="dashed", linewidth=3)
        plt.plot(df.index, df["SMA150"], label="SMA150", color="red", linestyle="dashed", linewidth=3)

        # Highlight the trend area (Golden Cross or Death Cross)
        if trend == "bullish":
            plt.fill_between(df.index, df["SMA50"], df["SMA150"], where=(df["SMA50"] >= df["SMA150"]), 
                             color="green", alpha=0.3, label="Golden Cross Area")
        elif trend == "bearish":
            plt.fill_between(df.index, df["SMA50"], df["SMA150"], where=(df["SMA50"] <= df["SMA150"]), 
                             color="red", alpha=0.3, label="Death Cross Area")

        # Mark the latest crossover point with a scatter
        color = "green" if trend == "bullish" else "red"
        label = "Golden Cross" if trend == "bullish" else "Death Cross"
        plt.scatter(df.index[-1], df["SMA50"].iloc[-1], color=color, marker="o", label=label, s=100, edgecolors="black")

        # Add titles and labels
        plt.title(f"{ticker} - {label} Detected", fontsize=14, fontweight="bold")
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Price ($)", fontsize=12)
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.legend()
        plt.grid(True, linestyle='--', linewidth=0.5)

        # Format x-axis to show one label per month
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

        # Ensure the output directory exists
        plot_dir = os.path.join(output_dir, "plots")
        os.makedirs(plot_dir, exist_ok=True)

        # Save the plot as a PNG file
        plot_filename = os.path.join(plot_dir, f"{ticker}_plot.png")
        plt.savefig(plot_filename, bbox_inches="tight", dpi=300)

        plt.close()  # Close plot to free memory

        print(Fore.GREEN + f"📊 Plot saved successfully: {plot_filename}" + Style.RESET_ALL)
        return plot_filename

    except Exception as e:
        print(Fore.RED + f"🚨 Error generating plot for {ticker}: {e}" + Style.RESET_ALL)
        return None



# Function to save the results
def save_results_to_file(results, output_dir, mode):
    """Save results to both TXT and CSV format with structured formatting."""
    
    if not results:
        print(Fore.RED + "⚠️ No results to save!" + Style.RESET_ALL)
        return

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    # File paths
    txt_filename = os.path.join(output_dir, f"{mode}_{timestamp}.txt")
    csv_filename = os.path.join(output_dir, f"{mode}_{timestamp}.csv")

    # Organize results into categories
    golden_crosses = [res[0] for res in results if res[3] == "bullish"]
    death_crosses = [res[0] for res in results if res[3] == "bearish"]

    # Save structured TXT report
    with open(txt_filename, "w", encoding="utf-8") as file:
        file.write("📊 STOCK CROSSOVER REPORT\n")
        file.write("-" * 40 + "\n")

        if golden_crosses:
            file.write(f"\n🟢 GOLDEN CROSSES ({len(golden_crosses)})\n")
            for stock in golden_crosses:
                file.write(f"- {stock}\n")

        if death_crosses:
            file.write(f"\n🔴 DEATH CROSSES ({len(death_crosses)})\n")
            for stock in death_crosses:
                file.write(f"- {stock}\n")

        file.write("\n✅ End of Report\n")

    # Save structured CSV report
    df = pd.DataFrame(results, columns=["Ticker", "Signal", "Volume", "Trend"])
    df.to_csv(csv_filename, index=False)

    print(Fore.GREEN + f"✅ Results saved to: {txt_filename}" + Style.RESET_ALL)
    print(Fore.GREEN + f"✅ CSV file saved to: {csv_filename}" + Style.RESET_ALL)


def fetch_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    try:
        tables = pd.read_html(url)
        df = tables[0]
        tickers = df['Symbol'].tolist()
        tickers = [ticker for ticker in tickers if re.fullmatch(r'[A-Z]+', ticker)]
        with open('sp500_tickers.txt', 'w') as f:
            for ticker in tickers:
                f.write(f"{ticker}\n")
        print(f"✅ S&P 500 file created with {len(tickers)} stocks.")
        return tickers
    except Exception as e:
        print(f"🚨 Error fetching S&P 500: {e}")
        return []

# Function to fetch NASDAQ-100 tickers
def fetch_NASDAQ_tickers():
    url = 'https://en.wikipedia.org/wiki/Nasdaq-100#Components'
    try:
        tables = pd.read_html(url)
        df = tables[4]
        tickers = df['Symbol'].tolist()
        tickers = [ticker for ticker in tickers if re.fullmatch(r'[A-Z]+', ticker)]
        with open('NASDAQ_tickers.txt', 'w') as f:
            for ticker in tickers:
                f.write(f"{ticker}\n")
        print(f"✅ NASDAQ file created with {len(tickers)} stocks.")
        return tickers
    except Exception as e:
        print(f"🚨 Error fetching NASDAQ: {e}")
        return []

def get_tickers_from_file(filename):
    try:
        with open(filename, "r") as file:
            tickers = [line.strip().upper() for line in file.readlines() if line.strip()]
            tickers = [ticker for ticker in tickers if re.fullmatch(r'[A-Z]+', ticker)]
            if not tickers:
                print("⚠️ No valid tickers found in the file.")
                return None
            return tickers
    except FileNotFoundError:
        print(f"⚠️ File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"🚨 Error reading file: {e}")
        return None

# Main function
def main():
    output_dir = create_output_directory()

    while True:
        print(Fore.CYAN + "\n📊 STOCK CROSSOVER DETECTOR | MODE SELECTION")
        choice = input(Fore.YELLOW + "Select mode - File (F), Manual (M), S&P 500 (S), NASDAQ (N): " + Style.RESET_ALL).strip().lower()

        if choice == 'f':
            filename = input(Fore.MAGENTA + "Enter filename (e.g., stocks.txt): " + Style.RESET_ALL).strip()
            tickers = get_tickers_from_file(filename)
            mode_name = "File"
            if tickers is None:
                continue
        elif choice == 'm':
            tickers_input = input(Fore.MAGENTA + "Enter stock tickers (comma-separated): " + Style.RESET_ALL).strip()
            tickers = [ticker.strip().upper() for ticker in tickers_input.split(',')]
            mode_name = "Manual"
            tickers = [ticker for ticker in tickers if re.fullmatch(r'[A-Z]+', ticker)]
        elif choice == 's':
            print(Fore.GREEN + "Fetching S&P 500 tickers..." + Style.RESET_ALL)
            tickers = fetch_sp500_tickers()
            mode_name = "SP500"
            if not tickers:
                continue
        elif choice == 'n':
            print(Fore.GREEN + "Fetching NASDAQ-100 tickers..." + Style.RESET_ALL)
            tickers = fetch_NASDAQ_tickers()
            mode_name = "NASDAQ"
            if not tickers:
                continue
        else:
            print(Fore.RED + "❌ Invalid choice. Please try again." + Style.RESET_ALL)
            continue

        # Check for crossovers and filter valid results
        results = []
        for ticker in tickers:
            result = check_stock_crossover(ticker)
            if result:
                results.append(result)

                # Generate and save the plot for each detected crossover
                stock_data = yf.Ticker(ticker).history(period="1y", interval="1d")
                plot_filename = plot_stock(stock_data, ticker, result[3], output_dir)
                if plot_filename:
                    print(Fore.CYAN + f"📊 Plot saved for {ticker}: {plot_filename}" + Style.RESET_ALL)

        # Count the crossovers
        golden_cross_count = sum(1 for res in results if res[3] == "bullish")
        death_cross_count = sum(1 for res in results if res[3] == "bearish")

        if results:
            print(Fore.CYAN + "\n📊 **Stocks with Crossover Signals:**" + Style.RESET_ALL)
            for result in results:
                print(result[1])

            # Print counts
            print(Fore.LIGHTGREEN_EX + f"\n✅ Total Golden Crosses: {golden_cross_count}" + Style.RESET_ALL)
            print(Fore.RED + f"❌ Total Death Crosses: {death_cross_count}" + Style.RESET_ALL)

            # Save results with formatted filename
            save_results_to_file(results, output_dir, mode_name)

        if input(Fore.CYAN + "\nCheck another list? (yes/no): " + Style.RESET_ALL).strip().lower() != 'yes':
            print(Fore.GREEN + "👋 Goodbye!" + Style.RESET_ALL)
            break



# Run script with Ctrl+C handling
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n🚪 Exiting... Goodbye! 👋" + Style.RESET_ALL)

