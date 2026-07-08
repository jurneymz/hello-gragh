"""
07 · AgentCore Memory — 단기 vs 장기 (agents-map 04)

- 단기(short-term): create_event 로 남기는 '원본 대화 턴'. 세션 스코프.
- 장기(long-term): 전략(strategy)이 이벤트에서 비동기로 '추출'한 기록.
  retrieve_memories 로 의미 검색해 다음 세션에 되불러온다.

내장 전략 타입:
  SEMANTIC        - 사실/의미 추출  (semanticMemoryStrategy)
  SUMMARY         - 세션 요약       (summaryMemoryStrategy)
  USER_PREFERENCE - 사용자 선호     (userPreferenceMemoryStrategy)
  (+ Custom 전략으로 추출/통합 프롬프트·모델 커스터마이즈 가능)

실행:  python memory_example.py   (AWS 자격증명 + AgentCore Memory 권한 필요)
"""

from bedrock_agentcore.memory import MemoryClient

client = MemoryClient(region_name="us-west-2")


def setup():
    # 장기 기억 전략과 함께 memory 리소스 생성 (ACTIVE 될 때까지 대기)
    memory = client.create_memory_and_wait(
        name="travel_assistant",
        strategies=[
            {"userPreferenceMemoryStrategy": {"name": "prefs", "namespaces": ["support/{actorId}/prefs"]}},
            {"summaryMemoryStrategy": {"name": "summary", "namespaces": ["support/{actorId}/summary"]}},
        ],
    )
    return memory["id"]


def demo(memory_id: str):
    # 1) 단기: 대화 턴을 이벤트로 기록
    client.create_event(
        memory_id=memory_id,
        actor_id="user-123",
        session_id="session-abc",
        messages=[
            ("나는 창가 좌석을 선호해", "USER"),
            ("알겠습니다, 기억할게요.", "ASSISTANT"),
        ],
    )

    # 2) 장기: 나중에(다른 세션에서도) 의미 검색으로 관련 기억만 회수
    records = client.retrieve_memories(
        memory_id=memory_id,
        namespace="support/user-123/prefs",
        query="좌석 선호",
    )
    for r in records:
        print(r)


if __name__ == "__main__":
    mid = setup()
    demo(mid)
