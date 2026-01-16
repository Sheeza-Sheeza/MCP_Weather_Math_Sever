# MCP Demo Project

A demonstration project showcasing the Model Context Protocol (MCP) with multiple servers and clients, integrated with LangGraph and Streamlit.

## Overview

This project demonstrates how to build and use MCP servers and clients for AI agent applications. It includes:

- **MCP Servers**: Math calculation servers with various operations
- **MCP Clients**: Multiple client implementations using different approaches
- **Web Applications**: Streamlit-based UI for interacting with MCP servers
- **Agent Orchestration**: LangGraph integration for building AI agents with tool calling

## Features

- 🧮 **Math Server**: MCP server providing mathematical operations (add, subtract, multiply, divide, power, square root, factorial)
- 🌤️ **Weather Integration**: Integration with OpenWeatherMap via MCP
- 🤖 **AI Agents**: LangGraph-based agents that can use MCP tools
- 🌐 **Web Interface**: Streamlit applications for interactive chat
- 🔌 **Multiple Transports**: Support for both stdio and HTTP transports

## Project Structure

```
MCPDEMO/
├── mathserver.py              # Simple math MCP server (stdio transport)
├── custom_mcp_server.py       # Enhanced math MCP server (HTTP transport)
├── client.py                  # Basic MCP client using Groq
├── mcp_client_langgraph.py    # LangGraph-based MCP client
├── weatherserver.py           # Streamlit app with weather & math integration
├── web_app.py                 # Streamlit app for math chat
├── requirements.txt           # Python dependencies
└── mcp-openweather/          # Weather MCP server (Go implementation)
```

## Prerequisites

- Python 3.8+
- OpenAI API key (for GPT models)
- Groq API key (optional, for Groq models)
- OpenWeatherMap API key (for weather functionality)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd MCPDEMO
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_groq_api_key_here  # Optional
OWM_API_KEY=your_openweathermap_api_key_here  # For weather features
```

## Usage

### Running MCP Servers

#### Math Server (stdio transport)
```bash
python mathserver.py
```

#### Math Server (HTTP transport)
```bash
python custom_mcp_server.py
```
This will start an HTTP server on `http://127.0.0.1:8000/mcp`

### Running Clients

#### Basic Client (Groq)
```bash
python client.py
```
This client connects to both math and weather servers and demonstrates basic tool usage.

#### LangGraph Client
```bash
python mcp_client_langgraph.py
```
This demonstrates using MCP tools with LangGraph for agent orchestration.

### Running Web Applications

#### Math Chat Web App
```bash
streamlit run web_app.py
```
A Streamlit interface for chatting with the math MCP server.

#### Weather & Math Chat
```bash
streamlit run weatherserver.py
```
A Streamlit interface that integrates both weather and math MCP servers.

## MCP Servers

### Math Server (`mathserver.py`)

Provides basic mathematical operations:
- `add(a, b)`: Add two numbers
- `subtract(a, b)`: Subtract b from a
- `multiply(a, b)`: Multiply two numbers
- `divide(a, b)`: Divide a by b
- `power(a, b)`: Raise a to the power of b

**Transport**: stdio

### Custom Math Server (`custom_mcp_server.py`)

Enhanced math server with additional operations:
- All operations from `mathserver.py`
- `square_root(x)`: Calculate square root
- `factorial(n)`: Calculate factorial

**Transport**: HTTP (streamable-http)

### Weather Server

Located in `mcp-openweather/`, this is a Go-based MCP server that provides weather information. The executable `mcp-weather.exe` is used by the weather integration.

## MCP Clients

### Basic Client (`client.py`)

- Uses Groq's `qwen-7b-instruct` model
- Connects to multiple MCP servers (math and weather)
- Demonstrates simple agent creation with tool calling

### LangGraph Client (`mcp_client_langgraph.py`)

- Uses OpenAI's `gpt-4o-mini` model
- Implements a LangGraph state machine for agent orchestration
- Supports conditional tool calling and multi-turn conversations

## Architecture

### Transport Types

1. **stdio**: Standard input/output transport for local execution
2. **HTTP**: HTTP-based transport for remote or web-based servers
3. **streamable-http**: HTTP transport with streaming support

### Agent Flow

The LangGraph-based clients follow this flow:
1. User sends a message
2. Model decides if tools are needed
3. If tools are needed, call MCP server tools
4. Return tool results to model
5. Model generates final response

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Required for OpenAI models
- `GROQ_API_KEY`: Required for Groq models (if using `client.py`)
- `OWM_API_KEY`: Required for weather functionality

### Server Configuration

In the client files, you can configure:
- Server transport type (stdio/HTTP)
- Server command/URL
- Environment variables for servers

Example from `weatherserver.py`:
```python
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
```

## Dependencies

- `langchain-groq`: Groq integration for LangChain
- `langchain-mcp-adapters`: MCP adapters for LangChain
- `mcp`: Model Context Protocol SDK
- `python-dotenv`: Environment variable management
- `langgraph`: Agent orchestration framework
- `openai`: OpenAI API client
- `streamlit`: Web application framework

## Examples

### Example Queries

**Math queries:**
- "What is 2 + 2 * 9 - 5/2?"
- "Calculate the square root of 144"
- "What is 5 factorial?"

**Weather queries:**
- "What's the weather in Tokyo?"
- "Weather in New York?"

**Combined:**
- "What's 15 * 8 and also tell me the weather in London?"

## Troubleshooting

### Common Issues

1. **Server not found**: Ensure the MCP server is running before starting the client
2. **API key errors**: Verify your `.env` file has all required keys
3. **Transport errors**: Check that the transport type matches the server configuration
4. **Port conflicts**: If using HTTP transport, ensure port 8000 is available

### Debugging

- Check server logs for connection issues
- Verify environment variables are loaded correctly
- Test MCP servers independently before using with clients

## License

[Add your license information here]

## Contributing

[Add contribution guidelines if applicable]

## Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain MCP Adapters](https://github.com/langchain-ai/langchain-mcp-adapters)
