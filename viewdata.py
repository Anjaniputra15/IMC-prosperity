import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import sys

# 1. Setup Files
if len(sys.argv) < 2:
    print("Usage: python viewdata.py <prices_file.csv>")
    sys.exit(1)

prices_file = sys.argv[1]
trades_file = prices_file.replace('prices_', 'trades_')

print(f"Loading {prices_file}...")
df = pd.read_csv(prices_file, sep=';')

print(f"Loading {trades_file}...")
try:
    trades_df = pd.read_csv(trades_file, sep=';')
except FileNotFoundError:
    print(f"Warning: {trades_file} not found.")
    trades_df = pd.DataFrame()

# 2. Prep Data
df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('datetime', inplace=True)
if not trades_df.empty:
    trades_df['datetime'] = pd.to_datetime(trades_df['timestamp'], unit='ms')

products = sorted(df['product'].unique())
num_prods = len(products)

# 3. Create the Grid (Standard Matplotlib style)
fig, axes = plt.subplots(nrows=num_prods, ncols=1, figsize=(12, 10), sharex=True)
if num_prods == 1:
    axes = [axes]

# 4. Loop through each product and plot
for i, product in enumerate(products):
    p_data = df[df['product'] == product]
    
    # Resample to 2-second candles (using 'ms' for your Pandas version)
    ohlc = p_data['mid_price'].resample('2000ms').ohlc().dropna()
    
    # List for extra overlays (Trades and the 10k Line)
    ap = []
    
    # Add a horizontal line at 10k specifically for Amethysts (Emeralds)
    if product == 'AMETHYSTS':
        h_line = [10000] * len(ohlc)
        ap.append(mpf.make_addplot(h_line, ax=axes[i], color='gray', linestyle='--'))

    # Add the Red 'X' for market trades
    if not trades_df.empty:
        t_data = trades_df[trades_df['symbol'] == product]
        trade_markers = pd.Series(index=ohlc.index, dtype=float)
        
        for _, row in t_data.iterrows():
            closest_candle = ohlc.index.asof(row['datetime'])
            if pd.notna(closest_candle):
                trade_markers[closest_candle] = row['price']

        if not trade_markers.dropna().empty:
            ap.append(mpf.make_addplot(trade_markers, type='scatter', markersize=40, 
                                      marker='x', color='red', ax=axes[i]))

    # 5. The actual candle plotting call
    mpf.plot(ohlc, 
             type='candle', 
             ax=axes[i], 
             addplot=ap,
             style='charles',
             datetime_format='%H:%M:%S')
    
    axes[i].set_title(f"{product} Price Action")
    axes[i].set_ylabel('Price')

# Global layout tweaks
plt.tight_layout()
plt.show()
