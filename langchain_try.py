from langchain.agents import initialize_agent, AgentExecutor, AgentType, Tool
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import DuckDuckGoSearchRun, BearlyInterpreterTool
from langchain.tools.render import format_tool_to_openai_tool
import json

def generative_insights(metadata_dict): 
    lc_tools = [DuckDuckGoSearchRun()]
    oai_tools = [format_tool_to_openai_tool(tool) for tool in lc_tools]

    llm = ChatOpenAI(
        model="gpt-4-1106-preview",
        openai_api_key="api-key",
        temperature=0,
        max_tokens=1000,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system", 
                "You are an AI that can make analisys about a company based on main_business_category, \
                number of employees, estimated revenue, number of locations, air quality, seismic risk and sustainability.",
            ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm.bind(tools=oai_tools)
        | OpenAIToolsAgentOutputParser()
    )

    agent_executor = AgentExecutor(agent=agent, tools=lc_tools, verbose=True)

    response = agent_executor.invoke(
        {
            "input": f"This is a json with all the metadata of the company that you need: {metadata_dict}. \
                Please, make an analisys and write a short paragraph about the company. \
                You need put accent on the pollution that the company is causing and the seismic risk of the locations. \
                These are very important factors for the company credit score. \
                You can make a search on the internet to find more information about the company. \
                This paragraph needs to be relevant and coherent for buisness people in a bank \
                that have to decide if the company will receive a loan or not. \
                The most important factor needs to be the sustainability of the company.",
        }
    )

    print(response["output"])
