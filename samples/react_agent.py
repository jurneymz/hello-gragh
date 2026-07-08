"""
01 · ReAct — 단일 에이전트 (index.html: 왼쪽 패널)

모델이 스스로 Reason -> Act(tool) -> Observe 루프를 돌며, 몇 번 돌지·어떤 툴을
부를지 매 스텝 판단한다. 개발자는 '툴만' 쥐어주면 된다.

실행:  python react_agent.py
전제:  AWS 자격증명 + Bedrock 모델 액세스(기본 모델). `aws configure` 등으로 설정.
"""

from strands import Agent, tool
from strands_tools import calculator, current_time  # 커뮤니티 툴 (strands-agents-tools)


# 커스텀 툴: @tool 데코레이터 + docstring 이 모델에게 주는 '사용 설명서'가 된다.
@tool
def letter_counter(word: str, letter: str) -> int:
    """단어 안에서 특정 글자가 몇 번 나오는지 센다.

    Args:
        word: 검사할 단어
        letter: 셀 글자 (한 글자)
    """
    if len(letter) != 1:
        raise ValueError("letter 는 한 글자여야 합니다")
    return word.lower().count(letter.lower())


# 툴 목록만 넘기면 루프(agentic loop)는 모델이 알아서 돈다.
agent = Agent(tools=[calculator, current_time, letter_counter])


if __name__ == "__main__":
    # 이 한 번의 호출 안에서 reason -> tool_use -> tool_result -> ... -> 최종 텍스트.
    # 반복 횟수는 실행 시점에 모델이 결정한다(비결정적).
    result = agent(
        "지금 몇 시야? 그리고 'strawberry'에 'r'이 몇 번 들어가는지도 알려줘."
    )
    print("\n=== 최종 응답 ===")
    print(result.message)   # 또는 str(result)
