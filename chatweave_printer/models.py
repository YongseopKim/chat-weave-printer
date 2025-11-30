"""Pydantic models for ConversationIR."""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


Role = Literal["user", "assistant"]
Platform = Literal["claude", "chatgpt", "gemini"]


class MessageIR(BaseModel):
    """Message in ConversationIR format."""

    id: str
    index: int
    role: Role
    timestamp: datetime
    raw_content: str
    normalized_content: Optional[str] = None
    content_format: str = "markdown"
    query_hash: Optional[str] = None
    meta: Dict[str, Any] = Field(default_factory=dict)

    def get_content(self) -> str:
        """Get message content (normalized if available, otherwise raw)."""
        if self.normalized_content is not None:
            return self.normalized_content
        return self.raw_content


class ConversationIR(BaseModel):
    """ConversationIR schema."""

    model_config = ConfigDict(populate_by_name=True)

    schema_: str = Field(alias="schema")
    platform: Platform
    conversation_id: str
    meta: Dict[str, Any]
    messages: List[MessageIR]


# Platform name mapping
PLATFORM_NAMES = {
    "claude": "Claude",
    "chatgpt": "ChatGPT",
    "gemini": "Gemini"
}


def get_platform_display_name(platform: Platform) -> str:
    """Get display name for platform."""
    return PLATFORM_NAMES.get(platform, platform.capitalize())
