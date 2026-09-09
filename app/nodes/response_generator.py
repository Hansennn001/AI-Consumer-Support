from app.state.agent_state import AgentState
from app.rag_chain import generate_answer
from app.llm import get_llm_with_fallback



def generate_response(state: AgentState):


    conversation_history = state.get(
        "conversation_history",
        []
    )


    # ============================
    # External Tool Response
    # ============================

    if state.get("tool_result"):


        llm = get_llm_with_fallback()


        prompt = f"""
You are a customer support AI assistant.

Answer the customer question using the external information provided.

Rules:

- Do not mention tools.
- Do not mention web search.
- Do not copy external information directly.
- Summarize naturally.
- Do not invent information.
- Maintain professional customer support tone.


Previous conversation history:

{conversation_history}


Current customer question:

{state["email"]}


External information:

{state["tool_result"]}


Generate the final customer response.
"""


        result = llm.invoke(prompt)

        answer = result.content



    # ============================
    # Internal Knowledge Response
    # ============================

    else:


        if conversation_history:


            llm = get_llm_with_fallback()


            prompt = f"""
You are a customer support AI assistant.

Use previous conversation history to answer the customer.

Rules:

- Use only information available in the conversation history.
- Do not invent previous issues.
- If the history does not contain the answer, say you do not have enough information.
- Maintain professional customer support tone.


Previous conversation history:

{conversation_history}


Current customer question:

{state["email"]}


Generate the final response.
"""


            result = llm.invoke(prompt)

            answer = result.content



        else:


            answer = generate_answer(
                state["email"]
            )



    state["response"] = answer

    state["status"] = "completed"


    return state