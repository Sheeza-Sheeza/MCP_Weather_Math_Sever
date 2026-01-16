# weatherserver_refactored.py
import os
import asyncio
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition

# Load keys
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
OWM_KEY = os.getenv("OWM_API_KEY")

# Initialize MCP client
async def init_tools():
    client = MultiServerMCPClient({
        "weather": {
            "transport": "stdio",
            "command": "D:/MCPDEMO/mcp-openweather/mcp-weather.exe",
            "args": [],
            "env": {"OWM_API_KEY": OWM_KEY},
        },
        "calculator": {
            "transport": "stdio",
            "command": "uvx",
            "args": ["mcp-server-calculator"],
        },
    })

    tools = await client.get_tools()
    model = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_KEY)

    # Node that calls model with bound tools
    async def call_model(state: MessagesState) -> MessagesState:
        response = await model.bind_tools(tools).ainvoke(state["messages"])
        return {"messages": response}

    # Build graph
    graph = StateGraph(MessagesState)
    graph.add_node("call_model", call_model)
    graph.add_node("tools", ToolNode(tools))
    graph.add_edge(START, "call_model")
    graph.add_conditional_edges("call_model", tools_condition)
    graph.add_edge("tools", "call_model")

    return graph.compile()

# Run MCP query
async def run_mcp_query(app, user_question: str):
    result = await app.ainvoke({"messages": [{"role": "user", "content": user_question}]})
    return result["messages"][-1].content

# Streamlit UI
def main():
    st.set_page_config(page_title="MCP Math & Weather Chat", page_icon="🧮")
    st.title("🧮 MCP Math & Weather Chat")
    st.write(
        "Ask me anything related to **Math** or **Weather**.\n"
        "Examples:\n- What is 2 + 2 * 5?\n- Weather in Tokyo?"
    )

    if "app" not in st.session_state:
        with st.spinner("Initializing MCP Agent..."):
            st.session_state.app = asyncio.run(init_tools())

    user_input = st.text_input("Your question:")
    if st.button("Send") and user_input.strip():
        with st.spinner("Thinking..."):
            answer = asyncio.run(run_mcp_query(st.session_state.app, user_input))
            st.success(answer)

if __name__ == "__main__":
    main()
