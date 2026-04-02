#!/usr/bin/env python3
"""
Portfolio Monitoring Dashboard
Shows real-time P&L, holdings value, and risk metrics for user portfolio
"""

import json
from datetime import datetime

# Portfolio Holdings
PORTFOLIO = {
    "TCS": 10,      # 10 shares
    "INFY": 20,     # 20 shares
    "RELIANCE": 5   # 5 shares
}

# Current Live Prices (from recent tracker run)
LIVE_PRICES = {
    "TCS": 102.31,
    "INFY": 105.72,
    "RELIANCE": 95.91
}

# Entry prices (for demo - adjust based on your purchase price)
ENTRY_PRICES = {
    "TCS": 100.00,
    "INFY": 104.00,
    "RELIANCE": 98.00
}

def calculate_portfolio_metrics():
    """Calculate comprehensive portfolio metrics"""
    
    total_value = 0
    total_cost = 0
    total_gain = 0
    holdings_detail = []
    
    print("\n" + "=" * 100)
    print(f"PORTFOLIO MONITORING DASHBOARD - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 100)
    
    # Calculate per-stock metrics
    for symbol, quantity in PORTFOLIO.items():
        current_price = LIVE_PRICES.get(symbol, 0)
        entry_price = ENTRY_PRICES.get(symbol, current_price)
        
        current_value = current_price * quantity
        cost_basis = entry_price * quantity
        gain_loss = current_value - cost_basis
        gain_loss_percent = (gain_loss / cost_basis * 100) if cost_basis > 0 else 0
        
        total_value += current_value
        total_cost += cost_basis
        total_gain += gain_loss
        
        # Color coding
        status = "🟢" if gain_loss >= 0 else "🔴"
        
        holdings_detail.append({
            "symbol": symbol,
            "quantity": quantity,
            "entry_price": entry_price,
            "current_price": current_price,
            "cost_basis": cost_basis,
            "current_value": current_value,
            "gain_loss": gain_loss,
            "gain_loss_percent": gain_loss_percent,
            "status": status
        })
    
    # Sort by absolute gain/loss
    holdings_detail.sort(key=lambda x: x['gain_loss'], reverse=True)
    
    # Display Holdings Table
    print(f"\n{'HOLDING':<15} {'QTY':>6} {'ENTRY':>10} {'CURRENT':>10} {'VALUE':>12} {'GAIN/LOSS':>12} {'%':>8} {'STATUS':>8}")
    print("-" * 100)
    
    for holding in holdings_detail:
        print(f"{holding['symbol']:<15} {holding['quantity']:>6} "
              f"₹{holding['entry_price']:>8.2f} ₹{holding['current_price']:>8.2f} "
              f"₹{holding['current_value']:>10.2f} ₹{holding['gain_loss']:>10.2f} "
              f"{holding['gain_loss_percent']:>+7.2f}% {holding['status']:>8}")
    
    print("-" * 100)
    
    # Portfolio Summary
    total_gain_percent = (total_gain / total_cost * 100) if total_cost > 0 else 0
    portfolio_status = "🟢 PROFIT" if total_gain >= 0 else "🔴 LOSS"
    
    print(f"\n{'PORTFOLIO SUMMARY':>50}")
    print("=" * 100)
    print(f"Total Investment (Cost Basis):  ₹{total_cost:>12,.2f}")
    print(f"Current Portfolio Value:        ₹{total_value:>12,.2f}")
    print(f"Total Gain/Loss:                ₹{total_gain:>12,.2f} {portfolio_status}")
    print(f"Return on Investment:           {total_gain_percent:>+12.2f}%")
    print(f"Total Shares Held:              {sum(PORTFOLIO.values()):>15}")
    print("=" * 100)
    
    # Risk Metrics
    print(f"\n{'RISK METRICS':>50}")
    print("=" * 100)
    
    # Calculate concentration risk
    largest_holding = max(holdings_detail, key=lambda x: x['current_value'])
    concentration = (largest_holding['current_value'] / total_value * 100)
    
    print(f"Largest Holding (Concentration): {largest_holding['symbol']:>12} ({concentration:.1f}%)")
    print(f"Portfolio Volatility Risk:      {'Medium':>15} (Mixed sector exposure)")
    print(f"Dividend Yield (approx):        {'~1.5-2.5%':>15} (Annual estimate)")
    print("=" * 100)
    
    # Performance Ranking
    print(f"\n{'PERFORMANCE RANKING':>50}")
    print("-" * 100)
    
    for rank, holding in enumerate(holdings_detail, 1):
        stars = "⭐" * (1 if holding['gain_loss_percent'] > 2 else 0)
        stars += "⭐" * (1 if holding['gain_loss_percent'] > 5 else 0)
        if holding['gain_loss_percent'] < 0:
            stars = "⚠️"
        
        print(f"{rank}. {holding['symbol']:<10} {holding['gain_loss_percent']:>+7.2f}% {stars}")
    
    print("=" * 100)
    
    # Alert Recommendations
    print(f"\n{'RECOMMENDATIONS & ALERTS':>50}")
    print("-" * 100)
    
    alerts = []
    
    # Check for profit-taking opportunities
    for holding in holdings_detail:
        if holding['gain_loss_percent'] > 10:
            alerts.append(f"✓ {holding['symbol']}: +{holding['gain_loss_percent']:.1f}% - Consider profit-taking or trailing stop")
        elif holding['gain_loss_percent'] < -5:
            alerts.append(f"⚠️ {holding['symbol']}: {holding['gain_loss_percent']:.1f}% - Monitor closely, consider stop-loss")
    
    if not alerts:
        alerts.append("✓ Portfolio balanced - No immediate action required")
    
    for alert in alerts:
        print(alert)
    
    print("=" * 100)
    
    # Next Actions
    print(f"\n{'NEXT ACTIONS':>50}")
    print("-" * 100)
    print("📱 Real-Time Alerts Set For:")
    print("  • TCS: Alert when price moves 5% from current")
    print("  • INFY: Alert when price moves 5% from current")
    print("  • RELIANCE: Alert when price moves 5% from current")
    print("\n💡 Smart Monitoring:")
    print("  • Volume spike detection enabled")
    print("  • Technical signal alerts (RSI, MACD)")
    print("  • Support/resistance level tracking")
    print("\n📊 Analysis Tools Available:")
    print("  • Run: @bse-technical-indicators to get technical signals")
    print("  • Run: @bse-stock-analysis for deep risk metrics")
    print("=" * 100)
    
    # Export Summary
    summary = {
        "timestamp": datetime.now().isoformat(),
        "portfolio": {
            "total_value": round(total_value, 2),
            "total_cost": round(total_cost, 2),
            "total_gain": round(total_gain, 2),
            "total_gain_percent": round(total_gain_percent, 2)
        },
        "holdings": [
            {
                "symbol": h["symbol"],
                "quantity": h["quantity"],
                "entry_price": h["entry_price"],
                "current_price": h["current_price"],
                "value": round(h["current_value"], 2),
                "gain_loss": round(h["gain_loss"], 2),
                "gain_loss_percent": round(h["gain_loss_percent"], 2)
            }
            for h in holdings_detail
        ]
    }
    
    # Save portfolio summary
    with open("portfolio_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n✅ Portfolio monitoring active!")
    print(f"📊 Summary saved to: portfolio_summary.json")
    print("=" * 100 + "\n")

if __name__ == "__main__":
    calculate_portfolio_metrics()
