# Real-Time Trading Dashboard - Complete User Guide

## 🎬 QUICK START (5 Steps)

### Step 1: Open the Dashboard File
```
📁 Location: f:\dotfiles\copilot-agents\

🔍 Find file: trading_dashboard_GUJARATALKALI_20260406_100456.html

✅ Double-click the file → Opens in browser
```

### Step 2: See the Main Dashboard
```
You will see:
┌─────────────────────────────────────────────────────────────┐
│  📊 Real-Time Trading Dashboard                              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Stock: GUJARATALKALI    Price: ₹605.50                      │
│  Change: +0.75 (+0.12%) High/Low: ₹612/₹596                 │
│                                                               │
│  🟢 BUY SIGNAL (Confidence: 8/10) ← THIS IS YOUR SIGNAL      │
│  Signal Strength: 8/10                                       │
│                                                               │
│  Last Updated: 2026-04-06 10:04:56                           │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│  🕯️ CANDLESTICK CHART (Last 100 bars)                       │
│                                                               │
│        Price (₹)  Chart Area with Lines & Candles            │
│           650 │     ╱╲____                                   │
│           640 │    ╱      ╲___                                │
│           630 │   ╱           ╲                               │
│           620 │  ╱              ╲___                          │
│           610 │ ╱                   ╲____                     │
│           600 │╱                        ╲___                  │
│           590 │                             ╲                │
│           580 └────────────────────────────────────────      │
│               └─ Time (Hours) ──────────→                    │
│                                                               │
│  Blue line = Price (closes)                                  │
│  Orange line = SMA20 (short-term trend)                      │
│  Red line = SMA50 (medium-term trend)                        │
│                                                               │
└─────────────────────────────────────────────────────────────┘

Below chart:
📈 RSI        │ 📊 MACD      │ 🎯 Bollinger │ 📍 Moving Avgs
Value: 48.2   │ Value: 0.45  │ Upper: 612.5 │ SMA20: 602.3
Status: Neutral│ Histogram:   │ Middle: 604  │ SMA50: 598.7
             │ +0.07 (Bull) │ Lower: 595.5 │ SMA200: 592.5
```

### Step 3: Read the BUY/SELL Signal
```
🟢 GREEN means BUY
   → Price is likely to go UP
   → Good time to enter a long position
   → Place a BUY order now

🔴 RED means SELL
   → Price is likely to go DOWN
   → Good time to exit or short sell
   → Close existing long positions

🟡 YELLOW means NEUTRAL/WAIT
   → No clear direction
   → Wait for better signal
   → Skip this trade
```

### Step 4: Check Confidence Level (1-10)
```
Confidence: 8/10  →  STRONG SIGNAL
├─ 9-10: Extreme confidence → GO ALL-IN ✅
├─ 7-8:  Strong → Trade normal size ✅
├─ 5-6:  Moderate → Trade half size ⚠️
└─ 1-4:  Weak → SKIP TRADE ❌
```

### Step 5: Execute the Trade
```
IF Signal = 🟢 BUY + Confidence ≥ 7:

Step 1: Open your broker (Zerodha, 5Paisa, etc.)

Step 2: Enter BUY order
Network: Buy
Symbol: GUJARATALKALI
Quantity: 100 shares (adjust based on capital)
Price: ₹605.50 or wait for better entry
Order Type: MARKET (for immediate) or LIMIT

Step 3: Set STOP-LOSS immediately
Order: SELL
Symbol: Same
Quantity: Same (100 shares)
Price: ₹595.50 (from dashboard) or ₹3 below entry
Trigger: If price falls below SL, auto-exit

Step 4: Set TARGETS
Sell 50% at Target 1: ₹612.00
Sell 50% at Target 2: ₹620.00

Step 5: Monitor & Wait
Watch dashboard for updates
Close position when target hit or SL triggered
```

---

## 📊 DETAILED INDICATOR EXPLANATIONS

