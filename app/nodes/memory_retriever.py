from app.state.agent_state import AgentState
from app.database.db import get_memory


def retrieve_memory(state: AgentState):

    customer_id = state["customer_id"]


    history = get_memory(
        customer_id
    )


    state["conversation_history"] = history


    print("==============================")
    print("MEMORY RETRIEVED")
    print("==============================")
    print(history)


    return state