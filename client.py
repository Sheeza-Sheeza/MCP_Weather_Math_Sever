from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent  # updated import
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import asyncio, os

load_dotenv()

async def main():
    client = MultiServerMCPClient(
        {
            "math": {"command": "python", "args": ["mathserver.py"], "transport": "stdio"},
            "weather": {"url": "http://127.0.0.1:9001/mcp/weather", "transport": "http"},
        }
    )


    tools = await client.get_tools()
    model = ChatGroq(model="qwen-7b-instruct")  # use valid model
    agent = create_agent(model, tools)

    math_response = await agent.ainvoke({"messages":[{"role":"user","content":"What is 2 + 2*9 - 5/2?"}]})
    weather_response = await agent.ainvoke({"messages":[{"role":"user","content":"Weather in Tokyo?"}]})

    print("Math response:", math_response)
    print("Weather response:", weather_response)
     

if __name__ == "__main__":
    asyncio.run(main())