### 1️⃣ CANDLESTICK CHART (The Main View)

```
What You See:
────────────────────────────────────────────────

Each vertical line = Price movement for that hour

🟢 GREEN CANDLE (Buyers Winning)
┌─────────────────┐
│                 │  ← High price
│                 │
│     ┌─────┐     │  ← Close > Open (Green)
│     │     │     │
│     └─────┘     │  ← Open
│                 │
│                 │  ← Low price
└─────────────────┘

🔴 RED CANDLE (Sellers Winning)
┌─────────────────┐
│                 │  ← High price  
│     ┌─────┐     │  ← Open
│     │     │     │
│     └─────┘     │  ← Close < Open (Red)
│                 │
│                 │  ← Low price
└─────────────────┘

⚪ DOJI CANDLE (Indecision)
┌─────────────────┐
│                 │  ← High
│      │ │        │  ← Nearly same open/close
│      └─┘        │
│                 │  ← Low
└─────────────────┘

🔨 HAMMER CANDLE (Bullish Signal)
┌─────────────────┐
│     ┌─────┐     │  ← Small body at top (buyers won)
│     └──┬──┘     │
│        │        │  ← Long wick down (rejected lower)
│        │        │
└────────┘────────┘  ← Shows rejection of lower prices

⭐ SHOOTING STAR (Bearish Signal)  
┌────────┬────────┐  ← Long wick up (rejected higher)
│        │        │
│     ┌──┴──┐     │  ← Small body at bottom (sellers won)
│     └─────┘     │
└─────────────────┘
```

**What to do:**
```
🟢 Green candles + Uptrend = BUY signal
🔴 Red candles + Downtrend = SELL signal
🔨 Hammer at bottom = Strong BUY
⭐ Shooting star at top = Strong SELL
```

---

### 2️⃣ RSI INDICATOR (Relative Strength Index)

```
What it measures: Is stock OVERBOUGHT or OVERSOLD?

Scale: 0 ────────────────────────────────── 100

Status Zones:
┌──────────────────────────────────────────┐
│ 0    OVERSOLD ZONE (Too low)      30     │  🟢 BUY ZONE
│      └─ Buyers entering, Price likely ↑  │
│                                           │
│ 30   NEUTRAL ZONE (Normal)         70    │  🟡 HOLD ZONE
│      └─ No extreme condition, wait       │
│                                           │
│ 70    OVERBOUGHT ZONE (Too high)   100   │  🔴 SELL ZONE
│       └─ Sellers entering, Price ↓      │
└──────────────────────────────────────────┘

Current Example:
GUJARATALKALI RSI = 48.2

            0            48.2          100
            │───────────█──────────────│
           OVERSOLD    NEUTRAL      OVERBOUGHT
                     ← You are here (Normal)
                        Action: WAIT or ENTER
```

**How to use:**
```
RSI < 30:   Stock is CHEAP → Good time to BUY 🟢
RSI 30-70:  Normal range → Follow trend ➖
RSI > 70:   Stock is EXPENSIVE → Good time to SELL 🔴
```

---

### 3️⃣ MACD INDICATOR (Moving Average Convergence Divergence)

```
What it measures: Momentum (is trend getting stronger/weaker?)

Three components:
1. MACD Line (blue)    = Fast line
2. Signal Line (red)   = Slow line  
3. Histogram (green/red bars) = Difference between them

Visual:
             MACD Line (0.45)
                 ↑
    Signal Line (0.38)
         ↑
    Histogram (+0.07) = Positive = Bullish momentum

Show in Chart:
┌────────────────────────────────────┐
│ MACD Line ─────┐                   │
│               └─── (0.45)          │
│                 │                  │
│ Signal Line ────┘ (0.38)           │
│                 │                  │
│ Histogram ██ (bars below)          │
│       Positive = BULLISH 📈        │
│       Negative = BEARISH 📉        │
└────────────────────────────────────┘

Current Example:
├─ MACD: 0.45
├─ Signal: 0.38
├─ MACD > Signal? YES ✅
└─ Histogram: +0.07 (Positive)
   → BULLISH MOMENTUM!
```

