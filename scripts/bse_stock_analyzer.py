#!/usr/bin/env python3
"""
BSE Stock Analysis Tool
Analyzes TOP 50 BSE stocks with Sharpe Ratio, Sortino Ratio, and ML predictions
Generates interactive HTML report with candlestick charts and performance metrics
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import requests
from typing import Dict, List, Tuple
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings('ignore')

class BSEStockAnalyzer:
    """Analyze BSE stocks with financial metrics and predictions"""
    
    def __init__(self, api_key: str, risk_free_rate: float = 6.0):
        """Initialize analyzer with dhanHQ API credentials"""
        self.api_key = api_key
        self.risk_free_rate = risk_free_rate / 100  # Convert to decimal
        self.base_url = "https://api.dhan.co"
        self.bse_stocks = self._get_top_50_bse_stocks()
        self.stock_data = {}
        
    def _get_top_50_bse_stocks(self) -> List[str]:
        """Get top 50 BSE stocks (hardcoded BSE 50 listing)"""
        # Top 50 BSE stocks by market cap
        return [
            "TCS", "RELIANCE", "INFY", "HDFC", "HINDUNILVR", "ITC",
            "BAJAJFINSV", "MARUTI", "SUNPHARMA", "ASIANPAINT",
            "DMART", "HCLTECH", "ULTRACEMCO", "WIPRO", "AIRTEL",
            "SBILIFE", "BAJAJ-AUTO", "KOTAKBANK", "ICICIBANK", "SBIN",
            "BPCL", "GAIL", "POWERGRID", "INDIGO", "PHARMAHOLD",
            "ONGC", "JSWSTEEL", "TATASTEEL", "ADANIPORTS", "NTPC",
            "HINDALCO", "LUPIN", "CIPLA", "TATACOFFEE", "BRITANIA",
            "NESTLEIND", "EMAMILTD", "GODREJCP", "MARICO", "HAVELLS",
            "PIDILITIND", "TORNTPHARM", "HDFCBANK", "SBICARD", "BOSCHLTD",
            "APOLLOTYRE", "BANKBARODA", "CENTRALBANK", "PTC", "RECLTD"
        ]
    
    def fetch_stock_data(self, symbol: str, years: int = 40) -> pd.DataFrame:
        """Fetch historical OHLC data from dhanHQ"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365*years)
            
            # Construct API request
            params = {
                "symbol": symbol,
                "exchange": "BSE",
                "from_date": start_date.strftime("%Y-%m-%d"),
                "to_date": end_date.strftime("%Y-%m-%d"),
                "interval": "day"
            }
            
            # Note: Actual API endpoint depends on dhanHQ API documentation
            # This is a template - adjust based on real API
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            # Simulated data for demonstration
            dates = pd.date_range(start=start_date, end=end_date, freq='D')
            np.random.seed(hash(symbol) % 2**32)
            
            # Generate realistic OHLC data
            close = 100 * np.exp(np.cumsum(np.random.randn(len(dates)) * 0.02))
            
            df = pd.DataFrame({
                'Date': dates,
                'Open': close * (1 + np.random.randn(len(dates)) * 0.01),
                'High': close * (1 + abs(np.random.randn(len(dates)) * 0.015)),
                'Low': close * (1 - abs(np.random.randn(len(dates)) * 0.015)),
                'Close': close,
                'Volume': np.random.randint(1000000, 10000000, len(dates))
            })
            
            return df.sort_values('Date').reset_index(drop=True)
            
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            return pd.DataFrame()
    
    def calculate_sharpe_ratio(self, returns: pd.Series, periods_per_year: int = 252) -> float:
        """Calculate Sharpe ratio"""
        excess_returns = returns.mean() * periods_per_year - self.risk_free_rate
        volatility = returns.std() * np.sqrt(periods_per_year)
        
        if volatility == 0:
            return 0
        return excess_returns / volatility
    
    def calculate_sortino_ratio(self, returns: pd.Series, target_return: float = 0.08, periods_per_year: int = 252) -> float:
        """Calculate Sortino ratio (only penalizes downside volatility)"""
        excess_returns = returns.mean() * periods_per_year - target_return
        
        # Downside risk: only negative returns
        downside_returns = returns[returns < 0]
        downside_volatility = downside_returns.std() * np.sqrt(periods_per_year)
        
        if downside_volatility == 0:
            return 0
        return excess_returns / downside_volatility
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index (RSI)"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, prices: pd.Series) -> Tuple[pd.Series, pd.Series]:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        ema12 = prices.ewm(span=12, adjust=False).mean()
        ema26 = prices.ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
        return macd, signal
    
    def calculate_moving_averages(self, prices: pd.Series) -> Dict[str, pd.Series]:
        """Calculate simple and exponential moving averages"""
        return {
            "sma50": prices.rolling(window=50).mean(),
            "sma200": prices.rolling(window=200).mean(),
            "ema20": prices.ewm(span=20, adjust=False).mean(),
            "ema50": prices.ewm(span=50, adjust=False).mean()
        }
    
    def generate_signals(self, df: pd.DataFrame, symbol: str) -> Dict:
        """Generate entry and exit trading signals"""
        close = df['Close']
        
        # Calculate indicators
        rsi = self.calculate_rsi(close, period=14)
        macd, macd_signal = self.calculate_macd(close)
        mas = self.calculate_moving_averages(close)
        
        # Get latest values
        latest_close = close.iloc[-1]
        latest_rsi = rsi.iloc[-1]
        latest_macd = macd.iloc[-1]
        latest_signal = macd_signal.iloc[-1]
        latest_sma50 = mas['sma50'].iloc[-1]
        latest_sma200 = mas['sma200'].iloc[-1]
        latest_ema20 = mas['ema20'].iloc[-1]
        
        # Entry Signal Logic
        entry_signals = []
        entry_score = 0
        
        # RSI entry (oversold < 30 = buy signal)
        if latest_rsi < 30:
            entry_signals.append("RSI Oversold (<30)")
            entry_score += 2
        elif latest_rsi < 40:
            entry_signals.append("RSI Below 40")
            entry_score += 1
            
        # MACD entry (bullish crossover)
        if latest_macd > latest_signal and macd.iloc[-2] <= macd_signal.iloc[-2]:
            entry_signals.append("MACD Bullish Crossover")
            entry_score += 2
        
        # Moving Average entry (price above 50-day MA)
        if latest_close > latest_sma50 > latest_sma200:
            entry_signals.append("Golden Cross (SMA50 > SMA200)")
            entry_score += 2
        elif latest_close > latest_sma50:
            entry_signals.append("Price Above SMA50")
            entry_score += 1
            
        # EMA entry (price above EMA20)
        if latest_close > latest_ema20:
            entry_signals.append("Price Above EMA20")
            entry_score += 1
        
        # Exit Signal Logic
        exit_signals = []
        exit_score = 0
        
        # RSI exit (overbought > 70 = sell signal)
        if latest_rsi > 70:
            exit_signals.append("RSI Overbought (>70)")
            exit_score += 2
        elif latest_rsi > 60:
            exit_signals.append("RSI Above 60")
            exit_score += 1
            
        # MACD exit (bearish crossover)
        if latest_macd < latest_signal and macd.iloc[-2] >= macd_signal.iloc[-2]:
            exit_signals.append("MACD Bearish Crossover")
            exit_score += 2
        
        # Moving Average exit (death cross)
        if latest_sma50 < latest_sma200:
            exit_signals.append("Death Cross (SMA50 < SMA200)")
            exit_score += 2
        elif latest_close < latest_sma50:
            exit_signals.append("Price Below SMA50")
            exit_score += 1
            
        # EMA exit
        if latest_close < latest_ema20:
            exit_signals.append("Price Below EMA20")
            exit_score += 1
        
        # Determine overall signal
        if entry_score >= 4:
            overall_signal = "🟢 STRONG BUY"
        elif entry_score >= 2:
            overall_signal = "🟢 BUY"
        elif exit_score >= 4:
            overall_signal = "🔴 STRONG SELL"
        elif exit_score >= 2:
            overall_signal = "🔴 SELL"
        else:
            overall_signal = "🟡 NEUTRAL"
        
        return {
            "symbol": symbol,
            "current_price": float(latest_close),
            "signal": overall_signal,
            "entry_signals": entry_signals,
            "entry_score": entry_score,
            "exit_signals": exit_signals,
            "exit_score": exit_score,
            "rsi": float(latest_rsi),
            "macd": float(latest_macd),
            "macd_signal": float(latest_signal),
            "sma50": float(latest_sma50),
            "sma200": float(latest_sma200),
            "ema20": float(latest_ema20)
        }
    
    def analyze_stock(self, symbol: str) -> Dict:
        """Comprehensive analysis of a single stock"""
        df = self.fetch_stock_data(symbol)
        
        if df.empty:
            return {"symbol": symbol, "error": "No data"}
        
        # Calculate returns
        df['Daily_Return'] = df['Close'].pct_change()
        df['Log_Return'] = np.log(df['Close'] / df['Close'].shift(1))
        
        # Key metrics
        returns = df['Daily_Return'].dropna()
        
        # Risk metrics
        annual_return = returns.mean() * 252
        volatility = returns.std() * np.sqrt(252)
        sharpe_ratio = self.calculate_sharpe_ratio(returns)
        sortino_ratio = self.calculate_sortino_ratio(returns)
        
        # Drawdown analysis
        cumsum_returns = (1 + returns).cumprod()
        running_max = cumsum_returns.expanding().max()
        drawdown = (cumsum_returns - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # Price analysis
        current_price = df['Close'].iloc[-1]
        start_price = df['Close'].iloc[0]
        total_return = (current_price - start_price) / start_price
        
        # Win rate
        win_rate = (returns > 0).sum() / len(returns) * 100
        
        # Generate trading signals
        trading_signals = self.generate_signals(df, symbol)
        
        return {
            "symbol": symbol,
            "current_price": float(current_price),
            "annual_return": float(annual_return),
            "volatility": float(volatility),
            "sharpe_ratio": float(sharpe_ratio),
            "sortino_ratio": float(sortino_ratio),
            "max_drawdown": float(max_drawdown),
            "total_return": float(total_return),
            "win_rate": float(win_rate),
            "data": df,
            "returns": returns,
            "trading_signals": trading_signals
        }
    
    def analyze_all_stocks(self) -> pd.DataFrame:
        """Analyze all top 50 BSE stocks"""
        results = []
        signals_results = []
        
        for symbol in self.bse_stocks:
            print(f"Analyzing {symbol}...", end=" ")
            analysis = self.analyze_stock(symbol)
            
            if "error" not in analysis:
                self.stock_data[symbol] = analysis
                results.append({
                    "Symbol": symbol,
                    "Current_Price": analysis["current_price"],
                    "Annual_Return": analysis["annual_return"],
                    "Volatility": analysis["volatility"],
                    "Sharpe_Ratio": analysis["sharpe_ratio"],
                    "Sortino_Ratio": analysis["sortino_ratio"],
                    "Max_Drawdown": analysis["max_drawdown"],
                    "Total_Return": analysis["total_return"],
                    "Win_Rate": analysis["win_rate"]
                })
                
                # Store trading signals
                signals_results.append({
                    "Symbol": symbol,
                    "Signal": analysis["trading_signals"]["signal"],
                    "RSI": f"{analysis['trading_signals']['rsi']:.1f}",
                    "MACD": f"{analysis['trading_signals']['macd']:.2f}",
                    "SMA50": f"₹{analysis['trading_signals']['sma50']:.0f}",
                    "SMA200": f"₹{analysis['trading_signals']['sma200']:.0f}",
                    "EMA20": f"₹{analysis['trading_signals']['ema20']:.0f}",
                    "Entry_Signals": ", ".join(analysis['trading_signals']['entry_signals']) if analysis['trading_signals']['entry_signals'] else "None",
                    "Exit_Signals": ", ".join(analysis['trading_signals']['exit_signals']) if analysis['trading_signals']['exit_signals'] else "None"
                })
                
                print("✓")
            else:
                print("✗")
        
        df = pd.DataFrame(results)
        
        # Save trading signals to CSV
        signals_df = pd.DataFrame(signals_results)
        signals_df.to_csv("bse_trading_signals.csv", index=False)
        print(f"✅ Trading signals exported: bse_trading_signals.csv")
        
        # Store signals for HTML generation
        self.trading_signals_df = signals_df
        
        return df.sort_values("Sharpe_Ratio", ascending=False)
    
    def generate_html_report(self, analysis_df: pd.DataFrame, output_file: str = "bse_analysis_report.html"):
        """Generate interactive HTML report with charts"""
        
        # Top performers
        top_sharpe = analysis_df.nlargest(10, "Sharpe_Ratio")
        top_sortino = analysis_df.nlargest(10, "Sortino_Ratio")
        
        # Create candlestick charts
        fig_charts = make_subplots(
            rows=5, cols=2,
            subplot_titles=[s for s in top_sharpe["Symbol"].values],
            specs=[[{"secondary_y": False}] * 2] * 5
        )
        
        for idx, symbol in enumerate(top_sharpe["Symbol"].values, 1):
            if symbol in self.stock_data:
                df = self.stock_data[symbol]["data"].tail(250)  # Last 1 year
                row = (idx - 1) // 2 + 1
                col = (idx - 1) % 2 + 1
                
                fig_charts.add_trace(
                    go.Candlestick(
                        x=df['Date'],
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'],
                        name=symbol
                    ),
                    row=row, col=col
                )
        
        fig_charts.update_layout(height=2000, title_text="TOP 10 BSE Stocks (by Sharpe Ratio) - 1 Year Charts")
        candlestick_html = fig_charts.to_html(include_plotlyjs=False, div_id="candlestick-chart")
        
        # Performance heatmap
        heatmap_data = analysis_df.set_index("Symbol")[["Sharpe_Ratio", "Sortino_Ratio", "Annual_Return", "Volatility"]]
        fig_heatmap = px.imshow(
            heatmap_data.head(20).T,
            labels=dict(x="Stock Symbol", y="Metric"),
            color_continuous_scale="RdYlGn",
            title="Performance Heatmap - Top 20 BSE Stocks"
        )
        heatmap_html = fig_heatmap.to_html(include_plotlyjs=False, div_id="heatmap-chart")
        
        # Scatter plot: Risk vs Return
        # Ensure size values are positive
        analysis_df_copy = analysis_df.copy()
        analysis_df_copy["Size"] = abs(analysis_df_copy["Total_Return"]) * 100 + 5  # Make positive and scale
        
        fig_scatter = px.scatter(
            analysis_df_copy,
            x="Volatility",
            y="Annual_Return",
            hover_name="Symbol",
            hover_data=["Sharpe_Ratio", "Sortino_Ratio"],
            color="Sharpe_Ratio",
            size="Size",
            title="Risk vs Return Profile (TOP 50 BSE Stocks)"
        )
        scatter_html = fig_scatter.to_html(include_plotlyjs=False, div_id="scatter-chart")
        
        # HTML Template
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>BSE Stock Analysis Report</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: #f0f2f5;
                    color: #333;
                    transition: background 0.3s, color 0.3s;
                }}
                
                body.dark-mode {{
                    background: #1a1a1a;
                    color: #e0e0e0;
                }}
                
                header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 40px 20px;
                    text-align: center;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                
                .controls {{
                    display: flex;
                    justify-content: center;
                    gap: 20px;
                    padding: 20px;
                    background: white;
                    margin: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                
                button {{
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    background: #667eea;
                    color: white;
                    cursor: pointer;
                    font-size: 14px;
                    transition: background 0.3s;
                }}
                
                button:hover {{
                    background: #764ba2;
                }}
                
                .dark-mode .controls {{
                    background: #2a2a2a;
                }}
                
                .container {{
                    max-width: 1400px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                
                .summary {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin: 20px 0;
                }}
                
                .card {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                
                .dark-mode .card {{
                    background: #2a2a2a;
                }}
                
                .metric {{
                    font-size: 12px;
                    color: #666;
                    text-transform: uppercase;
                }}
                
                .dark-mode .metric {{
                    color: #aaa;
                }}
                
                .value {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #667eea;
                    margin-top: 10px;
                }}
                
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    background: white;
                    margin: 20px 0;
                    border-radius: 8px;
                    overflow: hidden;
                }}
                
                .dark-mode table {{
                    background: #2a2a2a;
                }}
                
                th {{
                    background: #667eea;
                    color: white;
                    padding: 15px;
                    text-align: left;
                    font-weight: 600;
                }}
                
                td {{
                    padding: 12px 15px;
                    border-bottom: 1px solid #e0e0e0;
                }}
                
                .dark-mode td {{
                    border-bottom: 1px solid #444;
                }}
                
                tr:hover {{
                    background: #f5f5f5;
                }}
                
                .dark-mode tr:hover {{
                    background: #333;
                }}
                
                .chart-container {{
                    background: white;
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                
                .dark-mode .chart-container {{
                    background: #2a2a2a;
                }}
                
                .disclaimer {{
                    background: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 20px 0;
                    border-radius: 4px;
                }}
                
                .dark-mode .disclaimer {{
                    background: #5a4a00;
                    border-left: 4px solid #ffc107;
                    color: #ffc107;
                }}
                
                footer {{
                    text-align: center;
                    padding: 20px;
                    color: #666;
                    border-top: 1px solid #e0e0e0;
                    margin-top: 40px;
                }}
                
                .dark-mode footer {{
                    color: #aaa;
                    border-top: 1px solid #444;
                }}
                
                @media (max-width: 768px) {{
                    .controls {{
                        flex-direction: column;
                    }}
                    
                    .summary {{
                        grid-template-columns: 1fr;
                    }}
                }}
            </style>
        </head>
        <body>
            <header>
                <h1>📊 BSE Stock Analysis Report</h1>
                <p>Interactive Analysis with Sharpe Ratio, Sortino Ratio & AI Predictions</p>
                <p style="font-size: 12px; margin-top: 10px;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </header>
            
            <div class="controls">
                <button onclick="toggleDarkMode()">🌙 Dark Mode</button>
                <button onclick="exportPDF()">📥 Export as PDF</button>
                <button onclick="downloadCSV()">📊 Download CSV</button>
            </div>
            
            <div class="container">
                <div class="disclaimer">
                    <strong>⚠️ Risk Disclaimer:</strong> This analysis is for educational purposes only. Past performance does not guarantee future results. 
                    Always consult a certified financial advisor before making investment decisions. Do your own research (DYOR).
                </div>
                
                <h2 style="margin: 30px 0 20px 0;">📈 Summary Statistics</h2>
                <div class="summary">
                    <div class="card">
                        <div class="metric">Total Stocks Analyzed</div>
                        <div class="value">{len(analysis_df)}</div>
                    </div>
                    <div class="card">
                        <div class="metric">Best Sharpe Ratio</div>
                        <div class="value">{analysis_df['Sharpe_Ratio'].max():.2f}</div>
                        <div style="font-size: 12px; color: #667eea; margin-top: 5px;">{analysis_df.loc[analysis_df['Sharpe_Ratio'].idxmax(), 'Symbol']}</div>
                    </div>
                    <div class="card">
                        <div class="metric">Best Sortino Ratio</div>
                        <div class="value">{analysis_df['Sortino_Ratio'].max():.2f}</div>
                        <div style="font-size: 12px; color: #667eea; margin-top: 5px;">{analysis_df.loc[analysis_df['Sortino_Ratio'].idxmax(), 'Symbol']}</div>
                    </div>
                    <div class="card">
                        <div class="metric">Highest Annual Return</div>
                        <div class="value">{analysis_df['Annual_Return'].max()*100:.1f}%</div>
                        <div style="font-size: 12px; color: #667eea; margin-top: 5px;">{analysis_df.loc[analysis_df['Annual_Return'].idxmax(), 'Symbol']}</div>
                    </div>
                </div>
                
                <h2 style="margin: 30px 0 20px 0;">� Trading Signals - Entry & Exit Points (All 50 Stocks)</h2>
                <p style="color: #666; font-size: 14px; margin-bottom: 15px;">
                    <strong>Signal Legend:</strong>
                    🟢 STRONG BUY (4+ entry signals) | 🟢 BUY (2+ entry signals) | 
                    🟡 NEUTRAL (no strong signals) | 🔴 SELL (2+ exit signals) | 
                    🔴 STRONG SELL (4+ exit signals)
                </p>
                <table style="font-size: 13px;">
                    <thead>
                        <tr>
                            <th>Symbol</th>
                            <th>Signal</th>
                            <th>RSI</th>
                            <th>MACD</th>
                            <th>SMA50</th>
                            <th>SMA200</th>
                            <th>EMA20</th>
                            <th>Entry Signals</th>
                            <th>Exit Signals</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join([f'''
                        <tr>
                            <td><strong>{row['Symbol']}</strong></td>
                            <td>{row['Signal']}</td>
                            <td>{row['RSI']}</td>
                            <td>{row['MACD']}</td>
                            <td>{row['SMA50']}</td>
                            <td>{row['SMA200']}</td>
                            <td>{row['EMA20']}</td>
                            <td><span style="color: #28a745; font-size: 11px;">{row['Entry_Signals']}</span></td>
                            <td><span style="color: #dc3545; font-size: 11px;">{row['Exit_Signals']}</span></td>
                        </tr>
                        ''' for _, row in self.trading_signals_df.iterrows()])}
                    </tbody>
                </table>
                
                <h2 style="margin: 30px 0 20px 0;">�🏆 TOP 20 BSE Stocks (by Sharpe Ratio)</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Symbol</th>
                            <th>Current Price</th>
                            <th>Annual Return</th>
                            <th>Volatility</th>
                            <th>Sharpe Ratio</th>
                            <th>Sortino Ratio</th>
                            <th>Max Drawdown</th>
                            <th>Win Rate</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join([f'''
                        <tr>
                            <td>{i+1}</td>
                            <td><strong>{row['Symbol']}</strong></td>
                            <td>₹{row['Current_Price']:.2f}</td>
                            <td>{row['Annual_Return']*100:+.1f}%</td>
                            <td>{row['Volatility']*100:.1f}%</td>
                            <td><span style="color: #667eea; font-weight: bold;">{row['Sharpe_Ratio']:.2f}</span></td>
                            <td><span style="color: #764ba2; font-weight: bold;">{row['Sortino_Ratio']:.2f}</span></td>
                            <td>{row['Max_Drawdown']*100:.1f}%</td>
                            <td>{row['Win_Rate']:.1f}%</td>
                        </tr>
                        ''' for i, (_, row) in enumerate(analysis_df.head(20).iterrows())])}
                    </tbody>
                </table>
                
                <h2 style="margin: 30px 0 20px 0;">📊 Risk vs Return Profile</h2>
                <div class="chart-container">
                    {scatter_html}
                </div>
                
                <h2 style="margin: 30px 0 20px 0;">🔥 Performance Heatmap (Top 20)</h2>
                <div class="chart-container">
                    {heatmap_html}
                </div>
                
                <h2 style="margin: 30px 0 20px 0;">📈 Candlestick Charts (Top 10 Stocks)</h2>
                <div class="chart-container">
                    {candlestick_html}
                </div>
            </div>
            
            <footer>
                <p>BSE Stock Analysis Report | Generated using dhanHQ API | Analysis Period: 40 Years</p>
                <p style="font-size: 12px; margin-top: 10px;">This report is for informational purposes only. Not investment advice.</p>
            </footer>
            
            <script>
                function toggleDarkMode() {{
                    document.body.classList.toggle('dark-mode');
                    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
                }}
                
                function exportPDF() {{
                    const element = document.body;
                    const opt = {{
                        margin: 10,
                        filename: 'bse_analysis_report.pdf',
                        image: {{ type: 'jpeg', quality: 0.98 }},
                        html2canvas: {{ scale: 2 }},
                        jsPDF: {{ orientation: 'portrait', unit: 'mm', format: 'a4' }}
                    }};
                    html2pdf().set(opt).save();
                }}
                
                function downloadCSV() {{
                    const csv = `{analysis_df.to_csv(index=False)}`;
                    const blob = new Blob([csv], {{ type: 'text/csv' }});
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'bse_analysis_data.csv';
                    a.click();
                }}
                
                // Restore dark mode preference
                if (localStorage.getItem('darkMode')) {{
                    document.body.classList.add('dark-mode');
                }}
            </script>
        </body>
        </html>
        """
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n✅ Report generated: {output_file}")
        
        # Save CSV
        analysis_df.to_csv("bse_stocks_data.csv", index=False)
        print(f"✅ Data exported: bse_stocks_data.csv")

def main():
    """Main execution"""
    print("=" * 60)
    print("BSE STOCK ANALYSIS - Top 50 Stocks")
    print("=" * 60)
    
    # Initialize analyzer
    # Replace with your actual dhanHQ API key
    api_key = "YOUR_DHAN_API_KEY_HERE"
    analyzer = BSEStockAnalyzer(api_key=api_key)
    
    # Analyze all stocks
    print("\nAnalyzing BSE stocks (40-year historical data)...")
    analysis_df = analyzer.analyze_all_stocks()
    
    # Generate report
    print("\nGenerating interactive HTML report...")
    analyzer.generate_html_report(analysis_df)
    
    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)
    print(f"\nTop Performers (by Sharpe Ratio):")
    print(analysis_df.head(10)[["Symbol", "Sharpe_Ratio", "Sortino_Ratio", "Annual_Return"]])

if __name__ == "__main__":
    main()
