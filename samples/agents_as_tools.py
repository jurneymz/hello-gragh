"""
04 · Agents-as-Tools — 허브-스포크 (agents-map 01)

전문 에이전트를 @tool 로 감싸면, 오케스트레이터가 그것을 '기능(함수)'처럼 호출한다.
오케스트레이터는 라우팅만 하고, 실제 작업은 하위 에이전트가 수행.

실행:  python agents_as_tools.py
"""

from strands import Agent, tool
from strands_tools import calculator, http_request


@tool
def research_assistant(query: str) -> str:
    """사실 확인이 필요한 리서치 질문에 답한다. 출처를 함께 제시한다.

    Args:
        query: 리서치 질문
    """
    inner = Agent(
        system_prompt="너는 리서치 전문가다. 항상 근거/출처를 붙여라.",
        tools=[http_request],
    )
    return str(inner(query))     # 하위 에이전트의 출력을 문자열로 반환


@tool
def math_assistant(expression: str) -> str:
    """수식을 계산한다.

    Args:
        expression: 계산할 수식 (예: '(12000 * 1.08) ** 2')
    """
    inner = Agent(system_prompt="너는 계산 전문가다.", tools=[calculator])
    return str(inner(expression))


# 오케스트레이터는 하위 에이전트들을 그냥 tools 로 나열한다.
orchestrator = Agent(
    system_prompt="사용자 요청을 적절한 전문가 툴로 라우팅해라. 필요하면 여러 개를 조합해라.",
    tools=[research_assistant, math_assistant],
)


if __name__ == "__main__":
    result = orchestrator(
        "일본 인구를 조사해서, 1인당 100만원씩이면 총액이 얼마인지 계산해줘."
    )
    print("\n=== 최종 응답 ===")
    print(result.message)