**How to use:**
```
MACD > Signal Line:  🟢 BUY SIGNAL (bullish)
MACD < Signal Line:  🔴 SELL SIGNAL (bearish)
MACD crosses above:  🟢 STRONG BUY (momentum shift)
MACD crosses below:  🔴 STRONG SELL (momentum shift)
```

---

### 4️⃣ BOLLINGER BANDS (Price Range Indicator)

```
What it measures: Normal price range. When price breaks it = reversal likely.

Structure:
                Upper Band (612.50)
                      ┌─────────┐
                      │ Price   │  }
                      │ bounces │  } Normal
    Middle (SMA20)    │  here   │  } zone
    (604.00) ═════════║═════════║════════
                      │ Price   │  }
                      │ bounces │  } Normal
                      │  here   │  } zone
                      └─────────┘
                Lower Band (595.50)

Current Position: Price ₹605.50
                   │
╔═══════════════════════════════════╗
║ Upper: 612.50                     ║
║ Middle: 604.00 ← Price above here ║
║ Lower: 595.50                     ║
╚═══════════════════════════════════╝

Meaning: NORMAL position (between bands)
Action: Can BUY or SELL (no extreme)
```

**How to use:**
```
Price > Upper Band:   OVERBOUGHT 🔴 
                      → Expect reversal DOWN
                      → Good time to SELL

Price between Bands:  NORMAL 🟡
                      → Follow other signals
                      → No extreme condition

Price < Lower Band:   OVERSOLD 🟢
                      → Expect reversal UP
                      → Good time to BUY
```

---

### 5️⃣ MOVING AVERAGES (Trendet Direction)

```
What it measures: Average price over X days. Shows trend direction.

Three lines:
┌─────────────────────────────────────────┐
│                                          │
│     SMA200 (Long-term trend)            │
│        ↑                                 │
│        SMA50 (Medium-term trend)        │
│           ↑                              │
│           SMA20 (Short-term trend)      │
│              ↑                           │
│              Current Price              │
│                                          │
└─────────────────────────────────────────┘

Current Values:
├─ SMA20:  602.30 ← Short-term support
├─ SMA50:  598.75 ← Medium-term support
└─ SMA200: 592.50 ← Long-term support

Alignment Check:
Price (605.50) > SMA20 (602.30) ✅ Bullish
SMA20 (602.30) > SMA50 (598.75) ✅ Bullish
SMA50 (598.75) > SMA200 (592.50) ✅ Bullish

Result: STRONG UPTREND 📈
Action: Look for BUY opportunities
```

**How to use:**
```
Price > SMA20 > SMA50 > SMA200:    🟢 STRONG BUY (uptrend)
Price < SMA20 < SMA50 < SMA200:    🔴 STRONG SELL (downtrend)
Price between SMA20 & SMA50:       🟡 NEUTRAL (consolidation)
```

---

## 🎯 TRADING WORKFLOW (Real Example)

### Scenario: Dashboard shows 🟢 BUY Signal

