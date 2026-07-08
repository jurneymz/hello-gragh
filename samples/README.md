# Strands + Bedrock AgentCore — 돌아가는 코드 예제

시각화([`../index.html`](../index.html), [`../agents-map.html`](../agents-map.html))에 나온 개념들을 실제 코드로 옮긴 샘플 모음입니다. 모든 import·시그니처는 **2026-07 기준 공식 문서로 검증**했습니다.

## 파일 지도

| 파일 | 개념 | 시각화 위치 |
|---|---|---|
| [`react_agent.py`](react_agent.py) | ReAct — 단일 에이전트 루프 | index.html 왼쪽 |
| [`graph_agent.py`](graph_agent.py) | Graph — 결정적 DAG | index.html 오른쪽 / map 01 |
| [`swarm_agent.py`](swarm_agent.py) | Swarm — 자율 핸드오프 | map 01 |
| [`agents_as_tools.py`](agents_as_tools.py) | Agents-as-Tools — 허브-스포크 | map 01 |
| [`workflow_tool.py`](workflow_tool.py) | Workflow — 순차 파이프라인(툴) | map 01 |
| [`agentcore_app.py`](agentcore_app.py) | AgentCore Runtime 배포 진입점 | map 02 |
| [`memory_example.py`](memory_example.py) | Memory — 단기/장기 | map 04 |
| [`gateway_mcp.py`](gateway_mcp.py) | Gateway + MCP 툴 소비 | map 02 |

## 설치

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

- 패키지 이름과 import 루트가 다르니 주의:
  - `pip install strands-agents` → `import strands`
  - `pip install strands-agents-tools` → `import strands_tools` (밑줄!)
  - `pip install bedrock-agentcore` → `import bedrock_agentcore`

## AWS 준비

```bash
aws configure                 # 자격증명 + region
# Bedrock 콘솔에서 사용할 모델(예: Claude) 액세스 활성화
```

## 로컬 실행

```bash
python react_agent.py
python graph_agent.py
python swarm_agent.py
python agents_as_tools.py
```

## AgentCore 에 배포 (핵심)

**ReAct·Graph·Swarm 어느 것이든 배포 방식은 동일**합니다 — 에이전트를 `@app.entrypoint`로 감싸고 CLI로 올립니다.

```bash
pip install bedrock-agentcore-starter-toolkit   # `agentcore` 명령 제공

agentcore configure --entrypoint agentcore_app.py   # 1) 설정(IAM/ECR 등 자동)
agentcore launch                                     # 2) 빌드 + 배포
agentcore invoke '{"prompt": "안녕"}'                # 3) 호출 테스트
agentcore status                                     # 상태 확인
```

> ⚠️ **CLI 혼동 주의** — starter toolkit 은 `configure` → `launch` 이며 **pip** 설치입니다.
> 어딘가에서 본 `agentcore deploy` 나 `npm i @aws/agentcore` 는 별개의 **새 AgentCore CLI**(`aws/agentcore-cli`)로, starter toolkit 과 섞으면 안 됩니다. 이 예제는 starter toolkit 기준.

## Swarm 심화 — 핸드오프는 어떻게 도나

Graph 가 "개발자가 그린 고정 경로"라면 Swarm 은 "다음에 누가 일할지 **모델이 판단**"합니다.

1. `Swarm([a, b, c])` 로 묶으면 각 에이전트에 **`handoff_to_agent` 툴이 자동 주입**됩니다.
2. 에이전트가 이 툴을 호출해 제어권을 넘깁니다 — `handoff_to_agent(agent_name="reviewer", message=..., context=...)`.
3. **전체 작업 컨텍스트/히스토리가 공유**되므로, 넘겨받은 에이전트가 앞 맥락을 그대로 이어받습니다.
4. 현재는 **순차 핸드오프**(한 번에 한 에이전트). 한 턴에 여러 handoff 가 나오면 마지막 것이 적용됩니다.
5. 폭주 방지 장치:
   - `max_handoffs` / `max_iterations` — 총 횟수 상한
   - `execution_timeout` / `node_timeout` — 전체·개별 시간 상한(초)
   - `repetitive_handoff_detection_window` — A→B→A→B 핑퐁 감지

그래서 `result.node_history` 를 찍어 보면 **이번 실행에서 실제로 거친 경로**가 나오고, 이건 실행마다 달라질 수 있습니다 (Graph 의 고정 경로와 대비).

> `strands_tools` 안에도 `swarm` 이라는 **툴**이 따로 있는데, 이는 `strands.multiagent.Swarm` **클래스**와 다른 접근입니다. 다중 에이전트 프리미티브는 클래스 쪽을 쓰세요.

## Memory 심화 — 단기 vs 장기

- **단기**: `create_event()` 로 남기는 원본 대화 턴 (세션 스코프, 휘발).
- **장기**: 설정한 **전략(strategy)** 이 이벤트에서 비동기로 추출한 기록. `retrieve_memories()` 로 의미 검색.
- 내장 전략: `SEMANTIC`(사실 추출) · `SUMMARY`(요약) · `USER_PREFERENCE`(선호) + Custom.

## 참고 문서

- Strands 멀티에이전트: https://strandsagents.com/docs/user-guide/concepts/multi-agent/
- AgentCore Runtime 퀵스타트: https://aws.github.io/bedrock-agentcore-starter-toolkit/user-guide/runtime/quickstart.html
- AgentCore Memory: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-sdk-memory.html
- Gateway + MCP: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-agent-integration.html
