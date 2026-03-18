from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from mcp_tool import weather_tool

from dotenv import load_dotenv
import os

load_dotenv()  # 会默认读取当前目录下的 .env

api_key = os.getenv("API_KEY")
model_name = os.getenv("LLM_MODEL")

# LLM
llm = ChatOpenAI(
    model=model_name,
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
)

# OpenAI-compatible tools agent prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个有帮助的助手。需要查询天气时，使用可用工具。"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

agent = create_openai_tools_agent(
    llm=llm,
    tools=[weather_tool],
    prompt=prompt,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=[weather_tool],
    verbose=True,
)

# 测试
response = agent_executor.invoke({"input": "台中的天气怎么样？"})

print("\n最终回答：", response["output"])
