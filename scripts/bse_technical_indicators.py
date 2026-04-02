#!/usr/bin/env python3
"""
Enhanced BSE Stock Analysis with Technical Indicators
Includes: Bollinger Bands, MACD, RSI, Moving Averages, and more
Generates advanced technical analysis HTML report
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import warnings
from typing import Dict, Tuple

warnings.filterwarnings('ignore')

class TechnicalAnalyzer:
    """Calculate technical indicators for stock analysis"""
    
    @staticmethod
    def calculate_sma(prices: pd.Series, period: int = 20) -> pd.Series:
        """Simple Moving Average"""
        return prices.rolling(window=period).mean()
    
    @staticmethod
    def calculate_ema(prices: pd.Series, period: int = 20) -> pd.Series:
        """Exponential Moving Average"""
        return prices.ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
        """Relative Strength Index (0-100)
        < 30: Oversold (potential buy)
        > 70: Overbought (potential sell)
        """
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def calculate_macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """MACD (Moving Average Convergence Divergence)
        Returns: MACD line, Signal line, Histogram
        
        Interpretation:
        - MACD > Signal: Bullish
        - MACD < Signal: Bearish
        - Histogram: Momentum strength
        """
        ema_fast = prices.ewm(span=fast, adjust=False).mean()
        ema_slow = prices.ewm(span=slow, adjust=False).mean()
        
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        
        return macd, signal_line, histogram
    
    @staticmethod
    def calculate_bollinger_bands(prices: pd.Series, period: int = 20, num_std: float = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Bollinger Bands
        Returns: Upper Band, Middle Band (SMA), Lower Band
        
        Interpretation:
        - Price touches upper band: Potential sell
        - Price touches lower band: Potential buy
        - Band width: Volatility measure
        """
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        
        upper_band = sma + (std * num_std)
        lower_band = sma - (std * num_std)
        
        return upper_band, sma, lower_band
    
    @staticmethod
    def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """Average True Range - Volatility measure
        High ATR: High volatility
        Low ATR: Low volatility
        """
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        
        return atr
    
    @staticmethod
    def calculate_adx(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Average Directional Index - Trend strength
        Returns: +DI, -DI, ADX
        
        ADX Interpretation:
        0-25: Weak trend
        25-50: Moderate trend
        50-75: Strong trend
        75-100: Very strong trend
        """
        plus_dm = high.diff()
        minus_dm = -low.diff()
        
        plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0)
        minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0)
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        atr = tr.rolling(window=period).mean()
        plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(window=period).mean() / atr)
        
        di_diff = abs(plus_di - minus_di)
        di_sum = plus_di + minus_di
        dx = 100 * (di_diff / di_sum)
        adx = dx.rolling(window=period).mean()
        
        return plus_di, minus_di, adx
    
    @staticmethod
    def calculate_stochastic(high: pd.Series, low: pd.Series, close: pd.Series, 
                            period: int = 14, smooth_k: int = 3, smooth_d: int = 3) -> Tuple[pd.Series, pd.Series]:
        """Stochastic Oscillator (0-100)
        < 20: Oversold
        > 80: Overbought
        
        Returns: %K, %D
        """
        lowest_low = low.rolling(window=period).min()
        highest_high = high.rolling(window=period).max()
        
        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        k_line = k_percent.rolling(window=smooth_k).mean()
        d_line = k_line.rolling(window=smooth_d).mean()
        
        return k_line, d_line
    
    @staticmethod
    def calculate_obv(close: pd.Series, volume: pd.Series) -> pd.Series:
        """On Balance Volume - Volume trend indicator
        Rising OBV: Accumulation
        Falling OBV: Distribution
        """
        obv = (np.sign(close.diff()) * volume).fillna(0).cumsum()
        return obv

class EnhancedBSEAnalyzer:
    """Enhanced BSE analyzer with technical indicators"""
    
    def __init__(self):
        self.technical = TechnicalAnalyzer()
        self.stocks = [
            "TCS", "RELIANCE", "INFY", "HDFC", "HINDUNILVR", "ITC",
            "BAJAJFINSV", "MARUTI", "SUNPHARMA", "ASIANPAINT"
        ]
    
    def analyze_stock_technical(self, symbol: str, df: pd.DataFrame) -> Dict:
        """Calculate all technical indicators for a stock"""
        close = df['Close']
        high = df['High']
        low = df['Low']
        volume = df['Volume']
        
        # Moving Averages
        sma_20 = self.technical.calculate_sma(close, 20)
        sma_50 = self.technical.calculate_sma(close, 50)
        sma_200 = self.technical.calculate_sma(close, 200)
        ema_12 = self.technical.calculate_ema(close, 12)
        ema_26 = self.technical.calculate_ema(close, 26)
        
        # Momentum Indicators
        rsi = self.technical.calculate_rsi(close, 14)
        macd, signal, histogram = self.technical.calculate_macd(close)
        
        # Volatility Indicators
        upper_bb, middle_bb, lower_bb = self.technical.calculate_bollinger_bands(close, 20, 2)
        atr = self.technical.calculate_atr(high, low, close, 14)
        
        # Trend Indicators
        plus_di, minus_di, adx = self.technical.calculate_adx(high, low, close, 14)
        
        # Stochastic
        k_line, d_line = self.technical.calculate_stochastic(high, low, close)
        
        # Volume
        obv = self.technical.calculate_obv(close, volume)
        
        # Current values
        current_close = close.iloc[-1]
        current_rsi = rsi.iloc[-1]
        current_macd = macd.iloc[-1]
        current_signal = signal.iloc[-1]
        current_adx = adx.iloc[-1]
        current_k = k_line.iloc[-1]
        current_d = d_line.iloc[-1]
        
        # Signal generation
        signals = {
            "rsi_oversold": current_rsi < 30,
            "rsi_overbought": current_rsi > 70,
            "macd_bullish": current_macd > current_signal,
            "macd_bearish": current_macd < current_signal,
            "bb_upper_touch": current_close > upper_bb.iloc[-1],
            "bb_lower_touch": current_close < lower_bb.iloc[-1],
            "adx_strong_trend": current_adx > 25,
            "stoch_oversold": current_k < 20,
            "stoch_overbought": current_k > 80
        }
        
        # Generate trading signal
        bullish_count = sum([signals["rsi_oversold"], signals["macd_bullish"], 
                            signals["bb_lower_touch"], signals["stoch_oversold"]])
        bearish_count = sum([signals["rsi_overbought"], signals["macd_bearish"],
                            signals["bb_upper_touch"], signals["stoch_overbought"]])
        
        if bullish_count >= 2:
            signal_type = "STRONG BUY"
            signal_score = 90
        elif bullish_count == 1:
            signal_type = "BUY"
            signal_score = 60
        elif bearish_count >= 2:
            signal_type = "STRONG SELL"
            signal_score = -90
        elif bearish_count == 1:
            signal_type = "SELL"
            signal_score = -60
        else:
            signal_type = "NEUTRAL"
            signal_score = 0
        
        return {
            "symbol": symbol,
            "current_price": float(current_close),
            "sma_20": float(sma_20.iloc[-1]),
            "sma_50": float(sma_50.iloc[-1]),
            "sma_200": float(sma_200.iloc[-1]),
            "rsi": float(current_rsi),
            "macd": float(current_macd),
            "macd_signal": float(current_signal),
            "macd_histogram": float(histogram.iloc[-1]),
            "bb_upper": float(upper_bb.iloc[-1]),
            "bb_middle": float(middle_bb.iloc[-1]),
            "bb_lower": float(lower_bb.iloc[-1]),
            "atr": float(atr.iloc[-1]),
            "adx": float(current_adx),
            "plus_di": float(plus_di.iloc[-1]),
            "minus_di": float(minus_di.iloc[-1]),
            "stochastic_k": float(current_k),
            "stochastic_d": float(current_d),
            "obv": float(obv.iloc[-1]),
            "signals": signals,
            "signal_type": signal_type,
            "signal_score": signal_score,
            "full_data": {
                "sma_20": sma_20,
                "sma_50": sma_50,
                "sma_200": sma_200,
                "rsi": rsi,
                "macd": macd,
                "signal": signal,
                "upper_bb": upper_bb,
                "middle_bb": middle_bb,
                "lower_bb": lower_bb,
                "k_line": k_line,
                "d_line": d_line
            }
        }
    
    def generate_technical_html_report(self, analysis_results: list, output_file: str = "bse_technical_analysis.html"):
        """Generate HTML report with technical indicators"""
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>BSE Technical Analysis Report</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
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
                }}
                
                header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 40px 20px;
                    text-align: center;
                }}
                
                .container {{
                    max-width: 1400px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                
                .card {{
                    background: white;
                    padding: 20px;
                    margin: 15px 0;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                
                .signal-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin: 20px 0;
                }}
                
                .indicator {{
                    background: #f9f9f9;
                    padding: 15px;
                    border-radius: 5px;
                    border-left: 4px solid #667eea;
                }}
                
                .buy {{
                    color: #28a745;
                    font-weight: bold;
                    font-size: 18px;
                }}
                
                .sell {{
                    color: #dc3545;
                    font-weight: bold;
                    font-size: 18px;
                }}
                
                .neutral {{
                    color: #ffc107;
                    font-weight: bold;
                    font-size: 18px;
                }}
                
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    background: white;
                    margin: 20px 0;
                }}
                
                th {{
                    background: #667eea;
                    color: white;
                    padding: 12px;
                    text-align: left;
                }}
                
                td {{
                    padding: 10px 12px;
                    border-bottom: 1px solid #e0e0e0;
                }}
                
                tr:hover {{
                    background: #f5f5f5;
                }}
            </style>
        </head>
        <body>
            <header>
                <h1>📊 BSE Technical Analysis Report</h1>
                <p>Advanced Indicators: RSI, MACD, Bollinger Bands, Stochastic, ADX</p>
                <p style="font-size: 12px; margin-top: 10px;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </header>
            
            <div class="container">
                <h2 style="margin: 30px 0 20px 0;">🎯 Trading Signals Summary</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Symbol</th>
                            <th>Current Price</th>
                            <th>Signal</th>
                            <th>RSI</th>
                            <th>MACD</th>
                            <th>ADX</th>
                            <th>Stochastic %K</th>
                            <th>Bollinger Bands</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join([f'''
                        <tr>
                            <td><strong>{result['symbol']}</strong></td>
                            <td>₹{result['current_price']:.2f}</td>
                            <td><span class="{'buy' if 'BUY' in result['signal_type'] else 'sell' if 'SELL' in result['signal_type'] else 'neutral'}">{result['signal_type']}</span></td>
                            <td>{result['rsi']:.1f} {'(Oversold)' if result['rsi'] < 30 else '(Overbought)' if result['rsi'] > 70 else ''}</td>
                            <td>{'Bullish' if result['macd'] > result['macd_signal'] else 'Bearish'}</td>
                            <td>{result['adx']:.1f} {'(Strong)' if result['adx'] > 25 else '(Weak)'}</td>
                            <td>{result['stochastic_k']:.1f}% {'(Oversold)' if result['stochastic_k'] < 20 else '(Overbought)' if result['stochastic_k'] > 80 else ''}</td>
                            <td>{'Upper' if result['current_price'] > result['bb_upper'] else 'Lower' if result['current_price'] < result['bb_lower'] else 'Middle'}</td>
                        </tr>
                        ''' for result in analysis_results])}
                    </tbody>
                </table>
                
                <h2 style="margin: 30px 0 20px 0;">📈 Detailed Technical Indicators</h2>
                {"".join([f'''
                <div class="card">
                    <h3>{result['symbol']} - Trading Signal: <span class="{'buy' if 'BUY' in result['signal_type'] else 'sell' if 'SELL' in result['signal_type'] else 'neutral'}">{result['signal_type']}</span></h3>
                    
                    <div class="signal-grid">
                        <div class="indicator">
                            <strong>RSI (14)</strong><br>
                            <span style="font-size: 18px; color: #667eea;">{result['rsi']:.1f}</span>
                            <br><small>{'🔴 Oversold (<30)' if result['rsi'] < 30 else '🟢 Overbought (>70)' if result['rsi'] > 70 else '🟡 Neutral'}</small>
                        </div>
                        
                        <div class="indicator">
                            <strong>MACD</strong><br>
                            <span style="font-size: 18px; color: #667eea;">{result['macd']:.4f}</span>
                            <br><small>Signal: {result['macd_signal']:.4f} | Hist: {result['macd_histogram']:.4f}</small>
                            <br><small>{'🐂 Bullish' if result['signals']['macd_bullish'] else '🐻 Bearish'}</small>
                        </div>
                        
                        <div class="indicator">
                            <strong>Bollinger Bands</strong><br>
                            Upper: ₹{result['bb_upper']:.2f}<br>
                            Mid: ₹{result['bb_middle']:.2f}<br>
                            Lower: ₹{result['bb_lower']:.2f}
                        </div>
                        
                        <div class="indicator">
                            <strong>ADX (Trend)</strong><br>
                            <span style="font-size: 18px; color: #667eea;">{result['adx']:.1f}</span>
                            <br><small>{'💪 Strong (>25)' if result['adx'] > 25 else '😴 Weak (<25)'}</small>
                        </div>
                        
                        <div class="indicator">
                            <strong>Stochastic %K/%D</strong><br>
                            <span style="font-size: 18px; color: #667eea;">{result['stochastic_k']:.1f}% / {result['stochastic_d']:.1f}%</span>
                            <br><small>{'🔴 Oversold (<20)' if result['stochastic_k'] < 20 else '🟢 Overbought (>80)' if result['stochastic_k'] > 80 else '🟡 Neutral'}</small>
                        </div>
                        
                        <div class="indicator">
                            <strong>Moving Averages</strong><br>
                            SMA(20): ₹{result['sma_20']:.2f}<br>
                            SMA(50): ₹{result['sma_50']:.2f}<br>
                            SMA(200): ₹{result['sma_200']:.2f}
                        </div>
                    </div>
                    
                    <h4 style="margin-top: 20px; color: #667eea;">🎲 Technical Signals</h4>
                    <ul style="margin-left: 20px;">
                        <li>{'✓' if result['signals']['rsi_oversold'] else '✗'} RSI Oversold (< 30)</li>
                        <li>{'✓' if result['signals']['rsi_overbought'] else '✗'} RSI Overbought (> 70)</li>
                        <li>{'✓' if result['signals']['macd_bullish'] else '✗'} MACD Bullish Crossover</li>
                        <li>{'✓' if result['signals']['bb_lower_touch'] else '✗'} Price near Bollinger Lower Band</li>
                        <li>{'✓' if result['signals']['adx_strong_trend'] else '✗'} ADX Strong Trend (> 25)</li>
                        <li>{'✓' if result['signals']['stoch_oversold'] else '✗'} Stochastic Oversold</li>
                    </ul>
                </div>
                ''' for result in analysis_results])}
            </div>
            
            <footer style="text-align: center; padding: 20px; color: #666; border-top: 1px solid #e0e0e0;">
                <p>This is for educational purposes only. Not investment advice. Always consult a financial advisor.</p>
            </footer>
        </body>
        </html>
        """
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Technical analysis report generated: {output_file}")

def main():
    """Generate enhanced technical analysis"""
    print("=" * 60)
    print("ENHANCED BSE TECHNICAL ANALYSIS")
    print("Indicators: RSI, MACD, Bollinger Bands, Stochastic, ADX")
    print("=" * 60)
    
    analyzer = EnhancedBSEAnalyzer()
    results = []
    
    for symbol in analyzer.stocks:
        print(f"\nAnalyzing {symbol}...", end=" ")
        
        # Simulated data (in real scenario, fetch from dhanHQ)
        dates = pd.date_range(start='2020-01-01', end='2026-04-02', freq='D')
        np.random.seed(hash(symbol) % 2**32)
        close = 100 * np.exp(np.cumsum(np.random.randn(len(dates)) * 0.01))
        
        df = pd.DataFrame({
            'Date': dates,
            'Open': close * (1 + np.random.randn(len(dates)) * 0.005),
            'High': close * (1 + abs(np.random.randn(len(dates)) * 0.01)),
            'Low': close * (1 - abs(np.random.randn(len(dates)) * 0.01)),
            'Close': close,
            'Volume': np.random.randint(1000000, 10000000, len(dates))
        })
        
        analysis = analyzer.analyze_stock_technical(symbol, df)
        results.append(analysis)
        print(f"✓ Signal: {analysis['signal_type']}")
    
    # Generate report
    analyzer.generate_technical_html_report(results)
    
    print("\n" + "=" * 60)
    print("Technical Analysis Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
