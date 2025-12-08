"""Tests for markdown formatter."""

from datetime import datetime

from chatweave_printer.models import ConversationIR, MessageIR
from chatweave_printer.formatters.markdown import (
    adjust_heading_level,
    format_message_content,
    format_conversation_to_markdown,
)


def test_adjust_heading_level():
    """Test heading level adjustment."""
    # Basic increment
    assert adjust_heading_level("## Heading", 1) == "### Heading"
    assert adjust_heading_level("# H1", 1) == "## H1"

    # Multiple headings
    content = "## First\n\nSome text\n\n### Second"
    expected = "### First\n\nSome text\n\n#### Second"
    assert adjust_heading_level(content, 1) == expected

    # Max level (6)
    assert adjust_heading_level("###### Max", 1) == "###### Max"
    assert adjust_heading_level("##### Five", 1) == "###### Five"


def test_format_message_content_empty_user():
    """Test empty user message formatting."""
    msg = MessageIR(
        id="m0000",
        index=0,
        role="user",
        timestamp=datetime.now(),
        raw_content="",
        normalized_content=None,
    )
    assert format_message_content(msg) == "(빈 질문)"


def test_format_message_content_empty_assistant():
    """Test empty assistant message formatting."""
    msg = MessageIR(
        id="m0001",
        index=1,
        role="assistant",
        timestamp=datetime.now(),
        raw_content="",
        normalized_content=None,
    )
    assert format_message_content(msg) == "(빈 응답)"


def test_format_message_content_assistant_heading():
    """Test assistant message with heading adjustment."""
    msg = MessageIR(
        id="m0001",
        index=1,
        role="assistant",
        timestamp=datetime.now(),
        raw_content="## Analysis\n\nSome content",
        normalized_content="## Analysis\n\nSome content",
    )
    result = format_message_content(msg)
    assert "### Analysis" in result
    assert "Some content" in result


def test_format_conversation_basic():
    """Test basic conversation formatting."""
    conv = ConversationIR(
        schema="conversation-ir/v1",
        platform="claude",
        conversation_id="test-123",
        meta={"url": "https://claude.ai/chat/test-123"},
        messages=[
            MessageIR(
                id="m0000",
                index=0,
                role="user",
                timestamp=datetime.now(),
                raw_content="Hello",
                normalized_content="Hello",
            ),
            MessageIR(
                id="m0001",
                index=1,
                role="assistant",
                timestamp=datetime.now(),
                raw_content="Hi there!",
                normalized_content="Hi there!",
            ),
        ],
    )

    result = format_conversation_to_markdown(conv)

    # Check structure
    assert "# [Claude](https://claude.ai/chat/test-123)" in result
    assert "## USER 질문" not in result  # User input should be excluded
    assert "Hello" not in result  # User content should be excluded
    assert "Hi there!" in result  # Assistant content should be present
    assert "---" in result
