#!/usr/bin/env python3
"""
Real-Time Trading Dashboard
Displays candlestick patterns with technical indicators and buy/sell signals
Fetches live data and updates dashboard every minute
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
from typing import Dict, List, Tuple
import base64

class RealtimeTradingDashboard:
    """Real-time dashboard with indicators and signals"""
    
    def __init__(self, api_key: str = None):
        """Initialize dashboard"""
        self.api_key = api_key or "YOUR_DHANIQ_API_KEY"
        self.stock_symbol = None
        self.df = None
        self.html_content = ""
    
    def fetch_live_data(self, symbol: str, days: int = 30):
        """Fetch live data from dhanHQ API"""
        self.stock_symbol = symbol
        
        # Generate mock data for demonstration
        # In production, replace with actual dhanHQ API call
        dates = pd.date_range(end=datetime.now(), periods=days*24, freq='h')
        
        np.random.seed(42)
        base_price = 605
        closes = base_price + np.cumsum(np.random.randn(len(dates)) * 0.5)
        
        self.df = pd.DataFrame({
            'datetime': dates,
            'open': closes + np.random.randn(len(dates)) * 0.3,
            'high': closes + np.abs(np.random.randn(len(dates)) * 0.8),
            'low': closes - np.abs(np.random.randn(len(dates)) * 0.8),
            'close': closes,
            'volume': np.random.randint(1000000, 5000000, len(dates))
        })
        
        # Ensure OHLC integrity
        self.df['high'] = self.df[['open', 'high', 'close', 'low']].max(axis=1)
        self.df['low'] = self.df[['open', 'high', 'close', 'low']].min(axis=1)
        
        return self.df
    
    def calculate_rsi(self, period: int = 14) -> np.ndarray:
        """Calculate RSI indicator"""
        delta = self.df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple:
        """Calculate MACD indicator"""
        ema_fast = self.df['close'].ewm(span=fast).mean()
        ema_slow = self.df['close'].ewm(span=slow).mean()
        
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal).mean()
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    def calculate_bollinger_bands(self, period: int = 20, std_dev: float = 2.0) -> Tuple:
        """Calculate Bollinger Bands"""
        sma = self.df['close'].rolling(window=period).mean()
        std = self.df['close'].rolling(window=period).std()
        
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        
        return upper_band, sma, lower_band
    
    def calculate_moving_averages(self, periods: List[int] = [20, 50, 200]) -> Dict:
        """Calculate multiple moving averages"""
        mas = {}
        for period in periods:
            mas[f'SMA{period}'] = self.df['close'].rolling(window=period).mean()
        return mas
    
    def generate_signals(self) -> pd.DataFrame:
        """Generate buy/sell signals"""
        signals_df = self.df.copy()
        
        # Calculate indicators
        signals_df['RSI'] = self.calculate_rsi()
        macd, macd_signal, macd_hist = self.calculate_macd()
        signals_df['MACD'] = macd
        signals_df['MACD_Signal'] = macd_signal
        signals_df['MACD_Hist'] = macd_hist
        
        upper_bb, middle_bb, lower_bb = self.calculate_bollinger_bands()
        signals_df['BB_Upper'] = upper_bb
        signals_df['BB_Middle'] = middle_bb
        signals_df['BB_Lower'] = lower_bb
        
        mas = self.calculate_moving_averages()
        for ma_name, ma_values in mas.items():
            signals_df[ma_name] = ma_values
        
        # Generate signals
        signals_df['signal'] = 0
        signals_df['signal_strength'] = 0
        
        for i in range(1, len(signals_df)):
            buy_signals = 0
            sell_signals = 0
            
            # RSI signals
            if signals_df['RSI'].iloc[i] < 30:
                buy_signals += 2  # Strong buy signal
            elif signals_df['RSI'].iloc[i] > 70:
                sell_signals += 2  # Strong sell signal
            
            # MACD signals
            if (signals_df['MACD'].iloc[i] > signals_df['MACD_Signal'].iloc[i] and 
                signals_df['MACD'].iloc[i-1] <= signals_df['MACD_Signal'].iloc[i-1]):
                buy_signals += 2  # Bullish crossover
            
            if (signals_df['MACD'].iloc[i] < signals_df['MACD_Signal'].iloc[i] and 
                signals_df['MACD'].iloc[i-1] >= signals_df['MACD_Signal'].iloc[i-1]):
                sell_signals += 2  # Bearish crossover
            
            # Bollinger Bands signals
            if signals_df['close'].iloc[i] < signals_df['BB_Lower'].iloc[i]:
                buy_signals += 1  # Price below lower band
            elif signals_df['close'].iloc[i] > signals_df['BB_Upper'].iloc[i]:
                sell_signals += 1  # Price above upper band
            
            # Moving average signals
            if (signals_df['close'].iloc[i] > signals_df['SMA20'].iloc[i] and
                signals_df['SMA20'].iloc[i] > signals_df['SMA50'].iloc[i]):
                buy_signals += 1  # Bullish alignment
            
            if (signals_df['close'].iloc[i] < signals_df['SMA20'].iloc[i] and
                signals_df['SMA20'].iloc[i] < signals_df['SMA50'].iloc[i]):
                sell_signals += 1  # Bearish alignment
            
            # Determine final signal
            if buy_signals > sell_signals:
                signals_df.loc[i, 'signal'] = 1  # Buy
                signals_df.loc[i, 'signal_strength'] = buy_signals
            elif sell_signals > buy_signals:
                signals_df.loc[i, 'signal'] = -1  # Sell
                signals_df.loc[i, 'signal_strength'] = sell_signals
        
        return signals_df
    
    def identify_candlestick_pattern(self, i: int) -> str:
        """Identify candlestick patterns"""
        if i < 2 or i >= len(self.df):
            return "N/A"
        
        o = self.df['open'].iloc[i]
        h = self.df['high'].iloc[i]
        l = self.df['low'].iloc[i]
        c = self.df['close'].iloc[i]
        
        body = abs(c - o)
        wick_up = h - max(o, c)
        wick_down = min(o, c) - l
        total_range = h - l
        
        # Hammer
        if body < total_range * 0.3 and wick_down > body * 2:
            return "🔨 Hammer (Bullish)"
        
        # Shooting Star
        if body < total_range * 0.3 and wick_up > body * 2:
            return "⭐ Shooting Star (Bearish)"
        
        # Doji
        if body < total_range * 0.1:
            return "⚪ Doji (Neutral)"
        
        # Bullish Engulfing
        if i > 0:
            prev_o = self.df['open'].iloc[i-1]
            prev_c = self.df['close'].iloc[i-1]
            if c > prev_o and o < prev_c:
                return "📈 Bullish Engulfing"
        
        # Bearish Engulfing
        if i > 0:
            prev_o = self.df['open'].iloc[i-1]
            prev_c = self.df['close'].iloc[i-1]
            if c < prev_o and o > prev_c:
                return "📉 Bearish Engulfing"
        
        # Regular candle
        if c > o:
            return "🟢 Green candle (Bullish)"
        else:
            return "🔴 Red candle (Bearish)"
    
    def generate_html_dashboard(self, signals_df: pd.DataFrame) -> str:
        """Generate interactive HTML dashboard"""
        
        # Get last 100 candles
        display_df = signals_df.tail(100).copy()
        display_df['datetime_str'] = display_df['datetime'].dt.strftime('%H:%M')
        
        # Current values
        current = signals_df.iloc[-1]
        previous = signals_df.iloc[-2]
        
        # Signal interpretation
        if current['signal'] == 1:
            signal_text = "🟢 BUY"
            signal_color = "#00AA00"
            signal_bg = "#E8F5E9"
        elif current['signal'] == -1:
            signal_text = "🔴 SELL"
            signal_color = "#DD0000"
            signal_bg = "#FFEBEE"
        else:
            signal_text = "🟡 NEUTRAL"
            signal_color = "#FFA500"
            signal_bg = "#FFF3E0"
        
        # Candlestick data for chart
        candle_data = []
        for i, row in display_df.iterrows():
            candle_data.append({
                'x': row['datetime_str'],
                'o': round(row['open'], 2),
                'h': round(row['high'], 2),
                'l': round(row['low'], 2),
                'c': round(row['close'], 2),
                'pattern': self.identify_candlestick_pattern(len(signals_df) - len(display_df) + i)
            })
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Real-Time Trading Dashboard - {self.stock_symbol}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        
        .header h1 {{
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }}
        
        .header-info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }}
        
        .info-box {{
            padding: 10px;
            background: #f5f5f5;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }}
        
        .info-label {{
            font-size: 12px;
            color: #666;
            font-weight: bold;
        }}
        
        .info-value {{
            font-size: 18px;
            color: #333;
            font-weight: bold;
            margin-top: 5px;
        }}
        
        .signal-box {{
            background: {signal_bg};
            padding: 15px 25px;
            border-radius: 8px;
            border-left: 5px solid {signal_color};
            margin-top: 10px;
        }}
        
        .signal-text {{
            font-size: 24px;
            color: {signal_color};
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .signal-strength {{
            font-size: 12px;
            color: #666;
        }}
        
        .dashboard {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
        }}
        
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            position: relative;
            height: 500px;
        }}
        
        .chart-title {{
            font-size: 16px;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
        }}
        
        .indicators-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        
        .indicator-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .indicator-title {{
            font-size: 14px;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .indicator-value {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }}
        
        .indicator-label {{
            font-size: 12px;
            color: #666;
        }}
        
        .indicator-result {{
            font-size: 16px;
            font-weight: bold;
            color: #333;
        }}
        
        .positive {{
            color: #00AA00;
        }}
        
        .negative {{
            color: #DD0000;
        }}
        
        .neutral {{
            color: #FFA500;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: bold;
            margin-left: 10px;
        }}
        
        .buy-badge {{
            background: #C8E6C9;
            color: #00AA00;
        }}
        
        .sell-badge {{
            background: #FFCDD2;
            color: #DD0000;
        }}
        
        .neutral-badge {{
            background: #FFE0B2;
            color: #FFA500;
        }}
        
        .timestamp {{
            font-size: 12px;
            color: #999;
            margin-top: 10px;
        }}
        
        .pattern-alert {{
            background: #FFF9C4;
            border-left: 4px solid #FFC107;
            padding: 10px 15px;
            border-radius: 4px;
            margin-bottom: 10px;
            font-size: 12px;
        }}
        
        .instructions {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-top: 20px;
        }}
        
        .instructions h3 {{
            color: #333;
            margin-bottom: 15px;
        }}
        
        .instructions ul {{
            list-style: none;
            margin-left: 0;
        }}
        
        .instructions li {{
            padding: 8px 0;
            color: #666;
            font-size: 13px;
            border-bottom: 1px solid #eee;
        }}
        
        .instructions li:before {{
            content: "✓ ";
            color: #00AA00;
            font-weight: bold;
            margin-right: 10px;
        }}
        
        @media (max-width: 768px) {{
            .header-info {{
                grid-template-columns: 1fr 1fr;
            }}
            
            .indicators-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Real-Time Trading Dashboard</h1>
            <div class="header-info">
                <div class="info-box">
                    <div class="info-label">Stock</div>
                    <div class="info-value">{self.stock_symbol}</div>
                </div>
                <div class="info-box">
                    <div class="info-label">Current Price</div>
                    <div class="info-value">₹{current['close']:.2f}</div>
                </div>
                <div class="info-box">
                    <div class="info-label">Change</div>
                    <div class="info-value positive" if current['close'] > previous['close'] else "negative">
                        {((current['close'] - previous['close']) / previous['close'] * 100):.2f}%
                    </div>
                </div>
                <div class="info-box">
                    <div class="info-label">High / Low</div>
                    <div class="info-value">₹{current['high']:.2f} / ₹{current['low']:.2f}</div>
                </div>
            </div>
            
            <div class="signal-box">
                <div class="signal-text">{signal_text}</div>
                <div class="signal-strength">
                    Signal Strength: {int(current['signal_strength'])}/10 
                    <span class="status-badge {'buy-badge' if current['signal'] == 1 else 'sell-badge' if current['signal'] == -1 else 'neutral-badge'}">
                        {'STRONG BUY' if current['signal_strength'] >= 7 else 'BUY' if current['signal'] == 1 else 'STRONG SELL' if current['signal_strength'] >= 7 else 'SELL' if current['signal'] == -1 else 'HOLD'}
                    </span>
                </div>
                <div class="timestamp">Last Updated: {current['datetime'].strftime('%Y-%m-%d %H:%M:%S')}</div>
            </div>
        </div>
        
        <div class="dashboard">
            <div class="chart-container">
                <div class="chart-title">🕯️ Candlestick Chart (Last 100 Bars)</div>
                <canvas id="candleChart"></canvas>
            </div>
            
            <div class="indicators-grid">
                <div class="indicator-card">
                    <div class="indicator-title">📈 RSI (14)</div>
                    <div class="indicator-value">
                        <span class="indicator-label">RSI Value</span>
                        <span class="indicator-result {'positive' if current['RSI'] < 30 else 'negative' if current['RSI'] > 70 else 'neutral'}">
                            {current['RSI']:.2f}
                        </span>
                    </div>
                    <div class="indicator-value">
                        <span class="indicator-label">Status</span>
                        <span class="indicator-result">
                            {'Oversold 🟢' if current['RSI'] < 30 else 'Overbought 🔴' if current['RSI'] > 70 else 'Neutral 🟡'}
                        </span>
                    </div>
                </div>
                
                <div class="indicator-card">
                    <div class="indicator-title">📊 MACD</div>
                    <div class="indicator-value">
                        <span class="indicator-label">MACD Line</span>
                        <span class="indicator-result {'positive' if current['MACD'] > current['MACD_Signal'] else 'negative'}">
                            {current['MACD']:.4f}
                        </span>
                    </div>
                    <div class="indicator-value">
                        <span class="indicator-label">Signal Line</span>
                        <span class="indicator-result">{current['MACD_Signal']:.4f}</span>
                    </div>
                    <div class="indicator-value">
                        <span class="indicator-label">Histogram</span>
                        <span class="indicator-result {'positive' if current['MACD_Hist'] > 0 else 'negative'}">
                            {current['MACD_Hist']:.4f}
                        </span>
                    </div>
                </div>
                
                <div class="indicator-card">
                    <div class="indicator-title">🎯 Bollinger Bands</div>
                    <div class="indicator-value">
                        <span class="indicator-label">Upper Band</span>
                        <span class="indicator-result">{current['BB_Upper']:.2f}</span>
                    </div>
                    <div class="indicator-value">
                        <span class="indicator-label">Middle (SMA20)</span>
                        <span class="indicator-result">{current['BB_Middle']:.2f}</span>
                    </div>
                    <div class="indicator-value">
                        <span class="indicator-label">Lower Band</span>
                        <span class="indicator-result">{current['BB_Lower']:.2f}</span>
                    </div>
                </div>
                
                <div class="indicator-card">
                    <div class="indicator-title">📍 Moving Averages</div>
                    <div class="indicator-value">
                        <span class="indicator-label">SMA20</span>
                        <span class="indicator-result">{current['SMA20']:.2f}</span>
                    </div>
                    <div class="indicator-value">
                        <span class="indicator-label">SMA50</span>
                        <span class="indicator-result">{current['SMA50']:.2f}</span>
                    </div>
                    <div class="indicator-value">
                        <span class="indicator-label">SMA200</span>
                        <span class="indicator-result">{current['SMA200']:.2f}</span>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="instructions">
            <h3>📋 Latest Candlestick Pattern Analysis</h3>
            <div class="pattern-alert">
                <strong>Latest Pattern:</strong> {self.identify_candlestick_pattern(len(signals_df)-1)}
            </div>
            
            <h3 style="margin-top: 20px;">🎯 Trading Instructions</h3>
            <ul>
                <li><strong>When Signal is 🟢 BUY:</strong> Enter long position, set stop-loss below recent support</li>
                <li><strong>When Signal is 🔴 SELL:</strong> Exit long or enter short, set stop-loss above recent resistance</li>
                <li><strong>RSI < 30:</strong> Stock is oversold, potential buying opportunity</li>
                <li><strong>RSI > 70:</strong> Stock is overbought, potential selling opportunity</li>
                <li><strong>MACD Crossover:</strong> Watch for MACD crossing signal line for momentum shift</li>
                <li><strong>Price Beyond BB:</strong> Price outside Bollinger Bands suggests reversal</li>
                <li><strong>Moving Average Alignment:</strong> When SMA20 > SMA50 > SMA200, trend is up</li>
                <li><strong>Risk Management:</strong> Always maintain 2:1 risk/reward ratio</li>
                <li><strong>Position Size:</strong> Never risk more than 1% of account per trade</li>
                <li><strong>Stop-Loss:</strong> ALWAYS set stop-loss before entering position</li>
            </ul>
        </div>
    </div>
    
    <script>
        // Create candlestick chart
        const ctx = document.getElementById('candleChart').getContext('2d');
        
        const candles = {json.dumps(candle_data)};
        
        // Simple candlestick data preparation
        const chartLabels = candles.map(c => c.x);
        const openPrices = candles.map(c => c.o);
        const closePrices = candles.map(c => c.c);
        const highPrices = candles.map(c => c.h);
        const lowPrices = candles.map(c => c.l);
        
        // Color based on close vs open
        const colors = closePrices.map((close, i) => 
            close >= openPrices[i] ? 'rgba(0, 170, 0, 0.6)' : 'rgba(221, 0, 0, 0.6)'
        );
        
        new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: chartLabels,
                datasets: [
                    {{
                        label: 'Close Price',
                        data: closePrices,
                        borderColor: 'rgb(102, 126, 234)',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        borderWidth: 2,
                        fill: false,
                        pointRadius: 3,
                        pointBackgroundColor: colors,
                        tension: 0.1
                    }},
                    {{
                        label: 'SMA20',
                        data: {json.dumps([round(x, 2) for x in display_df['SMA20'].tolist()])},
                        borderColor: 'rgba(255, 165, 0, 0.8)',
                        borderWidth: 1.5,
                        fill: false,
                        pointRadius: 1,
                        tension: 0.1
                    }},
                    {{
                        label: 'SMA50',
                        data: {json.dumps([round(x, 2) for x in display_df['SMA50'].tolist()])},
                        borderColor: 'rgba(220, 20, 60, 0.8)',
                        borderWidth: 1.5,
                        fill: false,
                        pointRadius: 1,
                        tension: 0.1
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top'
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: false,
                        title: {{
                            display: true,
                            text: 'Price (₹)'
                        }}
                    }},
                    x: {{
                        title: {{
                            display: true,
                            text: 'Time'
                        }}
                    }}
                }}
            }}
        }});
        
        // Auto-refresh every minute
        setTimeout(function() {{
            location.reload();
        }}, 60000);
    </script>
</body>
</html>
        """
        
        return html
    
    def save_dashboard(self, output_file: str = None) -> str:
        """Generate and save dashboard"""
        if output_file is None:
            output_file = f"trading_dashboard_{self.stock_symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        signals_df = self.generate_signals()
        html = self.generate_html_dashboard(signals_df)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Dashboard saved: {output_file}")
        print(f"📊 Open in browser to view real-time charts and indicators")
        
        return output_file

def main():
    """Main execution"""
    import sys
    
    # Get symbol from command line or use default
    symbol = sys.argv[1] if len(sys.argv) > 1 else "GUJARATALKALI"
    
    print(f"\n📊 Generating Real-Time Trading Dashboard for {symbol}...")
    print("=" * 70)
    
    try:
        # Create dashboard
        dashboard = RealtimeTradingDashboard()
        
        # Fetch live data
        print(f"📈 Fetching live data for {symbol}...")
        dashboard.fetch_live_data(symbol, days=5)
        
        # Generate and save
        output_file = dashboard.save_dashboard()
        
        print("\n✅ Dashboard Generated Successfully!")
        print(f"📍 File: {output_file}")
        print(f"\n💡 Open the HTML file in your browser to see:")
        print("   ✓ Real-time candlestick charts")
        print("   ✓ Technical indicators (RSI, MACD, BB, MA)")
        print("   ✓ Buy/Sell signals with confidence levels")
        print("   ✓ Candlestick pattern recognition")
        print("   ✓ Auto-refresh every minute with latest data")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
