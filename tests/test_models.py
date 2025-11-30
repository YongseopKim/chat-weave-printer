"""Tests for models.py"""

from datetime import datetime

from chatweave_printer.models import (
    ConversationIR,
    MessageIR,
    get_platform_display_name,
)


def test_message_get_content_with_normalized():
    """Test MessageIR.get_content() returns normalized_content when available."""
    msg = MessageIR(
        id="m0001",
        index=0,
        role="user",
        timestamp=datetime.now(),
        raw_content="raw text",
        normalized_content="normalized text",
    )
    assert msg.get_content() == "normalized text"


def test_message_get_content_without_normalized():
    """Test MessageIR.get_content() returns raw_content when normalized is None."""
    msg = MessageIR(
        id="m0001",
        index=0,
        role="user",
        timestamp=datetime.now(),
        raw_content="raw text",
        normalized_content=None,
    )
    assert msg.get_content() == "raw text"


def test_platform_display_names():
    """Test platform display name mapping."""
    assert get_platform_display_name("claude") == "Claude"
    assert get_platform_display_name("chatgpt") == "ChatGPT"
    assert get_platform_display_name("gemini") == "Gemini"


def test_conversation_ir_parsing():
    """Test ConversationIR can parse valid JSON."""
    data = {
        "schema": "conversation-ir/v1",
        "platform": "claude",
        "conversation_id": "test-123",
        "meta": {"url": "https://example.com"},
        "messages": [
            {
                "id": "m0000",
                "index": 0,
                "role": "user",
                "timestamp": "2025-11-30T14:25:46.551000+00:00",
                "raw_content": "Hello",
                "normalized_content": "Hello",
                "content_format": "markdown",
                "query_hash": None,
                "meta": {},
            }
        ],
    }

    conv = ConversationIR.model_validate(data)
    assert conv.platform == "claude"
    assert conv.conversation_id == "test-123"
    assert len(conv.messages) == 1
    assert conv.messages[0].get_content() == "Hello"
