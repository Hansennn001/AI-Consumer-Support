from app.state.agent_state import AgentState
from app.llm import get_llm_with_fallback
import json



def decide_tool(state: AgentState):

    llm = get_llm_with_fallback()


    prompt = f"""
You are a customer support AI agent.

Your task is to decide whether external web search is required.

Use Tavily ONLY when the customer question requires:

- current information
- latest updates
- real-time status
- information unavailable in internal knowledge base


Do NOT use Tavily for:

- refund policy questions
- password reset instructions
- general how-to questions
- standard customer support questions


You MUST return ONLY valid JSON.

Do not use markdown.
Do not add explanation.
Do not add ```.


If web search is required:

{{
    "use_tool": true,
    "tool_name": "tavily",
    "tool_query": "search query"
}}


If web search is NOT required:

{{
    "use_tool": false,
    "tool_name": "",
    "tool_query": ""
}}


Customer message:

{state["email"]}


Customer category:

{state["category"]}

"""


    result = llm.invoke(prompt)


    raw_output = result.content.strip()


    print("==============================")
    print("RAW TOOL DECISION OUTPUT")
    print("==============================")
    print(repr(raw_output))
    print("==============================")


    # Remove markdown formatting if Gemini returns ```json

    if raw_output.startswith("```"):

        raw_output = (
            raw_output
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )


    try:

        data = json.loads(raw_output)


    except json.JSONDecodeError:

        print("JSON parsing failed")

        data = {
            "use_tool": False,
            "tool_name": "",
            "tool_query": ""
        }



    state["use_tool"] = data.get(
        "use_tool",
        False
    )


    state["tool_name"] = data.get(
        "tool_name",
        ""
    )


    state["tool_query"] = data.get(
        "tool_query",
        ""
    )


    return state