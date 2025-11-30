"""Markdown formatter for ConversationIR."""

import re
from typing import List

from chatweave_printer.models import ConversationIR, MessageIR, get_platform_display_name


def adjust_heading_level(content: str, increment: int = 1) -> str:
    """
    Adjust markdown heading levels by incrementing them.

    Args:
        content: Markdown content
        increment: Number of levels to increment (default: 1)

    Returns:
        Content with adjusted heading levels

    Examples:
        >>> adjust_heading_level("## Heading", 1)
        "### Heading"
        >>> adjust_heading_level("###### Max", 1)
        "###### Max"
    """
    def replace_heading(match):
        hashes = match.group(1)
        text = match.group(2)
        new_level = min(len(hashes) + increment, 6)  # Max level is 6
        return '#' * new_level + ' ' + text

    return re.sub(r'^(#{1,6})\s+(.+)$', replace_heading, content, flags=re.MULTILINE)


def format_message_content(message: MessageIR) -> str:
    """
    Format a single message content.

    Args:
        message: MessageIR instance

    Returns:
        Formatted message content
    """
    content = message.get_content()

    # Handle empty content
    if not content.strip():
        return "(빈 질문)" if message.role == "user" else "(빈 응답)"

    # Adjust heading levels for assistant messages
    if message.role == "assistant":
        content = adjust_heading_level(content, increment=1)

    return content


def format_conversation_to_markdown(conversation: ConversationIR) -> str:
    """
    Convert ConversationIR to Markdown format.

    Args:
        conversation: ConversationIR instance

    Returns:
        Markdown formatted string
    """
    output_lines: List[str] = []

    # Header with platform name and URL
    platform_name = get_platform_display_name(conversation.platform)
    url = conversation.meta.get("url", "")
    output_lines.append(f"# [{platform_name}]({url})")
    output_lines.append("")

    # Group messages into user-assistant pairs
    i = 0
    while i < len(conversation.messages):
        msg = conversation.messages[i]

        # Add separator
        output_lines.append("---")
        output_lines.append("---")
        output_lines.append("")

        if msg.role == "user":
            # User message
            output_lines.append("## USER 질문")
            output_lines.append("")
            output_lines.append(format_message_content(msg))
            output_lines.append("")

            # Check for assistant response
            if i + 1 < len(conversation.messages):
                next_msg = conversation.messages[i + 1]
                if next_msg.role == "assistant":
                    output_lines.append("## LLM 응답")
                    output_lines.append("")
                    output_lines.append(format_message_content(next_msg))
                    output_lines.append("")
                    i += 2
                    continue
        elif msg.role == "assistant":
            # Standalone assistant message (rare case)
            output_lines.append("## LLM 응답")
            output_lines.append("")
            output_lines.append(format_message_content(msg))
            output_lines.append("")

        i += 1

    return "\n".join(output_lines)
