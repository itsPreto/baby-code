import os

from langchain import SerpAPIWrapper
from langchain.agents import Tool

os.environ["SERPAPI_API_KEY"] = "34a54bbdd2adbba455c07986d1ca7703700c9cf944a59905f570f7db58b89d97"

# Define which tools the agent can use to answer user queries
search = SerpAPIWrapper()
tools = [
    Tool(
        name = "Search",
        func=search.run,
        description="useful for when you need to answer questions about current events"
    )
]

query = "How many people live in Canada as of 2023?"
result = search.run(query)
print(result)


