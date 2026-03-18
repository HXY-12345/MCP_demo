from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather-demo")

@mcp.tool()
def get_weather(city: str) -> str:
    """获取某个城市的天气，例如：台中、北京"""
    return f"{city} 当前天气：36.5°C，晴"

if __name__ == "__main__":
    mcp.run()