"""CLI for chat-weave-printer."""

import json
import sys
from pathlib import Path
from typing import Optional

import click

from chatweave_printer.models import ConversationIR
from chatweave_printer.formatters.markdown import format_conversation_to_markdown


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
                # Default: replace .json extension with .md
                output_file = input_file.with_suffix('.md')

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
