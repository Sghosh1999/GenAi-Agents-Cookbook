import asyncio
from mcp import ClientSession, StdioServerParameters
from IPython.display import display, Markdown
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
load_dotenv()

model = ChatOpenAI(
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key="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",
    model_name="llama3-8b-8192",
    temperature=0,
    max_tokens=1000,
)


async def run_app(user_question):  
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

        # Create the agent with math tools only  
        agent = create_react_agent(model, client.get_tools())  
        
        # Wrap the user question in a format the agent expects  
        user_message = [{"role": "user", "content": user_question}]  
        agent_response = await agent.ainvoke({"messages": user_message})  
        
        # Assuming we want the last response from the AI message  
        return agent_response['messages'][-1].content  

if __name__ == "__main__":  
    user_question = "what's 4 x 12?"  
    response = asyncio.run(run_app(user_question=user_question))  
    print(response)  
# if __name__ == "__main__":
#     #user_question = "what is the weather in california?"
#     user_question = "what's 4 x 12?"
#     #user_question = "what's the weather in seattle?"
#     #user_question = "what's the weather in NYC?"
#     response = asyncio.run(run_app(user_question=user_question))
#     print(response)