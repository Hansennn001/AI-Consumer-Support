from langgraph.graph import StateGraph, END

from app.state.agent_state import AgentState

from app.nodes.classifier import classify_email
from app.nodes.risk_detector import detect_risk
from app.nodes.tool_decision import decide_tool
from app.nodes.tavily_search import execute_tavily
from app.nodes.response_generator import generate_response
from app.nodes.logger import log_conversation

from app.nodes.memory_retriever import retrieve_memory
from app.nodes.memory_saver import save_conversation



def route_after_risk(state: AgentState):

    if state["requires_human"]:
        return "human_review"

    return "tool_decision"



def route_after_tool(state: AgentState):

    if state.get("use_tool"):

        return "tavily_search"

    return "generate_response"



def human_review(state: AgentState):

    state["response"] = (
        "This request has been escalated "
        "to a human support specialist."
    )

    state["status"] = "pending_review"

    return state



workflow = StateGraph(AgentState)



# =========================
# Register Nodes
# =========================

workflow.add_node(
    "memory_retriever",
    retrieve_memory
)


workflow.add_node(
    "classifier",
    classify_email
)


workflow.add_node(
    "risk_detector",
    detect_risk
)


workflow.add_node(
    "tool_decision",
    decide_tool
)


workflow.add_node(
    "tavily_search",
    execute_tavily
)


workflow.add_node(
    "generate_response",
    generate_response
)


workflow.add_node(
    "human_review",
    human_review
)


workflow.add_node(
    "memory_saver",
    save_conversation
)


workflow.add_node(
    "logger",
    log_conversation
)



# =========================
# Workflow Start
# =========================

workflow.set_entry_point(
    "memory_retriever"
)



# =========================
# Memory -> Classification
# =========================

workflow.add_edge(
    "memory_retriever",
    "classifier"
)



# =========================
# Classification -> Risk
# =========================

workflow.add_edge(
    "classifier",
    "risk_detector"
)



# =========================
# Risk Routing
# =========================

workflow.add_conditional_edges(
    "risk_detector",
    route_after_risk,
    {
        "human_review": "human_review",
        "tool_decision": "tool_decision"
    }
)



# =========================
# Tool Decision Routing
# =========================

workflow.add_conditional_edges(
    "tool_decision",
    route_after_tool,
    {
        "tavily_search": "tavily_search",
        "generate_response": "generate_response"
    }
)



# =========================
# Tool -> Response
# =========================

workflow.add_edge(
    "tavily_search",
    "generate_response"
)



# =========================
# Finalization Flow
# =========================

workflow.add_edge(
    "generate_response",
    "memory_saver"
)


workflow.add_edge(
    "human_review",
    "memory_saver"
)


workflow.add_edge(
    "memory_saver",
    "logger"
)


workflow.add_edge(
    "logger",
    END
)



# Compile Agent

customer_agent = workflow.compile()