```
STEP 1: VERIFY THE SIGNAL
═══════════════════════════════════════════

Dashboard shows:
├─ Signal: 🟢 BUY
├─ Confidence: 8/10 ✅ (Good, proceed)
├─ Stock: GUJARATALKALI
├─ Price: ₹605.50
└─ Check indicators:
   ├─ RSI: 48.2 (Neutral) ✅
   ├─ MACD: Bullish (+0.07 positive) ✅
   ├─ BB: Price in middle (normal) ✅
   ├─ MA: Price > SMA20 > SMA50 ✅
   └─ Result: ALL ALIGNED = STRONG SIGNAL ✓

DECISION: ✅ PROCEED WITH TRADE


STEP 2: CALCULATE POSITION SIZE
═══════════════════════════════════════════

Account Size: ₹100,000
Risk per Trade: 1% (standard) = ₹1,000

Entry Price: ₹605.50
Stop-Loss: ₹595.50 (from dashboard)
Risk per share: ₹605.50 - ₹595.50 = ₹10.00

Position Size = Risk Amount ÷ Risk per share
              = ₹1,000 ÷ ₹10.00
              = 100 shares

Capital Needed: 100 × ₹605.50 = ₹60,550 ✅ (You have ₹100K, OK)


STEP 3: SET UP ORDERS IN BROKER
═══════════════════════════════════════════

Order 1: BUY ENTRY
┌────────────────────────────────────────┐
│ Action: BUY                            │
│ Symbol: GUJARATALKALI                  │
│ Quantity: 100 shares                   │
│ Order Type: MARKET (buy now) or LIMIT  │
│ Price: ₹605.50 (market) or ₹604.50 (limit wait)
│ Submit Order ✅                        │
└────────────────────────────────────────┘

Order 2: STOP-LOSS (Protective exit)
┌────────────────────────────────────────┐
│ Action: SELL                           │
│ Symbol: GUJARATALKALI                  │
│ Quantity: 100 shares (SAME)            │
│ Trigger Type: STOP LOSS                │
│ Trigger Price: ₹595.50 (from dashboard)│
│ Order Type: MARKET (when triggered)    │
│ Status: ACTIVE immediately after buy   │
│ Submit Order ✅                        │
│ (Now you're PROTECTED - max loss ₹1,000)
└────────────────────────────────────────┘

Order 3: TARGET 1 (Partial profit)
┌────────────────────────────────────────┐
│ Action: SELL (50% of position)         │
│ Symbol: GUJARATALKALI                  │
│ Quantity: 50 shares (50% of 100)       │
│ Order Type: LIMIT                      │
│ Price: ₹612.00 (from dashboard)        │
│ Status: ACTIVE until filled            │
│ Submit Order ✅                        │
│ Expected Profit: 50 × ₹6.50 = ₹325    │
└────────────────────────────────────────┘

Order 4: TARGET 2 (Remaining profit)
┌────────────────────────────────────────┐
│ Action: SELL (remaining 50%)           │
│ Symbol: GUJARATALKALI                  │
│ Quantity: 50 shares (remaining)        │
│ Order Type: LIMIT                      │
│ Price: ₹620.00 (from dashboard)        │
│ Status: ACTIVE until filled            │
│ Submit Order ✅                        │
│ Expected Profit: 50 × ₹14.50 = ₹725   │
└────────────────────────────────────────┘


STEP 4: MONITOR THE TRADE
═══════════════════════════════════════════

Time: 10:05 AM
├─ Order 1: ✅ FILLED at ₹605.50
│  └─ You own 100 shares, cost ₹60,550
│
├─ Order 2: ✅ ACTIVE (SL at ₹595.50)
│  └─ Protected, max loss ₹1,000
│
├─ Dashboard: Still shows 🟢 BUY
│  └─ RSI: 48.2 → 45.1 (slightly dropped)
│  └─ MACD: Still positive
│  └─ Price: ₹605.50 → ₹607.50 (+₹2.00) ⬆️
│
└─ Action: WAIT for targets

Time: 10:12 AM
├─ Price: ₹612.00 ← TARGET 1 HIT!
├─ Order 3: ✅ FILLED at ₹612.00
│  └─ You sold 50 shares
│  └─ Profit locked: 50 × ₹6.50 = ₹325
│
├─ Remaining: 50 shares still held
│  └─ Stop-loss moved to ₹604.00 (breakeven strategy)
│
└─ Action: WAIT for Target 2 or SL

Time: 10:23 AM
├─ Price: ₹620.00 ← TARGET 2 HIT!
├─ Order 4: ✅ FILLED at ₹620.00
│  └─ You sold remaining 50 shares
│  └─ Profit locked: 50 × ₹14.50 = ₹725
│
└─ TRADE COMPLETE ✅


STEP 5: REVIEW & RECORD
═══════════════════════════════════════════

Total Profit Calculation:
Entry price:        ₹605.50 (cost ₹60,550 for 100 shares)
Target 1 Exit:      ₹612.00 (50 shares) = ₹325 profit
Target 2 Exit:      ₹620.00 (50 shares) = ₹725 profit
────────────────────────────────────────────────
Total Profit:       ₹1,050 ✅
Account Return:     1.05% (₹1,050 / ₹100,000)

Trade Journal Entry:
Date: 2026-04-06
Time: 10:05 AM
Stock: GUJARATALKALI
Action: BUY 100 at ₹605.50
Exit: Sold 50 at ₹612.00 (T1) + 50 at ₹620.00 (T2)
Risk: ₹10.00, Reward: ₹6.50 + ₹14.50
Loss at SL: ₹1,000 (never hit)
Actual Profit: ₹1,050 ✅
Duration: 18 minutes ⚡
Win? YES! ✅
Lessons: Dashboard signals working perfectly! Confidence remains strong.
Next: Take 5-10 more trades, track results, refine strategy.
```

