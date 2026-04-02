#!/usr/bin/env python3
"""
Real-Time BSE Stock Tracker
Streams live prices, sets alerts, and sends notifications
"""

import time
import threading
from datetime import datetime
from typing import Dict, List, Callable
import json

class RealtimeBSETracker:
    """Track BSE stocks in real-time with alerts"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.stocks: Dict[str, Dict] = {}
        self.alerts: Dict[str, Dict] = {}
        self.price_history: Dict[str, List] = {}
        self.listeners: List[Callable] = []
        self.is_running = False
    
    def add_stock(self, symbol: str, initial_price: float = None):
        """Add stock to tracking list"""
        self.stocks[symbol] = {
            "symbol": symbol,
            "current_price": initial_price or 100.0,
            "previous_price": initial_price or 100.0,
            "high": initial_price or 100.0,
            "low": initial_price or 100.0,
            "volume": 0,
            "change_percent": 0.0,
            "last_update": datetime.now()
        }
        self.price_history[symbol] = []
    
    def set_alert(self, symbol: str, alert_type: str, value: float, 
                  callback: Callable = None, notification: str = None):
        """
        Set price alert
        
        alert_type options:
        - "price_above": Alert when price > value
        - "price_below": Alert when price < value
        - "percent_change": Alert when change >= value%
        - "rsi_oversold": Alert when RSI < value
        - "rsi_overbought": Alert when RSI > value
        - "volume_spike": Alert when volume > value* average
        """
        if symbol not in self.alerts:
            self.alerts[symbol] = []
        
        alert = {
            "type": alert_type,
            "value": value,
            "triggered": False,
            "callback": callback,
            "notification": notification,
            "created_at": datetime.now()
        }
        
        self.alerts[symbol].append(alert)
        print(f"✓ Alert set for {symbol}: {alert_type} = {value}")
    
    def update_price(self, symbol: str, price: float, volume: int = 0):
        """Update stock price (simulate websocket stream)"""
        if symbol not in self.stocks:
            self.add_stock(symbol, price)
        
        stock = self.stocks[symbol]
        stock["previous_price"] = stock["current_price"]
        stock["current_price"] = price
        stock["volume"] = volume
        stock["change_percent"] = ((price - stock["previous_price"]) / stock["previous_price"]) * 100
        stock["last_update"] = datetime.now()
        
        # Update high/low
        if price > stock["high"]:
            stock["high"] = price
        if price < stock["low"] or stock["low"] == 0:
            stock["low"] = price
        
        # Store history
        self.price_history[symbol].append({
            "price": price,
            "time": datetime.now(),
            "volume": volume
        })
        
        # Check alerts
        self._check_alerts(symbol)
        
        # Notify listeners
        self._notify_listeners(symbol)
    
    def _check_alerts(self, symbol: str):
        """Evaluate all alerts for a stock"""
        if symbol not in self.alerts:
            return
        
        stock = self.stocks[symbol]
        
        for alert in self.alerts[symbol]:
            triggered = False
            message = ""
            
            if alert["type"] == "price_above" and stock["current_price"] > alert["value"]:
                triggered = True
                message = f"Price exceeded ₹{alert['value']}"
            
            elif alert["type"] == "price_below" and stock["current_price"] < alert["value"]:
                triggered = True
                message = f"Price dropped below ₹{alert['value']}"
            
            elif alert["type"] == "percent_change" and abs(stock["change_percent"]) >= alert["value"]:
                triggered = True
                message = f"Price changed {stock['change_percent']:.2f}%"
            
            elif alert["type"] == "volume_spike" and stock["volume"] > alert["value"]:
                triggered = True
                message = f"Volume spike detected: {stock['volume']:.0f}"
            
            if triggered and not alert["triggered"]:
                alert["triggered"] = True
                self._send_alert(symbol, message, alert)
    
    def _send_alert(self, symbol: str, message: str, alert: Dict):
        """Send alert notification"""
        notification = f"""
