# Finance Banking Agent Template

A lightweight banking conversational agent template for the fictional **Fenlo Bank** that handles account management, card services, and money transfers.

## 🚀 What's Included

This template provides a banking assistant with:
- **Account Management**: Balance checking and statement downloads
- **Card Services**: Card activation, blocking, replacement, and listing  
- **Money Transfers**: Account-to-account transfers and third-party payments
- **Contact Management**: Add, list, and remove trusted contacts
- **Bill Management**: Bill payment reminders and scheduling
- **Banking Knowledge**: FAQ system with Fenlo Bank documentation

## 📁 Directory Structure

```
├── .claude/skills/  # Agent skills for building/maintaining this assistant (rasa-agent-skills)
├── actions/         # Custom Python logic for banking operations
├── data/            # Banking conversation flows and training data
├── domain/          # Banking agent configuration
├── db/              # Mock JSON database for testing
├── docs/            # Fenlo Bank knowledge base and FAQ documents
├── prompts/         # LLM prompts for enhanced banking responses
└── config.yml       # Training pipeline configuration
```

## 🧠 Agent Skills

`.claude/skills/` bundles the official [RasaHQ/rasa-agent-skills](https://github.com/RasaHQ/rasa-agent-skills) (Apache-2.0) — packaged instructions that guide AI coding agents through building flows, custom actions, e2e tests, MCP integrations, and more for this Rasa CALM project. They're picked up automatically; no separate install step needed.