---

## 🔄 DAILY WORKFLOW

### Morning (Before Market Opens)
```
1. Generate fresh dashboard
   └─ python scripts/realtime_trading_dashboard.py GUJARATALKALI

2. Open HTML file in browser
   └─ Check overnight trends

3. Prepare trading plan
   └─ Which stocks to watch
   └─ Entry prices ready
   └─ Stop-losses calculated
```

### During Trading Hours
```
1. Monitor dashboard (auto-updates every 60 seconds)
   └─ Watch for 🟢 or 🔴 signals

2. When signal appears with Confidence ≥ 7:
   └─ Verify all indicators aligned
   └─ Calculate position size
   └─ Place orders (entry + SL + targets)

3. Manage trade:
   └─ Monitor price movement
   └─ Take profits at targets
   └─ Cut losses at stop-loss
   └─ Record in trade journal

4. Wait for next signal
   └─ Don't overtrade
   └─ Quality > Quantity
   └─ 1-3 good trades per day = great success
```

### End of Day
```
1. Close all positions
   └─ Don't hold overnight on intraday setups

2. Refresh dashboard for next day
   └─ Generate new HTML with today's data

3. Review trades:
   └─ Wins: What worked? Do more of it!
   └─ Losses: What went wrong? Learn & avoid!

4. Update trading journal
   └─ Calculate profit/loss
   └─ Note patterns observed
   └─ Plan for tomorrow
```

---

## ⚠️ CRITICAL DO's & DON'Ts

### ✅ DO THESE:

```
1. ✅ Set STOP-LOSS before entering trade
   └─ Without it, 1 bad trade wipes out 10 good ones

2. ✅ Use LIMIT ORDERS for entry
   └─ Don't buy at market price (too expensive)
   └─ Place limit at ₹2-3 below signal price

3. ✅ Risk only 1% per trade maximum
   └─ Position size = Risk Amount ÷ Risk per share

4. ✅ Take profits at TARGETS
   └─ Don't get greedy waiting for more
   └─ 50% profit at T1, rest at T2 = perfect

5. ✅ Wait for Confidence ≥ 7
   └─ Don't trade weak signals (< 5)
   └─ Quality signals = better win rate

6. ✅ Keep TRADING JOURNAL
   └─ Every trade recorded
   └─ Learn from wins and losses
   └─ Track your stats

7. ✅ Use MULTIPLE INDICATORS
   └─ Don't trade on RSI alone
   └─ Confirm with MACD + BB + MA alignment
```

### ❌ DON'T DO THESE:

