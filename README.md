# Copilot Agents Repository

A curated collection of custom VS Code Copilot agents for specialized development tasks.

## Agents Included

### 🚀 Flutter APK Release Agent
**File**: `.github/agents/flutter-apk-release.agent.md`

Specialized agent for building, signing, and releasing Flutter Android APK files to Google Play Store.

**Use when**:
- Building release APKs for Play Store
- Managing signing certificates and keystores
- Troubleshooting APK build failures
- Configuring version codes and build variants
- Preparing app updates and patch releases

**Example prompts**:
```
@flutter-apk-release Create a keystore file and sign my Flutter app for the first Play Store release

@flutter-apk-release Build a production APK and verify it meets Play Store requirements

@flutter-apk-release Update the app version code and build a new release bundle (AAB)
```

---

### 📊 BSE Stock Analysis Agent
**File**: `.github/agents/bse-stock-analysis.agent.md`

Specialized agent for analyzing TOP 50 BSE stocks using quantitative financial metrics and AI predictions.

**Capabilities**:
- Analyzes 40+ years of historical stock data
- Calculates Sharpe Ratio (risk-adjusted returns)
- Calculates Sortino Ratio (downside risk measurement)
- Generates interactive HTML dashboards
- Creates candlestick charts with Plotly.js
- Provides real-time price updates
- Exportable to PDF and CSV formats
- Dark mode toggle for comfortable viewing

**Use when**:
- Analyzing TOP 50 BSE stocks systematically
- Calculating risk-adjusted return metrics
- Building quantitative analysis reports
- Comparing multiple stocks side-by-side
- Understanding volatility and downside risk
- Generating investment analysis dashboards

**Example prompts**:
```
@bse-stock-analysis Analyze TOP 50 BSE stocks and show which ones have the best Sharpe and Sortino ratios

@bse-stock-analysis Generate an interactive HTML report with candlestick charts for top 10 BSE performers

@bse-stock-analysis Calculate Sortino ratio vs Sharpe ratio for NIFTY50 stocks and identify low-volatility winners

@bse-stock-analysis Show me the risk-adjusted returns of BSE banks sector using 10-year historical data
```

**Key Metrics**:
- **Sharpe Ratio**: Risk-adjusted return (benchmark: > 1.0)
- **Sortino Ratio**: Downside risk measurement (benchmark: > 1.0)
- **Annual Return**: Percentage gain/loss per year
- **Volatility**: Standard deviation of returns
- **Max Drawdown**: Largest peak-to-trough decline
- **Win Rate**: Percentage of profitable days

**Output Files Generated**:
- `bse_analysis_report.html` — Interactive dashboard
- `bse_stocks_data.csv` — Detailed metrics
- `bse_analysis.pdf` — Printable report
- Candlestick charts for individual stocks

**Setup**:
1. Get dhanHQ API key from https://www.dhan.co
2. Update `DHAN_API_KEY` in configuration
3. Run analysis: `python scripts/bse_stock_analyzer.py`
4. Open HTML report in browser for interactive charts

---

## How to Use These Agents

### In VS Code Settings

1. Clone or fork this repository
2. Copy the `.github/agents/` folder to your VS Code settings:
   ```
   ~/.vscode/extensions/github.copilot-chat-0.42.2/assets/prompts/agents/
   ```
   Or for user-level (cross-workspace):
   ```
   ~/AppData/Roaming/Code/User/prompts/
   ```

3. Reload VS Code or restart Copilot Chat
4. Open Chat and select the agent from the agent picker dropdown

### Via VS Code Settings Sync
If you have Settings Sync enabled:
1. Copy agents to your user profile folder
2. Enable sync in VS Code
3. Agents automatically sync to all devices

---

## Agent Structure

Each agent is a markdown file (`.agent.md`) with YAML frontmatter:

```yaml
---
description: "Use when... trigger words"
name: "Agent Name"
tools: [list, of, tools]
user-invocable: true
---
```

**Fields**:
- `description`: How Copilot discovers when to use this agent
- `name`: Display name in agent picker
- `tools`: Which tools the agent can use
- `user-invocable`: Show in agent picker (true/false)

---

## Creating Your Own Agents

Follow the template structure:

```markdown
---
description: "Use when [specific task] for [domain]"
name: "Agent Name"
tools: [read, edit, search, execute]
---

# Agent Name

[Role and purpose]

## Constraints
- DO NOT [restriction]
- ALWAYS [requirement]

## Approach
1. [Step one]
2. [Step two]
3. [Step three]
```

**Tips**:
- ✓ Use specific trigger words in description ("Use when...")
- ✓ Limit to one primary role per agent
- ✓ Include only necessary tools
- ✓ Define clear constraints and boundaries
- ✓ Provide example prompts in README

---

## Contributing

Want to add more agents? Create a PR with:
1. New `.agent.md` file in `.github/agents/`
2. Updated README.md with description and examples
3. Clear naming convention: `domain-function.agent.md`

---

## Resources

- [VS Code Copilot Customization Docs](https://code.visualstudio.com/docs/copilot/customization)
- [Agent Customization Skill Guide](https://github.com/your-username/copilot-agents/wiki/Agent-Customization)
- [GitHub Copilot Chat Documentation](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-chat-in-your-ide)

---

## License

These agents are provided as-is for educational and development purposes.

---

**Created**: April 2, 2026  
**Maintained by**: [@ravi-chudgar](https://github.com/ravi-chudgar)

