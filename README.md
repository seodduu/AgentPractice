# 에이전트 실습 자료

서브에이전트와 에이전트팀을 직접 써 보고 비교하는 실습 자료입니다.

| 폴더 | 용도 |
|---|---|
| `subagent-practice-flask/` | 서브에이전트 실습. Flask 3.1.3 (아래 환경 준비에서 직접 받음) |
| `team-practice-shop/` | 에이전트팀 실습. 버그를 심은 주문 정산 샘플 |

## 환경 준비

강사 환경과 똑같이 맞추려면 아래 순서를 그대로 따르세요.

### 1. 필요한 도구

| 도구 | 강사 환경 버전 | 확인 명령 |
|---|---|---|
| Python | 3.13.9 (3.10 이상이면 동작) | `python3 --version` |
| pytest | 8.4.2 | `python3 -m pytest --version` |
| git | 아무 버전 | `git --version` |
| Claude Code | 2.1.312 | `claude --version` |

pytest 가 없다면 `python3 -m pip install pytest` 로 설치합니다.

### 2. 저장소 받기

```bash
git clone https://github.com/seodduu/AgentPractice.git
cd AgentPractice
```

### 3. Flask 받기 (서브에이전트 실습용)

Flask 는 이 저장소에 들어 있지 않습니다. 아래 명령으로 받아서 **반드시 3.1.3 릴리스로 고정**하세요.
버전이 다르면 강사가 준비한 정답과 결과가 달라집니다.

```bash
git clone https://github.com/pallets/flask.git subagent-practice-flask
cd subagent-practice-flask
git checkout 3.1.3
git switch -c practice
git log --oneline -1    # 22d92470 release version 3.1.3 이 나오면 성공
cd ..
```

### 4. 에이전트팀 실습 샘플 확인

```bash
cd team-practice-shop
python3 -m pytest       # 1 failed, 10 passed 가 정상 시작 상태
cd ..
```

테스트 1건이 실패하는 것은 의도된 상태입니다. 그 버그를 찾는 것이 실습입니다.

### 5. 에이전트팀 기능 켜기

에이전트팀은 실험 기능이라 Claude Code 버전에 따라 별도 설정이 필요할 수 있습니다.
수업 시간에 안내하는 방법으로 활성화하세요.

## 공통 규칙

- Claude 는 **각 실습 폴더 안에서** 실행합니다.
- 비교 실험은 **매번 새 세션**으로 시작합니다. 앞선 대화가 섞이면 공정한 비교가 안 됩니다.
- 실습 중 코드가 바뀌었다면 다음 단계 전에 되돌립니다.
  `team-practice-shop` 은 저장소 최상위에서 `git checkout -- team-practice-shop` 으로 되돌릴 수 있습니다.

## 서브에이전트 실습 (subagent-practice-flask)

시작하자마자 `/context` 를 한 번 확인해 기준값을 기록해 두세요.

### 1단계: 직접 vs 위임

새 세션 두 개에서 같은 질문을 합니다.

세션 A (직접):

```
서브에이전트 쓰지 말고 직접 찾아줘. 요청이 들어와서 뷰 함수가 호출되고 응답이 나가기까지의 흐름을 함수 이름 순서대로 정리해줘.
```

세션 B (위임):

```
Explore 서브에이전트로 찾아줘. 요청이 들어와서 뷰 함수가 호출되고 응답이 나가기까지의 흐름을 함수 이름 순서대로 정리해줘.
```

비교: 두 세션의 `/context` 증가량, 결과 품질, 이어서 후속 질문을 할 때 어느 쪽이 유리한지

### 2단계: 단일 vs 병렬

새 세션 두 개에서 같은 질문을 합니다.

세션 C (단일):

```
서브에이전트 1개에게 app.py, ctx.py, sessions.py를 모두 맡겨서 분석해줘. 각 모듈의 책임을 세 줄씩 요약하고, 요청 하나를 처리할 때 세 모듈이 어떻게 연결되는지 설명해줘.
```

세션 D (병렬):

```
서브에이전트 3개에게 app.py, ctx.py, sessions.py를 하나씩 맡겨 동시에 분석해줘. 각 모듈의 책임을 세 줄씩 요약하고, 요청 하나를 처리할 때 세 모듈이 어떻게 연결되는지 설명해줘.
```

비교: 걸린 시간, 모듈 간 연결 설명의 정확도

세션 D 에서 이어서:

```
sessions.py를 분석한 서브에이전트가 읽은 쿠키 서명 코드를 그대로 보여줘.
```

### 3단계: 커스텀 서브에이전트 만들기

```
Read, Grep, Glob만 쓰는 읽기 전용 코드 리뷰어 서브에이전트를 이 프로젝트에 만들어줘. 이름은 flask-reviewer.
```

생성된 `.claude/agents/flask-reviewer.md` 를 열어 구조를 확인한 뒤 실험합니다.

```
flask-reviewer로 helpers.py에 타입 힌트를 추가해줘.
```

`description` 을 바꾸기 전과 후에 이름을 말하지 않고 요청해 자동 위임이 달라지는지 봅니다.

```
views.py 리뷰해줘.
```

## 에이전트팀 실습 (team-practice-shop)

`team-practice-shop/README.md` 를 따릅니다.

## 마무리 질문

각 단계가 끝날 때마다 스스로 답해 보세요. **"지금 메인 컨텍스트에 무엇이 남아 있나요?"**
