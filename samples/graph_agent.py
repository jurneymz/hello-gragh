"""
02 · Graph — 다중 에이전트 DAG (index.html: 오른쪽 패널 / agents-map 01)

노드(에이전트)와 엣지를 미리 정의한다. 실행 순서·분기·병렬이 '결정적'으로 고정.
같은 입력이면 항상 같은 경로로 흐른다.

실행:  python graph_agent.py
"""

from strands import Agent
from strands.multiagent import GraphBuilder


# 각 노드는 전문화된 에이전트. name 을 주면 결과 추적이 쉽다.
classifier = Agent(name="classifier", system_prompt="질문을 한 문장으로 분류/정리해라.")
researcher = Agent(name="researcher", system_prompt="핵심 사실을 bullet 로 조사해라.")
analyst    = Agent(name="analyst",    system_prompt="조사 내용을 표로 비교 분석해라.")
writer     = Agent(name="writer",     system_prompt="분석을 바탕으로 최종 답변을 작성해라.")


def has_content(state) -> bool:
    """조건부 엣지 예시: 앞 노드에 결과가 있을 때만 다음으로 진행."""
    return True


builder = GraphBuilder()
builder.add_node(classifier, "classify")
builder.add_node(researcher, "research")
builder.add_node(analyst,    "analyze")
builder.add_node(writer,     "write")

builder.add_edge("classify", "research")
builder.add_edge("research", "analyze", condition=has_content)  # 조건부 엣지
builder.add_edge("analyze",  "write")

builder.set_entry_point("classify")
graph = builder.build()


if __name__ == "__main__":
    # 그래프 호출 -> GraphResult 반환
    result = graph("프랑스와 일본의 GDP를 비교해줘")

    print("status:", result.status)                       # COMPLETED / FAILED
    print("실행 순서:", [n for n in result.execution_order])
    # 특정 노드의 출력 꺼내기
    print("\n=== writer 노드 결과 ===")
    print(result.results["write"].result)
