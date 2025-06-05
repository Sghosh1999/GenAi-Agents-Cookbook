import asyncio
import os
from nemoguardrails import LLMRails, RailsConfig
from langchain_openai import AzureChatOpenAI

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["AZURE_OPENAI_API_VERSION"] = "2023-07-01-preview"
os.environ["AZURE_OPENAI_ENDPOINT"] = ""
os.environ["AZURE_OPENAI_API_KEY"] = ""

llm = AzureChatOpenAI(
        azure_deployment="gpt-35-turbo",
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
        )

input_config = RailsConfig.from_path("config/")
app = LLMRails(input_config, llm = llm)

def process_with_guardrails(user_propt: str):
    response = app.generate(
                    messages=[{"role": "user", "content": user_propt}]
                )
    info = app.explain()
    print(response, info)


if __name__ == '__main__':
    process_with_guardrails("Hi, Hello")
