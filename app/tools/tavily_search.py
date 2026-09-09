import os

from tavily import TavilyClient


client = TavilyClient(
    api_key=os.getenv(
        "TAVILY_API_KEY"
    )
)



def tavily_search(query: str):

    response = client.search(
        query=query,
        max_results=3
    )


    return response