# chat-weave-printer

A CLI tool that converts ConversationIR (JSON) to readable Markdown format.

## Overview

Reads chat-weave's ConversationIR format (JSON) and converts it to highly readable Markdown documents. Only LLM responses are included in the output, with user inputs excluded.

### Supported Platforms
- Claude
- ChatGPT
- Gemini
- Grok

### Key Features
- Full support for ConversationIR v1 schema
- Automatic Markdown heading level adjustment (LLM response's `##` → `###`)
- Automatic empty message display ("(empty question)" / "(empty response)")
- Automatic platform name formatting (claude → Claude)
- Prioritizes normalized_content, falls back to raw_content
- Numbered LLM response headers (## LLM Response 1, 2, ...)
- Platform-based output filename convention (chatgpt-xxx.json → chatgpt.md)
- Batch conversion script for multiple files

### Future Support Planned
- PDF output
- HTML output

## Installation

### User Installation
```bash
pip install -e .
```

### Developer Installation
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install with development dependencies
pip install -e ".[dev]"
```

## Usage

### Basic Usage
Automatically generates output by changing the input filename extension to `.md`:

```bash
cwprint conversation.json
# → conversation.md created
```

#### Platform-based Filename Convention
When the input filename starts with a platform name, the output uses just the platform name:

```bash
cwprint chatgpt-2024-01-15.json
# → chatgpt.md created

cwprint claude-conversation.json
# → claude.md created
```

### Specify Output File

```bash
cwprint conversation.json -o output.md
```

### stdout Output (for piping)

```bash
cwprint conversation.json --stdout
cwprint conversation.json --stdout | less
```

### Batch Conversion

Convert multiple ConversationIR files at once using the batch script:

```bash
python scripts/batch_convert.py -d ~/Downloads
```

This processes all directories containing `ir/conversation-ir/*.json` files and creates markdown files in a `md/` subdirectory.

## Markdown Output Format

```markdown
# [Claude](https://claude.ai/chat/xxx)

---
---

## LLM Response 1

LLM's response content

### Original ## heading
(automatically incremented one level)

#### Original ### heading
(automatically incremented one level)

---
---

## LLM Response 2

Next response...
```

## Development

### Running Tests

```bash
# All tests
pytest

# Verbose mode
pytest -v

# With coverage
pytest --cov=chatweave_printer
```

### Code Validation

```bash
# Syntax check
python -m py_compile chatweave_printer/*.py
```

## Requirements

- Python 3.10+
- pydantic >= 2.0
- click >= 8.0

## Project Structure

```
chat-weave-printer/
├── chatweave_printer/
│   ├── __init__.py
│   ├── models.py           # Pydantic models (ConversationIR, MessageIR)
│   ├── cli.py              # CLI entry point
│   └── formatters/
│       ├── __init__.py
│       └── markdown.py     # Markdown conversion logic
├── scripts/
│   └── batch_convert.py    # Batch conversion script
├── tests/
│   ├── test_models.py      # Model tests
│   ├── test_cli.py         # CLI tests
│   └── test_markdown.py    # Conversion logic tests
├── pyproject.toml
└── README.md
```

## License

MIT
