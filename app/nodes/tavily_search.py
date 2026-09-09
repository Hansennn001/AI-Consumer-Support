from app.state.agent_state import AgentState
from app.tools.tavily_search import tavily_search



def execute_tavily(state: AgentState):


    query = state["tool_query"]


    result = tavily_search(query)


    print("==============================")
    print("RAW TAVILY RESULT")
    print("==============================")
    print(result)
    print("==============================")


    formatted_result = ""


    for item in result["results"]:

        formatted_result += f"""
Title:
{item["title"]}

Content:
{item["content"]}

"""


    state["tool_result"] = formatted_result


    return state