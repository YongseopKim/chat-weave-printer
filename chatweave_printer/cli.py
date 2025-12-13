"""CLI for chat-weave-printer."""

import json
import sys
from pathlib import Path
from typing import Optional

import click

from chatweave_printer.models import ConversationIR
from chatweave_printer.formatters.markdown import format_conversation_to_markdown


PLATFORMS = ["chatgpt", "claude", "grok", "gemini"]


def determine_output_filename(input_file: Path) -> Path:
    """입력 파일명을 기반으로 출력 파일명 결정.

    플랫폼 이름(chatgpt, claude, grok, gemini)으로 시작하면 {platform}.md로 변환.
    그 외에는 기존 방식대로 확장자만 .md로 변경.
    """
    stem = input_file.stem.lower()

    for platform in PLATFORMS:
        if stem.startswith(platform):
            return input_file.parent / f"{platform}.md"

    # 플랫폼으로 시작하지 않으면 기존 방식
    return input_file.with_suffix('.md')


@click.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
@click.option('-o', '--output', type=click.Path(path_type=Path), help='Output file path')
@click.option('--stdout', is_flag=True, help='Output to stdout instead of file')
def main(input_file: Path, output: Optional[Path], stdout: bool):
    """
    Convert ConversationIR JSON to Markdown format.

    INPUT_FILE: Path to ConversationIR JSON file
    """
    try:
        # Read and parse JSON
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Parse into Pydantic model
        conversation = ConversationIR.model_validate(data)

        # Convert to Markdown
        markdown_output = format_conversation_to_markdown(conversation)

        # Determine output destination
        if stdout:
            # Output to stdout
            click.echo(markdown_output)
        else:
            # Determine output file path
            if output:
                output_file = output
            else:
                # Default: use platform-based naming rule
                output_file = determine_output_filename(input_file)

            # Write to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_output)

            click.echo(f"✓ Markdown saved to: {output_file}", err=True)

    except json.JSONDecodeError as e:
        click.echo(f"Error: Invalid JSON file - {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
