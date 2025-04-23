# GenAI Agents Cookbook

## Description
The **GenAI Agents Cookbook** is a comprehensive guide and implementation framework for building AI-powered agents using the **Model Context Protocol (MCP)**. MCP is an open protocol that standardizes how applications provide context to large language models (LLMs). This project demonstrates how to integrate multiple servers and tools, such as math operations and weather services, into a unified agentic architecture.

The project leverages MCP to connect LLMs with various data sources and tools, enabling seamless workflows and intelligent decision-making. It includes examples of multi-server setups, asynchronous communication, and tool integration with LLMs.

## Features
- **Multi-Server Integration**:
  - Connect multiple MCP servers (e.g., Math and Weather servers) to a single client.
  - Demonstrates both `stdio` and `sse` transport mechanisms.
- **Tool-Based Architecture**:
  - Expose tools like `add`, `multiply`, and weather forecasting to LLMs.
  - Use MCP to standardize tool communication.
- **Asynchronous Communication**:
  - Utilize `httpx` for asynchronous API requests.
  - Handle errors gracefully for robust operations.
- **Agentic Workflows**:
  - Build agents using the LangChain framework.
  - Route user queries to appropriate tools via MCP.
- **LLM Integration**:
  - Use OpenAI-compatible models (e.g., `llama3-8b-8192`) for natural language understanding.
  - Customize prompts and workflows for specific use cases.

## Installation
Follow these steps to set up the project:

1. Clone the repository:
   ```bash
   git clone https://github.com/username/repo.git
   cd GenAi-Agents-Cookbook
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the `mcp` directory with the following content:
     ```env
     OPENAI_API_KEY=your_openai_api_key
     GOOGLE_API_KEY=your_google_api_key
     ```

## Usage
### Running the Servers
1. **Math Server**:
   - Start the math server to expose tools like addition and multiplication:
     ```bash
     python mcp/math_server.py
     ```
   - You should see:
     ```
     Math server is running...
     ```

2. **Weather Server**:
   - Start the weather server to fetch weather alerts and forecasts:
     ```bash
     python mcp/weather.py
     ```

### Running the Multi-Server Client
- Use the `langchain_mcp_multiserver.py` script to interact with both servers:
  ```bash
  python mcp/langchain_mcp_multiserver.py
  ```
- Example query:
  ```python
  user_question = "What's 4 x 12?"
  ```
  Output:
  ```
  48
  ```

### Jupyter Notebooks
- Explore the notebooks for detailed examples and workflows:
  - **Tri-Agents-Openai.ipynb**: Demonstrates multi-agent setups for math, weather, and account-related queries.
  - **langchain_tool_agent.ipynb**: Shows how to build custom tools and integrate them with LangChain.

## Configuration
### MCP Server Configuration
- The `MultiServerMCPClient` in `langchain_mcp_multiserver.py` connects to multiple servers:
  ```python
  async with MultiServerMCPClient(
      {
          "math": {
              "command": "python",
              "args": ["math_server.py"],
              "transport": "stdio",
          },
          "weather": {
              "url": "http://localhost:8000/sse",
              "transport": "sse",
          },
      }
  ) as client:
  ```

### Model Configuration
- The project uses OpenAI-compatible models:
  ```python
  model = ChatOpenAI(
      openai_api_base="https://api.groq.com/openai/v1",
      openai_api_key="your_openai_api_key",
      model_name="llama3-8b-8192",
      temperature=0,
      max_tokens=1000,
  )
  ```

## API Reference
### Math Server
- **Tools**:
  - `add(a: int, b: int) -> int`: Adds two numbers.
  - `multiply(a: int, b: int) -> int`: Multiplies two numbers.

### Weather Server
- **Tools**:
  - `get_alerts(state: str) -> str`: Fetches weather alerts for a US state.
  - `get_forecast(latitude: float, longitude: float) -> str`: Retrieves weather forecasts for a location.

## Development
### Prerequisites
- Python 3.8 or higher
- MCP-compatible tools and libraries
- OpenAI API key for LLM integration



## Acknowledgments
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction)
- [LangChain Framework](https://langchain.com/)
- [OpenAI](https://openai.com/)
