# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Rasa banking agent template** for "Trout Bank" 🎣—the world's first fishing-focused bank! A conversational AI assistant that handles account management, card services, money transfers, contact management, and bill payments with a fun, relaxed attitude. It uses Rasa's flows-based approach with Python custom actions and a mock JSON database.

## Architecture

The agent consists of four interconnected layers:

### 1. **Flows** (`data/` directory)
YAML files that define conversation patterns and agent behaviors. Flows are step-by-step recipes for handling user intents.
- Each feature (accounts, cards, transfers, etc.) has a dedicated folder with flows
- Flows execute a sequence of actions and utterances in response to user intent
- Example: `data/transfers/transfer_money.yml` defines the logic for processing money transfers

### 2. **Domain** (`domain/` directory)
YAML files that define the agent's state, communication capabilities, and available actions.
- **Slots**: Agent memory (e.g., `bank_name`, `recipient_account`, `transfer_amount`)
- **Responses**: Bot messages keyed as `utter_*` that can use slot interpolation (e.g., `{bank_name}`)
- **Actions**: References to custom Python actions the agent can execute
- Organized by feature with a `general/` folder for common patterns

### 3. **Custom Actions** (`actions/` directory)
Python classes extending `rasa_sdk.Action` that implement business logic.
- Each action has a `name()` method (matches flow action references) and a `run()` method
- Actions interact with the database, validate data, and set slots
- Core utilities: `actions/db.py` handles session-based database operations for contacts, cards, transactions, and account info
- Organized by feature (accounts, cards, transfers, contacts)

### 4. **Configuration**
- **`config.yml`**: LLM pipeline setup, policy definitions, and vector store configuration for knowledge retrieval
- **`credentials.yml`**: Channel and service credentials (REST, Slack, Facebook, etc.); includes ASR/TTS settings
- **`endpoints.yml`**: Action endpoint, NLG setup, tracker store, and model group definitions
- **`prompts/`**: Jinja2 templates for response rephrasing and customization

## Key Concepts

### Session-Based Database
All database operations are session-scoped. Each conversation session gets its own copy of the database files in a temp directory (`/tmp/rasa-calm-demo/{session_id}/`). This allows safe, isolated testing.

### Testing with E2E Test Cases
Tests live in `tests/e2e_test_cases/`. Format is YAML with test steps, user inputs, and assertions:
- `flow_started`: Check that a specific flow was triggered
- `action_executed`: Verify an action ran
- `slot_was_set`: Assert slot values
- `bot_uttered`: Check bot responses

Example: `test_payee_validation.yml` tests transfer flows with valid and invalid payees.

### LLM Integration
The agent uses OpenAI models configured in `endpoints.yml`:
- `openai-gpt-5-1` for main command generation (SearchReadyLLMCommandGenerator)
- `openai-gpt-5-mini` for knowledge retrieval and relevancy checking
- `openai-embeddings` for document embedding in the vector store

## Common Development Tasks

### Adding a New Banking Feature
1. Create YAML flows in `data/feature_name/` defining the conversation steps
2. Create domain elements in `domain/feature_name/` (slots, responses, actions)
3. Implement custom actions in `actions/feature_name/` as Python classes
4. If needed, add E2E tests in `tests/e2e_test_cases/`

### Creating a Custom Action
```python
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionMyFeature(Action):
    def name(self) -> str:
        return "my_feature"
    
    def run(self, dispatcher, tracker, domain):
        # Access slots: tracker.get_slot("slot_name")
        # Read database: from actions.db import get_contacts
        return [SlotSet("return_value", value)]
```

### Updating Bot Responses
Edit `domain/{feature}/` YAML files. Use `{slot_name}` for interpolation.
- The `bank_name` slot is "Trout" by default—change it in `domain/general/welcome.yml` to rebrand
- Responses with `metadata: {rephrase: True}` are enhanced by the NLG rephraser (LLM-based)

### Running Tests
```bash
rasa test --e2e tests/e2e_test_cases/
```
(Replace the path with a specific test file to run a single test)

### Training the Agent
```bash
rasa train
```
Trains the NLU and dialogue models based on flows and domain.

### Starting the Agent
```bash
rasa run --enable-api
```
Starts the agent on `http://localhost:5005`. The REST API allows chat via `POST /webhooks/rest/webhook`.

### Running Custom Actions Server
```bash
rasa run actions
```
Starts the action server on `http://localhost:5055`. Ensure this is running before testing flows that use custom actions.

## Rasa Agent Skills

This project can benefit from [rasa-agent-skills](https://github.com/RasaHQ/rasa-agent-skills), a collection of packaged instructions for AI agents building Rasa CALM systems. When working on this codebase, you can leverage skills covering:

- **Flow development**: Building and connecting flows for new features
- **Configuration**: Setting up `config.yml`, `endpoints.yml`, model groups
- **Domain authoring**: Defining slots, responses, and custom actions
- **Integrations**: Enterprise search, MCP tools, voice channels (ASR/TTS)
- **Testing**: Writing and running E2E tests, conversation simulation
- **Advanced patterns**: ReAct agents, A2A agents, external integrations

These skills activate automatically and provide detailed guidance when you describe development tasks naturally (e.g., "Add a flow for scheduling bills" or "Set up a custom ASR provider").

## Important Files & Patterns

- **`actions/db.py`**: Core database API (read/write JSON files, session management). Import from here for database access.
- **`domain/general/welcome.yml`**: Main greeting flow and skill summary; good place to see how slots and responses work together.
- **`credentials.yml`**: Voice/chat channel setup (REST is enabled by default; Slack/Facebook commented out).
- **Slots in domain**: Are the primary way to pass data between flows and actions. Always define them in domain YAML before using.

## Notes for Future Development

- **Database**: The mock database in `db/` is reset per session. For persistence, update `actions/db.py` to use a real database.
- **Knowledge Base**: Documents in `docs/trout_banking_faq/` are retrieved via vector store when the EnterpriseSearchPolicy is triggered.
- **Rebranding**: The `bank_name` slot defaults to "Trout". Change it once in `domain/general/welcome.yml` and it propagates everywhere via response interpolation.
