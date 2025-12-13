"""Tests for cli.py"""

from pathlib import Path

from chatweave_printer.cli import determine_output_filename, PLATFORMS


class TestDetermineOutputFilename:
    """Tests for determine_output_filename function."""

    def test_chatgpt_prefix(self, tmp_path: Path):
        """chatgpt로 시작하는 파일은 chatgpt.md로 변환."""
        input_file = tmp_path / "chatgpt-abc123.json"
        result = determine_output_filename(input_file)
        assert result == tmp_path / "chatgpt.md"

    def test_claude_prefix(self, tmp_path: Path):
        """claude로 시작하는 파일은 claude.md로 변환."""
        input_file = tmp_path / "claude-conversation-xyz.json"
        result = determine_output_filename(input_file)
        assert result == tmp_path / "claude.md"

    def test_grok_prefix(self, tmp_path: Path):
        """grok으로 시작하는 파일은 grok.md로 변환."""
        input_file = tmp_path / "grok-session.json"
        result = determine_output_filename(input_file)
        assert result == tmp_path / "grok.md"

    def test_gemini_prefix(self, tmp_path: Path):
        """gemini로 시작하는 파일은 gemini.md로 변환."""
        input_file = tmp_path / "gemini-chat-001.json"
        result = determine_output_filename(input_file)
        assert result == tmp_path / "gemini.md"

    def test_case_insensitive(self, tmp_path: Path):
        """플랫폼 이름은 대소문자 구분 없이 인식."""
        input_file = tmp_path / "ChatGPT-test.json"
        result = determine_output_filename(input_file)
        assert result == tmp_path / "chatgpt.md"

    def test_non_platform_filename(self, tmp_path: Path):
        """플랫폼으로 시작하지 않는 파일은 기존 방식 유지."""
        input_file = tmp_path / "my-conversation.json"
        result = determine_output_filename(input_file)
        assert result == tmp_path / "my-conversation.md"

    def test_random_filename(self, tmp_path: Path):
        """임의의 파일명은 확장자만 변경."""
        input_file = tmp_path / "random-file-name.json"
        result = determine_output_filename(input_file)
        assert result == tmp_path / "random-file-name.md"

    def test_platforms_constant(self):
        """PLATFORMS 상수에 모든 플랫폼이 포함되어 있는지 확인."""
        expected = {"chatgpt", "claude", "grok", "gemini"}
        assert set(PLATFORMS) == expected
