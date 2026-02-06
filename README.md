# Todo Test Project

Python Playwright 기반 E2E 및 API 테스트 자동화 프로젝트

## 프로젝트 구조

```
todo_test/
├── tests/
│   ├── api/                    # API 테스트
│   │   └── __init__.py
│   ├── e2e/                    # E2E 테스트
│   │   ├── case/               # 테스트 케이스
│   │   │   └── test_todo.py
│   │   ├── feature/            # BDD 시나리오 (.feature)
│   │   │   └── your_scenario.feature
│   │   ├── steps/              # BDD 스텝 정의
│   │   ├── conftest.py         # E2E fixtures
│   │   └── __init__.py
│   └── __init__.py
├── pytest.ini                  # pytest 설정
├── pyproject.toml
├── requirements.txt
└── README.md
```

## 설치

```bash
# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# Playwright 브라우저 설치
playwright install

# pre-commit 훅 설치
pre-commit install
```

## 코드 품질

커밋 전 반드시 pre-commit 검사를 실행하세요:

```bash
pre-commit run -a
```

이 명령어는 ruff 린트/포맷팅 및 기타 코드 품질 검사를 수행합니다.

## 테스트 실행

```bash
# 전체 테스트 실행
pytest

# E2E 테스트만 실행
pytest tests/e2e

# API 테스트만 실행
pytest tests/api

# BDD 시나리오 실행
pytest tests/e2e/feature

# 특정 테스트 파일 실행
pytest tests/e2e/case/test_todo.py

# 상세 출력
pytest -v

# 실패 시 재시도 (pytest-rerunfailures)
pytest --reruns 2
```

## 주요 패키지

| 패키지 | 버전 | 용도 |
|--------|------|------|
| playwright | 1.58.0 | 브라우저 자동화 |
| pytest | 9.0.2 | 테스트 프레임워크 |
| pytest-playwright | 0.7.2 | Playwright pytest 통합 |
| pytest-bdd | 8.1.0 | BDD 스타일 테스트 |
| requests | 2.32.5 | API 테스트 |
| pytest-rerunfailures | 16.1 | 실패 테스트 재시도 |

## 환경 설정

### 1. `.env` 파일 생성 (필수)

프로젝트 루트에 `.env` 파일을 생성하고 테스트할 페이지 URL을 설정하세요:

```
PAGE_URL=https://your-todo-app.com
```

### 2. Fixture 이름 변경

`tests/e2e/conftest.py`에서 `your_page_or_driver_name`을 원하는 이름으로 변경하세요:

```python
# 변경 전
@pytest.fixture
def your_page_or_driver_name(browser, playwright: Playwright, request, web_session_driver):
    ...

# 변경 후 (예시)
@pytest.fixture
def todo_page(browser, playwright: Playwright, request, web_session_driver):
    ...
```

테스트 파일에서도 동일한 이름으로 사용:

```python
def test_example(todo_page):
    todo_page.click("button")
```
