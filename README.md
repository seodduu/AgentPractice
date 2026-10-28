# 에이전트 실습 자료

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
