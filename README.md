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

