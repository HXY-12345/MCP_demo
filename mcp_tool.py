import json

import anyio
from langchain.tools import StructuredTool
from mcp.shared.memory import create_connected_server_and_client_session
from pydantic import BaseModel, Field
from mcp_server import mcp as weather_mcp_server

class MCPClient:
    async def _call_tool(self, name, arguments):
        async with create_connected_server_and_client_session(weather_mcp_server) as session:
            result = await session.call_tool(name, arguments)

        if result.isError:
            raise RuntimeError(f"MCP tool call failed: {result.content}")

        texts = [block.text for block in result.content if getattr(block, "type", None) == "text"]
        if texts:
            return "\n".join(texts)

        return json.dumps(
            [block.model_dump(mode="json") for block in result.content],
            ensure_ascii=False,
        )

    def call_tool(self, name, arguments):
        return anyio.run(self._call_tool, name, arguments)


# 创建 MCP 客户端
mcp_client = MCPClient()


# 包装成 LangChain Tool
def weather_tool_func(city: str) -> str:
    """获取某个城市的天气。"""
    return mcp_client.call_tool("get_weather", {"city": city})


class WeatherToolInput(BaseModel):
    city: str = Field(description="要查询天气的城市名称，例如台中、东京")


weather_tool = StructuredTool.from_function(
    name="get_weather",
    func=weather_tool_func,
    description="获取某个城市的天气，比如：台中、东京",
    args_schema=WeatherToolInput,
)
