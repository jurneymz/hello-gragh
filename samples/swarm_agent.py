"""
03 · Swarm — 자율 핸드오프 (agents-map 01 · Swarm 심화)

Graph 가 '개발자가 그린 고정 경로'라면, Swarm 은 '다음에 누가 일할지 모델이 판단'한다.
경로가 매번 달라질 수 있는 자율적 협업.

── 핸드오프(handoff)가 동작하는 방식 ──────────────────────────────
1. Swarm([a, b, c]) 로 묶으면, 각 에이전트에 `handoff_to_agent` 툴이 자동 주입된다.
2. 에이전트는 이 툴을 호출해 제어권을 넘긴다:
       handoff_to_agent(agent_name="reviewer", message="검토 부탁", context={...})
3. 전체 작업 컨텍스트/히스토리는 에이전트들 사이에서 공유된다.
4. 현재 구현은 '순차' 핸드오프 — 한 번에 한 에이전트만 활성.
5. 폭주 방지 장치:
     - max_handoffs / max_iterations : 총 상한
     - execution_timeout / node_timeout : 시간 상한(초)
     - repetitive_handoff_detection_window : 같은 핑퐁(A→B→A→B) 감지 창
─────────────────────────────────────────────────────────────

실행:  python swarm_agent.py
"""

from strands import Agent
from strands.multiagent import Swarm


coordinator = Agent(
    name="coordinator",
    system_prompt="요구사항을 쪼개고, 필요한 전문가에게 handoff 해라.",
)
coder = Agent(
    name="coder",
    system_prompt="코드를 구현한다. 리뷰가 필요하면 reviewer 에게 handoff 해라.",
)
reviewer = Agent(
    name="reviewer",
    system_prompt="코드를 검토한다. 수정이 필요하면 coder 에게 되돌려라.",
)


swarm = Swarm(
    [coordinator, coder, reviewer],   # 에이전트를 '리스트'로 (positional)
    entry_point=coordinator,          # 생략 시 첫 번째가 진입점
    max_handoffs=20,
    max_iterations=20,
    execution_timeout=900.0,          # 전체 벽시계 상한
    node_timeout=300.0,               # 에이전트 1개당 상한
    repetitive_handoff_detection_window=8,
    repetitive_handoff_min_unique_agents=3,
)


if __name__ == "__main__":
    result = swarm("todo 앱용 간단한 REST API 를 설계하고 구현한 뒤 리뷰까지 해줘")

    print("status:", result.status)
    # 어떤 순서로 손을 거쳤는지 = 이번 실행의 실제 경로 (매번 다를 수 있음)
    print("핸드오프 경로:", [n.node_id for n in result.node_history])
    print("총 실행 횟수:", result.execution_count)
