"""Tests for scripts/batch_convert.py"""

import sys
from pathlib import Path

import pytest

# Add scripts directory to path for importing
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from batch_convert import get_base_output_name, get_unique_output_path, PLATFORMS


class TestGetBaseOutputName:
    """Tests for get_base_output_name function."""

    def test_chatgpt_prefix(self, tmp_path: Path):
        """chatgpt로 시작하는 파일은 chatgpt 반환."""
        json_file = tmp_path / "chatgpt-abc123.json"
        result = get_base_output_name(json_file)
        assert result == "chatgpt"

    def test_claude_prefix(self, tmp_path: Path):
        """claude로 시작하는 파일은 claude 반환."""
        json_file = tmp_path / "claude-conversation-xyz.json"
        result = get_base_output_name(json_file)
        assert result == "claude"

    def test_grok_prefix(self, tmp_path: Path):
        """grok으로 시작하는 파일은 grok 반환."""
        json_file = tmp_path / "grok-session.json"
        result = get_base_output_name(json_file)
        assert result == "grok"

    def test_gemini_prefix(self, tmp_path: Path):
        """gemini로 시작하는 파일은 gemini 반환."""
        json_file = tmp_path / "gemini-chat-001.json"
        result = get_base_output_name(json_file)
        assert result == "gemini"

    def test_case_insensitive(self, tmp_path: Path):
        """플랫폼 이름은 대소문자 구분 없이 인식."""
        json_file = tmp_path / "ChatGPT-test.json"
        result = get_base_output_name(json_file)
        assert result == "chatgpt"

    def test_non_platform_filename(self, tmp_path: Path):
        """플랫폼으로 시작하지 않는 파일은 원본 파일명 반환."""
        json_file = tmp_path / "my-conversation.json"
        result = get_base_output_name(json_file)
        assert result == "my-conversation"

    def test_platforms_constant(self):
        """PLATFORMS 상수에 모든 플랫폼이 포함되어 있는지 확인."""
        expected = {"chatgpt", "claude", "grok", "gemini"}
        assert set(PLATFORMS) == expected


class TestGetUniqueOutputPath:
    """Tests for get_unique_output_path function."""

    def test_first_file_no_suffix(self, tmp_path: Path):
        """첫 번째 파일은 번호 없이 생성."""
        used_names = {}
        result = get_unique_output_path(tmp_path, "chatgpt", used_names)
        assert result == tmp_path / "chatgpt.md"

    def test_second_file_gets_suffix_2(self, tmp_path: Path):
        """두 번째 파일은 -2 접미사."""
        used_names = {}
        get_unique_output_path(tmp_path, "chatgpt", used_names)
        result = get_unique_output_path(tmp_path, "chatgpt", used_names)
        assert result == tmp_path / "chatgpt-2.md"

    def test_third_file_gets_suffix_3(self, tmp_path: Path):
        """세 번째 파일은 -3 접미사."""
        used_names = {}
        get_unique_output_path(tmp_path, "chatgpt", used_names)
        get_unique_output_path(tmp_path, "chatgpt", used_names)
        result = get_unique_output_path(tmp_path, "chatgpt", used_names)
        assert result == tmp_path / "chatgpt-3.md"

    def test_different_names_independent(self, tmp_path: Path):
        """다른 이름은 독립적으로 카운트."""
        used_names = {}
        result1 = get_unique_output_path(tmp_path, "chatgpt", used_names)
        result2 = get_unique_output_path(tmp_path, "claude", used_names)
        assert result1 == tmp_path / "chatgpt.md"
        assert result2 == tmp_path / "claude.md"

    def test_output_to_session_directory(self, tmp_path: Path):
        """세션 디렉토리에 직접 출력 (md/ 하위가 아님)."""
        session_dir = tmp_path / "session-1"
        session_dir.mkdir()
        used_names = {}
        result = get_unique_output_path(session_dir, "chatgpt", used_names)
        # md/ 하위가 아닌 세션 디렉토리에 직접 출력되어야 함
        assert result == session_dir / "chatgpt.md"
        assert result.parent == session_dir
        # md/ 디렉토리가 경로에 없어야 함 (파일 확장자 .md는 무관)
        assert "/md/" not in str(result)