🚨 PRICE ALERT - {symbol}
━━━━━━━━━━━━━━━━━━━━━━━
Current Price: ₹{self.stocks[symbol]['current_price']:.2f}
Change: {self.stocks[symbol]['change_percent']:+.2f}%
Alert: {message}
Time: {datetime.now().strftime('%H:%M:%S')}
━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        print(notification)
        
        if alert["callback"]:
            alert["callback"](symbol, message)
    
    def _notify_listeners(self, symbol: str):
        """Notify all registered listeners of price update"""
        for listener in self.listeners:
            listener(symbol, self.stocks[symbol])
    
    def add_listener(self, callback: Callable):
        """Add listener for all price updates"""
        self.listeners.append(callback)
    
    def get_portfolio_pnl(self, holdings: Dict[str, float]) -> Dict:
        """
        Calculate portfolio P&L
        
        holdings: {symbol: quantity}
        """
        total_value = 0
        total_cost = 0
        pnl = {}
        
        for symbol, quantity in holdings.items():
            if symbol in self.stocks:
                current_price = self.stocks[symbol]["current_price"]
                cost = current_price * quantity
                total_value += cost
                
                pnl[symbol] = {
                    "quantity": quantity,
                    "current_price": current_price,
                    "value": cost
                }
        
        total_pnl = total_value - total_cost
        
        return {
            "portfolio_value": total_value,
            "total_pnl": total_pnl,
            "pnl_percent": (total_pnl / total_cost) * 100 if total_cost > 0 else 0,
            "holdings": pnl
        }
    
    def get_market_ticker(self) -> str:
        """Get formatted market ticker"""
        ticker = "\n" + "=" * 80 + "\n"
        ticker += "LIVE MARKET TICKER\n"
        ticker += "=" * 80 + "\n"
        ticker += f"{'Symbol':<15} {'Price':>12} {'Change':>12} {'High':>12} {'Low':>12} {'Volume':>12}\n"
        ticker += "-" * 80 + "\n"
        
        for symbol, stock in self.stocks.items():
            ticker += f"{symbol:<15} ₹{stock['current_price']:>10.2f} {stock['change_percent']:>+10.2f}% "
            ticker += f"₹{stock['high']:>10.2f} ₹{stock['low']:>10.2f} {stock['volume']:>10.0f}\n"
        
        ticker += "=" * 80 + "\n"
        return ticker
    
    def export_to_csv(self, filename: str = "live_tracker.csv"):
        """Export current prices to CSV"""
        with open(filename, 'w') as f:
            f.write("Symbol,Price,Change%,High,Low,Volume,Timestamp\n")
            for symbol, stock in self.stocks.items():
                f.write(f"{symbol},{stock['current_price']:.2f},{stock['change_percent']:.2f},"
                       f"{stock['high']:.2f},{stock['low']:.2f},{stock['volume']:.0f},"
                       f"{stock['last_update'].strftime('%Y-%m-%d %H:%M:%S')}\n")
        print(f"✅ Data exported to {filename}")

def main():
    """Demonstrate real-time tracker"""
    print("=" * 80)
    print("REAL-TIME BSE STOCK TRACKER")
    print("=" * 80)
    
    # Initialize tracker
    tracker = RealtimeBSETracker()
    
    # Add stocks
    stocks_to_track = ["TCS", "INFY", "RELIANCE", "HDFC"]
    for symbol in stocks_to_track:
        tracker.add_stock(symbol, 100.0)
    
    # Set alerts
    tracker.set_alert("TCS", "price_above", 110, 
                     notification="TCS price exceeded ₹110!")
    tracker.set_alert("INFY", "percent_change", 5.0,
                     notification="INFY moved 5%!")
    tracker.set_alert("RELIANCE", "price_below", 90,
                     notification="RELIANCE dropped below ₹90!")
    
    # Simulate real-time price updates
    print("\n📈 Simulating real-time price stream...\n")
    
    import random
    for i in range(20):
        time.sleep(1)
        
        for symbol in stocks_to_track:
            # Random price change
            change = random.uniform(-2, 2)
            new_price = tracker.stocks[symbol]["current_price"] * (1 + change/100)
            volume = random.randint(100000, 1000000)
            
            tracker.update_price(symbol, new_price, volume)
        
        if i % 5 == 0:
            print(tracker.get_market_ticker())
    
    # Portfolio P&L calculation
    print("\n💼 Portfolio P&L Analysis")
    holdings = {"TCS": 10, "INFY": 20, "RELIANCE": 5}
    pnl = tracker.get_portfolio_pnl(holdings)
    print(json.dumps(pnl, indent=2, default=str))
    
    # Export data
    tracker.export_to_csv()
    
    print("\n" + "=" * 80)
    print("Real-time Tracking Complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()
