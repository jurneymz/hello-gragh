"""
05 · Workflow — 순차 파이프라인 (agents-map 01)

주의: Strands 에 `Workflow` '클래스'는 없다. 워크플로우는
  (a) strands_tools 의 `workflow` '툴' 로 선언형 태스크 그래프를 만들거나
  (b) GraphBuilder 로 프로그래밍적 DAG 를 짜서
구현한다. 아래는 (a) 방식.

의존성이 있는 태스크들을 정의하면, 툴이 순서를 계산해 실행한다.

실행:  python workflow_tool.py
"""

from strands import Agent
from strands_tools import workflow


agent = Agent(tools=[workflow])


if __name__ == "__main__":
    # 1) 워크플로우 정의 (태스크 + 의존성)
    agent.tool.workflow(
        action="create",
        workflow_id="data_analysis",
        tasks=[
            {
                "task_id": "extract",
                "description": "원본 데이터에서 수치를 추출한다.",
                "system_prompt": "너는 데이터 추출기다.",
                "priority": 5,
            },
            {
                "task_id": "analyze",
                "description": "추세를 분석한다.",
                "dependencies": ["extract"],   # extract 이후에만 실행
                "priority": 3,
            },
            {
                "task_id": "report",
                "description": "분석을 보고서로 정리한다.",
                "dependencies": ["analyze"],
                "priority": 1,
            },
        ],
    )

    # 2) 실행 — 의존성 순서(extract -> analyze -> report)대로 진행
    agent.tool.workflow(action="start", workflow_id="data_analysis")

    # 3) 상태 확인
    agent.tool.workflow(action="status", workflow_id="data_analysis")
