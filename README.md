# Chatbot2

A lightweight, rule-based chatbot with both a CLI and minimal HTTP interface. The bot remembers small pieces of context (like a user's name) during a session and responds to a handful of intents defined in `chatbot/intents.json`.

## Getting started

1. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies (there are none outside the standard library, so this is optional):

   ```bash
   pip install -r requirements.txt
   ```

### Talk to the bot in the terminal

Run the CLI and start chatting:

```bash
python -m chatbot.cli
```

Type `exit` to leave the session.

### Run the HTTP API

Start the built-in HTTP server:

```bash
python -m chatbot.server
```

Send a message with `curl` (the server will create a session ID on the first call and reuse it when you send it back):

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "my name is Casey"}'
```

The response includes `reply` and `session_id`. Reuse `session_id` in the next request to keep conversation memory:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "do you know my name?", "session_id": "<the-session-id>"}'
```

The server also exposes a simple health check at `http://localhost:8000/healthz`.

## Testing

Run the test suite with the standard library test runner:

```bash
python -m unittest discover -s tests -p "test*.py"
```
