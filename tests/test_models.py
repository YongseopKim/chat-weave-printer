"""Tests for models.py"""

from datetime import datetime

from chatweave_printer.models import (
    ArtifactIR,
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
    assert get_platform_display_name("grok") == "Grok"


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
    assert conv.artifacts == []  # default empty when key absent


def test_artifact_ir_model():
    """Test ArtifactIR Pydantic model."""
    artifact = ArtifactIR(
        id="a0000",
        title="My Component",
        version="v1",
        content="export default function() {}",
    )
    assert artifact.id == "a0000"
    assert artifact.title == "My Component"
    assert artifact.version == "v1"
    assert artifact.content == "export default function() {}"
    assert artifact.meta == {}


def test_artifact_ir_defaults():
    """Test ArtifactIR default values."""
    artifact = ArtifactIR(id="a0000", title="Test")
    assert artifact.version is None
    assert artifact.content == ""
    assert artifact.meta == {}


def test_conversation_ir_with_artifacts():
    """Test ConversationIR parsing with artifacts field."""
    data = {
        "schema": "conversation-ir/v1",
        "platform": "claude",
        "conversation_id": "test-456",
        "meta": {"url": "https://claude.ai/chat/test-456"},
        "messages": [],
        "artifacts": [
            {
                "id": "a0000",
                "title": "My Framework",
                "version": "v3",
                "content": "# Framework\n\nCode here",
                "meta": {"language": "typescript"},
            }
        ],
    }

    conv = ConversationIR.model_validate(data)
    assert len(conv.artifacts) == 1
    assert conv.artifacts[0].title == "My Framework"
    assert conv.artifacts[0].version == "v3"
    assert conv.artifacts[0].meta["language"] == "typescript"


def test_conversation_ir_without_artifacts_backward_compat():
    """Test that existing JSON without artifacts key still parses."""
    data = {
        "schema": "conversation-ir/v1",
        "platform": "chatgpt",
        "conversation_id": "old-123",
        "meta": {},
        "messages": [],
    }

    conv = ConversationIR.model_validate(data)
    assert conv.artifacts == []
