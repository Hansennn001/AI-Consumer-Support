from app.state.agent_state import AgentState
from app.llm import get_llm_with_fallback
import json
import re


def classify_email(state: AgentState):

    llm = get_llm_with_fallback()


    prompt = f"""
Classify this customer support email.

Choose exactly one category:

- refund
- payment
- security_breach
- data_loss
- service_outage
- general


Return ONLY JSON.

Example:

{{
    "category": "security_breach",
    "risk_level": "high"
}}


Customer email:

{state["email"]}

"""


    result = llm.invoke(prompt)


    raw = result.content.strip()


    print("==============================")
    print("RAW CLASSIFIER OUTPUT")
    print("==============================")
    print(raw)


    # remove markdown json block
    raw = re.sub(
        r"```json",
        "",
        raw
    )

    raw = re.sub(
        r"```",
        "",
        raw
    )


    raw = raw.strip()


    try:

        data = json.loads(raw)


    except Exception:


        data = {
            "category": "general",
            "risk_level": "low"
        }



    state["category"] = data.get(
        "category",
        "general"
    )


    state["risk_level"] = data.get(
        "risk_level",
        "low"
    )


    return state