from typing import TypedDict


class AgentState(TypedDict):

    request_id: str

    conversation_id: str

    customer_id: str

    email: str

    conversation_history: list

    category: str

    risk_level: str

    risk_reason: str

    contact_count: int

    use_tool: bool

    tool_name: str

    tool_query: str

    tool_result: str

    response: str

    requires_human: bool

    status: str

    processing_time: float