"""
08 · AgentCore Gateway + MCP (agents-map 02)

Gateway 는 Lambda/OpenAPI/다른 MCP 서버 같은 툴들을 하나의 관리형 MCP 엔드포인트
(streamable-HTTP, Bearer 토큰 보안) 뒤에 노출한다. Strands 에이전트는 MCPClient 로 소비.

실행:  python gateway_mcp.py   (gatewayUrl / access_token 을 실제 값으로 교체)
"""

from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp.mcp_client import MCPClient
from mcp.client.streamable_http import streamablehttp_client


GATEWAY_URL = "https://<your-gateway>.gateway.bedrock-agentcore.<region>.amazonaws.com/mcp"
ACCESS_TOKEN = "<oauth-or-jwt-bearer-token>"


def _transport():
    # MCPClient 는 '인자 없는 콜러블'을 받아서, 그것이 transport 를 반환하게 한다.
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    return streamablehttp_client(GATEWAY_URL, headers=headers)


def invoke(prompt: str):
    model = BedrockModel(
        inference_profile_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
        temperature=0.0,
        streaming=True,
    )
    mcp_client = MCPClient(_transport)
    with mcp_client:                          # 컨텍스트 매니저로 연결 관리
        tools = mcp_client.list_tools_sync()  # Gateway 가 노출한 툴 목록
        agent = Agent(model=model, tools=tools)
        return agent(prompt)


if __name__ == "__main__":
    print(invoke("내 주문 목록 알려줘"))
