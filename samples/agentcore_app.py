"""
06 · Bedrock AgentCore Runtime — 배포 진입점 (agents-map 02)

ReAct든 Graph든 Swarm이든, AgentCore 에 올리는 방식은 '동일'하다:
에이전트를 @app.entrypoint 로 감싸고 app.run() 하면 끝.

로컬 실행:   python agentcore_app.py        # http://localhost:8080 에서 서비스
로컬 테스트: curl -X POST http://localhost:8080/invocations \
               -H 'Content-Type: application/json' -d '{"prompt":"안녕"}'

배포 (starter toolkit CLI):
    agentcore configure --entrypoint agentcore_app.py
    agentcore launch
    agentcore invoke '{"prompt": "안녕"}'
"""

from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent

app = BedrockAgentCoreApp()
agent = Agent()   # 여기에 tools=[...] 또는 graph/swarm 을 넣어도 방식은 같다


@app.entrypoint
def invoke(payload):
    """AgentCore 가 요청마다 호출. payload 는 dict, 관례상 'prompt' 키 사용."""
    user_message = payload.get("prompt", "무엇을 도와드릴까요?")
    result = agent(user_message)
    return {"result": result.message}


# ── 스트리밍이 필요하면 async generator 로 (위 invoke 대신 사용) ──
# @app.entrypoint
# async def invoke(payload):
#     async for event in agent.stream_async(payload.get("prompt", "")):
#         yield event


if __name__ == "__main__":
    app.run()
