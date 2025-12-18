from __future__ import annotations

import json
import random
import re
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional


@dataclass
class Intent:
    name: str
    patterns: List[str]
    responses: List[str]
    slots: List[str] = field(default_factory=list)


class ChatSession:
    """A lightweight rule-based chatbot that keeps short-term memory."""

    def __init__(self, intents: Iterable[Intent]):
        self.intents: List[Intent] = list(intents)
        self.memory: Dict[str, str] = {}
        self.conversation: List[Dict[str, str]] = []
        self.session_id = str(uuid.uuid4())

    def respond(self, message: str) -> str:
        cleaned = message.strip()
        if not cleaned:
            return "Say something so I can help!"

        intent, match = self._find_intent(cleaned)
        response = self._build_response(intent, match)
        self.conversation.append({"user": cleaned, "bot": response, "intent": intent.name})
        self.memory["last_intent"] = intent.name
        return response

    def _find_intent(self, message: str):
        for intent in self.intents:
            for pattern in intent.patterns:
                match = re.search(pattern, message, flags=re.IGNORECASE)
                if match:
                    return intent, match
        fallback_intent = Intent(
            name="fallback",
            patterns=[],
            responses=[
                "I'm not sure I follow. Could you rephrase that?",
                "I didn't catch that. What do you need help with?",
                "I'm still learning. Could you ask that a different way?",
            ],
        )
        return fallback_intent, None

    def _capture_slots(self, intent: Intent, match: Optional[re.Match]):
        if not match:
            return
        for slot in intent.slots:
            value = match.groupdict().get(slot)
            if value:
                self.memory[slot] = value.strip()

    def _build_response(self, intent: Intent, match: Optional[re.Match]) -> str:
        self._capture_slots(intent, match)
        template = random.choice(intent.responses)
        context = self._response_context()
        try:
            return template.format_map(context)
        except KeyError:
            # If a key is missing, fall back to the raw template without formatting
            return template

    def _response_context(self) -> Dict[str, str]:
        context = dict(self.memory)
        context.setdefault("name", "I don't know yet")
        user_name = context.get("name")
        if user_name:
            context.setdefault("personal_touch", f" How can I help, {user_name}?")
        else:
            context.setdefault("personal_touch", " How can I help today?")
        return context


def load_chatbot(intents_path: Optional[Path] = None) -> ChatSession:
    base = intents_path or Path(__file__).with_name("intents.json")
    data = json.loads(base.read_text())
    intents = [
        Intent(
            name=item["name"],
            patterns=item["patterns"],
            responses=item["responses"],
            slots=item.get("slots", []),
        )
        for item in data["intents"]
    ]
    return ChatSession(intents)