```
1. ❌ Trade WITHOUT stop-loss
   └─ Biggest mistake traders make
   └─ Can lose entire account fast

2. ❌ Chase MOVING PRICES
   └─ Order at ₹605.50, price now ₹608
   └─ Wait for pullback, don't chase
   └─ Use limit orders, not market

3. ❌ Trade WEAK SIGNALS
   └─ Confidence 4/10? SKIP IT
   └─ Only trade 7+ confidence
   └─ Quality over quantity

4. ❌ Move stop-loss LOWER
   └─ Turns winners into losers
   └─ Breaks your plan
   └─ Fixed SL = fixed risk

5. ❌ Over-leverage
   └─ Just because you CAN buy 500 shares
   └─ Doesn't mean you SHOULD
   └─ Use 1% risk rule always

6. ❌ Hold trades OVERNIGHT
   └─ Gaps happen while market closed
   └─ Can lose 5-10% overnight
   └─ Intraday = close by end of day

7. ❌ Ignore the TREND
   └─ Don't sell in uptrend
   └─ Don't buy in downtrend
   └─ Trade WITH the trend

8. ❌ Get EMOTIONAL
   └─ Loss? Don't revenge trade
   └─ Win? Don't get overconfident
   └─ Follow your PLAN always
```

---

## 🚀 START YOUR FIRST TRADE RIGHT NOW

### Checklist:
```
☐ 1. Dashboard open in browser
☐ 2. Read the signal (🟢 🔴 or 🟡)
☐ 3. Check confidence (target ≥ 7)
☐ 4. Verify all indicators aligned
☐ 5. Calculate position size (1% risk)
☐ 6. Broker app open & logged in
☐ 7. Set entry, stop-loss, targets
☐ 8. Place orders in sequence
☐ 9. Monitor price movement
☐ 10. Journal your results

Once all checked ✅ → YOU'RE READY TO TRADE!
```

---

## 💬 COMMON QUESTIONS

**Q: Signal shows BUY but I'm scared?**  
A: Paper trade first! Use fake money to practice. Once you win 10-20 trades reliably, go real.

**Q: How many trades per day?**  
A: Quality > Quantity. 1-2 good trades with +1% each = +2% day. Better than 10 bad trades = -5% day.

**Q: Dashboard showing conflicting signals?**  
A: Wait! When RSI says buy but MACD says sell = NEUTRAL. Skip trade, wait for alignment.

**Q: Should I hold overnight?**  
A: NO! Gaps happen. Close all by 3:30 PM. New positions next day based on new dashboard.

**Q: Price hit SL but I think it will bounce?**  
A: EXIT IMMEDIATELY! Your plan said SL ₹595.50. Price hit ₹595.50 = you exit. No "I think" allowed.

**Q: I have ₹50,000, can I trade?**  
A: YES! Start smaller: 50 shares instead of 100. Risk ₹500 per trade (1% of ₹50K). Scale up as profits grow.

---

## 📈 SUCCESS FORMULA

```
Winning Trader = 
    Good Signals (Red, Yellow, Green - ours does this ✅)
    +
    Risk Management (1% rule, position sizing - you control this ✅)
    +
    Discipline (Follow plan, cut losses - requires YOU ✅)
    +
    Patience (Wait for quality entries - needs YOU ✅)
    
Your Success = 50% Dashboard Signal + 50% Your Discipline
```

---

## 🎓 NEXT STEPS

### Day 1-5:
```
1. Paper trade 5-10 setups using dashboard
2. Track every trade (win/loss/duration)
3. Get comfortable with the signals
4. Learn the indicators
```

### Week 2-4:
```
1. Paper trade 20-50 more setups
2. Achieve 60%+ win rate on paper
3. Understand your best timeframe
4. Refine position sizing
```

### Month 2+:
```
1. Start real trading with small size (₹500 risk per trade)
2. Track live results in journal
3. Once 10+ real trades profitable = increase size to ₹1,000
4. Scale gradually as confidence grows
```

---

**You're all set! Open the dashboard and start your first trade RIGHT NOW! 🚀**

**Remember: Dashboard gives signals, YOU control the rest. Make it count!** 💪
