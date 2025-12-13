# chat-weave-printer

ConversationIR(JSON)을 읽기 쉬운 Markdown 포맷으로 변환하는 CLI 도구입니다.

## 개요

chat-weave의 ConversationIR 포맷(JSON)을 읽어서 가독성 높은 Markdown 문서로 변환합니다. 사용자 입력은 제외하고 LLM 응답만 출력됩니다.

### 지원 플랫폼
- Claude
- ChatGPT
- Gemini
- Grok

### 주요 기능
- ConversationIR v1 스키마 완벽 지원
- Markdown heading 레벨 자동 조정 (LLM 응답의 `##` → `###`)
- 빈 메시지 자동 표시 ("(빈 질문)" / "(빈 응답)")
- 플랫폼 이름 자동 포맷팅 (claude → Claude)
- normalized_content 우선 사용, 없으면 raw_content 사용
- 번호가 매겨진 LLM 응답 헤더 (## LLM 응답 1, 2, ...)
- 플랫폼 기반 출력 파일명 규칙 (chatgpt-xxx.json → chatgpt.md)
- 여러 파일을 한 번에 처리하는 배치 변환 스크립트

### 향후 지원 예정
- PDF 출력
- HTML 출력

## 설치

### 사용자 설치
```bash
pip install -e .
```

### 개발자 설치
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 개발 의존성 포함 설치
pip install -e ".[dev]"
```

## 사용법

### 기본 사용
입력 파일명에서 확장자를 `.md`로 변경하여 자동 생성:

```bash
cwprint conversation.json
# → conversation.md 생성
```

#### 플랫폼 기반 파일명 규칙
입력 파일명이 플랫폼 이름으로 시작하면 플랫폼 이름만 사용:

```bash
cwprint chatgpt-2024-01-15.json
# → chatgpt.md 생성

cwprint claude-conversation.json
# → claude.md 생성
```

### 출력 파일 지정

```bash
cwprint conversation.json -o output.md
```

### stdout 출력 (파이프 사용)

```bash
cwprint conversation.json --stdout
cwprint conversation.json --stdout | less
```

### 배치 변환

배치 스크립트를 사용하여 여러 ConversationIR 파일을 한 번에 변환:

```bash
python scripts/batch_convert.py -d ~/Downloads
```

이 스크립트는 `ir/conversation-ir/*.json` 파일이 있는 모든 디렉토리를 처리하고, `md/` 서브디렉토리에 마크다운 파일을 생성합니다.

## Markdown 출력 포맷

```markdown
# [Claude](https://claude.ai/chat/xxx)

---
---

## LLM 응답 1

LLM의 응답 내용

### 원본이 ## 였던 heading
(자동으로 한 단계 증가)

#### 원본이 ### 였던 heading
(자동으로 한 단계 증가)

---
---

## LLM 응답 2

다음 응답...
```

## 개발

### 테스트 실행

```bash
# 전체 테스트
pytest

# verbose 모드
pytest -v

# 커버리지 포함
pytest --cov=chatweave_printer
```

### 코드 검증

```bash
# 문법 체크
python -m py_compile chatweave_printer/*.py
```

## 요구사항

- Python 3.10+
- pydantic >= 2.0
- click >= 8.0

## 프로젝트 구조

```
chat-weave-printer/
├── chatweave_printer/
│   ├── __init__.py
│   ├── models.py           # Pydantic 모델 (ConversationIR, MessageIR)
│   ├── cli.py              # CLI 진입점
│   └── formatters/
│       ├── __init__.py
│       └── markdown.py     # Markdown 변환 로직
├── scripts/
│   └── batch_convert.py    # 배치 변환 스크립트
├── tests/
│   ├── test_models.py      # 모델 테스트
│   ├── test_cli.py         # CLI 테스트
│   └── test_markdown.py    # 변환 로직 테스트
├── pyproject.toml
└── README.md
```

## 라이선스

MIT
