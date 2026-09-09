from app.state.agent_state import AgentState
from app.tools.customer_history import get_recent_contact_count



def detect_risk(state: AgentState):

    email = state["email"].lower()


    risk_level = "low"

    requires_human = False

    reasons = []


    security_keywords = [

        "hack",
        "hacked",
        "account breach",
        "unauthorized access",
        "stolen password",
        "security breach"

    ]


    data_loss_keywords = [

        "lost data",
        "data loss",
        "data disappeared",
        "files disappeared",
        "deleted files",
        "missing files",
        "database deleted"

    ]


    outage_keywords = [

        "service down",
        "service is down",
        "system down",
        "system is down",
        "outage",
        "cannot access",
        "unable to access",
        "service unavailable"

    ]


    # Check security breach

    for keyword in security_keywords:

        if keyword in email:

            reasons.append(
                "security breach detected"
            )

            break



    # Check data loss

    for keyword in data_loss_keywords:

        if keyword in email:

            reasons.append(
                "data loss detected"
            )

            break



    # Check service outage

    for keyword in outage_keywords:

        if keyword in email:

            reasons.append(
                "service outage detected"
            )

            break



    # Check customer history

    contact_count = get_recent_contact_count(
    state["customer_id"]
    )


    state["contact_count"] = contact_count


    if contact_count > 3:

        reasons.append(
            "customer contacted support more than 3 times in 7 days"
        )



    # Final escalation decision

    if reasons:

        risk_level = "high"

        requires_human = True



    state["risk_level"] = risk_level

    state["requires_human"] = requires_human

    state["risk_reason"] = ", ".join(reasons)


    return state